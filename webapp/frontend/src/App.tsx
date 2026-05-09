import { useState } from "react";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import "./styles.css";

export default function App() {
  const [userId, setUserId] = useState<number | null>(null);

  return (
    <main className="app-shell">
      {userId ? (
        <DashboardPage userId={userId} onLogout={() => setUserId(null)} />
      ) : (
        <LoginPage onLogin={setUserId} />
      )}
    </main>
  );
}