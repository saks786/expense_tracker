"""
Group Management Routes
Handles group creation, member management, expenses, balances, and settlements.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import date, datetime
from typing import List, Dict, Any, Union
from collections import defaultdict

from .database import SessionLocal
from .models import (
    User,
    Group,
    GroupMember,
    GroupExpense,
    GroupExpenseParticipant,
    GroupSettlement,
    Friendship,
)
from .schemas import (
    GroupCreate,
    GroupUpdate,
    GroupResponse,
    GroupMemberInfo,
    GroupInvite,
    GroupMemberUpdate,
    GroupExpenseCreate,
    GroupExpenseUpdate,
    GroupExpenseResponse,
    GroupExpenseParticipantResponse,
    GroupSettlementCreate,
    GroupSettlementResponse,
)

# Import get_current_user from routes module
from .routes import get_current_user

router = APIRouter(prefix="/api/groups", tags=["groups"])


# ================= HELPER FUNCTIONS =================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def is_group_member(group_id: int, user_id: int, db: Session, accepted_only: bool = True) -> GroupMember:
    """Check if user is a member of the group"""
    query = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == user_id
    )
    if accepted_only:
        query = query.filter(GroupMember.status == "accepted")
    
    member = query.first()
    if not member:
        raise HTTPException(status_code=403, detail="You are not a member of this group")
    return member


def is_group_admin(group_id: int, user_id: int, db: Session) -> GroupMember:
    """Check if user is an admin of the group"""
    member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == user_id,
        GroupMember.status == "accepted",
        GroupMember.role == "admin"
    ).first()
    
    if not member:
        raise HTTPException(status_code=403, detail="You must be a group admin to perform this action")
    return member


def get_group_or_404(group_id: int, db: Session) -> Group:
    """Get group or raise 404"""
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group


# ================= GROUP MANAGEMENT ENDPOINTS =================

@router.post("", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
def create_group(
    group_data: GroupCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new group.
    The creator is automatically added as an admin member.
    """
    # Create the group
    new_group = Group(
        name=group_data.name,
        description=group_data.description,
        currency=group_data.currency,
        image_url=group_data.image_url,
        created_by=current_user.id,
    )
    db.add(new_group)
    db.flush()  # Get the ID without committing

    # Add creator as admin member
    creator_member = GroupMember(
        group_id=new_group.id,
        user_id=current_user.id,
        role="admin",
        status="accepted",
    )
    db.add(creator_member)
    
    db.commit()
    db.refresh(new_group)

    # Build response with member info
    return build_group_response(new_group, db)


@router.get("", response_model=List[GroupResponse])
def list_user_groups(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    include_pending: bool = False,
):
    """
    List all groups the current user is a member of.
    By default, only shows accepted memberships.
    """
    query = db.query(Group).join(GroupMember).filter(
        GroupMember.user_id == current_user.id,
        Group.is_active == True,
    )
    
    if not include_pending:
        query = query.filter(GroupMember.status == "accepted")
    
    groups = query.all()
    return [build_group_response(group, db) for group in groups]


