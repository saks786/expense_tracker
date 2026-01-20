"""
Test Supabase PostgreSQL Migration
This script tests the connection and verifies all tables exist
"""
import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

# Load environment variables
load_dotenv()

def print_success(message):
    print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")

def print_error(message):
    print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")

def print_info(message):
    print(f"{Fore.CYAN}ℹ️  {message}{Style.RESET_ALL}")

def print_warning(message):
    print(f"{Fore.YELLOW}⚠️  {message}{Style.RESET_ALL}")

def test_connection():
    """Test connection to Supabase PostgreSQL"""
    print_info("Testing Supabase PostgreSQL connection...")
    
    DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
    
    if not DATABASE_URL:
        print_error("DATABASE_URL not found in environment variables!")
        print_info("Please set DATABASE_URL in your .env file")
        return False
    
    if not DATABASE_URL.startswith("postgresql"):
        print_error(f"Invalid DATABASE_URL: Must start with 'postgresql://'")
        print_info(f"Current: {DATABASE_URL[:20]}...")
        return False
    
    print_info(f"Connecting to: {DATABASE_URL[:30]}...")
    
    try:
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print_success("Connected to Supabase PostgreSQL successfully!")
            print_info(f"PostgreSQL Version: {version.split(',')[0]}")
            return engine
    except Exception as e:
        print_error(f"Connection failed: {e}")
        return None

def verify_tables(engine):
    """Verify all required tables exist"""
    print_info("\nVerifying database tables...")
    
    required_tables = [
        "users",
        "expenses",
        "budgets",
        "debts",
        "friendships",
        "split_expenses",
        "split_participants",
        "settlements",
        "transactions"
    ]
    
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    print_info(f"Found {len(existing_tables)} tables in database")
    
    all_present = True
    for table in required_tables:
        if table in existing_tables:
            print_success(f"Table '{table}' exists")
        else:
            print_error(f"Table '{table}' is MISSING!")
            all_present = False
    
    if not all_present:
        print_warning("\nSome tables are missing. Run the migration SQL script in Supabase Dashboard:")
        print_info("1. Go to Supabase Dashboard → SQL Editor")
        print_info("2. Copy contents of supabase_migration.sql")
        print_info("3. Paste and run the SQL script")
        return False
    
    print_success("\nAll required tables are present!")
    return True

def verify_indexes(engine):
    """Verify indexes are created"""
    print_info("\nVerifying database indexes...")
    
    inspector = inspect(engine)
    
    tables_with_indexes = [
        ("expenses", ["idx_expenses_user_id", "idx_expenses_date"]),
        ("budgets", ["idx_budgets_user_id"]),
        ("debts", ["idx_debts_user_id"]),
        ("friendships", ["idx_friendships_user_id", "idx_friendships_friend_id"]),
        ("split_expenses", ["idx_split_expenses_created_by"]),
        ("transactions", ["idx_transactions_user_id"]),
    ]
    
    for table, expected_indexes in tables_with_indexes:
        indexes = inspector.get_indexes(table)
        index_names = [idx["name"] for idx in indexes]
        
        for expected_idx in expected_indexes:
            if expected_idx in index_names:
                print_success(f"Index '{expected_idx}' exists on '{table}'")
            else:
                print_warning(f"Index '{expected_idx}' not found on '{table}'")

def test_crud_operations(engine):
    """Test basic CRUD operations"""
    print_info("\nTesting CRUD operations...")
    
    try:
        with engine.connect() as conn:
            # Test INSERT
            print_info("Testing INSERT...")
            result = conn.execute(text("""
                INSERT INTO users (username, email, password, is_active)
                VALUES ('test_migration_user', 'test_migration@example.com', 'hashed_password', true)
                RETURNING id, username, email
            """))
            user = result.fetchone()
            user_id = user[0]
            print_success(f"Created user: {user[1]} ({user[2]}) with ID: {user_id}")
            
            # Test SELECT
            print_info("Testing SELECT...")
            result = conn.execute(text("SELECT COUNT(*) FROM users WHERE id = :id"), {"id": user_id})
            count = result.fetchone()[0]
            if count == 1:
                print_success("SELECT operation successful")
            
            # Test UPDATE
            print_info("Testing UPDATE...")
            conn.execute(text("""
                UPDATE users SET email = 'updated_migration@example.com'
                WHERE id = :id
            """), {"id": user_id})
            print_success("UPDATE operation successful")
            
            # Test DELETE
            print_info("Testing DELETE...")
            conn.execute(text("DELETE FROM users WHERE id = :id"), {"id": user_id})
            print_success("DELETE operation successful")
            
            conn.commit()
            
        print_success("\nAll CRUD operations completed successfully!")
        return True
        
    except Exception as e:
        print_error(f"CRUD operations failed: {e}")
        return False

def main():
    """Main test function"""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  Supabase PostgreSQL Migration Test{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    # Test connection
    engine = test_connection()
    if not engine:
        print_error("\n❌ Migration test FAILED - Cannot connect to database")
        sys.exit(1)
    
    # Verify tables
    tables_ok = verify_tables(engine)
    if not tables_ok:
        print_error("\n❌ Migration test FAILED - Missing tables")
        sys.exit(1)
    
    # Verify indexes
    verify_indexes(engine)
    
    # Test CRUD operations
    crud_ok = test_crud_operations(engine)
    if not crud_ok:
        print_error("\n❌ Migration test FAILED - CRUD operations failed")
        sys.exit(1)
    
    print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}  ✅ MIGRATION TEST PASSED!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}  Your database is ready for production!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")

if __name__ == "__main__":
    main()
