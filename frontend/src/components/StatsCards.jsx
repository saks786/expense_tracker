import React from "react";

export default function StatsCards({ expenses }) {
  const total = expenses.reduce((sum, e) => sum + e.amount, 0);
  const count = expenses.length;
  const average = count > 0 ? total / count : 0;

  const thisMonth = new Date().getMonth();
  const thisYear = new Date().getFullYear();
  const monthlyExpenses = expenses.filter(e => {
    const expenseDate = new Date(e.date);
    return expenseDate.getMonth() === thisMonth && expenseDate.getFullYear() === thisYear;
  });
  const monthlyTotal = monthlyExpenses.reduce((sum, e) => sum + e.amount, 0);

  return (
    <div className="stats-container">
      <div className="stat-card">
        <div className="stat-label">Total Expenses</div>
        <div className="stat-value">₹{total.toFixed(2)}</div>
      </div>
      
      <div className="stat-card">
        <div className="stat-label">This Month</div>
        <div className="stat-value">₹{monthlyTotal.toFixed(2)}</div>
      </div>
      
      <div className="stat-card">
        <div className="stat-label">Average</div>
        <div className="stat-value">₹{average.toFixed(2)}</div>
      </div>
      
      <div className="stat-card">
        <div className="stat-label">Total Count</div>
        <div className="stat-value">{count}</div>
      </div>
    </div>
  );
}
