import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix

from db import get_ratings, get_movies, get_ratings_with_movies


class RecommenderSystem:
    def __init__(self, top_k: int = 100, random_state: int = 42):
        self.top_k = top_k
        self.random_state = random_state

        self.ratings = None
        self.movies = None
        self.ratings_with_movies = None

        self.train_ratings = None
        self.train_matrix = None

        self.global_mean = None
        self.user_means = {}
        self.movie_means = {}

        self.user_rating_dict = {}
        self.item_ids = None

        self.top_user_neighbors = {}
        self.top_item_neighbors = {}

        self.is_ready = False

    def load_data(self):
        """Load preprocessed data from MySQL."""
        self.ratings = get_ratings()
        self.movies = get_movies()
        self.ratings_with_movies = get_ratings_with_movies()

        self.ratings["userId"] = self.ratings["userId"].astype(int)
        self.ratings["movieId"] = self.ratings["movieId"].astype(int)
        self.ratings["rating"] = self.ratings["rating"].astype(float)

        self.movies["movieId"] = self.movies["movieId"].astype(int)
        self.ratings_with_movies["userId"] = self.ratings_with_movies["userId"].astype(int)
        self.ratings_with_movies["movieId"] = self.ratings_with_movies["movieId"].astype(int)
        self.ratings_with_movies["rating"] = self.ratings_with_movies["rating"].astype(float)

    def train(self):
        """Train recommender structures using Part II logic."""
        self.load_data()

        self.train_ratings, _ = train_test_split(
            self.ratings,
            test_size=0.20,
            random_state=self.random_state,
            stratify=self.ratings["userId"],
        )

        self.train_matrix = self.train_ratings.pivot_table(
            index="userId",
            columns="movieId",
            values="rating",
        )

        self.global_mean = self.train_ratings["rating"].mean()
        self.user_means = self.train_ratings.groupby("userId")["rating"].mean().to_dict()
        self.movie_means = self.train_ratings.groupby("movieId")["rating"].mean().to_dict()

        self.user_rating_dict = self.train_ratings.groupby("userId").apply(
            lambda df: dict(zip(df["movieId"], df["rating"]))
        ).to_dict()

        self._build_user_neighbors()
        self._build_item_neighbors()

        self.is_ready = True

    def _build_user_neighbors(self):
        """Compute top-k similar users using cosine similarity."""
        user_matrix_filled = self.train_matrix.fillna(0)
        user_similarity_matrix = cosine_similarity(user_matrix_filled)

        user_ids = self.train_matrix.index.to_numpy()

        user_similarity_df = pd.DataFrame(
            user_similarity_matrix,
            index=user_ids,
            columns=user_ids,
        )

        self.top_user_neighbors = {}

        for user_id in user_ids:
            sims = user_similarity_df.loc[user_id].drop(index=user_id)
            top_neighbors = sims.sort_values(ascending=False).head(self.top_k)
            self.top_user_neighbors[int(user_id)] = [
                (int(neighbor_id), float(sim))
                for neighbor_id, sim in zip(top_neighbors.index, top_neighbors.values)
            ]

    def _build_item_neighbors(self):
        """Compute top-k similar movies using nearest neighbors."""
        item_user_matrix = self.train_matrix.T.fillna(0)
        self.item_ids = item_user_matrix.index.to_numpy()

        item_user_sparse = csr_matrix(item_user_matrix.values)

        n_neighbors = min(self.top_k + 1, len(self.item_ids))

        item_nn_model = NearestNeighbors(
            n_neighbors=n_neighbors,
            metric="cosine",
            algorithm="brute",
        )

        item_nn_model.fit(item_user_sparse)

        distances, indices = item_nn_model.kneighbors(item_user_sparse)

        self.top_item_neighbors = {}

        for item_position, movie_id in enumerate(self.item_ids):
            neighbor_list = []

            for dist, idx in zip(distances[item_position], indices[item_position]):
                neighbor_movie_id = self.item_ids[idx]

                if neighbor_movie_id == movie_id:
                    continue

                similarity = 1 - dist

                if similarity > 0:
                    neighbor_list.append((int(neighbor_movie_id), float(similarity)))

            self.top_item_neighbors[int(movie_id)] = neighbor_list[: self.top_k]

    def predict_item_based(self, user_id: int, movie_id: int):
        """Predict rating using item-based collaborative filtering."""
        user_id = int(user_id)
        movie_id = int(movie_id)

        user_ratings = self.user_rating_dict.get(user_id, {})

        if movie_id not in self.top_item_neighbors:
            return float(self.user_means.get(user_id, self.movie_means.get(movie_id, self.global_mean)))

        weighted_sum = 0.0
        similarity_sum = 0.0

        for neighbor_movie_id, similarity in self.top_item_neighbors[movie_id][: self.top_k]:
            if neighbor_movie_id in user_ratings and similarity > 0:
                weighted_sum += similarity * user_ratings[neighbor_movie_id]
                similarity_sum += abs(similarity)

        if similarity_sum > 0:
            prediction = weighted_sum / similarity_sum
        else:
            prediction = self.user_means.get(
                user_id,
                self.movie_means.get(movie_id, self.global_mean),
            )

        return float(np.clip(prediction, 0.5, 5.0))

    def get_rated_movies(self, user_id: int, limit: int = 25):
        """Return movies already rated by a user."""
        user_id = int(user_id)

        rated = self.ratings_with_movies[
            self.ratings_with_movies["userId"] == user_id
        ][["movieId", "title", "genres", "rating"]]

        rated = rated.sort_values("rating", ascending=False).head(limit)

        return rated.to_dict(orient="records")

    def get_similar_users(self, user_id: int, limit: int = 10):
        """Return similar users based on user-user cosine similarity."""
        user_id = int(user_id)

        if user_id not in self.top_user_neighbors:
            return []

        neighbors = self.top_user_neighbors[user_id][:limit]

        result = []
        for similar_user_id, similarity in neighbors:
            result.append(
                {
                    "userId": similar_user_id,
                    "similarity": round(float(similarity), 4),
                }
            )

        return result

    def get_recommendations(self, user_id: int, limit: int = 10, min_num_ratings: int = 20):
        """Return item-based movie recommendations for movies the user has not rated."""
        user_id = int(user_id)

        if user_id not in self.user_rating_dict:
            return []

        rated_movies = set(self.ratings[self.ratings["userId"] == user_id]["movieId"].astype(int))

        movie_popularity = self.train_ratings.groupby("movieId").size()

        candidate_movies = [
            int(movie_id)
            for movie_id in self.item_ids
            if int(movie_id) not in rated_movies
            and movie_popularity.get(movie_id, 0) >= min_num_ratings
        ]

        scored_movies = []

        for movie_id in candidate_movies:
            predicted_rating = self.predict_item_based(user_id, movie_id)
            scored_movies.append((movie_id, predicted_rating))

        recommendations = pd.DataFrame(
            scored_movies,
            columns=["movieId", "predicted_rating"],
        )

        recommendations = recommendations.merge(
            self.movies,
            on="movieId",
            how="left",
        )

        recommendations = recommendations.sort_values(
            "predicted_rating",
            ascending=False,
        ).head(limit)

        return recommendations[
            ["movieId", "title", "genres", "predicted_rating"]
        ].round({"predicted_rating": 3}).to_dict(orient="records")

    def get_sample_users(self, limit: int = 20):
        """Return sample valid users for login/testing."""
        users = (
            self.ratings.groupby("userId")
            .size()
            .reset_index(name="num_ratings")
            .sort_values("num_ratings", ascending=False)
            .head(limit)
        )

        return users.to_dict(orient="records")

    def user_exists(self, user_id: int):
        """Check whether user exists in the MovieLens ratings table."""
        user_id = int(user_id)
        return user_id in set(self.ratings["userId"].unique())



recommender = RecommenderSystem(top_k=100)