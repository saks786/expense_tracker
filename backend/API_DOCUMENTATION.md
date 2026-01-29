# Expense Tracker API Documentation

Base URL: `http://localhost:8000`

## Authentication

All endpoints (except registration and login) require JWT authentication.

**Header Format:**
```
Authorization: Bearer <access_token>
```

---

## 1. Authentication & User Management

### 1.1 Register User
**POST** `/api/register`

Creates a new user account.

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**Response (200):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "is_active": true
}
```

### 1.2 Login
**POST** `/api/token`

Authenticates user and returns JWT token.

**Request Body (Form Data):**
```
username=john_doe
password=password123
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 1.3 Get Current User
**GET** `/api/users/me`

Returns authenticated user's profile.

**Response (200):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "is_active": true
}
```

---

## 2. Expenses

### 2.1 Create Expense
**POST** `/api/expenses`

Creates a personal expense.

**Request Body:**
```json
{
  "category": "Food",
  "amount": 500.0,
  "description": "Lunch at restaurant",
  "date": null
}
```

**Note:** `date` and `description` are optional. Date defaults to today if not provided.

**Response (200):**
```json
{
  "id": 1,
  "category": "Food",
  "amount": 500.0,
  "description": "Lunch at restaurant",
  "date": "2026-01-29",
  "owner_id": 1
}
```

### 2.2 List Expenses
**GET** `/api/expenses`

Returns all expenses for the authenticated user.

**Response (200):**
```json
[
  {
    "id": 1,
    "category": "Food",
    "amount": 500.0,
    "description": "Lunch",
    "date": "2026-01-29",
    "owner_id": 1
  }
]
```

### 2.3 Update Expense
**PUT** `/api/expenses/{expense_id}`

Updates an existing expense.

**Request Body:**
```json
{
  "category": "Food",
  "amount": 600.0,
  "description": "Updated description",
  "date": "2026-01-29"
}
```

**All fields are optional** - only include fields you want to update.

**Response (200):**
```json
{
  "id": 1,
  "category": "Food",
  "amount": 600.0,
  "description": "Updated description",
  "date": "2026-01-29",
  "owner_id": 1
}
```

### 2.4 Delete Expense
**DELETE** `/api/expenses/{expense_id}`

Deletes an expense.

**Response (200):**
```json
{
  "message": "Expense deleted"
}
```

---

## 3. Budgets

### 3.1 Create Budget
**POST** `/api/budgets`

Creates a monthly budget for a category.

**Request Body:**
```json
{
  "category": "Food",
  "limit_amount": 5000.0,
  "month": 1,
  "year": 2026
}
```

**Response (200):**
```json
{
  "id": 1,
  "category": "Food",
  "limit_amount": 5000.0,
  "month": 1,
  "year": 2026,
  "owner_id": 1
}
```

### 3.2 List Budgets
**GET** `/api/budgets`

Returns all budgets for the authenticated user.

**Query Parameters:**
- `month` (optional): Filter by month (1-12)
- `year` (optional): Filter by year

**Response (200):**
```json
[
  {
    "id": 1,
    "category": "Food",
    "limit_amount": 5000.0,
    "month": 1,
    "year": 2026,
    "owner_id": 1
  }
]
```

### 3.3 Delete Budget
**DELETE** `/api/budgets/{budget_id}`

Deletes a budget.

**Response (200):**
```json
{
  "message": "Budget deleted"
}
```

---

## 4. Debts

### 4.1 Create Debt
**POST** `/api/debts`

Creates a debt/loan record.

**Request Body:**
```json
{
  "name": "Personal Loan",
  "principal_amount": 50000.0,
  "remaining_amount": 50000.0,
  "interest_rate": 10.5,
  "emi_amount": 5000.0,
  "emi_date": 5,
  "start_date": "2026-01-01",
  "status": "active"
}
```

**Fields:**
- `emi_date`: Day of month for EMI payment (1-31)
- `start_date`: Date string in format "YYYY-MM-DD" (required)
- `status`: Optional, defaults to "active"

**Response (200):**
```json
{
  "id": 1,
  "name": "Personal Loan",
  "principal_amount": 50000.0,
  "remaining_amount": 50000.0,
  "interest_rate": 10.5,
  "emi_amount": 5000.0,
  "emi_date": 5,
  "start_date": "2026-01-01",
  "status": "active",
  "owner_id": 1
}
```

### 4.2 List Debts
**GET** `/api/debts`

Returns all debts for the authenticated user.

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "Personal Loan",
    "principal_amount": 50000.0,
    "remaining_amount": 45000.0,
    "interest_rate": 10.5,
    "emi_amount": 5000.0,
    "emi_date": 5,
    "start_date": "2026-01-01",
    "status": "active",
    "owner_id": 1
  }
]
```

