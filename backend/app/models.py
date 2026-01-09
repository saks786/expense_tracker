from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean, Table, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# Association table for split expenses participants
split_participants = Table(
    'split_participants',
    Base.metadata,
    Column('split_expense_id', Integer, ForeignKey('split_expenses.id', ondelete='CASCADE')),
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'))
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    expenses = relationship("Expense", back_populates="owner", cascade="all, delete-orphan")
    budgets = relationship("Budget", back_populates="owner", cascade="all, delete-orphan")
    debts = relationship("Debt", back_populates="owner", cascade="all, delete-orphan")
    # Friendships where this user is the requester
    friendships_initiated = relationship("Friendship", foreign_keys="Friendship.user_id", back_populates="user", cascade="all, delete-orphan")
    # Friendships where this user is the friend
    friendships_received = relationship("Friendship", foreign_keys="Friendship.friend_id", back_populates="friend", cascade="all, delete-orphan")
    # Split expenses created by this user
    split_expenses_created = relationship("SplitExpense", back_populates="creator", cascade="all, delete-orphan")
    # Split expenses this user is part of
    split_expenses_participating = relationship("SplitExpense", secondary=split_participants, back_populates="participants")

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    amount = Column(Float)
    date = Column(Date)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="expenses")

class Budget(Base):
    __tablename__ = "budgets"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    limit_amount = Column(Float)
    month = Column(Integer)
    year = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="budgets")

class Debt(Base):
    __tablename__ = "debts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)  # Debt name/description
    principal_amount = Column(Float)
    interest_rate = Column(Float)  # Annual interest rate percentage
    emi_amount = Column(Float)
    emi_date = Column(Integer)  # Day of month (1-31)
    start_date = Column(Date)
    remaining_amount = Column(Float)
    status = Column(String, default="active")  # active, paid
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="debts")

class Friendship(Base):
    __tablename__ = "friendships"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    friend_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pending")  # pending, accepted, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", foreign_keys=[user_id], back_populates="friendships_initiated")
    friend = relationship("User", foreign_keys=[friend_id], back_populates="friendships_received")

class SplitExpense(Base):
    __tablename__ = "split_expenses"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    total_amount = Column(Float)
    category = Column(String)
    date = Column(Date)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    creator = relationship("User", foreign_keys=[created_by], back_populates="split_expenses_created")
    participants = relationship("User", secondary=split_participants, back_populates="split_expenses_participating")
