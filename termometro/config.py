import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DB_PATH = os.getenv("DB_PATH", "banco_dados.db")
DATABASE_URL = os.getenv("DATABASE_URL")


def get_database_uri():
    """Retorna a URI do PostgreSQL (DATABASE_URL) ou fallback local para SQLite."""
    db_url = os.getenv("DATABASE_URL", DATABASE_URL)
    if db_url:
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)

        # Força o driver psycopg2 (instalado via psycopg2-binary) para
        # compatibilidade tanto com SQLAlchemy 2.0 quanto SQLAlchemy 2.1+.
        if db_url.startswith("postgresql://"):
            db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)

        return db_url

    db_path = os.getenv("DB_PATH", DB_PATH)
    return f"sqlite:///{os.path.abspath(db_path)}"
