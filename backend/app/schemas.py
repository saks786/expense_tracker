from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date, datetime
from typing import Optional, List, Union, Any

# ================= USERS =================

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


# ================= EXPENSES =================

class ExpenseCreate(BaseModel):
    category: str
    amount: float
    description: Optional[str] = ""
    date: Optional[date] = None


class ExpenseUpdate(BaseModel):
    category: Optional[str] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    date: Optional[date] = None


class ExpenseResponse(BaseModel):
    id: int
    category: str
    amount: float
    description: str
    date: date
    user_id: int

    class Config:
        from_attributes = True


# ================= BUDGETS =================

class BudgetCreate(BaseModel):
    category: str
    limit_amount: float
    month: int
    year: int


class BudgetResponse(BaseModel):
    id: int
    category: str
    limit_amount: float
    month: int
    year: int
    user_id: int

    class Config:
        from_attributes = True


# ================= DEBTS =================

class DebtCreate(BaseModel):
    name: str
    principal_amount: float
    interest_rate: float
    emi_amount: float
    emi_date: int
    start_date: date
    remaining_amount: float
    status: Optional[str] = "active"


class DebtUpdate(BaseModel):
    remaining_amount: Optional[float] = None
    status: Optional[str] = None


class DebtResponse(BaseModel):
    id: int
    name: str
    principal_amount: float
    interest_rate: float
    emi_amount: float
    emi_date: int
    start_date: date
    remaining_amount: float
    status: str
    user_id: int

    class Config:
        from_attributes = True


# ================= FRIENDS =================

class FriendRequest(BaseModel):
    friend_username: str


class FriendshipResponse(BaseModel):
    id: int
    user_id: int
    friend_id: int
    status: str
    created_at: datetime
    friend_username: Optional[str] = None

    class Config:
        from_attributes = True


# ================= SPLIT EXPENSES =================

class SplitExpenseCreate(BaseModel):
    description: str
    total_amount: float
    category: str
    participant_ids: List[int]  # Changed from participant_usernames to participant_ids
    date: Any = None  # Accept any type, will be validated/converted
    
    @field_validator('date', mode='before')
    @classmethod
    def validate_date(cls, v):
        if v is None or v == '':
            return None
        if isinstance(v, date):
            return v
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except:
                return None
        return None


class ParticipantInfo(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class SplitExpenseResponse(BaseModel):
    id: int
    description: str
    total_amount: float
    category: str
    date: date
    created_by: int
    created_at: datetime
    participants: List[ParticipantInfo]

    class Config:
        from_attributes = True


# ================= SETTLEMENTS (PHASE 3) =================

class SettlementCreate(BaseModel):
    to_username: str
    amount: float


class SettlementResponse(BaseModel):
    id: int
    from_user_id: int
    to_user_id: int
    amount: float
    created_at: datetime

    class Config:
        from_attributes = True


# ================= PAYMENTS & TRANSACTIONS =================

class PaymentIntentCreate(BaseModel):
    amount: float
    payment_method: str  # "card" or "upi"
    transaction_type: str  # "debt_payment" or "split_expense_payment"
    debt_id: Optional[int] = None
    split_expense_id: Optional[int] = None
    description: Optional[str] = None


class PaymentConfirmCreate(BaseModel):
    payment_intent_id: str
    payment_method_id: str


class TransactionResponse(BaseModel):
    id: int
    user_id: int
    stripe_payment_intent_id: Optional[str]
    amount: float
    currency: str
    payment_method: str
    transaction_type: str
    debt_id: Optional[int]
    split_expense_id: Optional[int]
    status: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ================= GROUPS =================

class GroupCreate(BaseModel):
    name: str
    description: Optional[str] = None
    currency: str = "INR"
    image_url: Optional[str] = None


class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    currency: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class GroupMemberInfo(BaseModel):
    id: int
    user_id: int
    username: str
    role: str
    status: str
    joined_at: datetime

    class Config:
        from_attributes = True


class GroupResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    currency: str
    image_url: Optional[str]
    is_active: bool
    created_by: int
    created_at: datetime
    members: List[GroupMemberInfo] = []

    class Config:
        from_attributes = True


class GroupInvite(BaseModel):
    usernames: List[str]  # List of usernames to invite


class GroupMemberUpdate(BaseModel):
    role: Optional[str] = None  # "admin" or "member"
    status: Optional[str] = None  # "pending" or "accepted"


# ================= GROUP EXPENSES =================

class GroupExpenseParticipantInput(BaseModel):
    user_id: int
    share_amount: float


class GroupExpenseCreate(BaseModel):
    description: str
    total_amount: float
    category: str
    paid_by: int  # User ID who paid
    participants: List[GroupExpenseParticipantInput]
    date: Any = None
    
    @field_validator('date', mode='before')
    @classmethod
    def validate_date(cls, v):
        if v is None or v == '':
            return None
        if isinstance(v, date):
            return v
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except:
                return None
        return None
    
    @field_validator('participants')
    @classmethod
    def validate_participants(cls, v):
        if not v or len(v) == 0:
            raise ValueError('At least one participant is required')
        return v


class GroupExpenseUpdate(BaseModel):
    description: Optional[str] = None
    total_amount: Optional[float] = None
    category: Optional[str] = None
    date: Optional[date] = None


class GroupExpenseParticipantResponse(BaseModel):
    user_id: int
    username: str
    share_amount: float

    class Config:
        from_attributes = True


class GroupExpenseResponse(BaseModel):
    id: int
    group_id: int
    description: str
    total_amount: float
    category: str
    date: date
    paid_by: int
    payer_username: str
    created_at: datetime
    participants: List[GroupExpenseParticipantResponse]

    class Config:
        from_attributes = True


# ================= GROUP SETTLEMENTS =================

class GroupSettlementCreate(BaseModel):
    to_user_id: int
    amount: float


class GroupSettlementResponse(BaseModel):
    id: int
    group_id: int
    from_user_id: int
    to_user_id: int
    amount: float
    created_at: datetime

    class Config:
        from_attributes = True
