from pydantic import BaseModel, EmailStr
from datetime import date as date_type, datetime
from typing import Optional, List

class ExpenseCreate(BaseModel):
    category: str
    amount: float
    description: Optional[str] = ""
    date: Optional[date_type] = None

class ExpenseUpdate(BaseModel):
    category: Optional[str] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    date: Optional[date_type] = None

class ExpenseResponse(BaseModel):
    id: int
    category: str
    amount: float
    description: str
    date: date_type
    user_id: int

    class Config:
        from_attributes = True

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

class DebtCreate(BaseModel):
    name: str
    principal_amount: float
    interest_rate: float
    emi_amount: float
    emi_date: int  # Day of month (1-31)
    start_date: date_type

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
    start_date: date_type
    remaining_amount: float
    status: str
    user_id: int

    class Config:
        from_attributes = True

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

class SplitExpenseCreate(BaseModel):
    description: str
    total_amount: float
    category: str
    date: date_type
    participant_ids: List[int]  # List of user IDs to split with

class SplitExpenseResponse(BaseModel):
    id: int
    description: str
    total_amount: float
    category: str
    date: date_type
    created_by: int
    created_at: datetime
    participants: List[int]  # User IDs
    split_amount: Optional[float] = None  # Amount per person

    class Config:
        from_attributes = True
