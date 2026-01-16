import React, { useState, useEffect } from "react";
import {
  getSplitExpenses,
  deleteSplitExpense,
  getCurrentUser,
  getBalances,
  getSettlementSuggestions,
} from "../api";

export default function SplitExpenseList({ refresh }) {
  const [splitExpenses, setSplitExpenses] = useState([]);
  const [balances, setBalances] = useState({});
  const [suggestions, setSuggestions] = useState([]);
  const [currentUserId, setCurrentUserId] = useState(null);

  useEffect(() => {
    loadData();
  }, [refresh]);

  async function loadData() {
    const user = await getCurrentUser();
    setCurrentUserId(user.id);
    setSplitExpenses(await getSplitExpenses());
    setBalances(await getBalances());
    setSuggestions(await getSettlementSuggestions());
  }

  return (
    <div>
      <h3>💰 Balances</h3>
      {Object.entries(balances).map(([u, a]) => (
        <p key={u}>{u}: ₹{a.toFixed(2)}</p>
      ))}

      <h3>🔁 Settlement Suggestions</h3>
      {suggestions.length === 0
        ? <p>All settled 🎉</p>
        : suggestions.map((s, i) => (
            <p key={i}>{s.from} ➜ {s.to}: ₹{s.amount}</p>
          ))}

      <h3>🤝 Split Expenses</h3>
      {splitExpenses.map(exp => (
        <div key={exp.id}>
          <strong>{exp.description}</strong> – ₹{exp.total_amount}
        </div>
      ))}
    </div>
  );
}
