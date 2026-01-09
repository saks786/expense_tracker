from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Expense, User, Budget, Debt, Friendship, SplitExpense
from .schemas import (
    ExpenseCreate, ExpenseUpdate, ExpenseResponse, 
    BudgetCreate, BudgetResponse,
    DebtCreate, DebtUpdate, DebtResponse,
    FriendRequest, FriendshipResponse,
    SplitExpenseCreate, SplitExpenseResponse
)
from .auth import (
    verify_password, get_password_hash, create_access_token,
    verify_token, UserCreate, UserResponse, Token, ACCESS_TOKEN_EXPIRE_MINUTES
)
from datetime import date, timedelta
from typing import List

router = APIRouter(prefix="/api")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
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

# Authentication Routes
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_email = db.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# Expense Routes
@router.get("/expenses", response_model=List[ExpenseResponse])
def list_expenses(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Expense).filter(Expense.user_id == current_user.id).all()

@router.post("/expenses", response_model=ExpenseResponse)
def add_expense(expense: ExpenseCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    expense_date = expense.date if expense.date else date.today()
    new_exp = Expense(
        category=expense.category,
        amount=expense.amount,
        description=expense.description,
        date=expense_date,
        user_id=current_user.id
    )
    db.add(new_exp)
    db.commit()
    db.refresh(new_exp)
    return new_exp

@router.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    if expense.category is not None:
        db_expense.category = expense.category
    if expense.amount is not None:
        db_expense.amount = expense.amount
    if expense.description is not None:
        db_expense.description = expense.description
    if expense.date is not None:
        db_expense.date = expense.date
    
    db.commit()
    db.refresh(db_expense)
    return db_expense

@router.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db.delete(db_expense)
    db.commit()
    return {"message": "Expense deleted successfully"}

# Budget Routes
@router.get("/budgets", response_model=List[BudgetResponse])
def list_budgets(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Budget).filter(Budget.user_id == current_user.id).all()

@router.post("/budgets", response_model=BudgetResponse)
def create_budget(
    budget: BudgetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_budget = Budget(
        category=budget.category,
        limit_amount=budget.limit_amount,
        month=budget.month,
        year=budget.year,
        user_id=current_user.id
    )
    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)
    return new_budget

@router.get("/analytics/category")
def get_category_analytics(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    expenses = db.query(Expense).filter(Expense.user_id == current_user.id).all()
    category_totals = {}
    for exp in expenses:
        if exp.category in category_totals:
            category_totals[exp.category] += exp.amount
        else:
            category_totals[exp.category] = exp.amount
    return category_totals

@router.get("/analytics/monthly")
def get_monthly_analytics(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    expenses = db.query(Expense).filter(Expense.user_id == current_user.id).all()
    monthly_data = {}
    for exp in expenses:
        month_key = f"{exp.date.year}-{exp.date.month:02d}"
        if month_key in monthly_data:
            monthly_data[month_key] += exp.amount
        else:
            monthly_data[month_key] = exp.amount
    return monthly_data

# Debt Routes
@router.get("/debts", response_model=List[DebtResponse])
def list_debts(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Debt).filter(Debt.user_id == current_user.id).all()

@router.post("/debts", response_model=DebtResponse)
def create_debt(debt: DebtCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_debt = Debt(
        name=debt.name,
        principal_amount=debt.principal_amount,
        interest_rate=debt.interest_rate,
        emi_amount=debt.emi_amount,
        emi_date=debt.emi_date,
        start_date=debt.start_date,
        remaining_amount=debt.principal_amount,
        user_id=current_user.id
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
    db: Session = Depends(get_db)
):
    db_debt = db.query(Debt).filter(
        Debt.id == debt_id,
        Debt.user_id == current_user.id
    ).first()
    if not db_debt:
        raise HTTPException(status_code=404, detail="Debt not found")
    
    if debt.remaining_amount is not None:
        db_debt.remaining_amount = debt.remaining_amount
    if debt.status is not None:
        db_debt.status = debt.status
    
    db.commit()
    db.refresh(db_debt)
    return db_debt

@router.delete("/debts/{debt_id}")
def delete_debt(
    debt_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_debt = db.query(Debt).filter(
        Debt.id == debt_id,
        Debt.user_id == current_user.id
    ).first()
    if not db_debt:
        raise HTTPException(status_code=404, detail="Debt not found")
    
    db.delete(db_debt)
    db.commit()
    return {"message": "Debt deleted successfully"}

# Friend Routes
@router.get("/friends", response_model=List[FriendshipResponse])
def list_friends(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Get accepted friendships
    friendships = db.query(Friendship).filter(
        ((Friendship.user_id == current_user.id) | (Friendship.friend_id == current_user.id)),
        Friendship.status == "accepted"
    ).all()
    
    result = []
    for f in friendships:
        friend_user = None
        if f.user_id == current_user.id:
            friend_user = db.query(User).filter(User.id == f.friend_id).first()
        else:
            friend_user = db.query(User).filter(User.id == f.user_id).first()
        
        result.append(FriendshipResponse(
            id=f.id,
            user_id=f.user_id,
            friend_id=f.friend_id,
            status=f.status,
            created_at=f.created_at,
            friend_username=friend_user.username if friend_user else None
        ))
    return result

@router.get("/friends/requests", response_model=List[FriendshipResponse])
def list_friend_requests(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Get pending friend requests received by current user
    requests = db.query(Friendship).filter(
        Friendship.friend_id == current_user.id,
        Friendship.status == "pending"
    ).all()
    
    result = []
    for r in requests:
        requester = db.query(User).filter(User.id == r.user_id).first()
        result.append(FriendshipResponse(
            id=r.id,
            user_id=r.user_id,
            friend_id=r.friend_id,
            status=r.status,
            created_at=r.created_at,
            friend_username=requester.username if requester else None
        ))
    return result

@router.post("/friends/request", response_model=FriendshipResponse)
def send_friend_request(
    friend_req: FriendRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Find friend by username
    friend = db.query(User).filter(User.username == friend_req.friend_username).first()
    if not friend:
        raise HTTPException(status_code=404, detail="User not found")
    
    if friend.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot add yourself as friend")
    
    # Check if friendship already exists
    existing = db.query(Friendship).filter(
        ((Friendship.user_id == current_user.id) & (Friendship.friend_id == friend.id)) |
        ((Friendship.user_id == friend.id) & (Friendship.friend_id == current_user.id))
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Friendship already exists")
    
    new_friendship = Friendship(
        user_id=current_user.id,
        friend_id=friend.id,
        status="pending"
    )
    db.add(new_friendship)
    db.commit()
    db.refresh(new_friendship)
    
    return FriendshipResponse(
        id=new_friendship.id,
        user_id=new_friendship.user_id,
        friend_id=new_friendship.friend_id,
        status=new_friendship.status,
        created_at=new_friendship.created_at,
        friend_username=friend.username
    )

@router.put("/friends/{friendship_id}/accept")
def accept_friend_request(
    friendship_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
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
    return {"message": "Friend request accepted"}

@router.delete("/friends/{friendship_id}")
def remove_friend(
    friendship_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    friendship = db.query(Friendship).filter(
        Friendship.id == friendship_id,
        ((Friendship.user_id == current_user.id) | (Friendship.friend_id == current_user.id))
    ).first()
    
    if not friendship:
        raise HTTPException(status_code=404, detail="Friendship not found")
    
    db.delete(friendship)
    db.commit()
    return {"message": "Friend removed successfully"}

# Split Expense Routes
@router.get("/split-expenses", response_model=List[SplitExpenseResponse])
def list_split_expenses(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Get split expenses where current user is creator or participant
    split_expenses = db.query(SplitExpense).filter(
        (SplitExpense.created_by == current_user.id) |
        (SplitExpense.participants.any(id=current_user.id))
    ).all()
    
    result = []
    for se in split_expenses:
        participant_ids = [p.id for p in se.participants]
        split_amount = se.total_amount / len(participant_ids) if participant_ids else se.total_amount
        
        result.append(SplitExpenseResponse(
            id=se.id,
            description=se.description,
            total_amount=se.total_amount,
            category=se.category,
            date=se.date,
            created_by=se.created_by,
            created_at=se.created_at,
            participants=participant_ids,
            split_amount=round(split_amount, 2)
        ))
    return result

@router.post("/split-expenses", response_model=SplitExpenseResponse)
def create_split_expense(
    split_exp: SplitExpenseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify all participants are friends
    for participant_id in split_exp.participant_ids:
        if participant_id == current_user.id:
            continue
        
        friendship = db.query(Friendship).filter(
            ((Friendship.user_id == current_user.id) & (Friendship.friend_id == participant_id)) |
            ((Friendship.user_id == participant_id) & (Friendship.friend_id == current_user.id)),
            Friendship.status == "accepted"
        ).first()
        
        if not friendship:
            raise HTTPException(status_code=400, detail=f"User {participant_id} is not your friend")
    
    # Get participant user objects
    participants = db.query(User).filter(User.id.in_(split_exp.participant_ids)).all()
    
    # Include creator if not already in participants
    if current_user.id not in split_exp.participant_ids:
        participants.append(current_user)
    
    new_split = SplitExpense(
        description=split_exp.description,
        total_amount=split_exp.total_amount,
        category=split_exp.category,
        date=split_exp.date,
        created_by=current_user.id,
        participants=participants
    )
    db.add(new_split)
    db.commit()
    db.refresh(new_split)
    
    participant_ids = [p.id for p in new_split.participants]
    split_amount = new_split.total_amount / len(participant_ids) if participant_ids else new_split.total_amount
    
    return SplitExpenseResponse(
        id=new_split.id,
        description=new_split.description,
        total_amount=new_split.total_amount,
        category=new_split.category,
        date=new_split.date,
        created_by=new_split.created_by,
        created_at=new_split.created_at,
        participants=participant_ids,
        split_amount=round(split_amount, 2)
    )

@router.delete("/split-expenses/{split_id}")
def delete_split_expense(
    split_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    split_exp = db.query(SplitExpense).filter(
        SplitExpense.id == split_id,
        SplitExpense.created_by == current_user.id
    ).first()
    
    if not split_exp:
        raise HTTPException(status_code=404, detail="Split expense not found or not authorized")
    
    db.delete(split_exp)
    db.commit()
    return {"message": "Split expense deleted successfully"}
