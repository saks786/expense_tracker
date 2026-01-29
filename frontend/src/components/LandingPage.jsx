import React from "react";
import { useNavigate } from "react-router-dom";

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="saas-landing">
      {/* Hero Section */}
      <section className="saas-hero">
        <div className="saas-container">
          <div className="hero-content">
            <h1 className="hero-headline">
              Track Expenses. Split Smarter. Settle Instantly.
            </h1>
            <p className="hero-subtext">
              A modern expense tracking platform that helps you manage personal finances, 
              split bills with friends, and settle payments seamlessly.
            </p>
            <div className="hero-ctas">
              <button className="btn-primary" onClick={() => navigate("/register")}>
                Get Started
              </button>
              <button className="btn-secondary" onClick={() => navigate("/login")}>
                Sign In
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="saas-features">
        <div className="saas-container">
          <h2 className="section-title">Everything you need to manage finances</h2>
          
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon-wrapper">
                <svg className="feature-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="feature-title">Expense Tracking</h3>
              <p className="feature-desc">Record and categorize expenses with ease. View spending patterns over time.</p>
            </div>

            <div className="feature-card">
              <div className="feature-icon-wrapper">
                <svg className="feature-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="feature-title">Analytics</h3>
              <p className="feature-desc">Visualize your spending with charts and get insights into your habits.</p>
            </div>

            <div className="feature-card">
              <div className="feature-icon-wrapper">
                <svg className="feature-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <h3 className="feature-title">Split Bills</h3>
              <p className="feature-desc">Divide expenses with friends and keep track of who owes what.</p>
            </div>

            <div className="feature-card">
              <div className="feature-icon-wrapper">
                <svg className="feature-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="feature-title">Settlements</h3>
              <p className="feature-desc">Process payments securely using Stripe integration for quick settlements.</p>
            </div>

            <div className="feature-card">
              <div className="feature-icon-wrapper">
                <svg className="feature-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                </svg>
              </div>
              <h3 className="feature-title">Budgeting</h3>
              <p className="feature-desc">Set spending limits and track progress towards your financial goals.</p>
            </div>

            <div className="feature-card">
              <div className="feature-icon-wrapper">
                <svg className="feature-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h3 className="feature-title">Security</h3>
              <p className="feature-desc">Your data is protected with JWT authentication and secure encryption.</p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="saas-how-it-works">
        <div className="saas-container">
          <h2 className="section-title">How it works</h2>
          <div className="steps-grid">
            <div className="step-card">
              <div className="step-number">1</div>
              <h3 className="step-title">Track</h3>
              <p className="step-desc">Add your expenses and categorize them for better organization.</p>
            </div>
            <div className="step-card">
              <div className="step-number">2</div>
              <h3 className="step-title">Split</h3>
              <p className="step-desc">Share bills with friends and calculate who owes what automatically.</p>
            </div>
            <div className="step-card">
              <div className="step-number">3</div>
              <h3 className="step-title">Settle</h3>
              <p className="step-desc">Pay or receive money securely through integrated payment processing.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Trust Section */}
      <section className="saas-trust">
        <div className="saas-container">
          <div className="trust-content">
            <h2 className="section-title">Built with security in mind</h2>
            <div className="trust-features">
              <div className="trust-item">
                <span className="trust-check">✓</span>
                <span>JWT Authentication</span>
              </div>
              <div className="trust-item">
                <span className="trust-check">✓</span>
                <span>End-to-end Encryption</span>
              </div>
              <div className="trust-item">
                <span className="trust-check">✓</span>
                <span>Secure Cloud Storage</span>
              </div>
              <div className="trust-item">
                <span className="trust-check">✓</span>
                <span>Stripe Payment Integration</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="saas-footer">
        <div className="saas-container">
          <div className="footer-content">
            <div className="footer-links">
              <a href="#docs">Documentation</a>
              <a href="#github">GitHub</a>
              <a href="#privacy">Privacy Policy</a>
              <a href="#contact">Contact</a>
            </div>
            <p className="footer-copy">© 2026 Expense Tracker. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
