# High-Level Design (HLD)
## Group-Based Expense & Settlement Platform (Splitwise-like)

---

## 1. System Overview

### Purpose
Design a **group-centric expense sharing platform** that enables users to:
- Track personal and group expenses
- Split expenses accurately among participants
- Maintain transparent balances and settlements
- Control spending via budgets
- Scale features without architectural rewrites

The system is designed to evolve from a **personal finance tool** into a **sellable SaaS-ready product**.

---

## 2. Key Design Principles

- **Group-first architecture** (not user-first)
- **Financial correctness over UI shortcuts**
- **Auditability and trust**
- **Horizontal feature scalability**
- **Backend-driven business logic**

---

## 3. High-Level Architecture

### Architecture Style
- **Client–Server Architecture**
- **RESTful APIs**
- **Stateless backend**
- **JWT-based authentication**


---

## 4. Major Components

### 4.1 Frontend (React)

**Responsibilities**
- UI rendering
- Client-side validation
- State management (auth, groups, balances)
- API interaction

**Key Modules**
- Authentication Module
- Group Management Module
- Expense & Split Module
- Settlement Module
- Budget & Analytics Module
- Notifications UI

**Key Characteristics**
- Group context is global
- Minimal business logic
- Error-resilient UI (fallbacks, loaders)

---

### 4.2 Backend (FastAPI)

**Responsibilities**
- Authentication & authorization
- Business logic enforcement
- Financial calculations
- Data validation
- Audit logging

**Core Services**
- Auth Service (JWT, OAuth2)
- Group Service
- Expense & Split Service
- Balance Engine
- Settlement Service
- Budget Service
- Notification Service

**Characteristics**
- Stateless APIs
- Centralized validation
- Deterministic calculations

---

### 4.3 Database (PostgreSQL)

**Role**
- Source of truth
- ACID-compliant financial data
- Relationship-driven access control

**Key Characteristics**
- Strong foreign key constraints
- Indexed financial queries
- Soft deletes for auditability

---

## 5. Core Domain Model (High Level)

### 5.1 User
- Identity & authentication
- Can belong to multiple groups

---

### 5.2 Group
- Primary financial context
- Defines scope for expenses, balances, budgets

**Key Rules**
- All split expenses belong to a group
- Group members only can view/edit group data

---

### 5.3 Group Member
- User-to-group mapping
- Role-based permissions (admin/member)

---

### 5.4 Expense
- Belongs to a group
- Created by one user
- Can be personal or shared

---

### 5.5 Split Expense
- Specialized group expense
- Distributed among participants
- Supports multiple split strategies

---

### 5.6 Balance
- Derived entity (not stored)
- Calculated per group
- Represents net owed/owing state

---

### 5.7 Settlement
- Records payments between users
- Requires confirmation
- Affects balances

---

### 5.8 Budget
- Group or personal
- Time-bound (monthly)
- Category-based

---

## 6. Split & Balance Logic (High Level)

### Split Types Supported
- Equal
- Exact Amount
- Percentage
- Shares

### Balance Computation
1. Aggregate all split expenses in a group
2. Calculate per-user contribution vs share
3. Compute net balances
4. Generate optimized settlement suggestions

**Note**
- Balances are **derived**, not persisted
- Ensures consistency and correctness

---

## 7. Audit & Trust Model

### Audit Logs
- Expense creation, update, deletion
- Settlement confirmations
- Budget changes

### Design Choice
- No hard deletes for financial entities
- Full history preserved for dispute resolution

---

## 8. Security Design

### Authentication
- JWT Bearer tokens
- Short-lived access tokens

### Authorization
- User ownership validation
- Group membership enforcement
- Role-based access for admin actions

### Data Isolation
- Users can only access:
  - Their own data
  - Groups they are members of

---

## 9. Scalability Considerations

### Backend
- Stateless APIs → horizontal scaling
- Separate services possible in future

### Database
- Indexed on:
  - user_id
  - group_id
  - expense_id
- Ready for read replicas

### Future Enhancements
- Redis caching for analytics
- Async workers for notifications
- WebSockets for live balance updates

---

## 10. Failure Handling & Edge Cases

- Partial settlements
- Expense edits after settlements
- User leaving group with outstanding balance
- Deleted expenses with existing settlements

Handled via:
- Audit logs
- Soft deletes
- Deterministic recalculation

---

## 11. Deployment View (Logical)

---

## 12. Non-Goals (Explicit)

- Real-time payments (UPI/Stripe) – deferred
- AI predictions – future phase
- Native mobile apps – future phase

---

## 13. Key Architectural Decisions (ADR Summary)

| Decision | Reason |
|--------|-------|
Group-first design | Prevents future rewrites |
Derived balances | Avoids data inconsistency |
Soft deletes | Auditability |
Backend-driven logic | Financial correctness |
Feature flags | Monetization readiness |

---

## 14. Conclusion

This architecture:
- Matches real-world financial behavior
- Scales feature-wise without refactor
- Supports monetization and compliance
- Is suitable for portfolio **and** production

This is a **foundation system**, not a demo app.

---
