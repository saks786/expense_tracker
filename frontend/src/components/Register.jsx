import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { register } from "../api";

export default function Register({ onRegister }) {
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: "", email: "", password: "", confirmPassword: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    
    if (form.password !== form.confirmPassword) {
      setError("Passwords don't match");
      return;
    }
    
    if (form.password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }
    
    setLoading(true);
    
    try {
      await register(form.username, form.email, form.password);
      toast.success("Registration successful! Redirecting to login...");
      setTimeout(() => navigate("/login"), 1000);
    } catch (err) {
      setError(err.message || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h2>🎉 Join Us!</h2>
          <p>Create an account to start tracking</p>
        </div>
        
        <form onSubmit={handleSubmit} className="auth-form">
          {error && <div className="error-message">{error}</div>}
          
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              type="text"
              placeholder="Choose a username"
              value={form.username}
              onChange={(e) => setForm({ ...form, username: e.target.value })}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              placeholder="your.email@example.com"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              placeholder="At least 6 characters"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <input
              id="confirmPassword"
              type="password"
              placeholder="Re-enter your password"
              value={form.confirmPassword}
              onChange={(e) => setForm({ ...form, confirmPassword: e.target.value })}
              required
            />
          </div>

          <button type="submit" className="btn btn-primary btn-full" disabled={loading}>
            {loading ? "Creating account..." : "Register"}
          </button>
        </form>

        <div className="auth-footer">
          Already have an account?{" "}
          <Link to="/login" className="link-button">
            Login here
          </Link>
        </div>
        
        <div className="auth-footer" style={{ marginTop: '8px' }}>
          <Link to="/" className="link-button">
            ← Back to Home
          </Link>
        </div>
      </div>
    </div>
  );
}
