import React, { useEffect, useState } from "react";
import { loadStripe } from "@stripe/stripe-js";
import { Elements } from "@stripe/react-stripe-js";
import {
  getExpenses,
  addExpense,
  isAuthenticated,
  removeToken,
  getCurrentUser,
} from "./api";

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
import PaymentModal from "./components/PaymentModal";
import TransactionHistory from "./components/TransactionHistory";

const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLIC_KEY);

export default function App() {
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterCategory, setFilterCategory] = useState("all");
  const [authenticated, setAuthenticated] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [showRegister, setShowRegister] = useState(false);
  const [activeTab, setActiveTab] = useState("expenses");
  const [refreshDebts, setRefreshDebts] = useState(0);
  const [refreshSplit, setRefreshSplit] = useState(0);
  const [paymentModal, setPaymentModal] = useState({ open: false, debt: null, splitExpense: null, amount: 0, paymentType: null });

  useEffect(() => {
    async function init() {
      if (isAuthenticated()) {
        try {
          setAuthenticated(true);
          const user = await getCurrentUser();
          setCurrentUser(user);
          await fetchExpenses();
        } catch {
          handleLogout();
        }
      } else {
        setLoading(false);
      }
    }
    init();
  }, []);

  async function fetchExpenses() {
    try {
      setLoading(true);
      const data = await getExpenses();
      setExpenses(data);
    } finally {
      setLoading(false);
    }
  }

  async function handleAdd(expense) {
    await addExpense(expense);
    await fetchExpenses();
  }

  async function handleLogin() {
    setAuthenticated(true);
    const user = await getCurrentUser();
    setCurrentUser(user);
    fetchExpenses();
  }

  function handleLogout() {
    removeToken();
    setAuthenticated(false);
    setCurrentUser(null);
    setExpenses([]);
  }

  const handleDebtPaymentClick = (debt, amount) => {
    setPaymentModal({
      open: true,
      debt,
      splitExpense: null,
      amount,
      paymentType: "debt_payment",
    });
  };

  const handleSplitPaymentClick = (splitExpense, amount, type) => {
    setPaymentModal({
      open: true,
      debt: null,
      splitExpense,
      amount,
      paymentType: "split_expense_payment",
    });
  };

  const handlePaymentSuccess = async () => {
    setPaymentModal({ open: false, debt: null, splitExpense: null, amount: 0, paymentType: null });
    setRefreshDebts((p) => p + 1);
    setRefreshSplit((p) => p + 1);
  };

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

  const filteredExpenses =
    filterCategory === "all"
      ? expenses
      : expenses.filter(
          (e) => e.category.toLowerCase() === filterCategory.toLowerCase()
        );

  const categories = ["all", ...new Set(expenses.map((e) => e.category))];

  return (
    <div className="container">
      <Header onLogout={handleLogout} user={currentUser} />

      <div className="main-tabs">
        <button
          className={`main-tab ${activeTab === "expenses" ? "active" : ""}`}
          onClick={() => setActiveTab("expenses")}
        >
          💰 Expenses
        </button>

        <button
          className={`main-tab ${activeTab === "debts" ? "active" : ""}`}
          onClick={() => setActiveTab("debts")}
        >
          💳 Debts
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
          🤝 Split
        </button>

        <button
          className={`main-tab ${activeTab === "transactions" ? "active" : ""}`}
          onClick={() => setActiveTab("transactions")}
        >
          📊 Transactions
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

            <div className="filter-section">
              <label>Filter:</label>
              <select
                value={filterCategory}
                onChange={(e) => setFilterCategory(e.target.value)}
              >
                {categories.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </select>
            </div>

            {loading ? (
              <p>Loading...</p>
            ) : (
              <ExpenseList expenses={filteredExpenses} onUpdate={fetchExpenses} />
            )}
          </>
        )}

        {activeTab === "debts" && (
          <>
            <DebtForm onDebtAdded={() => setRefreshDebts((p) => p + 1)} />
            <DebtList refresh={refreshDebts} onPaymentClick={handleDebtPaymentClick} />
          </>
        )}

        {activeTab === "friends" && (
          <FriendList onUpdate={() => setRefreshSplit((p) => p + 1)} />
        )}

        {activeTab === "split" && (
          <>
            <SplitExpenseForm
              onExpenseAdded={() => setRefreshSplit((p) => p + 1)}
            />
            <SplitExpenseList refresh={refreshSplit} onPaymentClick={handleSplitPaymentClick} />
          </>
        )}

        {activeTab === "transactions" && (
          <TransactionHistory />
        )}
      </div>

      {paymentModal.open && (
        <Elements stripe={stripePromise}>
          <PaymentModal
            open={paymentModal.open}
            debt={paymentModal.debt}
            splitExpense={paymentModal.splitExpense}
            amount={paymentModal.amount}
            paymentType={paymentModal.paymentType}
            onClose={() => setPaymentModal({ open: false, debt: null, splitExpense: null, amount: 0, paymentType: null })}
            onSuccess={handlePaymentSuccess}
          />
        </Elements>
      )}
    </div>
  );
}