@router.get("/{group_id}", response_model=GroupResponse)
def get_group_details(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get detailed information about a specific group"""
    group = get_group_or_404(group_id, db)
    is_group_member(group_id, current_user.id, db)
    
    return build_group_response(group, db)


@router.put("/{group_id}", response_model=GroupResponse)
def update_group(
    group_id: int,
    group_data: GroupUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update group details (admin only)"""
    group = get_group_or_404(group_id, db)
    is_group_admin(group_id, current_user.id, db)
    
    # Update fields
    if group_data.name is not None:
        group.name = group_data.name
    if group_data.description is not None:
        group.description = group_data.description
    if group_data.currency is not None:
        group.currency = group_data.currency
    if group_data.image_url is not None:
        group.image_url = group_data.image_url
    if group_data.is_active is not None:
        group.is_active = group_data.is_active
    
    db.commit()
    db.refresh(group)
    
    return build_group_response(group, db)


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Archive a group (admin only).
    Sets is_active to False instead of deleting.
    """
    group = get_group_or_404(group_id, db)
    is_group_admin(group_id, current_user.id, db)
    
    group.is_active = False
    db.commit()
    
    return None


# ================= MEMBER MANAGEMENT ENDPOINTS =================

@router.post("/{group_id}/invite", response_model=Dict[str, str])
def invite_members(
    group_id: int,
    invite_data: GroupInvite,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Invite users to join the group (any member can invite, but users must be friends)"""
    group = get_group_or_404(group_id, db)
    is_group_member(group_id, current_user.id, db)
    
    invited_count = 0
    not_found = []
    already_members = []
    not_friends = []
    cannot_invite_self = []  # Separate category for self-invitation
    
    for username in invite_data.usernames:
        # Clean the username
        username = username.strip()
        
        # Check if user exists - fetch by username first
        user = db.query(User).filter(
            func.lower(User.username) == username.lower()
        ).first()
        
        if not user:
            not_found.append(username)
            continue
        
        # Don't allow inviting yourself
        if user.id == current_user.id:
            cannot_invite_self.append(username)  # Use specific list for self-invitation
            continue
        
        # Check if they are friends (REQUIRED for group invitations)
        friendship = db.query(Friendship).filter(
            or_(
                and_(
                    Friendship.user_id == current_user.id,
                    Friendship.friend_id == user.id,
                    Friendship.status == "accepted"
                ),
                and_(
                    Friendship.user_id == user.id,
                    Friendship.friend_id == current_user.id,
                    Friendship.status == "accepted"
                )
            )
        ).first()
        
        if not friendship:
            not_friends.append(username)
            continue
        
        # Check if already a member
        existing = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user.id
        ).first()
        
        if existing:
            already_members.append(username)
            continue
        
        # Create pending membership
        new_member = GroupMember(
            group_id=group_id,
            user_id=user.id,
            role="member",
            status="pending",
        )
        db.add(new_member)
        invited_count += 1
    
    db.commit()
    
    message_parts = []
    if invited_count > 0:
        message_parts.append(f"Successfully invited {invited_count} user(s)")
    if not_found:
        message_parts.append(f"Users not found: {', '.join(not_found)}")
    if cannot_invite_self:
        message_parts.append(f"Cannot invite yourself: {', '.join(cannot_invite_self)}")
    if not_friends:
        message_parts.append(f"Not friends with: {', '.join(not_friends)}. You can only invite friends to groups")
    if already_members:
        message_parts.append(f"Already members: {', '.join(already_members)}")
    
    return {"message": ". ".join(message_parts) if message_parts else "No users invited"}


@router.get("/invitations/pending", response_model=List[GroupResponse])
def get_pending_invitations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all pending group invitations for the current user"""
    # Find all groups where user has pending membership
    pending_memberships = db.query(GroupMember).filter(
        GroupMember.user_id == current_user.id,
        GroupMember.status == "pending"
    ).all()
    
    groups = []
    for membership in pending_memberships:
        group = db.query(Group).filter(
            Group.id == membership.group_id,
            Group.is_active == True
        ).first()
        if group:
            groups.append(build_group_response(group, db))
    
    return groups


@router.post("/{group_id}/join", response_model=Dict[str, str])
def accept_group_invitation(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Accept a pending group invitation"""
    group = get_group_or_404(group_id, db)
    
    member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == current_user.id,
        GroupMember.status == "pending"
    ).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="No pending invitation found")
    
    member.status = "accepted"
    db.commit()
    
    return {"message": "Successfully joined the group"}


@router.put("/{group_id}/members/{user_id}", response_model=Dict[str, str])
def update_member_role(
    group_id: int,
    user_id: int,
    update_data: GroupMemberUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update member role or status (admin only)"""
    group = get_group_or_404(group_id, db)
    is_group_admin(group_id, current_user.id, db)
    
    member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == user_id
    ).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Prevent removing the last admin
    if update_data.role == "member" and member.role == "admin":
        admin_count = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.role == "admin",
            GroupMember.status == "accepted"
        ).count()
        
        if admin_count <= 1:
            raise HTTPException(status_code=400, detail="Cannot remove the last admin")
    
    if update_data.role is not None:
        member.role = update_data.role
    if update_data.status is not None:
        member.status = update_data.status
    
    db.commit()
    
    return {"message": "Member updated successfully"}


@router.delete("/{group_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_member(
    group_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Remove a member from the group.
    Admins can remove any member. Members can remove themselves (leave group).
    """
    group = get_group_or_404(group_id, db)
    
    # Check permissions
    if user_id != current_user.id:
        is_group_admin(group_id, current_user.id, db)
    
    member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == user_id
    ).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Prevent removing the last admin
    if member.role == "admin":
        admin_count = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.role == "admin",
            GroupMember.status == "accepted"
        ).count()
        
        if admin_count <= 1:
            raise HTTPException(status_code=400, detail="Cannot remove the last admin")
    
    db.delete(member)
    db.commit()
    
    return None


# ================= GROUP EXPENSE ENDPOINTS =================

