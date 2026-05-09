import { Movie } from "../types";

function genreBadges(genres: string) {
  return genres.split("|").slice(0, 4);
}

export default function RecommendationCards({ movies }: { movies: Movie[] }) {
  return (
    <div className="recommendation-grid">
      {movies.map((movie, index) => (
        <article className="recommendation-card" key={movie.movieId}>
          <div className="rank-badge">#{index + 1}</div>

          <h3>{movie.title}</h3>

          <div className="genre-row">
            {genreBadges(movie.genres).map((genre) => (
              <span className="genre-badge" key={genre}>
                {genre}
              </span>
            ))}
          </div>

          <div className="prediction-row">
            <span>Predicted rating</span>
            <strong>{movie.predicted_rating?.toFixed(3)}</strong>
          </div>
        </article>
      ))}
    </div>
  );
}