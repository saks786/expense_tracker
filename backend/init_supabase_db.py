#!/usr/bin/env python3
"""
Initialize Supabase PostgreSQL database with all required tables.
Run this once to set up the database schema.
"""
from dotenv import load_dotenv
load_dotenv()

import logging
from app.database import engine, Base
from app.models import (
    User, Expense, Budget, Debt,
    Friendship, SplitExpense, Settlement, Transaction
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """Create all tables in Supabase PostgreSQL"""
    try:
        logger.info("🔄 Connecting to Supabase PostgreSQL...")
        logger.info(f"Database engine: {engine.url}")

        # Test connection
        with engine.connect() as conn:
            logger.info("✅ Database connection successful!")

        logger.info("🔄 Creating tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ All tables created successfully!")

        # List all created tables
        inspector = engine.dialect.get_table_names(engine.connect())
        logger.info(f"📋 Tables created: {', '.join(inspector)}")

    except Exception as e:
        logger.error(f"❌ Error initializing database: {e}")
        raise

if __name__ == "__main__":
    init_database()
