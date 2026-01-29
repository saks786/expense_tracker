# Group Expense Payload Format

## ✅ What Your Frontend Now Sends

When you add a group expense, the frontend will send this exact format:

### Equal Split Example (2 participants, ₹2000 total)
```json
{
  "description": "Groceries",
  "total_amount": 2000.0,
  "category": "Food",
  "paid_by": 1,
  "participants": [
    {"user_id": 1, "share_amount": 1000.0},
    {"user_id": 2, "share_amount": 1000.0}
  ],
  "date": "2026-01-29"
}
```

### Custom Split Example (3 participants, ₹3000 total)
```json
{
  "description": "Dinner",
  "total_amount": 3000.0,
  "category": "Food",
  "paid_by": 1,
  "participants": [
    {"user_id": 1, "share_amount": 1500.0},
    {"user_id": 2, "share_amount": 1000.0},
    {"user_id": 3, "share_amount": 500.0}
  ],
  "date": "2026-01-29"
}
```

## 🔧 Changes Made

### 1. GroupDashboard.jsx - AddGroupExpenseModal
**Fixed**: Equal split now calculates and includes `share_amount` for each participant

**Before** (was causing 422 errors):
```javascript
participants: formData.participants.map(id => ({ 
  user_id: parseInt(id) 
  // ❌ Missing share_amount!
}))
```

**After** (now works):
```javascript
participants: formData.participants.map(id => ({ 
  user_id: parseInt(id),
  share_amount: parseFloat((totalAmount / participantCount).toFixed(2))
  // ✅ Always includes share_amount
}))
```

### 2. Added Validation
- ✅ Ensures at least one participant is selected
- ✅ Validates custom splits sum to total amount
- ✅ Shows clear toast error messages

### 3. Payload Cleanup
- ✅ Only sends required fields to API
- ✅ Removes UI-only fields (split_method, custom_splits)
- ✅ Properly formats all numeric values

## 🧪 How to Test

1. **Create Equal Split Expense**:
   - Open a group
   - Click "Add Expense"
   - Enter description: "Groceries"
   - Enter amount: 2000
   - Select category: "Food"
   - Who paid: Select yourself
   - Select split method: "Equal"
   - Check at least one participant
   - Submit

2. **Verify in Network Tab**:
   - Open DevTools → Network
   - Filter: `expenses`
   - Look for POST request
   - Check "Payload" tab
   - Should see: All participants have `user_id` AND `share_amount`

3. **Expected Result**:
   - ✅ Green success toast: "Expense added successfully!"
   - ✅ Status 201 Created
   - ✅ Expense appears in group expense list
   - ❌ No 422 errors

## 📊 Validation Rules

The frontend now enforces:

1. **Participants**: At least 1 required
2. **Share Amounts**: 
   - Equal split: Auto-calculated as total ÷ participant count
   - Custom split: Must sum exactly to total amount
3. **All Fields**:
   - description: Required string
   - total_amount: Required positive number
   - category: Required string
   - paid_by: Required user_id (integer)
   - participants: Required array (min 1 item)
   - date: Optional, defaults to today

## 🎯 What This Fixes

- ❌ **Before**: 422 error "participants: Field required" or "share_amount: Field required"
- ✅ **After**: All fields properly formatted, no validation errors

## 💡 Notes

- The person who paid (paid_by) does NOT need to be in participants list
- Participants can be any accepted group members
- Share amounts are rounded to 2 decimal places
- Sum validation allows 0.01 tolerance for rounding differences

Your group expenses should now work perfectly! 🎉
