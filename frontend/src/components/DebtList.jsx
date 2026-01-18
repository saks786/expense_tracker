import React, { useState, useEffect } from "react";
import { getDebts, deleteDebt, updateDebt } from "../api";

export default function DebtList({ refresh, onPaymentClick }) {
  const [debts, setDebts] = useState([]);
  const [paymentAmount, setPaymentAmount] = useState({});

  useEffect(() => {
    fetchDebts();
  }, [refresh]);

  const fetchDebts = async () => {
    try {
      const data = await getDebts();
      setDebts(data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm("Are you sure you want to delete this debt?")) return;
    try {
      await deleteDebt(id);
      fetchDebts();
    } catch (err) {
      alert(err.message);
    }
  };

  const handlePaymentClick = (debt) => {
    const amount = parseFloat(paymentAmount[debt.id] || 0);
    if (amount <= 0) {
      alert("Please enter a valid payment amount");
      return;
    }
    if (onPaymentClick) {
      onPaymentClick(debt, amount);
    }
  };

  const calculateMonthsRemaining = (debt) => {
    if (debt.emi_amount === 0) return "N/A";
    return Math.ceil(debt.remaining_amount / debt.emi_amount);
  };

  return (
    <div className="debt-list">
      <h3>💳 Your Debts</h3>
      
      {debts.length === 0 ? (
        <p className="empty-state">No debts tracked yet. Add one above!</p>
      ) : (
        <div className="debts-grid">
          {debts.map((debt) => (
            <div key={debt.id} className={`debt-card ${debt.status}`}>
              <div className="debt-header">
                <h4>{debt.name}</h4>
                <span className={`debt-status ${debt.status}`}>
                  {debt.status === "paid" ? "✅ Paid" : "📌 Active"}
                </span>
              </div>

              <div className="debt-details">
                <div className="debt-row">
                  <span className="label">Principal:</span>
                  <span className="value">₹{debt.principal_amount.toLocaleString()}</span>
                </div>
                <div className="debt-row">
                  <span className="label">Interest Rate:</span>
                  <span className="value">{debt.interest_rate}% p.a.</span>
                </div>
                <div className="debt-row">
                  <span className="label">EMI Amount:</span>
                  <span className="value">₹{debt.emi_amount.toLocaleString()}</span>
                </div>
                <div className="debt-row">
                  <span className="label">EMI Date:</span>
                  <span className="value">{debt.emi_date} of each month</span>
                </div>
                <div className="debt-row highlight">
                  <span className="label">Remaining:</span>
                  <span className="value">₹{debt.remaining_amount.toLocaleString()}</span>
                </div>
                <div className="debt-row">
                  <span className="label">Months Left:</span>
                  <span className="value">{calculateMonthsRemaining(debt)} months</span>
                </div>
              </div>

              {debt.status === "active" && (
                <div className="payment-section">
                  <div className="payment-input-group">
                    <input
                      type="number"
                      step="0.01"
                      max={debt.remaining_amount}
                      placeholder="Payment amount"
                      value={paymentAmount[debt.id] || ""}
                      onChange={(e) => setPaymentAmount({ ...paymentAmount, [debt.id]: e.target.value })}
                    />
                    <button 
                      onClick={() => handlePaymentClick(debt)}
                      className="btn-payment"
                    >
                      Pay
                    </button>
                  </div>
                </div>
              )}

              <div className="debt-actions">
                <button
                  onClick={() => handleDelete(debt.id)}
                  className="btn-delete"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
