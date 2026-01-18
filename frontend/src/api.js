// frontend/src/api.js

const API_BASE =
  import.meta.env.VITE_API_URL ||
  "http://localhost:8000";

/* ================= TOKEN HELPERS ================= */

export function getToken() {
  return localStorage.getItem("token");
}

export function setToken(token) {
  localStorage.setItem("token", token);
}

export function removeToken() {
  localStorage.removeItem("token");
}

export function isAuthenticated() {
  return !!getToken();
}

/* ================= HEADERS ================= */

function authHeaders() {
  const token = getToken();
  return token
    ? {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      }
    : {
        "Content-Type": "application/json",
      };
}

/* ================= AUTH ================= */

export async function login(username, password) {
  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);

  const res = await fetch(`${API_BASE}/api/token`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: formData,
  });

  if (!res.ok) throw new Error("Invalid credentials");

  const data = await res.json();
  setToken(data.access_token);
  return data;
}

export async function register(username, email, password) {
  const res = await fetch(`${API_BASE}/api/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email, password }),
  });

  if (!res.ok) throw new Error("Registration failed");
  return res.json();
}

export async function getCurrentUser() {
  const res = await fetch(`${API_BASE}/api/users/me`, {
    headers: authHeaders(),
  });

  if (!res.ok) throw new Error("Unauthorized");
  return res.json();
}

/* ================= EXPENSES ================= */

export async function getExpenses() {
  const res = await fetch(`${API_BASE}/api/expenses`, {
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Failed to fetch expenses");
  return res.json();
}

export async function addExpense(expense) {
  const res = await fetch(`${API_BASE}/api/expenses`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(expense),
  });
  if (!res.ok) throw new Error("Failed to add expense");
  return res.json();
}

export async function updateExpense(id, expense) {
  const res = await fetch(`${API_BASE}/api/expenses/${id}`, {
    method: "PUT",
    headers: authHeaders(),
    body: JSON.stringify(expense),
  });
  if (!res.ok) throw new Error("Failed to update expense");
  return res.json();
}

export async function deleteExpense(id) {
  const res = await fetch(`${API_BASE}/api/expenses/${id}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Failed to delete expense");
  return res.json();
}

/* ================= DEBTS ================= */

export async function getDebts() {
  const res = await fetch(`${API_BASE}/api/debts`, {
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Failed to fetch debts");
  return res.json();
}

export async function addDebt(debt) {
  const res = await fetch(`${API_BASE}/api/debts`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(debt),
  });
  if (!res.ok) throw new Error("Failed to add debt");
  return res.json();
}

export async function updateDebt(id, debt) {
  const res = await fetch(`${API_BASE}/api/debts/${id}`, {
    method: "PUT",
    headers: authHeaders(),
    body: JSON.stringify(debt),
  });
  if (!res.ok) throw new Error("Failed to update debt");
  return res.json();
}

export async function deleteDebt(id) {
  const res = await fetch(`${API_BASE}/api/debts/${id}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Failed to delete debt");
  return res.json();
}

/* ================= FRIENDS ================= */

export async function getFriends() {
  const res = await fetch(`${API_BASE}/api/friends`, {
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Failed to fetch friends");
  return res.json();
}

export async function getFriendRequests() {
  const res = await fetch(`${API_BASE}/api/friends/requests`, {
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Failed to fetch friend requests");
  return res.json();
}

export async function sendFriendRequest(username) {
  const res = await fetch(`${API_BASE}/api/friends/request`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ friend_username: username }),
  });
  if (!res.ok) throw new Error("Failed to send request");
  return res.json();
}

export async function acceptFriendRequest(id) {
  const res = await fetch(`${API_BASE}/api/friends/${id}/accept`, {
    method: "PUT",
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Failed to accept request");
  return res.json();
}

export async function removeFriend(id) {
  const res = await fetch(`${API_BASE}/api/friends/${id}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Failed to remove friend");
  return res.json();
}

/* ================= SPLIT EXPENSES ================= */

export async function getSplitExpenses() {
  const res = await fetch(`${API_BASE}/api/split-expenses`, {
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Failed to fetch split expenses");
  return res.json();
}

export async function addSplitExpense(data) {
  const res = await fetch(`${API_BASE}/api/split-expenses`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to add split expense");
  return res.json();
}

export async function deleteSplitExpense(id) {
  const res = await fetch(`${API_BASE}/api/split-expenses/${id}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Failed to delete split expense");
  return res.json();
}

/* ================= SPLIT BALANCES (PHASE 3) ================= */

export async function getBalances() {
  const res = await fetch(`${API_BASE}/api/balances`, {
    headers: authHeaders(),
  });
  if (!res.ok) {
    throw new Error("Failed to fetch balances");
  }
  return res.json();
}

export async function getSettlementSuggestions() {
  const res = await fetch(`${API_BASE}/api/settlements/suggestions`, {
    headers: authHeaders(),
  });
  if (!res.ok) {
    throw new Error("Failed to fetch settlement suggestions");
  }
  return res.json();
}

/* ================= PAYMENTS & TRANSACTIONS ================= */

export async function createPaymentIntent(payload) {
  const res = await fetch(`${API_BASE}/api/payments/create-intent`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to create payment intent");
  return res.json();
}

export async function confirmPayment(payload) {
  const res = await fetch(`${API_BASE}/api/payments/confirm-payment`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to confirm payment");
  return res.json();
}

export async function getTransactionHistory() {
  const res = await fetch(`${API_BASE}/api/payments/history`, {
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Failed to fetch transactions");
  return res.json();
}

export async function getTransactionDetails(transactionId) {
  const res = await fetch(`${API_BASE}/api/payments/${transactionId}`, {
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Failed to fetch transaction details");
  return res.json();
}

