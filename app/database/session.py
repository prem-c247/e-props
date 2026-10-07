from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.config import settings

# Create database engine with connection health check
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
)

# Session factory: autocommit=False ensures transactions are controlled explicitly
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a transactional database session per HTTP request.
    Opens a connection, yields it to the route/controller, and safely closes it afterwards.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
