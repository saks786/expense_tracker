import React, { useState, useEffect } from "react";
import toast from "react-hot-toast";
import {
  getSplitExpenses,
  deleteSplitExpense,
  getCurrentUser,
  getBalances,
  getSettlementSuggestions,
} from "../api";

export default function SplitExpenseList({ refresh, onPaymentClick }) {
  const [splitExpenses, setSplitExpenses] = useState([]);
  const [balances, setBalances] = useState({});
  const [suggestions, setSuggestions] = useState([]);
  const [currentUserId, setCurrentUserId] = useState(null);

  useEffect(() => {
    loadData();
  }, [refresh]);

  async function loadData() {
    const user = await getCurrentUser();
    setCurrentUserId(user.id);
    setSplitExpenses(await getSplitExpenses());
    setBalances(await getBalances());
    setSuggestions(await getSettlementSuggestions());
  }

  const handleSplitPayment = (expense) => {
    const splitAmount = expense.total_amount / expense.participants.length;
    if (onPaymentClick) {
      onPaymentClick(expense, splitAmount, "split");
    }
  };

  const handleDeleteSplit = async (id) => {
    if (!confirm("Delete this split expense?")) return;
    try {
      await deleteSplitExpense(id);
      toast.success("Split expense deleted successfully");
      loadData();
    } catch (err) {
      toast.error(err.message || "Failed to delete split expense");
    }
  };

  return (
    <div>
      <h3>💰 Balances</h3>
      {Object.entries(balances).map(([u, a]) => (
        <p key={u}>{u}: ₹{a.toFixed(2)}</p>
      ))}

      <h3>🔁 Settlement Suggestions</h3>
      {suggestions.length === 0
        ? <p>All settled 🎉</p>
        : suggestions.map((s, i) => (
            <p key={i}>{s.from} ➜ {s.to}: ₹{s.amount}</p>
          ))}

      <h3>🤝 Split Expenses</h3>
      {splitExpenses.map(exp => {
        const splitAmount = exp.total_amount / exp.participants.length;
        return (
          <div key={exp.id} style={{ 
            padding: '12px', 
            border: '1px solid #ddd', 
            borderRadius: '6px', 
            marginBottom: '10px' 
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <strong>{exp.description}</strong> – ₹{exp.total_amount}
                <small style={{ display: 'block', color: '#666', marginTop: '4px' }}>
                  Your share: ₹{splitAmount.toFixed(2)} ({exp.participants.length} people)
                </small>
              </div>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button 
                  onClick={() => handleSplitPayment(exp)}
                  style={{
                    padding: '6px 12px',
                    background: '#667eea',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    fontSize: '13px'
                  }}
                >
                  Pay
                </button>
                <button 
                  onClick={() => handleDeleteSplit(exp.id)}
                  style={{
                    padding: '6px 12px',
                    background: '#f44336',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    fontSize: '13px'
                  }}
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