---

## 5. Friendships

### 5.1 Send Friend Request
**POST** `/api/friends/request`

Sends a friend request to another user.

**Request Body:**
```json
{
  "friend_username": "jane_doe"
}
```

**Response (200):**
```json
{
  "id": 1,
  "user_id": 1,
  "friend_id": 2,
  "status": "pending",
  "created_at": "2026-01-29T10:00:00"
}
```

**Note:** If friendship already exists, returns 200 with existing friendship and a message field.

### 5.2 List Friend Requests
**GET** `/api/friends/requests`

Returns pending friend requests for the authenticated user.

**Response (200):**
```json
[
  {
    "id": 1,
    "user_id": 2,
    "friend_id": 1,
    "status": "pending",
    "created_at": "2026-01-29T10:00:00"
  }
]
```

### 5.3 Accept Friend Request
**POST** `/api/friends/accept/{friendship_id}`

Accepts a pending friend request.

**Response (200):**
```json
{
  "id": 1,
  "user_id": 2,
  "friend_id": 1,
  "status": "accepted",
  "created_at": "2026-01-29T10:00:00"
}
```

### 5.4 Reject Friend Request
**POST** `/api/friends/reject/{friendship_id}`

Rejects a pending friend request.

**Response (200):**
```json
{
  "message": "Friend request rejected"
}
```

### 5.5 List Friends
**GET** `/api/friends`

Returns all accepted friends.

**Response (200):**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "friend_id": 2,
    "status": "accepted",
    "created_at": "2026-01-29T10:00:00"
  }
]
```

---

## 6. Split Expenses

### 6.1 Create Split Expense
**POST** `/api/split-expenses`

Creates an expense split between friends.

**Request Body:**
```json
{
  "description": "Dinner at restaurant",
  "total_amount": 1200.0,
  "category": "Food",
  "date": null,
  "participant_ids": [2, 3]
}
```

**Note:** 
- `participant_ids`: List of user IDs to split with (must be friends)
- Amount is automatically split equally among creator + participants
- `date` is optional, defaults to today

**Response (200):**
```json
{
  "id": 1,
  "description": "Dinner at restaurant",
  "total_amount": 1200.0,
  "category": "Food",
  "date": "2026-01-29",
  "created_by": 1,
  "created_at": "2026-01-29T10:00:00",
  "participants": [
    {
      "id": 1,
      "user_id": 1,
      "username": "john_doe",
      "share_amount": 400.0
    },
    {
      "id": 2,
      "user_id": 2,
      "username": "jane_doe",
      "share_amount": 400.0
    }
  ]
}
```

### 6.2 List Split Expenses
**GET** `/api/split-expenses`

Returns all split expenses for the authenticated user.

**Response (200):**
```json
[
  {
    "id": 1,
    "description": "Dinner",
    "total_amount": 1200.0,
    "category": "Food",
    "date": "2026-01-29",
    "created_by": 1,
    "created_at": "2026-01-29T10:00:00",
    "participants": [...]
  }
]
```

### 6.3 Get Balances
**GET** `/api/balances`

Returns balance summary with all friends.

**Response (200):**
```json
{
  "jane_doe": -400.0,
  "bob_smith": 200.0
}
```

**Interpretation:**
- Negative value: You owe them
- Positive value: They owe you

---

## 7. Groups

### 7.1 Create Group
**POST** `/api/groups`

Creates a new group.

**Request Body:**
```json
{
  "name": "Roommates",
  "description": "Apartment expenses",
  "currency": "INR",
  "image_url": null
}
```

**Response (201):**
```json
{
  "id": 1,
  "name": "Roommates",
  "description": "Apartment expenses",
  "currency": "INR",
  "image_url": null,
  "is_active": true,
  "created_by": 1,
  "created_at": "2026-01-29T10:00:00",
  "members": [
    {
      "id": 1,
      "user_id": 1,
      "username": "john_doe",
      "role": "admin",
      "status": "accepted",
      "joined_at": "2026-01-29T10:00:00"
    }
  ]
}
```

### 7.2 List Groups
**GET** `/api/groups`

Returns all groups for the authenticated user.

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "Roommates",
    "description": "Apartment expenses",
    "currency": "INR",
    "is_active": true,
    "created_by": 1,
    "created_at": "2026-01-29T10:00:00",
    "members": [...]
  }
]
```

