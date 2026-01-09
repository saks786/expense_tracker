import React, { useState, useEffect } from "react";
import { getSplitExpenses, deleteSplitExpense, getCurrentUser } from "../api";

export default function SplitExpenseList({ refresh }) {
  const [splitExpenses, setSplitExpenses] = useState([]);
  const [currentUserId, setCurrentUserId] = useState(null);

  useEffect(() => {
    fetchCurrentUser();
    fetchSplitExpenses();
  }, [refresh]);

  const fetchCurrentUser = async () => {
    try {
      const user = await getCurrentUser();
      setCurrentUserId(user.id);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchSplitExpenses = async () => {
    try {
      const data = await getSplitExpenses();
      setSplitExpenses(data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm("Are you sure you want to delete this split expense?")) return;
    try {
      await deleteSplitExpense(id);
      fetchSplitExpenses();
    } catch (err) {
      alert(err.message);
    }
  };

  const handleExportCSV = () => {
    if (splitExpenses.length === 0) return;

    const headers = ["Description", "Total Amount", "Your Share", "Category", "Date", "Participants"];
    const rows = splitExpenses.map(exp => [
      exp.description,
      exp.total_amount,
      exp.split_amount,
      exp.category,
      exp.date,
      exp.participants.length
    ]);

    const csvContent = [headers, ...rows]
      .map(row => row.join(","))
      .join("\n");

    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "split_expenses.csv";
    a.click();
  };

  return (
    <div className="split-expense-list">
      <div className="list-header">
        <h3>🤝 Split Expenses</h3>
        {splitExpenses.length > 0 && (
          <button onClick={handleExportCSV} className="btn-export">
            Export CSV
          </button>
        )}
      </div>

      {splitExpenses.length === 0 ? (
        <p className="empty-state">No split expenses yet. Create one above!</p>
      ) : (
        <div className="split-expenses-grid">
          {splitExpenses.map((exp) => {
            const isCreator = exp.created_by === currentUserId;
            
            return (
              <div key={exp.id} className="split-expense-card">
                <div className="expense-header">
                  <div>
                    <h4>{exp.description}</h4>
                    <span className="category-badge">{exp.category}</span>
                  </div>
                  <span className="date">{new Date(exp.date).toLocaleDateString()}</span>
                </div>

                <div className="expense-amounts">
                  <div className="amount-item">
                    <span className="label">Total:</span>
                    <span className="value total">₹{exp.total_amount.toLocaleString()}</span>
                  </div>
                  <div className="amount-item">
                    <span className="label">Your Share:</span>
                    <span className="value share">₹{exp.split_amount.toLocaleString()}</span>
                  </div>
                </div>

                <div className="participants-info">
                  <span className="participants-label">
                    👥 Split between {exp.participants.length} people
                  </span>
                  {isCreator && (
                    <span className="creator-badge">You created this</span>
                  )}
                </div>

                {isCreator && (
                  <div className="expense-actions">
                    <button
                      onClick={() => handleDelete(exp.id)}
                      className="btn-delete"
                    >
                      Delete
                    </button>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
