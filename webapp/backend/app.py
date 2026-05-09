from flask import Flask, jsonify, request, session
from flask_cors import CORS

from config import Config
from db import test_connection
from recommender import recommender


app = Flask(__name__)
app.config.from_object(Config)

CORS(

    app,

    supports_credentials=True,

    origins=[

        "http://localhost:5173",

        "http://127.0.0.1:5173",

        "https://cse482-frontend-816507479795.us-central1.run.app",

    ],

)


@app.before_request
def ensure_recommender_ready():
    if not recommender.is_ready:
        recommender.train()


@app.route("/api/health", methods=["GET"])
def health_check():
    db_ok = test_connection()

    return jsonify(
        {
            "status": "ok",
            "database_connected": db_ok,
            "recommender_ready": recommender.is_ready,
        }
    )


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    user_id = data.get("userId")

    if user_id is None:
        return jsonify({"error": "userId is required"}), 400

    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({"error": "userId must be a number"}), 400

    if not recommender.user_exists(user_id):
        return jsonify({"error": f"User {user_id} does not exist"}), 404

    session["user_id"] = user_id

    return jsonify(
        {
            "message": "Login successful",
            "userId": user_id,
        }
    )


@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()

    return jsonify(
        {
            "message": "Logout successful",
        }
    )


@app.route("/api/session", methods=["GET"])
def get_session():
    user_id = session.get("user_id")

    return jsonify(
        {
            "loggedIn": user_id is not None,
            "userId": user_id,
        }
    )


@app.route("/api/users/sample", methods=["GET"])
def sample_users():
    limit = request.args.get("limit", 20)

    try:
        limit = int(limit)
    except ValueError:
        limit = 20

    users = recommender.get_sample_users(limit=limit)

    return jsonify(users)


@app.route("/api/user/<int:user_id>/rated-movies", methods=["GET"])
def rated_movies(user_id):
    limit = request.args.get("limit", 25)

    try:
        limit = int(limit)
    except ValueError:
        limit = 25

    if not recommender.user_exists(user_id):
        return jsonify({"error": f"User {user_id} does not exist"}), 404

    movies = recommender.get_rated_movies(user_id=user_id, limit=limit)

    return jsonify(movies)


@app.route("/api/user/<int:user_id>/similar-users", methods=["GET"])
def similar_users(user_id):
    limit = request.args.get("limit", 10)

    try:
        limit = int(limit)
    except ValueError:
        limit = 10

    if not recommender.user_exists(user_id):
        return jsonify({"error": f"User {user_id} does not exist"}), 404

    users = recommender.get_similar_users(user_id=user_id, limit=limit)

    return jsonify(users)


@app.route("/api/user/<int:user_id>/recommendations", methods=["GET"])
def recommendations(user_id):
    limit = request.args.get("limit", 10)
    min_num_ratings = request.args.get("min_num_ratings", 20)

    try:
        limit = int(limit)
        min_num_ratings = int(min_num_ratings)
    except ValueError:
        limit = 10
        min_num_ratings = 20

    if not recommender.user_exists(user_id):
        return jsonify({"error": f"User {user_id} does not exist"}), 404

    recs = recommender.get_recommendations(
        user_id=user_id,
        limit=limit,
        min_num_ratings=min_num_ratings,
    )

    return jsonify(recs)


@app.route("/api/model-summary", methods=["GET"])
def model_summary():
    return jsonify(
        {
            "best_model": "Item-Based Collaborative Filtering",
            "top_k": 100,
            "baseline_rmse": 0.9413,
            "baseline_mae": 0.7347,
            "user_based_rmse": 0.9676,
            "user_based_mae": 0.7476,
            "item_based_rmse": 0.9016,
            "item_based_mae": 0.6801,
            "reason": (
                "Item-based collaborative filtering performed best on the test set. "
                "The dataset is highly sparse, so item similarities were more stable "
                "than user similarities."
            ),
        }
    )


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=Config.DEBUG)