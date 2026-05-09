import { SimilarUser } from "../types";

export default function SimilarUsers({ users }: { users: SimilarUser[] }) {
  return (
    <div className="similar-users-list">
      {users.map((user) => (
        <div className="similar-user-row" key={user.userId}>
          <div>
            <strong>User {user.userId}</strong>
            <span>Similarity score</span>
          </div>

          <div className="similarity-pill">{user.similarity.toFixed(4)}</div>
        </div>
      ))}
    </div>
  );
}