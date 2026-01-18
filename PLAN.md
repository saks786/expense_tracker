
# Expense Split App – Development Plan 

## Objective
Evolve the existing expense tracker into a **group-centric expense sharing platform** that is:
- Architecturally sound
- Feature-scalable
- Monetization-ready

This plan avoids UI-first work and focuses on **correct financial modeling**.

---

## Phase 0 – Baseline Lock (Week 0)

### Goals
- Stabilize current implementation
- Avoid regression during refactors

### Tasks
- Tag current codebase as `v1.0`
- Verify all existing APIs
- Document current flows (auth, expenses, splits)
- List incomplete features (debts, friends, budgets)

### Output
- Stable baseline version

---

## Phase 1 – Group-Centric Architecture (Week 1)

### 1. Introduce Groups (CRITICAL)

#### Backend
Create tables:
```text
groups
- id
- name
- currency
- created_by
- created_at
- is_archived

group_members
- group_id
- user_id
- role (admin | member)
- joined_at
````

Endpoints:

* POST /api/groups
* GET /api/groups
* POST /api/groups/{id}/invite
* POST /api/groups/{id}/leave
* PATCH /api/groups/{id}/archive

#### Frontend

* Group list screen
* Create group modal
* Active group selector

### Rules

* All split expenses must belong to a group
* Only group members can add or view expenses

### Output

* App becomes **group-first**, not user-first

---

## Phase 2 – Real Split Logic (Week 2)

### 2. Multiple Split Types

Replace equal-only split logic.

```text
split_participants
- split_expense_id
- user_id
- split_type (equal | exact | percentage | shares)
- split_value
```

### Validation Rules

* Equal → auto-calculated
* Exact → sum == total
* Percentage → sum == 100
* Shares → proportional split

### Frontend

* Split type selector
* Dynamic inputs
* Real-time validation

### Output

* Real-world splitting (Splitwise parity)

---

### 3. Balance Engine v2

* Group-level balance calculation
* Net balances per user
* Optimized settlement graph (min transactions)

### Output

* Accurate balances regardless of split complexity

---

## Phase 3 – Trust & Auditability (Week 3)

### 4. Expense Audit Logs

```text
expense_audit_logs
- expense_id
- changed_by
- action (create | edit | delete)
- before
- after
- timestamp
```

Rules:

* Soft delete only
* Full edit history preserved

Frontend:

* Expense history drawer

### Output

* Trust & transparency in shared finances

---

### 5. Settlements v2

```text
settlements
- from_user
- to_user
- amount
- status (pending | confirmed)
- created_at
```

Flow:

1. User marks payment as done
2. Receiver confirms
3. Balances update

### Output

* Dispute-safe settlement flow

---

## Phase 4 – Budgeting & Intelligence (Week 4)

### 6. Budget System

* Monthly budgets
* Category-based
* Group-level and personal budgets

Frontend:

* Budget vs actual
* Warning indicators

### Output

* Spending control, not just tracking

---

### 7. Notifications (Minimal)

Triggers:

* Group invite
* Expense added
* Settlement requested
* Budget exceeded

Channels:

* In-app (mandatory)
* Email (optional)

---

## Phase 5 – Sellability Layer (Week 5)

### 8. Data Export & Ownership

* CSV export
* PDF group summary
* Settlement history export

Purpose:

* Compliance
* Professional usage

---

### 9. Monetization Hooks (No Payments Yet)

Feature flags:

```text
features
- unlimited_groups
- advanced_splits
- exports
- receipt_upload
```

Enables:

* Future Stripe integration
* Tiered plans without refactor

---

## Phase 6 – Hardening & Polish (Week 6)

### Backend

* PostgreSQL default
* Proper indexing
* Background jobs for analytics

### Frontend

* Global group context
* Skeleton loaders
* Error boundaries

---

## Final Outcome

By completion:

* Group-based expense platform
* Advanced split logic
* Trustworthy settlements
* Budgeting + analytics
* Monetization-ready architecture

This is no longer a demo app — it is a **foundation product**.

---

## Non-Negotiable Rule

If **Groups** are not implemented first,
the system **will require a full rewrite later**.
