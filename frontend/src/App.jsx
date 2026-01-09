import React, { useEffect, useState } from "react";
import { getExpenses, addExpense, isAuthenticated, removeToken } from "./api";
import ExpenseForm from "./components/ExpenseForm";
import ExpenseList from "./components/ExpenseList";
import StatsCards from "./components/StatsCards";
import Header from "./components/Header";
import Login from "./components/Login";
import Register from "./components/Register";
import CategoryPieChart from "./components/CategoryPieChart";
import MonthlyLineChart from "./components/MonthlyLineChart";
import DebtForm from "./components/DebtForm";
import DebtList from "./components/DebtList";
import FriendList from "./components/FriendList";
import SplitExpenseForm from "./components/SplitExpenseForm";
import SplitExpenseList from "./components/SplitExpenseList";

export default function App() {
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterCategory, setFilterCategory] = useState("all");
  const [authenticated, setAuthenticated] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [activeTab, setActiveTab] = useState("expenses"); // expenses | debts | friends | split
  const [refreshDebts, setRefreshDebts] = useState(0);
  const [refreshSplit, setRefreshSplit] = useState(0);

  useEffect(() => {
    if (isAuthenticated()) {
      setAuthenticated(true);
      fetchExpenses();
    } else {
      setLoading(false);
    }
  }, []);

  async function fetchExpenses() {
    try {
      setLoading(true);
      const data = await getExpenses();
      setExpenses(data);
    } catch (error) {
      console.error("Error fetching expenses:", error);
      if (error.message === "Unauthorized") {
        handleLogout();
      }
    } finally {
      setLoading(false);
    }
  }

  async function handleAdd(expense) {
    try {
      await addExpense(expense);
      await fetchExpenses();
    } catch (error) {
      console.error("Error adding expense:", error);
      alert("Failed to add expense. Please try again.");
    }
  }

  function handleLogin() {
    setAuthenticated(true);
    fetchExpenses();
  }

  function handleLogout() {
    removeToken();
    setAuthenticated(false);
    setExpenses([]);
  }

  if (!authenticated) {
    return showRegister ? (
      <Register 
        onRegister={() => setShowRegister(false)}
        onSwitchToLogin={() => setShowRegister(false)}
      />
    ) : (
      <Login 
        onLogin={handleLogin}
        onSwitchToRegister={() => setShowRegister(true)}
      />
    );
  }

  const filteredExpenses = filterCategory === "all"
    ? expenses
    : expenses.filter(e => e.category.toLowerCase() === filterCategory.toLowerCase());

  const categories = ["all", ...new Set(expenses.map(e => e.category))];

  return (
    <div className="container">
      <Header onLogout={handleLogout} />
      
      <div className="main-tabs">
        <button
          className={`main-tab ${activeTab === "expenses" ? "active" : ""}`}
          onClick={() => setActiveTab("expenses")}
        >
          💰 Personal Expenses
        </button>
        <button
          className={`main-tab ${activeTab === "debts" ? "active" : ""}`}
          onClick={() => setActiveTab("debts")}
        >
          💳 Debts & Loans
        </button>
        <button
          className={`main-tab ${activeTab === "friends" ? "active" : ""}`}
          onClick={() => setActiveTab("friends")}
        >
          👥 Friends
        </button>
        <button
          className={`main-tab ${activeTab === "split" ? "active" : ""}`}
          onClick={() => setActiveTab("split")}
        >
          🤝 Split Expenses
        </button>
      </div>

      <div className="content">
        {activeTab === "expenses" && (
          <>
            <StatsCards expenses={expenses} />
            
            {expenses.length > 3 && (
              <div className="charts-grid">
                <CategoryPieChart />
                <MonthlyLineChart />
              </div>
            )}

            <ExpenseForm onAdd={handleAdd} />
            
            {expenses.length > 0 && (
              <div className="filter-section">
                <label htmlFor="category-filter">Filter by Category:</label>
                <select 
                  id="category-filter"
                  value={filterCategory} 
                  onChange={(e) => setFilterCategory(e.target.value)}
                >
                  {categories.map(cat => (
                    <option key={cat} value={cat}>
                      {cat === "all" ? "All Categories" : cat}
                    </option>
                  ))}
                </select>
              </div>
            )}

            {loading ? (
              <div className="loading">Loading expenses...</div>
            ) : (
              <ExpenseList expenses={filteredExpenses} onUpdate={fetchExpenses} />
            )}
          </>
        )}

        {activeTab === "debts" && (
          <>
            <DebtForm onDebtAdded={() => setRefreshDebts(prev => prev + 1)} />
            <DebtList refresh={refreshDebts} />
          </>
        )}

        {activeTab === "friends" && (
          <FriendList onUpdate={() => setRefreshSplit(prev => prev + 1)} />
        )}

        {activeTab === "split" && (
          <>
            <SplitExpenseForm onExpenseAdded={() => setRefreshSplit(prev => prev + 1)} />
            <SplitExpenseList refresh={refreshSplit} />
          </>
        )}
      </div>
    </div>
  );
}
