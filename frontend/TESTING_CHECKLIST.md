# API Testing Checklist

Use this checklist to systematically test all API endpoints after the fixes.

## ✅ Setup
- [ ] Backend server running on http://localhost:8000
- [ ] Frontend server running on http://localhost:5173
- [ ] Browser DevTools open (F12) → Network tab visible
- [ ] No errors in Console tab

---

## 🔐 Authentication

### Registration
- [ ] Register with valid data → Should succeed with success toast
- [ ] Register with existing username → Should show error toast
- [ ] Register with existing email → Should show error toast
- [ ] Register with invalid email format → Should show validation error

### Login
- [ ] Login with valid credentials → Should succeed and redirect to dashboard
- [ ] Login with wrong password → Should show "Invalid credentials" error
- [ ] Login with non-existent username → Should show "Invalid credentials" error

---

## 💰 Personal Expenses

### Create
- [ ] Add expense with all fields filled → Success toast
- [ ] Add expense without description → Should work (optional field)
- [ ] Add expense without date → Should work (defaults to today)
- [ ] Add expense with $0 amount → Should show validation error
- [ ] Add expense with negative amount → Should show validation error

### Update
- [ ] Edit existing expense → Success toast
- [ ] Update only amount → Should work (other fields unchanged)
- [ ] Update only description → Should work

### Delete
- [ ] Delete expense → Success toast
- [ ] Verify expense removed from list

---

## 💳 Debts

### Create (THIS WAS FIXED!)
- [ ] Add debt with all fields → Success toast (was giving 422 before)
- [ ] Add debt with EMI date > 31 → Should clamp to 31
- [ ] Add debt with EMI date < 1 → Should clamp to 1
- [ ] Add debt with negative amount → Validation error
- [ ] Add debt without name → Validation error

### Update
- [ ] Update remaining amount → Success toast
- [ ] Update EMI amount → Success toast

### Delete
- [ ] Delete debt → Success toast

---

## 👥 Friends

### Send Request
- [ ] Send request to existing user → Success toast
- [ ] Send request to non-existent user → Error toast
- [ ] Send request to existing friend → Should show appropriate message

### Manage Requests (FIXED!)
- [ ] Accept friend request → Success toast (method changed to POST)
- [ ] Reject friend request → Success toast (newly added endpoint)
- [ ] View pending requests → Should list all pending

### Remove
- [ ] Remove friend → Success toast
- [ ] Verify friend removed from list

---

## 🤝 Split Expenses

### Create
- [ ] Create split with 1 friend → Success toast, equal split
- [ ] Create split with multiple friends → Success toast, equal split
- [ ] Create split with non-friend → Error toast "Not friends with: username"
- [ ] Create split without selecting friends → Validation error
- [ ] Create split with $0 amount → Validation error

### View
- [ ] View all split expenses → Should list all
- [ ] View balances → Should show who owes whom

### Delete
- [ ] Delete split expense → Success toast

---

## 👨‍👩‍👧‍👦 Groups

### Create
- [ ] Create group with name only → Success toast
- [ ] Create group with all fields → Success toast
- [ ] Create group without name → Validation error

### Invite Members
- [ ] Invite friend to group → Success toast
- [ ] Invite non-friend → Error "Not friends with: username"
- [ ] Invite non-existent user → Error "Users not found: username"
- [ ] Invite yourself → Error "Cannot invite yourself"

### Manage
- [ ] Accept group invitation → Success toast
- [ ] Leave group (non-admin) → Success toast
- [ ] Leave group (admin with members) → Error toast
- [ ] Remove member (admin) → Success toast
- [ ] Remove member (non-admin) → Error "Only admins can..."

---

## 💸 Group Expenses

### Create (CRITICAL - Was causing 422 errors)
- [ ] Create expense with equal split → Success toast
- [ ] Create expense with custom splits (shares sum to total) → Success toast
- [ ] Create expense where shares ≠ total → Error "shares must sum to total"
- [ ] Create expense with non-member participant → Error
- [ ] Create expense with invalid paid_by → Error

### Update
- [ ] Update description → Success toast
- [ ] Update amount and recalculate splits → Success toast
- [ ] Update splits → Success toast

### Delete
- [ ] Delete group expense → Success toast

---

## 💱 Settlements

### View
- [ ] View group balances → Should show balance for each member
- [ ] Get settlement suggestions → Should show optimized payment plan

### Record
- [ ] Record settlement with all fields → Success toast
- [ ] Record settlement without payment method → Should work (optional)
- [ ] Record settlement without notes → Should work (optional)
- [ ] Record settlement with amount > owed → Should work (backend validates)

### History
- [ ] View settlement history → Should list all settlements

---

## 🔍 What to Check For

### In Browser Network Tab:
- ✅ All requests should return 200/201 status codes (success)
- ❌ No 422 errors (validation errors - these were fixed!)
- ❌ No 500 errors (server errors)

### In Console Tab:
- ✅ No red error messages
- ✅ No warnings about missing fields
- ⚠️ Optional: You might see some React warnings (not critical)

### In UI:
- ✅ Toast notifications appear for ALL operations
- ✅ Success toasts are green/checkmark
- ✅ Error toasts are red/x
- ✅ Toast messages are clear and descriptive
- ✅ Forms clear after successful submission
- ✅ Lists refresh after add/update/delete operations

---

## 🐛 Common Issues & Solutions

### "Port already in use"
```bash
# Find and kill process
netstat -ano | findstr :5173
taskkill /PID <process_id> /F
```

### "Could not validate credentials"
- Token expired → Logout and login again
- Backend not running → Start backend server

### "Failed to fetch"
- Backend not running → Start backend server
- CORS error → Check backend CORS configuration

### Still getting 422 errors?
1. Check Network tab → Request payload
2. Compare with API documentation
3. Verify all required fields are present
4. Check data types (numbers vs strings)

---

## 📊 Testing Score

Count your successful tests:

- Total Tests: ~50
- Passed: _____ / 50
- Failed: _____ / 50

Goal: All tests should pass! 🎯

---

## 💡 Tips

1. **Test in order**: Complete Authentication before testing other features
2. **Use DevTools**: Network tab shows exact request/response
3. **Read error messages**: Toast messages now show detailed errors
4. **Test edge cases**: Empty fields, invalid data, unauthorized actions
5. **Check backend logs**: May show additional error details

---

## 🎉 Success Criteria

Your API is working perfectly when:
- ✅ All forms submit without errors
- ✅ All toast notifications are meaningful
- ✅ No 422 errors in Network tab
- ✅ Data persists after page refresh
- ✅ Error messages guide users to fix issues

Good luck testing! 🚀
