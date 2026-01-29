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

/* ================= ERROR HANDLER ================= */

async function handleResponse(res) {
  if (!res.ok) {
    let errorMessage = `Error ${res.status}`;
    
    try {
      const errorData = await res.json();
      
      // Handle FastAPI validation errors (422)
      if (errorData.detail) {
        if (Array.isArray(errorData.detail)) {
          // Validation errors array
          const errors = errorData.detail.map(err => {
            const field = err.loc ? err.loc[err.loc.length - 1] : 'field';
            return `${field}: ${err.msg}`;
          }).join(', ');
          errorMessage = `Validation Error: ${errors}`;
        } else if (typeof errorData.detail === 'string') {
          // Simple error message
          errorMessage = errorData.detail;
        }
      } else if (errorData.message) {
        errorMessage = errorData.message;
      }
    } catch (e) {
      // If response is not JSON or parsing fails
      errorMessage = `Request failed with status ${res.status}`;
    }
    
    throw new Error(errorMessage);
  }
  
  return res.json();
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

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || "Invalid credentials");
  }

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

  return handleResponse(res);
}

export async function getCurrentUser() {
  const res = await fetch(`${API_BASE}/api/users/me`, {
    headers: authHeaders(),
  });

  return handleResponse(res);
}

/* ================= EXPENSES ================= */

export async function getExpenses() {
  const res = await fetch(`${API_BASE}/api/expenses`, {
    headers: authHeaders(),
  });
  return handleResponse(res);
}

