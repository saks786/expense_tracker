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

# ================= BUDGET ROUTES =================

@router.get("/budgets", response_model=List[BudgetResponse])
def list_budgets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(Budget).filter(Budget.user_id == current_user.id).all()


@router.post("/budgets", response_model=BudgetResponse)
def create_budget(
    budget: BudgetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_budget = Budget(
        category=budget.category,
        limit_amount=budget.limit_amount,
        month=budget.month,
        year=budget.year,
        user_id=current_user.id,
    )
    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)
    return new_budget


@router.delete("/budgets/{budget_id}")
def delete_budget(
    budget_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    budget = db.query(Budget).filter(
        Budget.id == budget_id,
        Budget.user_id == current_user.id,
    ).first()

    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    db.delete(budget)
    db.commit()
    return {"message": "Budget deleted successfully"}

# ================= DEBT ROUTES =================

@router.get("/debts", response_model=List[DebtResponse])
def list_debts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(Debt).filter(Debt.user_id == current_user.id).all()


@router.post("/debts", response_model=DebtResponse)
def create_debt(
    debt: DebtCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_debt = Debt(
        name=debt.name,
        principal_amount=debt.principal_amount,
        interest_rate=debt.interest_rate,
        emi_amount=debt.emi_amount,
        emi_date=debt.emi_date,
        start_date=debt.start_date,
        remaining_amount=debt.remaining_amount,
        status=debt.status or "active",
        user_id=current_user.id,
    )
    db.add(new_debt)
    db.commit()
    db.refresh(new_debt)
    return new_debt


@router.put("/debts/{debt_id}", response_model=DebtResponse)
def update_debt(
    debt_id: int,
    debt: DebtUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_debt = db.query(Debt).filter(
        Debt.id == debt_id,
        Debt.user_id == current_user.id,
    ).first()

    if not db_debt:
        raise HTTPException(status_code=404, detail="Debt not found")

    for field, value in debt.dict(exclude_unset=True).items():
        setattr(db_debt, field, value)

    db.commit()
    db.refresh(db_debt)
    return db_debt


@router.delete("/debts/{debt_id}")
def delete_debt(
    debt_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    debt = db.query(Debt).filter(
        Debt.id == debt_id,
        Debt.user_id == current_user.id,
    ).first()

    if not debt:
        raise HTTPException(status_code=404, detail="Debt not found")

    db.delete(debt)
    db.commit()
    return {"message": "Debt deleted successfully"}

# ================= FRIENDSHIP ROUTES =================

@router.get("/friends", response_model=List[FriendshipResponse])
def list_friends(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Get accepted friendships where current user is either user or friend
    friendships = db.query(Friendship).filter(
        ((Friendship.user_id == current_user.id) | (Friendship.friend_id == current_user.id)),
        Friendship.status == "accepted"
    ).all()
    return friendships


@router.get("/friends/requests", response_model=List[FriendshipResponse])
def list_friend_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Get pending friend requests sent to the current user
    requests = db.query(Friendship).filter(
        Friendship.friend_id == current_user.id,
        Friendship.status == "pending"
    ).all()
    return requests


@router.post("/friends/request", response_model=FriendshipResponse)
def send_friend_request(
    request: FriendRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        # Log the incoming request
        import logging
        logger = logging.getLogger("expense-backend")
        logger.info(f"Friend request from {current_user.username} to '{request.friend_username}'")
        
        # Clean the username input
        friend_username = request.friend_username.strip()
        
        if not friend_username:
            raise HTTPException(status_code=400, detail="Username cannot be empty")
        
        # Find the friend by username (case-insensitive search)
        friend = db.query(User).filter(
            func.lower(User.username) == friend_username.lower()
        ).first()
        
        if not friend:
            # List available users for debugging
            all_users = db.query(User.username).filter(User.id != current_user.id).all()
            available = [u.username for u in all_users]
            logger.info(f"Available users: {available}")
            raise HTTPException(
                status_code=404, 
                detail=f"User '{friend_username}' not found. Available users: {', '.join(available)}"
            )
        
        if friend.id == current_user.id:
            raise HTTPException(status_code=400, detail="Cannot send friend request to yourself")
        
        # Check if friendship already exists
        existing = db.query(Friendship).filter(
            ((Friendship.user_id == current_user.id) & (Friendship.friend_id == friend.id)) |
            ((Friendship.user_id == friend.id) & (Friendship.friend_id == current_user.id))
        ).first()
        
        if existing:
            logger.info(f"Existing friendship found: status={existing.status}, user_id={existing.user_id}, friend_id={existing.friend_id}")
            if existing.status == "accepted":
                raise HTTPException(
                    status_code=400, 
                    detail=f"You are already friends with {friend.username}"
                )
            elif existing.status == "pending":
                if existing.user_id == current_user.id:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Friend request to {friend.username} is already pending"
                    )
                else:
                    # Auto-accept if they sent us a request and we're trying to send one back
                    logger.info(f"Auto-accepting friend request from {friend.username}")
                    existing.status = "accepted"
                    db.commit()
                    db.refresh(existing)
                    return existing
        
        new_friendship = Friendship(
            user_id=current_user.id,
            friend_id=friend.id,
            status="pending"
        )
        db.add(new_friendship)
        db.commit()
        db.refresh(new_friendship)
        logger.info(f"Friend request created successfully: id={new_friendship.id}")
        return new_friendship
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error in send_friend_request: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/friends/{friendship_id}/accept", response_model=FriendshipResponse)
def accept_friend_request(
    friendship_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    friendship = db.query(Friendship).filter(
        Friendship.id == friendship_id,
        Friendship.friend_id == current_user.id,
        Friendship.status == "pending"
    ).first()
    
    if not friendship:
        raise HTTPException(status_code=404, detail="Friend request not found")
    
    friendship.status = "accepted"
    db.commit()
    db.refresh(friendship)
    return friendship


@router.delete("/friends/{friendship_id}")
def delete_friend(
    friendship_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    friendship = db.query(Friendship).filter(
        Friendship.id == friendship_id,
        ((Friendship.user_id == current_user.id) | (Friendship.friend_id == current_user.id))
    ).first()
    
    if not friendship:
        raise HTTPException(status_code=404, detail="Friendship not found")
    
    db.delete(friendship)
    db.commit()
    return {"message": "Friendship deleted successfully"}

# ================= SPLIT EXPENSE ROUTES =================

@router.get("/split-expenses", response_model=List[SplitExpenseResponse])
def list_split_expenses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Get split expenses where user is creator or participant
    split_expenses = db.query(SplitExpense).filter(
        (SplitExpense.created_by == current_user.id) |
        (SplitExpense.participants.any(id=current_user.id))
    ).all()
    return split_expenses


@router.post("/split-expenses", response_model=SplitExpenseResponse)
def create_split_expense(
    expense: SplitExpenseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Get participant users
    participants = []
    for username in expense.participant_usernames:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"User {username} not found")
        participants.append(user)
    
    # Add current user to participants if not already included
    if current_user not in participants:
        participants.append(current_user)
    
    new_split_expense = SplitExpense(
        description=expense.description,
        total_amount=expense.total_amount,
        category=expense.category,
        date=expense.date or date.today(),
        created_by=current_user.id,
        participants=participants
    )
    db.add(new_split_expense)
    db.commit()
    db.refresh(new_split_expense)
    return new_split_expense


@router.delete("/split-expenses/{expense_id}")
def delete_split_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    split_expense = db.query(SplitExpense).filter(
        SplitExpense.id == expense_id,
        SplitExpense.created_by == current_user.id
    ).first()
    
    if not split_expense:
        raise HTTPException(status_code=404, detail="Split expense not found or you're not the creator")
    
    db.delete(split_expense)
    db.commit()
    return {"message": "Split expense deleted successfully"}

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

