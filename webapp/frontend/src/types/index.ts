export interface Movie {
  movieId: number;
  title: string;
  genres: string;
  rating?: number;
  predicted_rating?: number;
}

export interface User {
  userId: number;
  num_ratings?: number;
}

export interface SimilarUser {
  userId: number;
  similarity: number;
}