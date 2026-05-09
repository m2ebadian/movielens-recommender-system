import { useEffect, useState } from "react";
import {
  getRatedMovies,
  getRecommendations,
  getSimilarUsers,
  getModelSummary,
  logout,
} from "../api/client";

import { Movie, SimilarUser } from "../types";
import MovieTable from "../components/MovieTable";
import RecommendationCards from "../components/RecommendationCards";
import SimilarUsers from "../components/SimilarUsers";
import ModelSummary from "../components/ModelSummary";

export default function DashboardPage({
  userId,
  onLogout,
}: {
  userId: number;
  onLogout: () => void;
}) {
  const [rated, setRated] = useState<Movie[]>([]);
  const [recs, setRecs] = useState<Movie[]>([]);
  const [similar, setSimilar] = useState<SimilarUser[]>([]);
  const [summary, setSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadDashboard() {
      setLoading(true);

      const [ratedData, recData, similarData, summaryData] = await Promise.all([
        getRatedMovies(userId),
        getRecommendations(userId),
        getSimilarUsers(userId),
        getModelSummary(),
      ]);

      setRated(ratedData);
      setRecs(recData);
      setSimilar(similarData);
      setSummary(summaryData);
      setLoading(false);
    }

    loadDashboard();
  }, [userId]);

  const handleLogout = async () => {
    await logout();
    onLogout();
  };

  if (loading) {
    return (
      <section className="dashboard-loading">
        <div className="loader" />
        <p>Loading recommender dashboard...</p>
      </section>
    );
  }

  return (
    <section className="dashboard-page">
      <header className="dashboard-header">
        <div>
          <p className="eyebrow">MovieLens Collaborative Filtering</p>
          <h1>Recommendation Dashboard</h1>
          <p className="muted">Logged in as User {userId}</p>
        </div>

        <button className="secondary-button" onClick={handleLogout}>
          Logout
        </button>
      </header>

      <div className="metrics-grid">
        <div className="metric-card">
          <span>Rated Movies Shown</span>
          <strong>{rated.length}</strong>
        </div>
        <div className="metric-card">
          <span>Recommendations</span>
          <strong>{recs.length}</strong>
        </div>
        <div className="metric-card">
          <span>Similar Users</span>
          <strong>{similar.length}</strong>
        </div>
        <div className="metric-card">
          <span>Best Model RMSE</span>
          <strong>{summary?.item_based_rmse}</strong>
        </div>
      </div>

      <ModelSummary data={summary} />

      <div className="content-grid">
        <section className="panel large-panel">
          <div className="section-title">
            <div>
              <h2>Recommended Movies</h2>
              <p>Movies not previously rated by this user.</p>
            </div>
          </div>

          <RecommendationCards movies={recs} />
        </section>

        <section className="panel side-panel">
          <div className="section-title">
            <div>
              <h2>Similar Users</h2>
              <p>Top users with related rating behavior.</p>
            </div>
          </div>

          <SimilarUsers users={similar} />
        </section>
      </div>

      <section className="panel">
        <div className="section-title">
          <div>
            <h2>Highly Rated Movies</h2>
            <p>Movies this user rated highly in the MovieLens dataset.</p>
          </div>
        </div>

        <MovieTable movies={rated} />
      </section>
    </section>
  );
}