from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta
from typing import List
from .email_service import send_email


from .database import SessionLocal
from .models import (
    Expense,
    User,
    Budget,
    Debt,
    Friendship,
    SplitExpense,
)
from .schemas import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
    BudgetCreate,
    BudgetResponse,
    DebtCreate,
    DebtUpdate,
    DebtResponse,
    FriendRequest,
    FriendshipResponse,
    SplitExpenseCreate,
    SplitExpenseResponse,
    SettlementCreate,
    SettlementResponse,
)
from .auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token,
    UserCreate,
    UserResponse,
    Token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

router = APIRouter(prefix="/api")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

# ================= DB DEPENDENCY =================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ================= AUTH DEPENDENCY =================

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_token(token)
    if token_data is None:
        raise credentials_exception

    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception

    return user

# ================= AUTH ROUTES =================

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# ================= EXPENSE ROUTES =================

@router.get("/expenses", response_model=List[ExpenseResponse])
def list_expenses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(Expense).filter(Expense.user_id == current_user.id).all()


@router.post("/expenses", response_model=ExpenseResponse)
def add_expense(
    expense: ExpenseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_expense = Expense(
        category=expense.category,
        amount=expense.amount,
        description=expense.description,
        date=expense.date or date.today(),
        user_id=current_user.id,
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id,
    ).first()

    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    for field, value in expense.dict(exclude_unset=True).items():
        setattr(db_expense, field, value)

    db.commit()
    db.refresh(db_expense)
    return db_expense


@router.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id,
    ).first()

    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(db_expense)
    db.commit()
    return {"message": "Expense deleted successfully"}

# ================= ANALYTICS =================

@router.get("/analytics/category")
def category_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    data = (
        db.query(Expense.category, func.sum(Expense.amount))
        .filter(Expense.user_id == current_user.id)
        .group_by(Expense.category)
        .all()
    )
    return [{"category": c, "total": float(t)} for c, t in data]


@router.get("/analytics/monthly")
def monthly_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    data = (
        db.query(
            func.date_trunc("month", Expense.date).label("month"),
            func.sum(Expense.amount).label("total"),
        )
        .filter(Expense.user_id == current_user.id)
        .group_by("month")
        .order_by("month")
        .all()
    )
    return [{"month": m.strftime("%Y-%m"), "total": float(t)} for m, t in data]

# ================= SPLIT BALANCES (PHASE 3) =================

@router.get("/balances")
def get_balances(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    balances = {}

    split_expenses = db.query(SplitExpense).filter(
        (SplitExpense.created_by == current_user.id)
        | (SplitExpense.participants.any(id=current_user.id))
    ).all()

    for exp in split_expenses:
        participants = exp.participants
        if not participants:
            continue

        split_amount = exp.total_amount / len(participants)

        for p in participants:
            if p.id == current_user.id:
                if exp.created_by == current_user.id:
                    balances["you"] = balances.get("you", 0) + (exp.total_amount - split_amount)
                else:
                    balances["you"] = balances.get("you", 0) - split_amount
            else:
                balances.setdefault(p.username, 0)
                if exp.created_by == current_user.id:
                    balances[p.username] -= split_amount
                elif p.id == exp.created_by:
                    balances[p.username] += split_amount

    return balances

# ================= SETTLEMENT SUGGESTIONS =================

@router.get("/settlements/suggestions")
def settlement_suggestions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    balances = get_balances(current_user, db)
    suggestions = []

    for user, amount in balances.items():
        if user == "you":
            continue
        if amount < 0:
            suggestions.append({"from": user, "to": "you", "amount": round(abs(amount), 2)})
        elif amount > 0:
            suggestions.append({"from": "you", "to": user, "amount": round(amount, 2)})

    return suggestions

# ================= CREATE SETTLEMENT =================

@router.post("/settlements", response_model=SettlementResponse)
def create_settlement(
    settlement: SettlementCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # ✅ Lazy import to avoid circular import
    from .models import Settlement

    to_user = db.query(User).filter(User.username == settlement.to_username).first()
    if not to_user:
        raise HTTPException(status_code=404, detail="User not found")

    new_settlement = Settlement(
        from_user_id=current_user.id,
        to_user_id=to_user.id,
        amount=settlement.amount,
    )

    db.add(new_settlement)
    db.commit()
    db.refresh(new_settlement)
    return new_settlement

# ================= EMAIL TEST =================

@router.get("/test-email")
def test_email():
    success = send_email(
        to_email="sohambose601@gmail.com",  # put your real email
        subject="SendGrid Test Email ✅",
        html_content="""
        <h2>Hello Saksham 👋</h2>
        <p>Your SendGrid email integration is working.</p>
        """
    )
    return {"email_sent": success}

