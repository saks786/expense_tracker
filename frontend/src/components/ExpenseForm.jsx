import React, { useState } from "react";

export default function ExpenseForm({ onAdd }) {
  const [form, setForm] = useState({ category: "", amount: "", description: "" });

  const categories = ["Food", "Transport", "Entertainment", "Shopping", "Bills", "Healthcare", "Other"];

  const submit = (e) => {
    e.preventDefault();
    if (!form.category || !form.amount) {
      alert("Please fill in category and amount");
      return;
    }
    onAdd({ ...form, amount: parseFloat(form.amount) });
    setForm({ category: "", amount: "", description: "" });
  };

  return (
    <div className="form-container">
      <h2 className="form-title">➕ Add New Expense</h2>
      <form onSubmit={submit} className="expense-form">
        <div className="form-group">
          <label htmlFor="category">Category *</label>
          <select
            id="category"
            value={form.category}
            onChange={(e) => setForm({ ...form, category: e.target.value })}
            required
          >
            <option value="">Select category...</option>
            {categories.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="amount">Amount (₹) *</label>
          <input
            id="amount"
            placeholder="0.00"
            type="number"
            step="0.01"
            min="0"
            value={form.amount}
            onChange={(e) => setForm({ ...form, amount: e.target.value })}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="description">Description</label>
          <input
            id="description"
            placeholder="What was this for?"
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
          />
        </div>

        <div className="form-group">
          <label>&nbsp;</label>
          <button type="submit" className="btn btn-primary">
            Add Expense
          </button>
        </div>
      </form>
    </div>
  );
}
