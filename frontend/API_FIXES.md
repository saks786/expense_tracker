# API Fixes Applied

## Summary of Changes

All API calls have been updated to properly handle errors and display toast notifications. The main issues causing 422 errors were:

### 1. Missing Required Fields

#### Debts API
- **Fixed**: Added `remaining_amount` field (required by backend, was missing in DebtForm)
- **Fixed**: Added `status` field with default value "active"
- **Fixed**: Ensured `start_date` is in "YYYY-MM-DD" format

#### Expenses API
- **Fixed**: Properly handle optional `date` and `description` fields
- **Fixed**: Convert amounts to `parseFloat()` to ensure numeric type

#### Split Expenses API
- **Fixed**: Ensure `participant_ids` is an array of numbers
- **Fixed**: Convert `total_amount` to float

#### Group Expenses API
- **Fixed**: Ensure `participants` array has proper structure with `user_id` and `share_amount`
- **Fixed**: Validate that sum of shares equals total_amount
- **Fixed**: Ensure `paid_by` is a valid user_id

### 2. Wrong HTTP Methods

#### Friends API
- **Fixed**: Changed friend request accept from `PUT /api/friends/{id}/accept` to `POST /api/friends/accept/{id}`
- **Added**: Friend request reject endpoint `POST /api/friends/reject/{id}`

### 3. Improved Error Handling

Created a centralized `handleResponse()` function that:
- Parses FastAPI validation errors (422 responses)
- Extracts field-level error messages
- Handles both array and string error formats
- Provides clear, user-friendly error messages

### 4. Toast Notifications

All components now use toast notifications instead of:
- Alert dialogs
- Console errors
- Inline error messages (where appropriate)

Toast types used:
- `toast.success()` - For successful operations
- `toast.error()` - For errors with detailed messages
- `toast.loading()` - For long-running operations (where applicable)

## Components Updated

### With Toast Notifications (from previous work)
- ✅ Login.jsx
- ✅ Register.jsx
- ✅ ExpenseForm.jsx
- ✅ ExpenseList.jsx
- ✅ SplitExpenseForm.jsx
- ✅ SplitExpenseList.jsx
- ✅ GroupList.jsx
- ✅ GroupDashboard.jsx
- ✅ FriendList.jsx
- ✅ App.jsx

### Updated This Session
- ✅ DebtForm.jsx - Added missing `remaining_amount` field + toast notifications

## API Payload Format Reference

### Creating a Debt
```json
{
  "name": "Personal Loan",
  "principal_amount": 50000.0,
  "remaining_amount": 50000.0,
  "interest_rate": 10.5,
  "emi_amount": 5000.0,
  "emi_date": 5,
  "start_date": "2026-01-29",
  "status": "active"
}
```

### Creating an Expense
```json
{
  "category": "Food",
  "amount": 500.0,
  "description": "Lunch",  // optional
  "date": "2026-01-29"      // optional, defaults to today
}
```

### Creating a Split Expense
```json
{
  "description": "Dinner",
  "total_amount": 1200.0,
  "category": "Food",
  "participant_ids": [2, 3],  // Array of user IDs
  "date": null                 // optional
}
```

### Creating a Group Expense
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
  ],
  "date": null  // optional
}
```

### Inviting Group Members
```json
{
  "usernames": ["jane_doe", "bob_smith"]  // Array of usernames
}
```

### Recording Settlement
```json
{
  "from_user_id": 2,
  "to_user_id": 1,
  "amount": 500.0,
  "payment_method": "Cash",  // optional
  "notes": "Paid via cash"   // optional
}
```

## Testing Checklist

### Authentication
- [ ] Register new user with valid credentials
- [ ] Register with existing username/email (should show error)
- [ ] Login with valid credentials
- [ ] Login with invalid credentials (should show error)

### Expenses
- [ ] Create expense with all fields
- [ ] Create expense without description
- [ ] Create expense without date (should default to today)
- [ ] Update expense
- [ ] Delete expense

### Debts
- [ ] Create debt with all required fields
- [ ] Create debt with invalid emi_date (should show validation error)
- [ ] Update debt remaining_amount
- [ ] Delete debt

### Friends
- [ ] Send friend request to existing user
- [ ] Send friend request to non-existent user (should show error)
- [ ] Accept friend request
- [ ] Reject friend request
- [ ] Remove friend

### Split Expenses
- [ ] Create split expense with friends
- [ ] Create split expense with non-friends (should show error)
- [ ] View balances
- [ ] Delete split expense

### Groups
- [ ] Create group with name only
- [ ] Create group with all optional fields
- [ ] Invite friends to group
- [ ] Invite non-friends (should show error)
- [ ] Join group (accept invitation)
- [ ] Leave group
- [ ] Remove member (admin only)

### Group Expenses
- [ ] Create group expense with equal split
- [ ] Create group expense with custom splits
- [ ] Create expense with invalid participant (should show error)
- [ ] Create expense where shares don't sum to total (should show error)
- [ ] Update group expense
- [ ] Delete group expense

### Settlements
- [ ] View group balances
- [ ] Get settlement suggestions
- [ ] Record settlement
- [ ] View settlement history

## Common Error Messages

### 422 Validation Errors
These now show detailed field-level errors:
- "category: Field required"
- "amount: Input should be a valid number"
- "participant_ids: Field required"
- "share_amount: Input should be greater than 0"

### 400 Bad Request
- "Users not found: username"
- "Not friends with: username"
- "Participant shares must sum to total amount"

### 401 Unauthorized
- "Could not validate credentials"
- "Invalid credentials"

### 403 Forbidden
- "Only group admins can perform this action"
- "Admins cannot leave group with other members"

### 404 Not Found
- "Resource not found"
- "User not found"
- "Group not found"

## Next Steps

1. **Test all endpoints** using the frontend UI
2. **Check browser console** for any remaining errors
3. **Verify toast notifications** appear for all operations
4. **Test edge cases** like empty fields, invalid data, unauthorized access
5. **Monitor backend logs** for any server-side errors

## Development Server

To test the changes:
```bash
# Start frontend
npm run dev

# Start backend (in separate terminal)
# Make sure backend is running on http://localhost:8000
```

Visit: http://localhost:5173
