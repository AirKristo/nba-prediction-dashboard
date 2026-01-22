#This module provides the SQLAlchemy engine and session factory
#for connecting to PostgreSQL.

from collections.abc import Generator

from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import create_engine

from app.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
)

# Use a factory pattern so each request gets its own session.
SessionLocal = sessionmaker(
    autocommit=False,  # We'll manage transactions explicitly
    autoflush=False,   # Don't auto-flush before queries for more control
    bind=engine,
)


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.

    """
    pass


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.

    Output a session and ensures it's closed after use,
    even if an exception occurs.

    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()