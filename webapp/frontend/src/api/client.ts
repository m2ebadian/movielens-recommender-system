const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:5001";

export async function login(userId: number) {
  const res = await fetch(`${API_BASE}/api/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ userId }),
  });

  if (!res.ok) throw new Error("Login failed");
  return res.json();
}

export async function logout() {
  await fetch(`${API_BASE}/api/logout`, {
    method: "POST",
    credentials: "include",
  });
}

export async function getRatedMovies(userId: number) {
  const res = await fetch(`${API_BASE}/api/user/${userId}/rated-movies`);
  return res.json();
}

export async function getRecommendations(userId: number) {
  const res = await fetch(`${API_BASE}/api/user/${userId}/recommendations`);
  return res.json();
}

export async function getSimilarUsers(userId: number) {
  const res = await fetch(`${API_BASE}/api/user/${userId}/similar-users`);
  return res.json();
}

export async function getModelSummary() {
  const res = await fetch(`${API_BASE}/api/model-summary`);
  return res.json();
}