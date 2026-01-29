from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey,
    Boolean,
    Table,
    DateTime
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# ------------------ ASSOCIATION TABLES ------------------

split_participants = Table(
    "split_participants",
    Base.metadata,
    Column("split_expense_id", Integer, ForeignKey("split_expenses.id", ondelete="CASCADE")),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
)

# ------------------ USER ------------------

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

    friendships_initiated = relationship(
        "Friendship",
        foreign_keys="Friendship.user_id",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    friendships_received = relationship(
        "Friendship",
        foreign_keys="Friendship.friend_id",
        back_populates="friend",
        cascade="all, delete-orphan",
    )

    split_expenses_created = relationship(
        "SplitExpense",
        back_populates="creator",
        cascade="all, delete-orphan",
    )
    split_expenses_participating = relationship(
        "SplitExpense",
        secondary=split_participants,
        back_populates="participants",
    )

    # Group relationships
    groups_created = relationship(
        "Group",
        back_populates="creator",
        cascade="all, delete-orphan",
    )
    group_memberships = relationship(
        "GroupMember",
        back_populates="user",
        cascade="all, delete-orphan",
    )

# ------------------ EXPENSE ------------------

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date)
    description = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="expenses")

# ------------------ BUDGET ------------------

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    limit_amount = Column(Float, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="budgets")

# ------------------ DEBT ------------------

class Debt(Base):
    __tablename__ = "debts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    principal_amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    emi_amount = Column(Float, nullable=False)
    emi_date = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    remaining_amount = Column(Float, nullable=False)
    status = Column(String, default="active")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="debts")

# ------------------ FRIENDSHIP ------------------

class Friendship(Base):
    __tablename__ = "friendships"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    friend_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", foreign_keys=[user_id], back_populates="friendships_initiated")
    friend = relationship("User", foreign_keys=[friend_id], back_populates="friendships_received")

# ------------------ SPLIT EXPENSE ------------------

class SplitExpense(Base):
    __tablename__ = "split_expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    total_amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    creator = relationship("User", back_populates="split_expenses_created")

    participants = relationship(
        "User",
        secondary=split_participants,
        back_populates="split_expenses_participating",
    )

# ------------------ SETTLEMENT ------------------

class Settlement(Base):
    __tablename__ = "settlements"

    id = Column(Integer, primary_key=True, index=True)
    from_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    to_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# ------------------ TRANSACTION (PAYMENTS) ------------------

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    stripe_payment_intent_id = Column(String, unique=True, index=True, nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="INR")
    payment_method = Column(String, nullable=False)  # "card" or "upi"
    transaction_type = Column(String, nullable=False)  # "debt_payment" or "split_expense_payment"
    debt_id = Column(Integer, ForeignKey("debts.id"), nullable=True)
    split_expense_id = Column(Integer, ForeignKey("split_expenses.id"), nullable=True)
    status = Column(String, default="pending")  # "pending", "succeeded", "failed"
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="transactions")
    debt = relationship("Debt", backref="payments")
    split_expense = relationship("SplitExpense", backref="payments")

# ------------------ GROUP ------------------

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    currency = Column(String, default="INR", nullable=False)
    image_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    creator = relationship("User", back_populates="groups_created")

    members = relationship("GroupMember", back_populates="group", cascade="all, delete-orphan")
    expenses = relationship("GroupExpense", back_populates="group", cascade="all, delete-orphan")
    settlements = relationship("GroupSettlement", back_populates="group", cascade="all, delete-orphan")

# ------------------ GROUP MEMBER ------------------

class GroupMember(Base):
    __tablename__ = "group_members"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String, default="member", nullable=False)  # "admin" or "member"
    status = Column(String, default="pending", nullable=False)  # "pending" or "accepted"
    joined_at = Column(DateTime, default=datetime.utcnow)

    group = relationship("Group", back_populates="members")
    user = relationship("User", back_populates="group_memberships")

# ------------------ GROUP EXPENSE ------------------

class GroupExpense(Base):
    __tablename__ = "group_expenses"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    description = Column(String, nullable=False)
    total_amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    paid_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    payer = relationship("User", backref="group_expenses_paid")
    
    group = relationship("Group", back_populates="expenses")
    participants = relationship(
        "GroupExpenseParticipant",
        back_populates="expense",
        cascade="all, delete-orphan"
    )

# ------------------ GROUP EXPENSE PARTICIPANT ------------------

class GroupExpenseParticipant(Base):
    __tablename__ = "group_expense_participants"

    id = Column(Integer, primary_key=True, index=True)
    group_expense_id = Column(Integer, ForeignKey("group_expenses.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    share_amount = Column(Float, nullable=False)

    expense = relationship("GroupExpense", back_populates="participants")
    user = relationship("User", backref="group_expense_participations")

# ------------------ GROUP SETTLEMENT ------------------

class GroupSettlement(Base):
    __tablename__ = "group_settlements"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    from_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    to_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    group = relationship("Group", back_populates="settlements")
    from_user = relationship("User", foreign_keys=[from_user_id], backref="group_settlements_made")
    to_user = relationship("User", foreign_keys=[to_user_id], backref="group_settlements_received")
