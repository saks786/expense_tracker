import React, { useEffect, useState } from "react";
import { Routes, Route, Navigate, useNavigate } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import toast from "react-hot-toast";
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
import LandingPage from "./components/LandingPage";
import GroupList from "./components/GroupList";
import GroupDashboard from "./components/GroupDashboard";

const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLIC_KEY);

// Protected Route Component
function ProtectedRoute({ children }) {
  const [checking, setChecking] = useState(true);
  const [authenticated, setAuthenticated] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuth = async () => {
      if (isAuthenticated()) {
        try {
          await getCurrentUser();
          setAuthenticated(true);
        } catch {
          removeToken();
          setAuthenticated(false);
        }
      }
      setChecking(false);
    };
    checkAuth();
  }, []);

  if (checking) {
    return <div className="loading-screen"><p>Loading...</p></div>;
  }

  return authenticated ? children : <Navigate to="/login" replace />;
}

// Dashboard Component
function Dashboard({ currentUser, onLogout }) {
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterCategory, setFilterCategory] = useState("all");
  const [activeTab, setActiveTab] = useState("expenses");
  const [refreshDebts, setRefreshDebts] = useState(0);
  const [refreshSplit, setRefreshSplit] = useState(0);
  const [paymentModal, setPaymentModal] = useState({ open: false, debt: null, splitExpense: null, amount: 0, paymentType: null });
  const [selectedGroupId, setSelectedGroupId] = useState(null);

  useEffect(() => {
    fetchExpenses();
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
    try {
      await addExpense(expense);
      await fetchExpenses();
      toast.success("Expense added successfully!");
    } catch (error) {
      console.error("Error adding expense:", error);
      toast.error("Failed to add expense");
    }
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

  const filteredExpenses =
    filterCategory === "all"
      ? expenses
      : expenses.filter(
          (e) => e.category.toLowerCase() === filterCategory.toLowerCase()
        );

  const categories = ["all", ...new Set(expenses.map((e) => e.category))];

  return (
    <div className="container">
      <Header onLogout={onLogout} user={currentUser} />

      <div className="main-tabs">
        <button
          className={`main-tab ${activeTab === "expenses" ? "active" : ""}`}
          onClick={() => setActiveTab("expenses")}
        >
          💰 Expenses
        </button>

        <button
          className={`main-tab ${activeTab === "groups" ? "active" : ""}`}
          onClick={() => {
            setActiveTab("groups");
            setSelectedGroupId(null);
          }}
        >
          👥 Groups
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
          🤝 Friends
        </button>

        <button
          className={`main-tab ${activeTab === "split" ? "active" : ""}`}
          onClick={() => setActiveTab("split")}
        >
          ✂️ Split
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

        {activeTab === "groups" && (
          <>
            {!selectedGroupId ? (
              <GroupList onSelectGroup={(groupId) => setSelectedGroupId(groupId)} />
            ) : (
              <GroupDashboard 
                groupId={selectedGroupId} 
                onBack={() => setSelectedGroupId(null)}
              />
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

export default function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (isAuthenticated()) {
      fetchCurrentUser();
    }
  }, []);

  async function fetchCurrentUser() {
    try {
      const user = await getCurrentUser();
      setCurrentUser(user);
    } catch (error) {
      console.error("Failed to fetch user:", error);
      handleLogout();
    }
  }

  async function handleLogin() {
    const user = await getCurrentUser();
    setCurrentUser(user);
    navigate("/dashboard");
  }

  function handleLogout() {
    removeToken();
    setCurrentUser(null);
    navigate("/");
  }

  return (
    <>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<LandingPage />} />
      <Route 
        path="/login" 
        element={
          isAuthenticated() ? (
            <Navigate to="/dashboard" replace />
          ) : (
            <Login onLogin={handleLogin} />
          )
        } 
      />
      <Route 
        path="/register" 
        element={
          isAuthenticated() ? (
            <Navigate to="/dashboard" replace />
          ) : (
            <Register onRegister={() => navigate("/login")} />
          )
        } 
      />

      {/* Protected Routes */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard currentUser={currentUser} onLogout={handleLogout} />
          </ProtectedRoute>
        }
      />

      {/* Catch all - redirect to home */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
    <Toaster
      position="top-right"
      toastOptions={{
        duration: 4000,
        style: {
          background: '#fff',
          color: '#111827',
          padding: '16px',
          borderRadius: '8px',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
        },
        success: {
          iconTheme: {
            primary: '#10B981',
            secondary: '#fff',
          },
        },
        error: {
          iconTheme: {
            primary: '#EF4444',
            secondary: '#fff',
          },
        },
      }}
    />
    </>
  );
}
