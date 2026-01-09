import React from "react";

export default function Header({ onLogout }) {
  return (
    <header className="header">
      <div className="header-content" style={styles.headerContent}>
        <div style={styles.textBlock}>
          <h1 style={styles.title}>💰 Expense Tracker</h1>
          <p style={styles.subtitle}>
            Take control of your finances, one expense at a time
          </p>
        </div>

        {onLogout && (
          <button
            onClick={onLogout}
            aria-label="Logout from your account"
            className="btn btn-logout"
            style={styles.logoutButton}
          >
            Logout
          </button>
        )}
      </div>
    </header>
  );
}

const styles = {
  headerContent: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    maxWidth: "1200px",
    margin: "0 auto",
    padding: "0 20px",
  },
  textBlock: {
    display: "flex",
    flexDirection: "column",
    gap: "6px",
  },
  title: {
    fontSize: "2.4rem",
    fontWeight: 700,
    margin: 0,
  },
  subtitle: {
    fontSize: "1rem",
    opacity: 0.92,
    margin: 0,
  },
  logoutButton: {
    padding: "10px 20px",
    borderRadius: "10px",
    background: "rgba(255, 255, 255, 0.2)",
    color: "white",
    border: "2px solid transparent",
  },
};
