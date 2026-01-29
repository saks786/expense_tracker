import React, { useState } from "react";
import toast from "react-hot-toast";
import EditExpenseModal from "./EditExpenseModal";
import { updateExpense, deleteExpense } from "../api";

export default function ExpenseList({ expenses, onUpdate }) {
  const [editingExpense, setEditingExpense] = useState(null);

  if (!expenses.length) {
    return (
      <div className="expense-list-container">
        <div className="empty-state">
          <div className="empty-state-icon">📭</div>
          <p>No expenses yet. Start by adding your first expense!</p>
        </div>
      </div>
    );
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    });
  };

  const handleEdit = (expense) => {
    setEditingExpense(expense);
  };

  const handleSave = async (updatedData) => {
    try {
      await updateExpense(editingExpense.id, updatedData);
      setEditingExpense(null);
      onUpdate();
      toast.success("Expense updated successfully!");
    } catch (error) {
      console.error("Error updating expense:", error);
      toast.error("Failed to update expense");
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this expense?")) {
      try {
        await deleteExpense(id);
        onUpdate();
        toast.success("Expense deleted successfully!");
      } catch (error) {
        console.error("Error deleting expense:", error);
        toast.error("Failed to delete expense");
      }
    }
  };

  const handleExportCSV = () => {
    const headers = ["Date", "Category", "Amount", "Description"];
    const rows = expenses.map(e => [
      e.date,
      e.category,
      e.amount,
      e.description
    ]);
    
    const csvContent = [
      headers.join(","),
      ...rows.map(row => row.join(","))
    ].join("\n");
    
    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `expenses_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
  };

  return (
    <div className="expense-list-container">
      <div className="list-header">
        <h2 className="list-title">📊 Recent Expenses</h2>
        <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
          <span style={{ color: '#999', fontSize: '0.95rem' }}>
            {expenses.length} {expenses.length === 1 ? 'expense' : 'expenses'}
          </span>
          <button onClick={handleExportCSV} className="btn btn-secondary">
            📥 Export CSV
          </button>
        </div>
      </div>
      
      <ul className="expense-list">
        {expenses.map((expense) => (
          <li key={expense.id} className="expense-item">
            <div className="expense-info">
              <div className="expense-header">
                <span className="expense-category">{expense.category}</span>
                <span className="expense-date">
                  {formatDate(expense.date)}
                </span>
              </div>
              {expense.description && (
                <div className="expense-description">
                  {expense.description}
                </div>
              )}
            </div>
            <div className="expense-amount">
              ₹{expense.amount.toFixed(2)}
            </div>
            <div className="expense-actions">
              <button 
                onClick={() => handleEdit(expense)}
                className="btn btn-edit"
                title="Edit"
              >
                ✏️
              </button>
              <button 
                onClick={() => handleDelete(expense.id)}
                className="btn btn-delete"
                title="Delete"
              >
                🗑️
              </button>
            </div>
          </li>
        ))}
      </ul>

      {editingExpense && (
        <EditExpenseModal
          expense={editingExpense}
          onSave={handleSave}
          onClose={() => setEditingExpense(null)}
        />
      )}
    </div>
  );
}
