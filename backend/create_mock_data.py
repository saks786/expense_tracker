"""
Script to create mock data for testing the Expense Tracker application.
Run this script from the backend directory: python create_mock_data.py
"""

from datetime import date, timedelta
from app.database import SessionLocal, engine
from app import models
from app.auth import get_password_hash

def create_mock_data():
    """Creates mock data for testing."""
    # Create database tables
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if mock data already exists
        existing_user = db.query(models.User).filter(models.User.username == "testuser1").first()
        if existing_user:
            print("✓ Mock data already exists!")
            print("  Delete the database file (dev.db) to recreate mock data.")
            return
        
        print("Creating mock data...")
        
        # Create test users
        print("\n1. Creating users...")
        users = []
        for i in range(1, 4):
            user = models.User(
                username=f"testuser{i}",
                email=f"test{i}@example.com",
                password=get_password_hash("password123"),
                is_active=True
            )
            db.add(user)
            users.append(user)
        
        db.commit()
        for user in users:
            db.refresh(user)
        print(f"   ✓ Created {len(users)} users")
        
        # Create expenses for user 1
        print("\n2. Creating expenses...")
        categories = ["Food", "Transport", "Entertainment", "Shopping", "Bills", "Healthcare"]
        today = date.today()
        
        for i in range(20):
            expense = models.Expense(
                category=categories[i % len(categories)],
                amount=round(50 + (i * 15.5), 2),
                date=today - timedelta(days=i * 3),
                description=f"Sample expense {i + 1} for testing",
                user_id=users[0].id
            )
            db.add(expense)
        
        db.commit()
        print("   ✓ Created 20 expenses")
        
        # Create budgets for user 1
        print("\n3. Creating budgets...")
        current_month = today.month
        current_year = today.year
        
        for category in categories[:4]:
            budget = models.Budget(
                category=category,
                limit_amount=500.0 + (categories.index(category) * 200),
                month=current_month,
                year=current_year,
                user_id=users[0].id
            )
            db.add(budget)
        
        db.commit()
        print("   ✓ Created 4 budgets")
        
        # Create debts for user 1
        print("\n4. Creating debts...")
        debts_data = [
            {"name": "Car Loan", "principal": 15000.0, "interest": 5.5, "emi": 300.0, "emi_date": 5},
            {"name": "Personal Loan", "principal": 5000.0, "interest": 8.0, "emi": 150.0, "emi_date": 15},
        ]
        
        for debt_data in debts_data:
            debt = models.Debt(
                name=debt_data["name"],
                principal_amount=debt_data["principal"],
                interest_rate=debt_data["interest"],
                emi_amount=debt_data["emi"],
                emi_date=debt_data["emi_date"],
                start_date=today - timedelta(days=180),
                remaining_amount=debt_data["principal"] * 0.7,
                status="active",
                user_id=users[0].id
            )
            db.add(debt)
        
        db.commit()
        print("   ✓ Created 2 debts")
        
        # Create friendships
        print("\n5. Creating friendships...")
        friendship1 = models.Friendship(
            user_id=users[0].id,
            friend_id=users[1].id,
            status="accepted"
        )
        friendship2 = models.Friendship(
            user_id=users[0].id,
            friend_id=users[2].id,
            status="pending"
        )
        db.add(friendship1)
        db.add(friendship2)
        db.commit()
        print("   ✓ Created 2 friendships")
        
        # Create split expenses
        print("\n6. Creating split expenses...")
        split_expense = models.SplitExpense(
            description="Dinner at restaurant",
            total_amount=150.0,
            category="Food",
            date=today - timedelta(days=2),
            created_by=users[0].id,
            participants=[users[0], users[1]]
        )
        db.add(split_expense)
        
        split_expense2 = models.SplitExpense(
            description="Movie tickets",
            total_amount=60.0,
            category="Entertainment",
            date=today - timedelta(days=5),
            created_by=users[0].id,
            participants=[users[0], users[1], users[2]]
        )
        db.add(split_expense2)
        db.commit()
        print("   ✓ Created 2 split expenses")
        
        # Create a settlement
        print("\n7. Creating settlements...")
        settlement = models.Settlement(
            from_user_id=users[1].id,
            to_user_id=users[0].id,
            amount=75.0
        )
        db.add(settlement)
        db.commit()
        print("   ✓ Created 1 settlement")
        
        print("\n" + "="*60)
        print("✓ Mock data created successfully!")
        print("="*60)
        print("\nTest User Credentials:")
        for i, user in enumerate(users, 1):
            print(f"  User {i}:")
            print(f"    Username: {user.username}")
            print(f"    Email:    {user.email}")
            print(f"    Password: password123")
        
        print("\nData Summary:")
        print(f"  • Expenses:       20")
        print(f"  • Budgets:        4")
        print(f"  • Debts:          2")
        print(f"  • Friendships:    2")
        print(f"  • Split Expenses: 2")
        print(f"  • Settlements:    1")
        print("="*60)
        
    except Exception as e:
        db.rollback()
        print(f"\n✗ Error creating mock data: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    create_mock_data()