export async function addExpense(expense) {
  // Ensure proper format: remove null/undefined date, keep description optional
  const payload = {
    category: expense.category,
    amount: parseFloat(expense.amount),
    ...(expense.description && { description: expense.description }),
    ...(expense.date && { date: expense.date }),
  };

  const res = await fetch(`${API_BASE}/api/expenses`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
}

export async function updateExpense(id, expense) {
  // Only include fields that are being updated
  const payload = {};
  if (expense.category) payload.category = expense.category;
  if (expense.amount !== undefined) payload.amount = parseFloat(expense.amount);
  if (expense.description !== undefined) payload.description = expense.description;
  if (expense.date !== undefined) payload.date = expense.date;

  const res = await fetch(`${API_BASE}/api/expenses/${id}`, {
    method: "PUT",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
}

export async function deleteExpense(id) {
  const res = await fetch(`${API_BASE}/api/expenses/${id}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  return handleResponse(res);
}

/* ================= DEBTS ================= */

export async function getDebts() {
  const res = await fetch(`${API_BASE}/api/debts`, {
    headers: authHeaders(),
  });
  return handleResponse(res);
}

export async function addDebt(debt) {
  // Ensure all required fields are present and properly formatted
  const payload = {
    name: debt.name,
    principal_amount: parseFloat(debt.principal_amount),
    remaining_amount: parseFloat(debt.remaining_amount),
    interest_rate: parseFloat(debt.interest_rate),
    emi_amount: parseFloat(debt.emi_amount),
    emi_date: parseInt(debt.emi_date),
    start_date: debt.start_date, // Must be in "YYYY-MM-DD" format
    ...(debt.status && { status: debt.status }),
  };

  const res = await fetch(`${API_BASE}/api/debts`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
}

export async function updateDebt(id, debt) {
  const payload = {};
  if (debt.name) payload.name = debt.name;
  if (debt.principal_amount !== undefined) payload.principal_amount = parseFloat(debt.principal_amount);
  if (debt.remaining_amount !== undefined) payload.remaining_amount = parseFloat(debt.remaining_amount);
  if (debt.interest_rate !== undefined) payload.interest_rate = parseFloat(debt.interest_rate);
  if (debt.emi_amount !== undefined) payload.emi_amount = parseFloat(debt.emi_amount);
  if (debt.emi_date !== undefined) payload.emi_date = parseInt(debt.emi_date);
  if (debt.start_date) payload.start_date = debt.start_date;
  if (debt.status) payload.status = debt.status;

  const res = await fetch(`${API_BASE}/api/debts/${id}`, {
    method: "PUT",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
}

export async function deleteDebt(id) {
  const res = await fetch(`${API_BASE}/api/debts/${id}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  return handleResponse(res);
}

/* ================= FRIENDS ================= */

export async function getFriends() {
  const res = await fetch(`${API_BASE}/api/friends`, {
    headers: authHeaders(),
  });
  return handleResponse(res);
}

export async function getFriendRequests() {
  const res = await fetch(`${API_BASE}/api/friends/requests`, {
    headers: authHeaders(),
  });
  return handleResponse(res);
}

export async function sendFriendRequest(username) {
  const res = await fetch(`${API_BASE}/api/friends/request`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ friend_username: username }),
  });
  return handleResponse(res);
}

export async function acceptFriendRequest(id) {
  const res = await fetch(`${API_BASE}/api/friends/accept/${id}`, {
    method: "POST",
    headers: authHeaders(),
  });
  return handleResponse(res);
}

export async function rejectFriendRequest(id) {
  const res = await fetch(`${API_BASE}/api/friends/reject/${id}`, {
    method: "POST",
    headers: authHeaders(),
  });
  return handleResponse(res);
}

export async function removeFriend(id) {
  const res = await fetch(`${API_BASE}/api/friends/${id}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  return handleResponse(res);
}

/* ================= SPLIT EXPENSES ================= */

export async function getSplitExpenses() {
  const res = await fetch(`${API_BASE}/api/split-expenses`, {
    headers: authHeaders(),
  });
  return handleResponse(res);
}

export async function addSplitExpense(data) {
  // Ensure proper format according to API spec
  const payload = {
    description: data.description,
    total_amount: parseFloat(data.total_amount),
    category: data.category,
    participant_ids: data.participant_ids, // Array of user IDs
    ...(data.date && { date: data.date }),
  };

  const res = await fetch(`${API_BASE}/api/split-expenses`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
}

export async function deleteSplitExpense(id) {
  const res = await fetch(`${API_BASE}/api/split-expenses/${id}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  return handleResponse(res);
}

/* ================= SPLIT BALANCES (PHASE 3) ================= */

export async function getBalances() {
  const res = await fetch(`${API_BASE}/api/balances`, {
    headers: authHeaders(),
  });
  return handleResponse(res);
}

export async function getSettlementSuggestions() {
  const res = await fetch(`${API_BASE}/api/settlements/suggestions`, {
    headers: authHeaders(),
  });
  return handleResponse(res);
}

/* ================= PAYMENTS & TRANSACTIONS ================= */

export async function createPaymentIntent(payload) {
  const res = await fetch(`${API_BASE}/api/payments/create-intent`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
}

export async function confirmPayment(payload) {
  const res = await fetch(`${API_BASE}/api/payments/confirm-payment`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
}

export async function getTransactionHistory() {
  const res = await fetch(`${API_BASE}/api/payments/history`, {
    headers: authHeaders(),
  });
  return handleResponse(res);
}

export async function getTransactionDetails(transactionId) {
  const res = await fetch(`${API_BASE}/api/payments/${transactionId}`, {
    headers: authHeaders(),
  });
  return handleResponse(res);
}

/* ================= GROUPS ================= */

export async function getGroups() {
  const res = await fetch(`${API_BASE}/api/groups`, {
    headers: authHeaders(),
  });
  return handleResponse(res);
}

export async function createGroup(groupData) {
  // Ensure proper format
  const payload = {
    name: groupData.name,
    ...(groupData.description && { description: groupData.description }),
    ...(groupData.currency && { currency: groupData.currency }),
    ...(groupData.image_url && { image_url: groupData.image_url }),
  };

  const res = await fetch(`${API_BASE}/api/groups`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
}

export async function getGroupDetails(groupId) {
  const res = await fetch(`${API_BASE}/api/groups/${groupId}`, {
    headers: authHeaders(),
  });
  return handleResponse(res);
}

export async function updateGroup(groupId, groupData) {
  const payload = {};
  if (groupData.name) payload.name = groupData.name;
  if (groupData.description !== undefined) payload.description = groupData.description;
  if (groupData.currency) payload.currency = groupData.currency;
  if (groupData.image_url !== undefined) payload.image_url = groupData.image_url;

  const res = await fetch(`${API_BASE}/api/groups/${groupId}`, {
    method: "PUT",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
}

export async function deleteGroup(groupId) {
  const res = await fetch(`${API_BASE}/api/groups/${groupId}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  return handleResponse(res);
}

/* ================= GROUP MEMBERS ================= */

export async function getGroupInvitations() {
  const res = await fetch(`${API_BASE}/api/groups/invitations/pending`, {
    headers: authHeaders(),
  });
  
  if (!res.ok) {
    console.error('Failed to fetch group invitations');
    return [];
  }
  
  const data = await res.json();
  return data;
}

export async function inviteGroupMembers(groupId, usernames) {
  // Accept array of usernames as per documentation
  const usernamesArray = Array.isArray(usernames) ? usernames : [usernames];
  
  const res = await fetch(`${API_BASE}/api/groups/${groupId}/invite`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ usernames: usernamesArray }),
  });
  
  return handleResponse(res);
}

// Legacy function for backward compatibility - invites single user
export async function inviteGroupMember(groupId, username) {
  return inviteGroupMembers(groupId, [username]);
}

export async function joinGroup(groupId) {
  const res = await fetch(`${API_BASE}/api/groups/${groupId}/join`, {
    method: "POST",
    headers: authHeaders(),
  });
  return handleResponse(res);
}

export async function leaveGroup(groupId) {
  const res = await fetch(`${API_BASE}/api/groups/${groupId}/leave`, {
    method: "POST",
    headers: authHeaders(),
  });
  return handleResponse(res);
}

export async function updateGroupMember(groupId, userId, memberData) {
  const res = await fetch(`${API_BASE}/api/groups/${groupId}/members/${userId}`, {
    method: "PUT",
    headers: authHeaders(),
    body: JSON.stringify(memberData),
  });
  return handleResponse(res);
}

export async function removeGroupMember(groupId, userId) {
  const res = await fetch(`${API_BASE}/api/groups/${groupId}/members/${userId}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  return handleResponse(res);
}

/* ================= GROUP EXPENSES ================= */

export async function getGroupExpenses(groupId) {
  const res = await fetch(`${API_BASE}/api/groups/${groupId}/expenses`, {
    headers: authHeaders(),
  });
  return handleResponse(res);
}

export async function addGroupExpense(groupId, expenseData) {
  // Ensure proper format according to API spec
  const payload = {
    description: expenseData.description,
    total_amount: parseFloat(expenseData.total_amount),
    category: expenseData.category,
    paid_by: expenseData.paid_by,
    participants: expenseData.participants.map(p => ({
      user_id: p.user_id,
      share_amount: parseFloat(p.share_amount),
    })),
    ...(expenseData.date && { date: expenseData.date }),
  };

  const res = await fetch(`${API_BASE}/api/groups/${groupId}/expenses`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
}

export async function updateGroupExpense(groupId, expenseId, expenseData) {
  const payload = {};
  if (expenseData.description) payload.description = expenseData.description;
  if (expenseData.total_amount !== undefined) payload.total_amount = parseFloat(expenseData.total_amount);
  if (expenseData.category) payload.category = expenseData.category;
  if (expenseData.paid_by) payload.paid_by = expenseData.paid_by;
  if (expenseData.date) payload.date = expenseData.date;
  if (expenseData.participants) {
    payload.participants = expenseData.participants.map(p => ({
      user_id: p.user_id,
      share_amount: parseFloat(p.share_amount),
    }));
  }

  const res = await fetch(`${API_BASE}/api/groups/${groupId}/expenses/${expenseId}`, {
    method: "PUT",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
}

export async function deleteGroupExpense(groupId, expenseId) {
  const res = await fetch(`${API_BASE}/api/groups/${groupId}/expenses/${expenseId}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  return handleResponse(res);
}

/* ================= GROUP BALANCES & SETTLEMENTS ================= */

export async function getGroupBalances(groupId) {
  const res = await fetch(`${API_BASE}/api/groups/${groupId}/balances`, {
    headers: authHeaders(),
  });
  return handleResponse(res);
}

export async function getGroupSettlementSuggestions(groupId) {
  const res = await fetch(`${API_BASE}/api/groups/${groupId}/settlements/suggestions`, {
    headers: authHeaders(),
  });
  return handleResponse(res);
}

export async function recordGroupSettlement(groupId, settlementData) {
  // Ensure proper format
  const payload = {
    from_user_id: settlementData.from_user_id,
    to_user_id: settlementData.to_user_id,
    amount: parseFloat(settlementData.amount),
    ...(settlementData.payment_method && { payment_method: settlementData.payment_method }),
    ...(settlementData.notes && { notes: settlementData.notes }),
  };

  const res = await fetch(`${API_BASE}/api/groups/${groupId}/settlements`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
}

export async function getGroupSettlements(groupId) {
  const res = await fetch(`${API_BASE}/api/groups/${groupId}/settlements`, {
    headers: authHeaders(),
  });
  return handleResponse(res);
}

