"""
Supabase client configuration for the expense tracker backend.
Uses Supabase REST API and Auth instead of direct PostgreSQL connection.
"""
import os
from supabase import create_client, Client
import logging

logger = logging.getLogger(__name__)

# Get Supabase credentials from environment
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")  # Use service role for backend

if not SUPABASE_URL or not SUPABASE_KEY:
    logger.warning("⚠️ Supabase credentials not configured!")
    supabase: Client | None = None
else:
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("✅ Supabase client initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Supabase client: {e}")
        supabase = None


def get_supabase() -> Client:
    """Get the Supabase client instance"""
    if supabase is None:
        raise RuntimeError("Supabase client not initialized. Check environment variables.")
    return supabase
