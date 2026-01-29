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

  // Calculate trends
  const lastMonth = thisMonth === 0 ? 11 : thisMonth - 1;
  const lastMonthYear = thisMonth === 0 ? thisYear - 1 : thisYear;
  const lastMonthExpenses = expenses.filter(e => {
    const expenseDate = new Date(e.date);
    return expenseDate.getMonth() === lastMonth && expenseDate.getFullYear() === lastMonthYear;
  });
  const lastMonthTotal = lastMonthExpenses.reduce((sum, e) => sum + e.amount, 0);
  const monthChange = lastMonthTotal > 0 ? ((monthlyTotal - lastMonthTotal) / lastMonthTotal * 100).toFixed(1) : 0;

  const categoryTotals = expenses.reduce((acc, e) => {
    acc[e.category] = (acc[e.category] || 0) + e.amount;
    return acc;
  }, {});
  
  const topCategory = Object.entries(categoryTotals).sort((a, b) => b[1] - a[1])[0];

  return (
    <div className="kpi-cards">
      <div className="kpi-card">
        <div className="kpi-header">
          <span className="kpi-label">Total Spent</span>
          <svg className="kpi-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div className="kpi-value">₹{total.toLocaleString('en-IN', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</div>
        <div className="kpi-footer">{count} transactions</div>
      </div>

      <div className="kpi-card">
        <div className="kpi-header">
          <span className="kpi-label">Monthly Spend</span>
          <svg className="kpi-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
        <div className="kpi-value">₹{monthlyTotal.toLocaleString('en-IN', {maximumFractionDigits: 0})}</div>
        <div className="kpi-footer">
          <span className={monthChange >= 0 ? 'trend-up' : 'trend-down'}>
            {monthChange >= 0 ? '↑' : '↓'} {Math.abs(monthChange)}%
          </span> vs last month
        </div>
      </div>

      <div className="kpi-card">
        <div className="kpi-header">
          <span className="kpi-label">Average</span>
          <svg className="kpi-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
        <div className="kpi-value">₹{average.toLocaleString('en-IN', {maximumFractionDigits: 0})}</div>
        <div className="kpi-footer">per transaction</div>
      </div>

      <div className="kpi-card">
        <div className="kpi-header">
          <span className="kpi-label">Top Category</span>
          <svg className="kpi-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
          </svg>
        </div>
        <div className="kpi-value">{topCategory?.[0] || 'N/A'}</div>
        <div className="kpi-footer">₹{(topCategory?.[1] || 0).toLocaleString('en-IN', {maximumFractionDigits: 0})}</div>
      </div>
    </div>
  );
}

