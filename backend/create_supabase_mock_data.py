#!/usr/bin/env python3
"""
Create mock data in Supabase for testing
Uses Supabase REST API (more reliable than direct PostgreSQL)
"""
from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client, Client
from datetime import date, timedelta
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Password: password123 (bcrypt hashed)
HASHED_PASSWORD = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYuQqCEw2jW"

def create_mock_data():
    """Create mock data in Supabase"""
    try:
        logger.info("=" * 60)
        logger.info("Creating Mock Data in Supabase")
        logger.info("=" * 60)

        # Connect to Supabase
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        supabase: Client = create_client(supabase_url, supabase_key)

        logger.info("\n1/7 Creating test users...")
        # Create users
        users_data = [
            {"username": "testuser1", "email": "test1@example.com", "password": HASHED_PASSWORD, "is_active": True},
            {"username": "testuser2", "email": "test2@example.com", "password": HASHED_PASSWORD, "is_active": True},
            {"username": "testuser3", "email": "test3@example.com", "password": HASHED_PASSWORD, "is_active": True},
        ]

        users = []
        for user_data in users_data:
            response = supabase.table("users").insert(user_data).execute()
            user = response.data[0]
            users.append(user)
            logger.info(f"   + Created user: {user['username']} (ID: {user['id']})")

        logger.info(f"\n   ✅ Created {len(users)} users")

        # Get user IDs
        user1_id = users[0]['id']
        user2_id = users[1]['id']
        user3_id = users[2]['id']

        logger.info("\n2/7 Creating expenses for testuser1...")
        # Create expenses
        categories = ["Food", "Transport", "Entertainment", "Shopping", "Bills", "Healthcare"]
        today = date.today()
        expenses_data = []

        for i in range(20):
            expense = {
                "category": categories[i % len(categories)],
                "amount": round(50 + (i * 15.5), 2),
                "date": str(today - timedelta(days=i * 3)),
                "description": f"Sample expense {i + 1} for testing",
                "user_id": user1_id
            }
            expenses_data.append(expense)

        response = supabase.table("expenses").insert(expenses_data).execute()
        logger.info(f"   ✅ Created {len(response.data)} expenses")

        logger.info("\n3/7 Creating budgets for testuser1...")
        # Create budgets
        current_month = today.month
        current_year = today.year
        budgets_data = []

        for i, category in enumerate(categories[:4]):
            budget = {
                "category": category,
                "limit_amount": 500.0 + (i * 200),
                "month": current_month,
                "year": current_year,
                "user_id": user1_id
            }
            budgets_data.append(budget)

        response = supabase.table("budgets").insert(budgets_data).execute()
        logger.info(f"   ✅ Created {len(response.data)} budgets")

        logger.info("\n4/7 Creating debts for testuser1...")
        # Create debts
        debts_data = [
            {
                "name": "Car Loan",
                "principal_amount": 15000.0,
                "interest_rate": 5.5,
                "emi_amount": 300.0,
                "emi_date": 5,
                "start_date": str(today - timedelta(days=180)),
                "remaining_amount": 10500.0,
                "status": "active",
                "user_id": user1_id
            },
            {
                "name": "Personal Loan",
                "principal_amount": 5000.0,
                "interest_rate": 8.0,
                "emi_amount": 150.0,
                "emi_date": 15,
                "start_date": str(today - timedelta(days=180)),
                "remaining_amount": 3500.0,
                "status": "active",
                "user_id": user1_id
            }
        ]

        response = supabase.table("debts").insert(debts_data).execute()
        logger.info(f"   ✅ Created {len(response.data)} debts")

        logger.info("\n5/7 Creating friendships...")
        # Create friendships
        friendships_data = [
            {
                "user_id": user1_id,
                "friend_id": user2_id,
                "status": "accepted"
            },
            {
                "user_id": user1_id,
                "friend_id": user3_id,
                "status": "pending"
            },
        ]

        response = supabase.table("friendships").insert(friendships_data).execute()
        friendships = response.data
        logger.info(f"   + testuser1 ↔ testuser2: accepted")
        logger.info(f"   + testuser1 → testuser3: pending")
        logger.info(f"   ✅ Created {len(friendships)} friendships")

        logger.info("\n6/7 Creating split expenses...")
        # Create split expenses
        split_expense1 = {
            "description": "Dinner at restaurant",
            "total_amount": 150.0,
            "category": "Food",
            "date": str(today - timedelta(days=2)),
            "created_by": user1_id
        }
        response = supabase.table("split_expenses").insert(split_expense1).execute()
        split_exp1_id = response.data[0]['id']

        # Add participants for split expense 1
        supabase.table("split_participants").insert([
            {"split_expense_id": split_exp1_id, "user_id": user1_id},
            {"split_expense_id": split_exp1_id, "user_id": user2_id}
        ]).execute()

        split_expense2 = {
            "description": "Movie tickets",
            "total_amount": 60.0,
            "category": "Entertainment",
            "date": str(today - timedelta(days=5)),
            "created_by": user1_id
        }
        response = supabase.table("split_expenses").insert(split_expense2).execute()
        split_exp2_id = response.data[0]['id']

        # Add participants for split expense 2
        supabase.table("split_participants").insert([
            {"split_expense_id": split_exp2_id, "user_id": user1_id},
            {"split_expense_id": split_exp2_id, "user_id": user2_id},
            {"split_expense_id": split_exp2_id, "user_id": user3_id}
        ]).execute()

        logger.info(f"   + Dinner split: testuser1 + testuser2 ($150)")
        logger.info(f"   + Movie split: testuser1 + testuser2 + testuser3 ($60)")
        logger.info(f"   ✅ Created 2 split expenses")

        logger.info("\n7/7 Creating settlement...")
        # Create settlement
        settlement = {
            "from_user_id": user2_id,
            "to_user_id": user1_id,
            "amount": 75.0
        }
        response = supabase.table("settlements").insert(settlement).execute()
        logger.info(f"   + testuser2 → testuser1: $75")
        logger.info(f"   ✅ Created 1 settlement")

        logger.info("\n" + "=" * 60)
        logger.info("✅ Mock Data Created Successfully!")
        logger.info("=" * 60)
        logger.info("\n📊 Summary:")
        logger.info(f"   • 3 users (testuser1, testuser2, testuser3)")
        logger.info(f"   • 20 expenses")
        logger.info(f"   • 4 budgets")
        logger.info(f"   • 2 debts")
        logger.info(f"   • 2 friendships (1 accepted, 1 pending)")
        logger.info(f"   • 2 split expenses")
        logger.info(f"   • 1 settlement")
        logger.info("\n🔑 Login Credentials:")
        logger.info("   Username: testuser1, testuser2, or testuser3")
        logger.info("   Password: password123")
        logger.info("\n✅ Ready to test!")

        return True

    except Exception as e:
        logger.error(f"\n❌ Error creating mock data: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_mock_data()
    exit(0 if success else 1)
