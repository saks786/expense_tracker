#!/usr/bin/env python3
"""
Test Supabase connection and verify tables exist
"""
from dotenv import load_dotenv
load_dotenv()

import logging
from app.database import engine, SessionLocal
from sqlalchemy import text, inspect

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_connection():
    """Test database connection and list tables"""
    try:
        logger.info("🔄 Testing Supabase connection...")

        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.scalar()
            logger.info(f"✅ Connected to PostgreSQL: {version}")

            # List all tables
            inspector = inspect(engine)
            tables = inspector.get_table_names()

            if tables:
                logger.info(f"📋 Found {len(tables)} tables:")
                for table in sorted(tables):
                    logger.info(f"   - {table}")
            else:
                logger.warning("⚠️  No tables found! Run the SQL migration script first.")
                logger.info("   Go to: https://supabase.com/dashboard/project/hhncftvcjkqtpjsohksi")
                logger.info("   Click: SQL Editor → New Query")
                logger.info("   Copy/paste: backend/supabase_migration.sql")
                return False

            # Check for required tables
            required_tables = ['users', 'expenses', 'budgets', 'debts', 'friendships',
                             'split_expenses', 'settlements', 'transactions']
            missing_tables = [t for t in required_tables if t not in tables]

            if missing_tables:
                logger.warning(f"⚠️  Missing tables: {', '.join(missing_tables)}")
                logger.info("   Run the SQL migration script to create them.")
                return False

            logger.info("✅ All required tables exist!")

            # Count records in each table
            logger.info("\n📊 Record counts:")
            db = SessionLocal()
            try:
                for table in sorted(tables):
                    result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.scalar()
                    logger.info(f"   {table}: {count} records")
            finally:
                db.close()

            return True

    except Exception as e:
        logger.error(f"❌ Connection failed: {e}")
        logger.info("\n💡 Troubleshooting:")
        logger.info("   1. Check if SQL migration was run in Supabase Dashboard")
        logger.info("   2. Verify DATABASE_URL in .env file")
        logger.info("   3. Check internet connection")
        return False

if __name__ == "__main__":
    success = test_connection()
    if success:
        print("\n✅ Ready to create mock data!")
    else:
        print("\n❌ Fix issues above before proceeding")
