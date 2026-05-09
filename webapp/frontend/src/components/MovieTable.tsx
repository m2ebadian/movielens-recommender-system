import { Movie } from "../types";

export default function MovieTable({ movies }: { movies: Movie[] }) {
  return (
    <div className="table-wrapper">
      <table className="movie-table">
        <thead>
          <tr>
            <th>Movie</th>
            <th>Genres</th>
            <th>Rating</th>
          </tr>
        </thead>

        <tbody>
          {movies.map((movie) => (
            <tr key={movie.movieId}>
              <td className="movie-title">{movie.title}</td>
              <td>{movie.genres}</td>
              <td>
                <span className="rating-pill">{movie.rating}</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}