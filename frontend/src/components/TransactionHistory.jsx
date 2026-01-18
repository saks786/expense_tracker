import React, { useState, useEffect } from "react";
import { getTransactionHistory } from "../api";
import "./TransactionHistory.css";

export default function TransactionHistory() {
  const [transactions, setTransactions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState("all"); // all, succeeded, pending, failed

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        setIsLoading(true);
        const data = await getTransactionHistory();
        setTransactions(data);
        setError(null);
      } catch (err) {
        setError(err.message || "Failed to load transaction history");
        setTransactions([]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchTransactions();
  }, []);

  const getFilteredTransactions = () => {
    if (filter === "all") return transactions;
    return transactions.filter((t) => t.status === filter);
  };

  const getStatusBadgeClass = (status) => {
    switch (status) {
      case "succeeded":
        return "status-succeeded";
      case "failed":
        return "status-failed";
      case "pending":
        return "status-pending";
      default:
        return "status-default";
    }
  };

  const getTransactionTypeLabel = (type) => {
    switch (type) {
      case "debt_payment":
        return "Debt Payment";
      case "split_expense_payment":
        return "Split Expense Payment";
      default:
        return type;
    }
  };

  const getPaymentMethodLabel = (method) => {
    switch (method) {
      case "card":
        return "💳 Card";
      case "upi":
        return "📱 UPI";
      default:
        return method;
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-IN", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const filteredData = getFilteredTransactions();

  return (
    <div className="transaction-history-container">
      <h2>Transaction History</h2>

      <div className="transaction-filters">
        <button
          className={`filter-btn ${filter === "all" ? "active" : ""}`}
          onClick={() => setFilter("all")}
        >
          All ({transactions.length})
        </button>
        <button
          className={`filter-btn ${filter === "succeeded" ? "active" : ""}`}
          onClick={() => setFilter("succeeded")}
        >
          Completed (
          {transactions.filter((t) => t.status === "succeeded").length})
        </button>
        <button
          className={`filter-btn ${filter === "pending" ? "active" : ""}`}
          onClick={() => setFilter("pending")}
        >
          Pending ({transactions.filter((t) => t.status === "pending").length})
        </button>
        <button
          className={`filter-btn ${filter === "failed" ? "active" : ""}`}
          onClick={() => setFilter("failed")}
        >
          Failed ({transactions.filter((t) => t.status === "failed").length})
        </button>
      </div>

      {isLoading && (
        <div className="transaction-loading">
          <p>Loading transactions...</p>
        </div>
      )}

      {error && <div className="transaction-error">{error}</div>}

      {!isLoading && !error && filteredData.length === 0 && (
        <div className="transaction-empty">
          <p>No transactions found</p>
        </div>
      )}

      {!isLoading && !error && filteredData.length > 0 && (
        <div className="transaction-table-wrapper">
          <table className="transaction-table">
            <thead>
              <tr>
                <th>Date & Time</th>
                <th>Type</th>
                <th>Amount</th>
                <th>Method</th>
                <th>Status</th>
                <th>Details</th>
              </tr>
            </thead>
            <tbody>
              {filteredData.map((transaction) => (
                <tr key={transaction.id} className="transaction-row">
                  <td className="date-cell">
                    <span className="transaction-date">
                      {formatDate(transaction.created_at)}
                    </span>
                  </td>
                  <td className="type-cell">
                    <span className="transaction-type">
                      {getTransactionTypeLabel(transaction.transaction_type)}
                    </span>
                  </td>
                  <td className="amount-cell">
                    <span className="transaction-amount">
                      ₹ {transaction.amount.toFixed(2)}
                    </span>
                  </td>
                  <td className="method-cell">
                    <span className="payment-method">
                      {getPaymentMethodLabel(transaction.payment_method)}
                    </span>
                  </td>
                  <td className="status-cell">
                    <span
                      className={`status-badge ${getStatusBadgeClass(
                        transaction.status
                      )}`}
                    >
                      {transaction.status.charAt(0).toUpperCase() +
                        transaction.status.slice(1)}
                    </span>
                  </td>
                  <td className="details-cell">
                    <span className="transaction-description" title={transaction.description}>
                      {transaction.description
                        ? transaction.description.substring(0, 20) + "..."
                        : "-"}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <div className="transaction-stats">
        <div className="stat-card">
          <span className="stat-label">Total Paid</span>
          <span className="stat-value">
            ₹{" "}
            {transactions
              .filter((t) => t.status === "succeeded")
              .reduce((sum, t) => sum + t.amount, 0)
              .toFixed(2)}
          </span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Pending Amount</span>
          <span className="stat-value">
            ₹{" "}
            {transactions
              .filter((t) => t.status === "pending")
              .reduce((sum, t) => sum + t.amount, 0)
              .toFixed(2)}
          </span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Total Transactions</span>
          <span className="stat-value">{transactions.length}</span>
        </div>
      </div>
    </div>
  );
}