### 7.3 Get Group Details
**GET** `/api/groups/{group_id}`

Returns detailed information about a specific group.

**Response (200):**
```json
{
  "id": 1,
  "name": "Roommates",
  "description": "Apartment expenses",
  "currency": "INR",
  "image_url": null,
  "is_active": true,
  "created_by": 1,
  "created_at": "2026-01-29T10:00:00",
  "members": [
    {
      "id": 1,
      "user_id": 1,
      "username": "john_doe",
      "role": "admin",
      "status": "accepted",
      "joined_at": "2026-01-29T10:00:00"
    }
  ]
}
```

### 7.4 Update Group
**PUT** `/api/groups/{group_id}`

Updates group information (admin only).

**Request Body:**
```json
{
  "name": "Updated Group Name",
  "description": "Updated description",
  "currency": "USD"
}
```

**All fields are optional.**

**Response (200):**
```json
{
  "id": 1,
  "name": "Updated Group Name",
  "description": "Updated description",
  "currency": "USD",
  "is_active": true,
  "created_by": 1,
  "created_at": "2026-01-29T10:00:00",
  "members": [...]
}
```

### 7.5 Invite Members to Group
**POST** `/api/groups/{group_id}/invite`

Invites friends to join the group.

**Request Body:**
```json
{
  "usernames": ["jane_doe", "bob_smith"]
}
```

**Requirements:**
- Users must be your friends
- Users cannot already be members
- Cannot invite yourself

**Response (200):**
```json
{
  "message": "Successfully invited 2 user(s)"
}
```

**Error Messages:**
```json
{
  "message": "Users not found: alice_smith. Not friends with: charlie_jones. Cannot invite yourself: john_doe"
}
```

### 7.6 Get Pending Group Invitations
**GET** `/api/groups/invitations/pending`

