import React, { useState } from "react";
import PaymentForm from "./PaymentForm";
import "./PaymentModal.css";

export default function PaymentModal({
  open,
  debt,
  splitExpense,
  amount,
  paymentType,
  onClose,
  onSuccess,
}) {
  const [paymentDone, setPaymentDone] = useState(false);

  if (!open) return null;

  const handlePaymentSuccess = (result) => {
    setPaymentDone(true);
    setTimeout(() => {
      onSuccess?.();
    }, 2000);
  };

  const handlePaymentError = (error) => {
    console.error("Payment error:", error);
  };

  const getModalTitle = () => {
    if (debt) {
      return `Pay Debt: ${debt.name}`;
    } else if (splitExpense) {
      return `Pay Split Expense: ${splitExpense.description}`;
    }
    return "Make Payment";
  };

  return (
    <div className="payment-modal-overlay" onClick={onClose}>
      <div className="payment-modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="payment-modal-header">
          <h2>{getModalTitle()}</h2>
          <button className="payment-modal-close" onClick={onClose}>
            ✕
          </button>
        </div>

        <div className="payment-modal-body">
          {paymentDone ? (
            <div className="payment-success-message">
              <div className="success-icon">✅</div>
              <h3>Payment Successful!</h3>
              <p>Your payment has been processed successfully.</p>
              <p className="payment-amount">₹ {amount.toFixed(2)}</p>
              <p className="payment-type">
                {paymentType === "debt_payment" ? "Debt Payment" : "Split Expense Payment"}
              </p>
              <small>Closing modal in a moment...</small>
            </div>
          ) : (
            <PaymentForm
              amount={amount}
              debtId={debt?.id}
              splitExpenseId={splitExpense?.id}
              transactionType={paymentType}
              description={debt?.name || splitExpense?.description}
              onSuccess={handlePaymentSuccess}
              onError={handlePaymentError}
            />
          )}
        </div>
      </div>
    </div>
  );
}
