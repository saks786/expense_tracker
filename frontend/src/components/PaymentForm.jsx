import React, { useState, useEffect } from "react";
import {
  CardElement,
  useStripe,
  useElements,
  PaymentRequestButtonElement,
} from "@stripe/react-stripe-js";
import { createPaymentIntent, confirmPayment } from "../api";
import "./PaymentForm.css";

export default function PaymentForm({
  amount,
  debtId,
  splitExpenseId,
  transactionType,
  onSuccess,
  onError,
  description,
}) {
  const stripe = useStripe();
  const elements = useElements();

  const [isLoading, setIsLoading] = useState(false);
  const [paymentMethod, setPaymentMethod] = useState("card");
  const [error, setError] = useState(null);
  const [clientSecret, setClientSecret] = useState(null);
  const [transactionId, setTransactionId] = useState(null);

  // Initialize payment intent on mount
  useEffect(() => {
    const initializePayment = async () => {
      try {
        const response = await createPaymentIntent({
          amount,
          payment_method: paymentMethod,
          transaction_type: transactionType,
          debt_id: debtId,
          split_expense_id: splitExpenseId,
          description,
        });

        setClientSecret(response.client_secret);
        setTransactionId(response.transaction_id);
      } catch (err) {
        setError(err.message || "Failed to initialize payment");
        onError?.(err.message);
      }
    };

    initializePayment();
  }, [amount, paymentMethod, transactionType, debtId, splitExpenseId, description, onError]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!stripe || !elements || !clientSecret) {
      setError("Payment system not ready");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      let result;

      if (paymentMethod === "card") {
        // Card payment
        const cardElement = elements.getElement(CardElement);

        result = await stripe.confirmCardPayment(clientSecret, {
          payment_method: {
            card: cardElement,
          },
        });
      } else if (paymentMethod === "upi") {
        // UPI payment
        result = await stripe.confirmUPIPayment(clientSecret);
      }

      if (result.error) {
        setError(result.error.message);
        onError?.(result.error.message);
      } else if (result.paymentIntent.status === "succeeded") {
        // Confirm with backend
        await confirmPayment({
          payment_intent_id: result.paymentIntent.id,
          payment_method_id: result.paymentIntent.payment_method,
        });

        setError(null);
        onSuccess?.({
          transactionId,
          amount,
          status: "succeeded",
        });
      } else {
        setError("Payment processing failed");
        onError?.("Payment processing failed");
      }
    } catch (err) {
      setError(err.message || "Payment failed");
      onError?.(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const cardElementOptions = {
    style: {
      base: {
        fontSize: "16px",
        color: "#424770",
        "::placeholder": {
          color: "#aab7c4",
        },
      },
      invalid: {
        color: "#9e2146",
      },
    },
  };

  return (
    <div className="payment-form-container">
      <h3>Payment Details</h3>

      <div className="payment-amount-display">
        <span className="amount-label">Amount:</span>
        <span className="amount-value">₹ {amount.toFixed(2)}</span>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="payment-method-selector">
          <label>
            <input
              type="radio"
              value="card"
              checked={paymentMethod === "card"}
              onChange={(e) => setPaymentMethod(e.target.value)}
              disabled={isLoading}
            />
            Debit/Credit Card
          </label>
          <label>
            <input
              type="radio"
              value="upi"
              checked={paymentMethod === "upi"}
              onChange={(e) => setPaymentMethod(e.target.value)}
              disabled={isLoading}
            />
            UPI
          </label>
        </div>

        {paymentMethod === "card" && (
          <div className="card-element-wrapper">
            <label>Card Details</label>
            <CardElement options={cardElementOptions} />
          </div>
        )}

        {paymentMethod === "upi" && (
          <div className="upi-info">
            <p>You will be redirected to your UPI app to complete the payment.</p>
          </div>
        )}

        {error && <div className="payment-error">{error}</div>}

        <button
          type="submit"
          disabled={!stripe || !elements || isLoading || !clientSecret}
          className="payment-button"
        >
          {isLoading ? "Processing..." : "Pay"}
        </button>
      </form>

      <div className="payment-disclaimer">
        <small>
          Your payment is secured with Stripe. We do not store your card details.
        </small>
      </div>
    </div>
  );
}
