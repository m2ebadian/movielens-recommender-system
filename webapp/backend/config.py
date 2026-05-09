import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")
    DEBUG = os.getenv("FLASK_ENV", "production") == "development"

    MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "cse482_movielens")
    MYSQL_USER = os.getenv("MYSQL_USER", "cse482_user")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "cse482_password")

    CLOUD_SQL_CONNECTION_NAME = os.getenv("CLOUD_SQL_CONNECTION_NAME")

    if CLOUD_SQL_CONNECTION_NAME:
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@/{MYSQL_DATABASE}"
            f"?unix_socket=/cloudsql/{CLOUD_SQL_CONNECTION_NAME}"
        )
    else:
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
            f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False