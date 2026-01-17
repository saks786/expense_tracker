import os
import stripe
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime

from .database import SessionLocal
from .models import User, Transaction, Debt, SplitExpense
from .schemas import PaymentIntentCreate, PaymentConfirmCreate, TransactionResponse
from .routes import get_current_user, get_db

router = APIRouter(prefix="/api/payments", tags=["payments"])

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
stripe_webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

logger = logging.getLogger("payments")

# ================= CREATE PAYMENT INTENT =================

@router.post("/create-intent")
async def create_payment_intent(
    payload: PaymentIntentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a Stripe Payment Intent for either debt payment or split expense payment.
    Validates that the user has permission to pay and that the amounts are correct.
    """
    try:
        # Validate transaction type
        if payload.transaction_type not in ["debt_payment", "split_expense_payment"]:
            raise HTTPException(status_code=400, detail="Invalid transaction type")

        # Validate amount
        if payload.amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be greater than 0")

        # Validate payment method
        if payload.payment_method not in ["card", "upi"]:
            raise HTTPException(status_code=400, detail="Invalid payment method")

        description = payload.description or f"{payload.transaction_type} - {payload.amount} INR"

        # Debt Payment Validation
        if payload.transaction_type == "debt_payment":
            if not payload.debt_id:
                raise HTTPException(status_code=400, detail="debt_id required for debt payment")

            debt = db.query(Debt).filter(
                Debt.id == payload.debt_id,
                Debt.user_id == current_user.id,
            ).first()

            if not debt:
                raise HTTPException(status_code=404, detail="Debt not found")

            if debt.status == "paid":
                raise HTTPException(status_code=400, detail="Debt already paid")

            if payload.amount > debt.remaining_amount:
                raise HTTPException(
                    status_code=400,
                    detail=f"Payment amount exceeds remaining debt. Remaining: {debt.remaining_amount}",
                )

        # Split Expense Payment Validation
        elif payload.transaction_type == "split_expense_payment":
            if not payload.split_expense_id:
                raise HTTPException(status_code=400, detail="split_expense_id required for split expense payment")

            split = db.query(SplitExpense).filter(
                SplitExpense.id == payload.split_expense_id,
                SplitExpense.participants.any(id=current_user.id),
            ).first()

            if not split:
                raise HTTPException(status_code=404, detail="Split expense not found or you're not a participant")

            # Check if already paid by this user
            existing_payment = db.query(Transaction).filter(
                Transaction.user_id == current_user.id,
                Transaction.split_expense_id == payload.split_expense_id,
                Transaction.status == "succeeded",
            ).first()

            if existing_payment:
                raise HTTPException(status_code=400, detail="You've already paid for this split expense")

            # Validate split amount
            split_amount = split.total_amount / len(split.participants)
            if abs(payload.amount - split_amount) > 0.01:  # Allow 1 paisa margin for float precision
                raise HTTPException(
                    status_code=400,
                    detail=f"Incorrect payment amount. Should be {split_amount}",
                )

        # Create Stripe Payment Intent
        intent = stripe.PaymentIntent.create(
            amount=int(payload.amount * 100),  # Convert to paisa (smallest unit for INR)
            currency="inr",
            payment_method_types=["card", "upi"],
            description=description,
            idempotency_key=f"{current_user.id}_{payload.debt_id or payload.split_expense_id}_{int(datetime.utcnow().timestamp())}",
        )

        # Record pending transaction in DB
        transaction = Transaction(
            user_id=current_user.id,
            stripe_payment_intent_id=intent.id,
            amount=payload.amount,
            currency="INR",
            payment_method=payload.payment_method,
            transaction_type=payload.transaction_type,
            debt_id=payload.debt_id,
            split_expense_id=payload.split_expense_id,
            status="pending",
            description=description,
        )

        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return {
            "client_secret": intent.client_secret,
            "transaction_id": transaction.id,
            "amount": payload.amount,
            "currency": "INR",
        }

    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {e}")
        raise HTTPException(status_code=400, detail=f"Payment error: {str(e)}")
    except Exception as e:
        logger.error(f"Error creating payment intent: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# ================= CONFIRM PAYMENT =================

@router.post("/confirm-payment")
async def confirm_payment(
    payload: PaymentConfirmCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Confirm Stripe payment and update DB accordingly.
    """
    try:
        # Retrieve and confirm payment intent
        intent = stripe.PaymentIntent.retrieve(payload.payment_intent_id)

        if intent.status != "succeeded":
            raise HTTPException(status_code=400, detail="Payment not succeeded")

        # Find transaction
        transaction = db.query(Transaction).filter(
            Transaction.stripe_payment_intent_id == payload.payment_intent_id,
            Transaction.user_id == current_user.id,
        ).first()

        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")

        # Update transaction status
        transaction.status = "succeeded"
        transaction.updated_at = datetime.utcnow()

        # Handle debt payment
        if transaction.transaction_type == "debt_payment":
            debt = db.query(Debt).filter(Debt.id == transaction.debt_id).first()
            if debt:
                debt.remaining_amount -= transaction.amount
                if debt.remaining_amount <= 0.01:  # Float precision margin
                    debt.remaining_amount = 0
                    debt.status = "paid"

        # Handle split expense payment
        elif transaction.transaction_type == "split_expense_payment":
            # Just mark as paid; split is settled when payment is made
            pass

        db.commit()
        db.refresh(transaction)

        return TransactionResponse.from_orm(transaction)

    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {e}")
        raise HTTPException(status_code=400, detail=f"Payment confirmation error: {str(e)}")
    except Exception as e:
        logger.error(f"Error confirming payment: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# ================= WEBHOOK HANDLER =================

@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Handle Stripe webhook events for payment confirmation and idempotency.
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_webhook_secret
        )
    except ValueError:
        logger.error("Invalid payload")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        logger.error("Invalid signature")
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle payment_intent.succeeded
    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        intent_id = payment_intent["id"]

        # Find and update transaction
        transaction = db.query(Transaction).filter(
            Transaction.stripe_payment_intent_id == intent_id
        ).first()

        if transaction and transaction.status == "pending":
            transaction.status = "succeeded"
            transaction.updated_at = datetime.utcnow()

            # Update debt or split accordingly
            if transaction.transaction_type == "debt_payment":
                debt = db.query(Debt).filter(Debt.id == transaction.debt_id).first()
                if debt:
                    debt.remaining_amount -= transaction.amount
                    if debt.remaining_amount <= 0.01:
                        debt.remaining_amount = 0
                        debt.status = "paid"

            db.commit()
            logger.info(f"Transaction {transaction.id} confirmed via webhook")

    # Handle payment_intent.payment_failed
    elif event["type"] == "payment_intent.payment_failed":
        payment_intent = event["data"]["object"]
        intent_id = payment_intent["id"]

        transaction = db.query(Transaction).filter(
            Transaction.stripe_payment_intent_id == intent_id
        ).first()

        if transaction:
            transaction.status = "failed"
            transaction.updated_at = datetime.utcnow()
            db.commit()
            logger.info(f"Transaction {transaction.id} failed")

    return {"received": True}


# ================= GET TRANSACTION HISTORY =================

@router.get("/history", response_model=list[TransactionResponse])
async def get_transaction_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get all transactions for the current user.
    """
    transactions = db.query(Transaction).filter(
        Transaction.user_id == current_user.id
    ).order_by(Transaction.created_at.desc()).all()

    return [TransactionResponse.from_orm(t) for t in transactions]


# ================= GET TRANSACTION DETAILS =================

@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get details of a specific transaction.
    """
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id,
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return TransactionResponse.from_orm(transaction)
