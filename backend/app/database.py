# backend/app/database.py
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

logger = logging.getLogger(__name__)

# Prefer explicit DATABASE_URL environment variable (set by Render / your env)
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

if not DATABASE_URL:
    # fallback to sqlite for local development when DATABASE_URL not provided.
    logger.warning("DATABASE_URL not set — falling back to sqlite:///./dev.db (development only)")
    DATABASE_URL = "sqlite:///./dev.db"

# For proper PostgreSQL parsing, accept both postgres:// and postgresql://
# SQLAlchemy >=1.4 handles these, so we just pass the URL through.
# create_engine() options: pool_pre_ping helps recover stale connections on cloud DBs
engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarative
Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
