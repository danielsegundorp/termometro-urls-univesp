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
        # Plataformas como Render/Heroku podem fornecer 'postgres://',
        # mas o SQLAlchemy 2.0+ exige 'postgresql://'.
        if db_url.startswith("postgres://"):
            return db_url.replace("postgres://", "postgresql://", 1)
        return db_url

    db_path = os.getenv("DB_PATH", DB_PATH)
    return f"sqlite:///{os.path.abspath(db_path)}"