@router.post("/{group_id}/expenses", response_model=GroupExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_group_expense(
    group_id: int,
    expense_data: GroupExpenseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new expense for the group"""
    group = get_group_or_404(group_id, db)
    is_group_member(group_id, current_user.id, db)
    
    # Validate paid_by is a group member
    payer_member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == expense_data.paid_by,
        GroupMember.status == "accepted"
    ).first()
    
    if not payer_member:
        raise HTTPException(status_code=400, detail="Payer must be a group member")
    
    # Validate all participants are group members
    for participant in expense_data.participants:
        member = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == participant.user_id,
            GroupMember.status == "accepted"
        ).first()
        
        if not member:
            raise HTTPException(
                status_code=400,
                detail=f"User {participant.user_id} is not a member of this group"
            )
    
    # Validate share amounts sum to total
    total_shares = sum(p.share_amount for p in expense_data.participants)
    if abs(total_shares - expense_data.total_amount) > 0.01:  # Allow for floating point errors
        raise HTTPException(
            status_code=400,
            detail=f"Participant shares ({total_shares}) must equal total amount ({expense_data.total_amount})"
        )
    
    # Create the expense
    expense_date = expense_data.date if expense_data.date else date.today()
    new_expense = GroupExpense(
        group_id=group_id,
        description=expense_data.description,
        total_amount=expense_data.total_amount,
        category=expense_data.category,
        paid_by=expense_data.paid_by,
        date=expense_date,
    )
    db.add(new_expense)
    db.flush()
    
    # Add participants
    for participant in expense_data.participants:
        participant_entry = GroupExpenseParticipant(
            group_expense_id=new_expense.id,
            user_id=participant.user_id,
            share_amount=participant.share_amount,
        )
        db.add(participant_entry)
    
    db.commit()
    db.refresh(new_expense)
    
    return build_expense_response(new_expense, db)


@router.get("/{group_id}/expenses", response_model=List[GroupExpenseResponse])
def list_group_expenses(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 100,
):
    """List all expenses for a group"""
    group = get_group_or_404(group_id, db)
    is_group_member(group_id, current_user.id, db)
    
    expenses = db.query(GroupExpense).filter(
        GroupExpense.group_id == group_id
    ).order_by(GroupExpense.date.desc()).limit(limit).all()
    
    return [build_expense_response(expense, db) for expense in expenses]


@router.put("/{group_id}/expenses/{expense_id}", response_model=GroupExpenseResponse)
def update_group_expense(
    group_id: int,
    expense_id: int,
    expense_data: GroupExpenseUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a group expense (admin only)"""
    group = get_group_or_404(group_id, db)
    is_group_admin(group_id, current_user.id, db)
    
    expense = db.query(GroupExpense).filter(
        GroupExpense.id == expense_id,
        GroupExpense.group_id == group_id
    ).first()
    
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    if expense_data.description is not None:
        expense.description = expense_data.description
    if expense_data.total_amount is not None:
        expense.total_amount = expense_data.total_amount
    if expense_data.category is not None:
        expense.category = expense_data.category
    if expense_data.date is not None:
        expense.date = expense_data.date
    
    db.commit()
    db.refresh(expense)
    
    return build_expense_response(expense, db)


@router.delete("/{group_id}/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group_expense(
    group_id: int,
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a group expense (admin only)"""
    group = get_group_or_404(group_id, db)
    is_group_admin(group_id, current_user.id, db)
    
    expense = db.query(GroupExpense).filter(
        GroupExpense.id == expense_id,
        GroupExpense.group_id == group_id
    ).first()
    
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db.delete(expense)
    db.commit()
    
    return None


# ================= BALANCES & SETTLEMENTS =================

@router.get("/{group_id}/balances", response_model=Dict[int, Dict[str, Union[str, float]]])
def get_group_balances(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Calculate net balances for all group members.
    Returns: {user_id: {"username": str, "balance": float}}
    Positive balance = others owe this user
    Negative balance = this user owes others
    """
    group = get_group_or_404(group_id, db)
    is_group_member(group_id, current_user.id, db)
    
    # Get all group members
    members = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.status == "accepted"
    ).all()
    
    member_ids = [m.user_id for m in members]
    balances = {m.user_id: 0.0 for m in members}
    
    # Get all group expenses
    expenses = db.query(GroupExpense).filter(
        GroupExpense.group_id == group_id
    ).all()
    
    for expense in expenses:
        # Payer gets credited
        balances[expense.paid_by] += expense.total_amount
        
        # Participants get debited by their share
        for participant in expense.participants:
            balances[participant.user_id] -= participant.share_amount
    
    # Subtract settlements
    settlements = db.query(GroupSettlement).filter(
        GroupSettlement.group_id == group_id
    ).all()
    
    for settlement in settlements:
        balances[settlement.from_user_id] += settlement.amount
        balances[settlement.to_user_id] -= settlement.amount
    
    # Build response with usernames
    result = {}
    for user_id, balance in balances.items():
        user = db.query(User).filter(User.id == user_id).first()
        result[user_id] = {
            "username": user.username if user else "Unknown",
            "balance": round(balance, 2)
        }
    
    return result


@router.get("/{group_id}/settlements/suggestions", response_model=List[Dict[str, Any]])
def get_settlement_suggestions(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Generate optimized settlement suggestions to minimize transactions.
    Uses greedy algorithm to match debtors with creditors.
    """
    group = get_group_or_404(group_id, db)
    is_group_member(group_id, current_user.id, db)
    
    # Get balances
    balances_dict = get_group_balances(group_id, current_user, db)
    
    # Separate debtors and creditors
    debtors = []   # People who owe money (negative balance)
    creditors = []  # People who are owed money (positive balance)
    
    for user_id, data in balances_dict.items():
        balance = data["balance"]
        if balance < -0.01:  # Owe money
            debtors.append({"user_id": user_id, "username": data["username"], "amount": abs(balance)})
        elif balance > 0.01:  # Owed money
            creditors.append({"user_id": user_id, "username": data["username"], "amount": balance})
    
    # Generate settlements
    settlements = []
    i, j = 0, 0
    
    while i < len(debtors) and j < len(creditors):
        debtor = debtors[i]
        creditor = creditors[j]
        
        amount = min(debtor["amount"], creditor["amount"])
        
        settlements.append({
            "from_user_id": debtor["user_id"],
            "from_username": debtor["username"],
            "to_user_id": creditor["user_id"],
            "to_username": creditor["username"],
            "amount": round(amount, 2)
        })
        
        debtor["amount"] -= amount
        creditor["amount"] -= amount
        
        if debtor["amount"] < 0.01:
            i += 1
        if creditor["amount"] < 0.01:
            j += 1
    
    return settlements


@router.post("/{group_id}/settlements", response_model=GroupSettlementResponse, status_code=status.HTTP_201_CREATED)
def create_group_settlement(
    group_id: int,
    settlement_data: GroupSettlementCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Record a settlement/payment between group members"""
    group = get_group_or_404(group_id, db)
    is_group_member(group_id, current_user.id, db)
    
    # Validate recipient is a group member
    recipient_member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == settlement_data.to_user_id,
        GroupMember.status == "accepted"
    ).first()
    
    if not recipient_member:
        raise HTTPException(status_code=400, detail="Recipient must be a group member")
    
    # Create settlement
    new_settlement = GroupSettlement(
        group_id=group_id,
        from_user_id=current_user.id,
        to_user_id=settlement_data.to_user_id,
        amount=settlement_data.amount,
    )
    
    db.add(new_settlement)
    db.commit()
    db.refresh(new_settlement)
    
    return new_settlement


@router.get("/{group_id}/settlements", response_model=List[GroupSettlementResponse])
def list_group_settlements(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all settlements for a group"""
    group = get_group_or_404(group_id, db)
    is_group_member(group_id, current_user.id, db)
    
    settlements = db.query(GroupSettlement).filter(
        GroupSettlement.group_id == group_id
    ).order_by(GroupSettlement.created_at.desc()).all()
    
    return settlements


# ================= HELPER RESPONSE BUILDERS =================

def build_group_response(group: Group, db: Session) -> GroupResponse:
    """Build a complete group response with member info"""
    members = db.query(GroupMember, User).join(
        User, GroupMember.user_id == User.id
    ).filter(GroupMember.group_id == group.id).all()
    
    member_infos = [
        GroupMemberInfo(
            id=member.GroupMember.id,
            user_id=member.GroupMember.user_id,
            username=member.User.username,
            role=member.GroupMember.role,
            status=member.GroupMember.status,
            joined_at=member.GroupMember.joined_at,
        )
        for member in members
    ]
    
    return GroupResponse(
        id=group.id,
        name=group.name,
        description=group.description,
        currency=group.currency,
        image_url=group.image_url,
        is_active=group.is_active,
        created_by=group.created_by,
        created_at=group.created_at,
        members=member_infos,
    )


def build_expense_response(expense: GroupExpense, db: Session) -> GroupExpenseResponse:
    """Build a complete expense response with participant info"""
    payer = db.query(User).filter(User.id == expense.paid_by).first()
    
    participants = db.query(GroupExpenseParticipant, User).join(
        User, GroupExpenseParticipant.user_id == User.id
    ).filter(GroupExpenseParticipant.group_expense_id == expense.id).all()
    
    participant_responses = [
        GroupExpenseParticipantResponse(
            user_id=part.GroupExpenseParticipant.user_id,
            username=part.User.username,
            share_amount=part.GroupExpenseParticipant.share_amount,
        )
        for part in participants
    ]
    
    return GroupExpenseResponse(
        id=expense.id,
        group_id=expense.group_id,
        description=expense.description,
        total_amount=expense.total_amount,
        category=expense.category,
        date=expense.date,
        paid_by=expense.paid_by,
        payer_username=payer.username if payer else "Unknown",
        created_at=expense.created_at,
        participants=participant_responses,
    )
