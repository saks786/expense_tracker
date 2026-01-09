import React, { useState } from "react";
import { addDebt } from "../api";

export default function DebtForm({ onDebtAdded }) {
  const today = new Date().toISOString().split("T")[0];
  const [form, setForm] = useState({
    name: "",
    principal_amount: "",
    interest_rate: "",
    emi_amount: "",
    emi_date: "",
    start_date: today
  });

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const clampEmiDate = (value) => {
    const n = Number(value);
    if (Number.isNaN(n)) return "";
    return Math.min(31, Math.max(1, Math.floor(n))).toString();
  };

  const handleChange = (field) => (e) => {
    const val = e.target.value;
    if (field === "emi_date") {
      setForm((s) => ({ ...s, emi_date: clampEmiDate(val) }));
    } else {
      setForm((s) => ({ ...s, [field]: val }));
    }
  };

  const validate = () => {
    if (!form.name.trim()) return "Please provide a debt name.";
    if (!form.principal_amount || Number(form.principal_amount) <= 0)
      return "Principal amount must be greater than 0.";
    if (
      form.interest_rate === "" ||
      Number(form.interest_rate) < 0 ||
      Number(form.interest_rate) > 100
    )
      return "Enter a valid interest rate (0 - 100%).";
    if (!form.emi_amount || Number(form.emi_amount) <= 0)
      return "EMI amount must be greater than 0.";
    if (!form.emi_date || Number(form.emi_date) < 1 || Number(form.emi_date) > 31)
      return "EMI date must be a day between 1 and 31.";
    if (!form.start_date) return "Please select a start date.";
    return "";
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    const v = validate();
    if (v) {
      setError(v);
      return;
    }

    setSubmitting(true);
    try {
      await addDebt({
        name: form.name.trim(),
        principal_amount: parseFloat(form.principal_amount),
        interest_rate: parseFloat(form.interest_rate),
        emi_amount: parseFloat(form.emi_amount),
        emi_date: parseInt(form.emi_date, 10),
        start_date: form.start_date
      });

      setForm({
        name: "",
        principal_amount: "",
        interest_rate: "",
        emi_amount: "",
        emi_date: "",
        start_date: today
      });

      if (typeof onDebtAdded === "function") onDebtAdded();
    } catch (err) {
      setError(err?.message || "Failed to add debt.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit} className="expense-form debt-form" aria-labelledby="debt-form-title">
        <div className="form-title" id="debt-form-title">📋 Add New Debt</div>

        {error && (
          <div role="alert" className="error-message" style={{ marginBottom: 12 }}>
            {error}
          </div>
        )}

        <div className="form-group">
          <label htmlFor="debt-name">Debt Name</label>
          <input
            id="debt-name"
            name="name"
            type="text"
            placeholder="e.g., Car Loan, Home Loan"
            value={form.name}
            onChange={handleChange("name")}
            required
            aria-required="true"
          />
        </div>

        <div className="form-group">
          <label htmlFor="principal-amount">Principal Amount (₹)</label>
          <input
            id="principal-amount"
            name="principal_amount"
            type="number"
            inputMode="decimal"
            step="0.01"
            placeholder="100000"
            value={form.principal_amount}
            onChange={handleChange("principal_amount")}
            required
            min="0"
          />
        </div>

        <div className="form-group">
          <label htmlFor="interest-rate">Interest Rate (%)</label>
          <input
            id="interest-rate"
            name="interest_rate"
            type="number"
            inputMode="decimal"
            step="0.01"
            placeholder="8.5"
            value={form.interest_rate}
            onChange={handleChange("interest_rate")}
            required
            min="0"
            max="100"
          />
        </div>

        <div className="form-group">
          <label htmlFor="emi-amount">EMI Amount (₹)</label>
          <input
            id="emi-amount"
            name="emi_amount"
            type="number"
            inputMode="decimal"
            step="0.01"
            placeholder="5000"
            value={form.emi_amount}
            onChange={handleChange("emi_amount")}
            required
            min="0"
          />
        </div>

        <div className="form-group">
          <label htmlFor="emi-date">EMI Date (Day of Month)</label>
          <input
            id="emi-date"
            name="emi_date"
            type="number"
            min="1"
            max="31"
            placeholder="5"
            value={form.emi_date}
            onChange={handleChange("emi_date")}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="start-date">Start Date</label>
          <input
            id="start-date"
            name="start_date"
            type="date"
            value={form.start_date}
            onChange={handleChange("start_date")}
            required
          />
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <button
            type="submit"
            className="btn btn-primary btn-full"
            disabled={submitting}
            aria-disabled={submitting}
          >
            {submitting ? "Adding..." : "Add Debt"}
          </button>
        </div>
      </form>
    </div>
  );
}
