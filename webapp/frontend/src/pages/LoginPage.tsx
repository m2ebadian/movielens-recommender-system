import { useState } from "react";
import { login } from "../api/client";

export default function LoginPage({ onLogin }: { onLogin: (userId: number) => void }) {
  const [userId, setUserId] = useState("414");
  const [error, setError] = useState("");

  const handleLogin = async () => {
    setError("");

    const parsedUserId = Number(userId);

    if (!parsedUserId) {
      setError("Please enter a valid MovieLens user ID.");
      return;
    }

    try {
      await login(parsedUserId);
      onLogin(parsedUserId);
    } catch {
      setError("User not found. Try 414, 599, 474, 448, or 1.");
    }
  };

  return (
    <section className="login-page">
      <div className="login-card">
        <div className="brand-pill">CSE 482 Recommender System</div>

        <h1>Movie Recommendation Dashboard</h1>

        <p className="muted">
          Log in using an anonymous MovieLens user ID to view rated movies,
          personalized recommendations, and similar users.
        </p>

        <label htmlFor="userId">MovieLens User ID</label>
        <input
          id="userId"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleLogin()}
          placeholder="Example: 414"
        />

        {error && <p className="error">{error}</p>}

        <button className="primary-button" onClick={handleLogin}>
          Open Dashboard
        </button>

        <div className="sample-users">
          <span>Good demo users:</span>
          <strong>414</strong>
          <strong>599</strong>
          <strong>474</strong>
          <strong>448</strong>
          <strong>1</strong>
        </div>
      </div>
    </section>
  );
}