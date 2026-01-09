// src/components/Login.jsx
import React, { useState } from "react";
import { login } from "../api";

export default function Login({ onLogin, onSwitchToRegister }) {
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    // inside handleSubmit ...
try {
  await login(form.username, form.password);
  onLogin();
} catch (err) {
  // err.message may contain raw server text; try to make it friendly
  const msg = err?.message ? String(err.message).replace(/\\n|\\r/g, " ") : "Login failed";
  setError(msg);
} finally {
  setLoading(false);
}

  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h2>Welcome Back</h2>
          <p>Sign in to continue</p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          {error && <div className="error-message">{error}</div>}

          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              type="text"
              value={form.username}
              onChange={(e) => setForm({ ...form, username: e.target.value })}
              placeholder="Enter username"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              placeholder="Enter password"
              required
            />
          </div>

          <button type="submit" className="btn-primary btn-full" disabled={loading}>
            {loading ? "Signing in..." : "Login"}
          </button>
        </form>

        <p className="auth-footer">
          Don’t have an account?{" "}
          <button onClick={onSwitchToRegister} className="link-button">
            Register
          </button>
        </p>
      </div>
    </div>
  );
}
