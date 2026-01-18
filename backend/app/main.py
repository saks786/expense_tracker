 # backend/app/main.py
from dotenv import load_dotenv
load_dotenv()  # 👈 THIS loads .env into os.environ

import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import date, timedelta

from . import models
from .database import engine, get_db
from .routes import router
from .auth import get_password_hash
from .payments import router as payment_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("expense-backend")

app = FastAPI(title="Expense Tracker API", version="2.0.0")

# CORS - keep narrow in production; allow_origins=["*"] only for temporary testing.
frontend_origins = [
    "http://localhost:5173",
    "http://localhost:5413",
    "http://localhost:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,  # don't duplicate keys
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create tables at startup — log errors but don't crash the entire process
@app.on_event("startup")
async def on_startup():
    logger.info("Startup: attempting to create/verify DB tables...")
    try:
        models.Base.metadata.create_all(bind=engine)
        logger.info("DB tables created/verified.")
    except Exception as e:
        # Log exception (important); don't re-raise to keep process alive
        logger.exception("Failed to create DB tables on startup — check DATABASE_URL and DB connectivity: %s", e)

# small root + ping endpoints for health checks
@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Expense Tracker backend is running"}

@app.get("/ping")
async def ping():
    return {"pong": True}

# Mock Data Creation Endpoint
@app.post("/api/create-mock-data", tags=["Development"])
async def create_mock_data(db: Session = Depends(get_db)):
    """
    Creates mock data for testing. Only use in development!
    """
    try:
        # Check if mock data already exists
        existing_user = db.query(models.User).filter(models.User.username == "testuser1").first()
        if existing_user:
            return {"message": "Mock data already exists", "note": "Delete database to recreate"}
        
        # Create test users
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
        
        # Create expenses for user 1
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
        
        # Create budgets for user 1
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
        
        # Create debts for user 1
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
        
        # Create friendships
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
        
        # Create split expenses
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
        
        # Create a settlement
        settlement = models.Settlement(
            from_user_id=users[1].id,
            to_user_id=users[0].id,
            amount=75.0
        )
        db.add(settlement)
        
        db.commit()
        
        return {
            "message": "Mock data created successfully!",
            "users": [
                {"username": u.username, "email": u.email, "password": "password123"} 
                for u in users
            ],
            "counts": {
                "expenses": 20,
                "budgets": 4,
                "debts": 2,
                "friendships": 2,
                "split_expenses": 2,
                "settlements": 1
            }
        }
    except Exception as e:
        db.rollback()
        logger.exception(f"Error creating mock data: {e}")
        return {"error": str(e)}

# include API router under /api
app.include_router(router)
app.include_router(payment_router)
