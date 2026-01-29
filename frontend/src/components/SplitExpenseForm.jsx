import React, { useState, useEffect } from "react";
import toast from "react-hot-toast";
import { addSplitExpense, getFriends } from "../api";

export default function SplitExpenseForm({ onExpenseAdded }) {
  const today = new Date().toISOString().split("T")[0];

  const [form, setForm] = useState({
    description: "",
    total_amount: "",
    category: "Food",
    date: today,
    participant_ids: []
  });

  const [friends, setFriends] = useState([]);
  const [loadingFriends, setLoadingFriends] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchFriends();
  }, []);

  const fetchFriends = async () => {
    setLoadingFriends(true);
    try {
      const data = await getFriends();
      setFriends(data || []);
    } catch (err) {
      toast.error(err?.message || "Failed to load friends");
    } finally {
      setLoadingFriends(false);
    }
  };

  const toggleFriend = (friendId) => {
    setForm((prev) => {
      const ids = prev.participant_ids.slice();
      const idx = ids.indexOf(friendId);
      if (idx > -1) {
        ids.splice(idx, 1);
      } else {
        ids.push(friendId);
      }
      return { ...prev, participant_ids: ids };
    });
  };

  const validate = () => {
    if (!form.description.trim()) return "Please provide a description.";
    const amount = parseFloat(form.total_amount);
    if (Number.isNaN(amount) || amount <= 0) return "Enter a valid total amount.";
    if (!form.participant_ids || form.participant_ids.length === 0)
      return "Select at least one friend to split with.";
    if (!form.date) return "Select a date.";
    return "";
  };

  const calculateSplitAmount = () => {
    const amount = parseFloat(form.total_amount);
    const participants = (form.participant_ids?.length || 0) + 1; // +1 for current user
    if (Number.isNaN(amount) || participants === 0) return "0.00";
    return (amount / participants).toFixed(2);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const v = validate();
    if (v) {
      toast.error(v);
      return;
    }

    setSubmitting(true);
    try {
      await addSplitExpense({
        description: form.description.trim(),
        total_amount: parseFloat(form.total_amount),
        category: form.category,
        date: form.date,
        participant_ids: form.participant_ids.map((id) => Number(id))
      });

      setForm({
        description: "",
        total_amount: "",
        category: "Food",
        date: today,
        participant_ids: []
      });

      toast.success("Split expense added successfully!");
      if (typeof onExpenseAdded === "function") onExpenseAdded();
    } catch (err) {
      toast.error(err?.message || "Failed to add split expense");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit} className="expense-form split-expense-form" aria-labelledby="split-form-title">
        <div className="form-title" id="split-form-title">🤝 Split an Expense</div>

        <div className="form-grid" style={{ gap: 16 }}>
          <div className="form-group full-width">
            <label htmlFor="split-desc">Description</label>
            <input
              id="split-desc"
              name="description"
              type="text"
              placeholder="e.g., Dinner at restaurant"
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="split-amount">Total Amount (₹)</label>
            <input
              id="split-amount"
              name="total_amount"
              type="number"
              inputMode="decimal"
              step="0.01"
              placeholder="1000"
              value={form.total_amount}
              onChange={(e) => setForm({ ...form, total_amount: e.target.value })}
              required
              min="0"
            />
          </div>

          <div className="form-group">
            <label htmlFor="split-category">Category</label>
            <select
              id="split-category"
              value={form.category}
              onChange={(e) => setForm({ ...form, category: e.target.value })}
            >
              <option value="Food">Food</option>
              <option value="Travel">Travel</option>
              <option value="Entertainment">Entertainment</option>
              <option value="Shopping">Shopping</option>
              <option value="Utilities">Utilities</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="split-date">Date</label>
            <input
              id="split-date"
              name="date"
              type="date"
              value={form.date}
              onChange={(e) => setForm({ ...form, date: e.target.value })}
              required
            />
          </div>
        </div>

        <div className="form-group full-width" style={{ marginTop: 12 }}>
          <label>Split with Friends</label>

          {loadingFriends ? (
            <p className="info-text">Loading friends…</p>
          ) : friends.length === 0 ? (
            <p className="info-text">Add friends first to split expenses with them!</p>
          ) : (
            <div className="friend-selector" style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
              {friends.map((friendship) => {
                const friendId = friendship.friend_id ?? friendship.id;
                const displayName = friendship.friend_username ?? friendship.username ?? "Friend";
                const isSelected = form.participant_ids.includes(friendId);
                return (
                  <button
                    key={friendId}
                    type="button"
                    aria-pressed={isSelected}
                    className={`friend-chip ${isSelected ? "selected" : ""}`}
                    onClick={() => toggleFriend(friendId)}
                    title={displayName}
                  >
                    <span className="friend-name">{displayName}</span>
                    {isSelected && <span className="checkmark" aria-hidden>✓</span>}
                  </button>
                );
              })}
            </div>
          )}
        </div>

        {form.total_amount && form.participant_ids.length > 0 && (
          <div className="split-preview" style={{ marginTop: 12 }}>
            <p>
              <strong>Split Amount:</strong> ₹{calculateSplitAmount()} per person ({form.participant_ids.length + 1} people)
            </p>
          </div>
        )}

        <div style={{ marginTop: 16 }}>
          <button
            type="submit"
            className="btn btn-primary btn-full"
            disabled={submitting || loadingFriends || friends.length === 0}
            aria-disabled={submitting || loadingFriends || friends.length === 0}
          >
            {submitting ? "Adding..." : "Add Split Expense"}
          </button>
        </div>
      </form>
    </div>
  );
}