Returns all pending group invitations for the authenticated user.

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "Roommates",
    "description": "Apartment expenses",
    "currency": "INR",
    "is_active": true,
    "created_by": 2,
    "created_at": "2026-01-29T10:00:00",
    "members": [...]
  }
]
```

### 7.7 Join Group (Accept Invitation)
**POST** `/api/groups/{group_id}/join`

Accepts a group invitation.

**Response (200):**
```json
{
  "message": "Successfully joined group"
}
```

### 7.8 Leave Group
**POST** `/api/groups/{group_id}/leave`

Leaves a group. Admins cannot leave if there are other members.

**Response (200):**
```json
{
  "message": "Successfully left group"
}
```

### 7.9 Remove Member from Group
**DELETE** `/api/groups/{group_id}/members/{user_id}`

Removes a member from the group (admin only).

**Response (200):**
```json
{
  "message": "Member removed from group"
}
```

---

## 8. Group Expenses

### 8.1 Create Group Expense
**POST** `/api/groups/{group_id}/expenses`

Creates an expense for the group.

**Request Body:**
```json
{
  "description": "Grocery shopping",
  "total_amount": 2000.0,
  "category": "Groceries",
  "paid_by": 1,
  "participants": [
    {
      "user_id": 1,
      "share_amount": 1000.0
    },
    {
      "user_id": 2,
      "share_amount": 1000.0
    }
  ]
}
```

**Important Notes:**
- `date` field is **optional** - omit it entirely or set to `null` for today's date
- All other fields are **required**
- `paid_by`: Integer user ID of the member who paid
- `participants`: Must be a non-empty array
- Each participant object must have `user_id` (integer) and `share_amount` (number)
- All participants must be accepted group members
- `paid_by` user must be an accepted group member
- Sum of all `share_amount` values must equal `total_amount`

**Example with date:**
```json
{
  "description": "Grocery shopping",
  "total_amount": 2000.0,
  "category": "Groceries",
  "paid_by": 1,
  "participants": [
    {"user_id": 1, "share_amount": 1000.0},
    {"user_id": 2, "share_amount": 1000.0}
  ],
  "date": "2026-01-29"
}
```

**Requirements:**
- All participants must be accepted group members
- `paid_by` must be an accepted group member
- Sum of `share_amount` must equal `total_amount`
- At least one participant is required

**Response (201):**
```json
{
  "id": 1,
  "group_id": 1,
  "description": "Grocery shopping",
  "total_amount": 2000.0,
  "category": "Groceries",
  "date": "2026-01-29",
  "paid_by": 1,
  "created_at": "2026-01-29T10:00:00",
  "participants": [
    {
      "id": 1,
      "user_id": 1,
      "username": "john_doe",
      "share_amount": 1000.0
    },
    {
      "id": 2,
      "user_id": 2,
      "username": "jane_doe",
      "share_amount": 1000.0
    }
  ]
}
```

### 8.2 List Group Expenses
**GET** `/api/groups/{group_id}/expenses`

Returns all expenses for a group.

**Query Parameters:**
- `limit`: Maximum number of expenses to return (default: 100)

**Response (200):**
```json
[
  {
    "id": 1,
    "group_id": 1,
    "description": "Grocery shopping",
    "total_amount": 2000.0,
    "category": "Groceries",
    "date": "2026-01-29",
    "paid_by": 1,
    "created_at": "2026-01-29T10:00:00",
    "participants": [...]
  }
]
```

### 8.3 Update Group Expense
**PUT** `/api/groups/{group_id}/expenses/{expense_id}`

Updates a group expense (admin only).

**Request Body:**
```json
{
  "description": "Updated description",
  "total_amount": 2500.0,
  "category": "Food",
  "participants": [
    {
      "user_id": 1,
      "share_amount": 1250.0
    },
    {
      "user_id": 2,
      "share_amount": 1250.0
    }
  ]
}
```

**All fields are optional.**

**Response (200):**
```json
{
  "id": 1,
  "group_id": 1,
  "description": "Updated description",
  "total_amount": 2500.0,
  "category": "Food",
  "date": "2026-01-29",
  "paid_by": 1,
  "created_at": "2026-01-29T10:00:00",
  "participants": [...]
}
```

### 8.4 Delete Group Expense
**DELETE** `/api/groups/{group_id}/expenses/{expense_id}`

Deletes a group expense (admin only).

**Response (200):**
```json
{
  "message": "Expense deleted"
}
```

---

## 9. Group Balances & Settlements

### 9.1 Get Group Balances
**GET** `/api/groups/{group_id}/balances`

Returns balance information for all group members.

**Response (200):**
```json
{
  "balances": [
    {
      "user_id": 1,
      "username": "john_doe",
      "balance": 500.0
    },
    {
      "user_id": 2,
      "username": "jane_doe",
      "balance": -500.0
    }
  ],
  "total_expenses": 5000.0
}
```

**Balance Interpretation:**
- Positive: Member is owed this amount
- Negative: Member owes this amount

### 9.2 Get Settlement Suggestions
**GET** `/api/groups/{group_id}/settlements/suggestions`

Returns optimized settlement suggestions to minimize transactions.

**Response (200):**
```json
{
  "settlements": [
    {
      "from_user_id": 2,
      "from_username": "jane_doe",
      "to_user_id": 1,
      "to_username": "john_doe",
      "amount": 500.0
    }
  ],
  "total_settlements": 1
}
```

### 9.3 Record Settlement
**POST** `/api/groups/{group_id}/settlements`

Records a settlement transaction between members.

**Request Body:**
```json
{
  "to_user_id": 1,
  "amount": 500.0
}
```

**Note:** The authenticated user is automatically set as the payer (`from_user_id`).

**Response (201):**
```json
{
  "id": 1,
  "group_id": 1,
  "from_user_id": 2,
  "to_user_id": 1,
  "amount": 500.0,
  "created_at": "2026-01-29T10:00:00"
}
```

### 9.4 List Settlements
**GET** `/api/groups/{group_id}/settlements`

Returns all settlement records for a group.

**Response (200):**
```json
[
  {
    "id": 1,
    "group_id": 1,
    "from_user_id": 2,
    "to_user_id": 1,
    "amount": 500.0,
    "created_at": "2026-01-29T10:00:00"
  }
]
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Error message describing what went wrong"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Only group admins can perform this action"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "field_name"],
      "msg": "Field required",
      "input": {...}
    }
  ]
}
```

---

## Common Validation Rules

### Username
- Required for registration
- Must be unique
- Case-insensitive for lookups

### Email
- Required for registration
- Must be valid email format
- Must be unique

### Amounts
- Must be positive numbers
- Floating point values accepted
- For group expenses, participant shares must sum to total

### Dates
- Optional in most cases, defaults to today
- Format: "YYYY-MM-DD" or ISO 8601
- Can also be null/omitted

### Group Membership
- Must be accepted member to access group resources
- Pending invitations don't grant access
- Admins have additional privileges (update, delete, remove members)

### Friendships
- Required for split expenses
- Required for group invitations
- Both users must have accepted friendship status

---

## Interactive API Documentation

The backend provides interactive API documentation at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Use these for testing endpoints directly from your browser!
