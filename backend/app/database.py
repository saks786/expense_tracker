# backend/app/database.py
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

logger = logging.getLogger(__name__)

# Supabase PostgreSQL DATABASE_URL (required for production)
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

if not DATABASE_URL:
    raise ValueError(
        "❌ DATABASE_URL environment variable is required! "
        "Please set your Supabase PostgreSQL connection string in .env file."
    )

if not DATABASE_URL.startswith("postgresql"):
    raise ValueError(
        f"❌ Invalid DATABASE_URL: {DATABASE_URL}. "
        "Only PostgreSQL (Supabase) is supported. URL must start with 'postgresql://'"
    )

logger.info("🔄 Connecting to Supabase PostgreSQL...")

# Create PostgreSQL engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=10,  # Maximum number of permanent connections
    max_overflow=20,  # Maximum number of temporary connections
    pool_recycle=3600,  # Recycle connections after 1 hour
    echo=False  # Set to True for SQL query logging during development
)

logger.info("✅ Successfully connected to Supabase PostgreSQL!")

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
