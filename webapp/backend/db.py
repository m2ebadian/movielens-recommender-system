from sqlalchemy import create_engine, text
import pandas as pd
from config import Config


engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    future=True
)


def test_connection():
    """Test database connection."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return result.scalar() == 1
    except Exception as e:
        print("DB connection error:", e)
        return False


def load_table(table_name: str) -> pd.DataFrame:
    """Load a full table into a pandas DataFrame."""
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, con=engine)


def execute_query(query: str):
    """Execute a raw SQL query."""
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return result.fetchall()


def get_ratings():
    return load_table("ratings")


def get_movies():
    return load_table("movies")


def get_movies_genres():
    return load_table("movies_genres")


def get_ratings_with_movies():
    return load_table("ratings_with_movies")