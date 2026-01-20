#!/usr/bin/env python3
"""
Test Supabase connection via REST API (more reliable than direct PostgreSQL)
"""
from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client, Client
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_supabase_api():
    """Test Supabase connection via REST API"""
    try:
        logger.info("🔄 Connecting to Supabase via REST API...")

        # Get credentials
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

        if not supabase_url or not supabase_key:
            logger.error("❌ Missing Supabase credentials in .env")
            return False

        # Create client
        supabase: Client = create_client(supabase_url, supabase_key)
        logger.info(f"✅ Connected to: {supabase_url}")

        # Test by checking if tables exist
        logger.info("\n📋 Checking tables...")

        # Try to query users table
        try:
            response = supabase.table("users").select("count").execute()
            logger.info("   ✅ users table exists")
        except Exception as e:
            if "relation" in str(e) or "does not exist" in str(e):
                logger.error("   ❌ users table not found!")
                logger.info("\n⚠️  Tables don't exist yet! Please run the SQL migration:")
                logger.info("   1. Go to: https://supabase.com/dashboard/project/hhncftvcjkqtpjsohksi")
                logger.info("   2. Click: SQL Editor → New Query")
                logger.info("   3. Copy/paste content from: backend/supabase_migration.sql")
                logger.info("   4. Click: Run")
                return False
            else:
                raise

        # Check other tables
        tables_to_check = [
            "expenses", "budgets", "debts", "friendships",
            "split_expenses", "settlements", "transactions"
        ]

        all_exist = True
        for table in tables_to_check:
            try:
                response = supabase.table(table).select("count").execute()
                logger.info(f"   ✅ {table} table exists")
            except Exception as e:
                logger.error(f"   ❌ {table} table not found")
                all_exist = False

        if not all_exist:
            logger.info("\n⚠️  Some tables are missing. Run the SQL migration script!")
            return False

        # Count records
        logger.info("\n📊 Record counts:")
        for table in ["users"] + tables_to_check:
            try:
                response = supabase.table(table).select("*", count="exact").execute()
                count = response.count
                logger.info(f"   {table}: {count} records")
            except Exception:
                logger.info(f"   {table}: unknown")

        logger.info("\n✅ Supabase API connection successful!")
        logger.info("✅ All tables exist and are ready!")
        return True

    except Exception as e:
        logger.error(f"❌ Error: {e}")
        logger.info("\n💡 Troubleshooting:")
        logger.info("   1. Check SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in .env")
        logger.info("   2. Verify internet connection")
        logger.info("   3. Run SQL migration if tables don't exist")
        return False

if __name__ == "__main__":
    success = test_supabase_api()
    if success:
        print("\n✅ Ready to create mock data!")
    else:
        print("\n❌ Fix issues above before proceeding")
