# Complete Testing Guide - Supabase Integration

## 🎯 What We've Accomplished

✅ **Backend:**
- Supabase Python client installed
- Environment configured with Supabase credentials
- Mock data created in Supabase (3 users, 20 expenses, friendships, etc.)

✅ **Frontend:**
- Supabase JavaScript client installed
- Real-time subscriptions added to FriendList component
- Auto-refresh when friendships change

✅ **Database:**
- All 9 tables created in Supabase PostgreSQL
- Row Level Security (RLS) policies configured
- Performance indexes added
- **31 total records** created across all tables

---

## 🧪 Testing Steps

### Step 1: Enable Real-time (REQUIRED)

Before testing, you **MUST** enable real-time for the friendships table:

1. Go to: https://supabase.com/dashboard/project/hhncftvcjkqtpjsohksi
2. Click **SQL Editor**
3. Run this SQL:

```sql
-- Enable real-time for friendships table
ALTER PUBLICATION supabase_realtime ADD TABLE friendships;

-- Verify
SELECT * FROM pg_publication_tables WHERE pubname = 'supabase_realtime';
```

You should see `friendships` in the output.

---

### Step 2: Start the Backend

**Option A: Using SQLite (Current Setup)**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

The backend will use SQLite (dev.db) by default if Supabase PostgreSQL connection fails due to network issues.

**Option B: Force Supabase Connection (If PostgreSQL works)**
- Backend is already configured to use Supabase
- Check logs for "Connected to PostgreSQL" message

---

### Step 3: Start the Frontend

```bash
cd frontend
npm run dev
```

Frontend should start on http://localhost:5173

---

### Step 4: Test Basic Login

**Login Credentials:**
- Username: `testuser1`, `testuser2`, or `testuser3`
- Password: `password123`

1. Open http://localhost:5173
2. Login as `testuser1`
3. Navigate to Friends section

**Expected:**
- See `testuser2` in friends list (accepted)
- See pending request to `testuser3` (if using Supabase data)

---

### Step 5: Test Real-time Updates

This tests if changes appear automatically without page refresh!

#### Test Setup:
1. **Open TWO browser tabs** (or use Incognito mode for second tab)
2. **Tab 1:** Login as `testuser1`
3. **Tab 2:** Login as `testuser2`

#### Test Case 1: Send Friend Request
1. **Tab 1:** Navigate to Friends
2. **Tab 1:** Send friend request to `testuser3`
3. **Tab 2:** Navigate to Friends → Requests tab
4. **Expected:** Request appears AUTOMATICALLY without refresh! 🎉

#### Test Case 2: Accept Friend Request
1. **Tab 2:** Accept the request from `testuser1`
2. **Tab 1:** Check Friends tab
3. **Expected:** New friend appears AUTOMATICALLY! 🎉

#### Test Case 3: Remove Friend
1. **Tab 1:** Remove a friend
2. **Tab 2:** Check Friends tab
3. **Expected:** Friend disappears AUTOMATICALLY! 🎉

---

### Step 6: Check Console Logs

Open browser DevTools (F12) and check Console:

**Expected Logs:**
```
✅ Supabase client initialized: https://hhncftvcjkqtpjsohksi.supabase.co
🔄 Setting up real-time subscription for friendships...
✅ Real-time subscription active for friendships!
```

**When changes occur:**
```
🔔 Real-time update received: {eventType: "INSERT", new: {...}}
➕ New friendship created
```

---

## 🔍 Troubleshooting

### Issue 1: Real-time Not Working

**Symptoms:** Changes don't appear automatically

**Solutions:**
1. **Enable real-time** (Step 1 above) - MOST COMMON ISSUE
2. Check browser console for errors
3. Verify Supabase client initialized (see console logs)
4. Check WebSocket connection:
   - Open DevTools → Network → WS tab
   - Look for `supabase.co/realtime` connection
   - Should show "101 Switching Protocols"

### Issue 2: Backend Using SQLite Instead of Supabase

**Symptoms:** Backend works, but real-time doesn't sync with backend changes

**Check:**
```bash
# In backend directory
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('DATABASE_URL'))"
```

Should output: `postgresql://postgres:...@db.hhncftvcjkqtpjsohksi.supabase.co:5432/postgres`

**If Backend Can't Connect to Supabase PostgreSQL:**

This is common on Windows due to IPv6/DNS issues. You have 3 options:

**Option 1: Use Supabase Connection Pooler** (Recommended)
1. Go to: Database Settings → Connection String
2. Copy the "Connection Pooling" URL (Transaction mode)
3. Update `DATABASE_URL` in `.env` with the pooler URL
4. Restart backend

**Option 2: Hybrid Approach**
- Development: Use SQLite (dev.db) locally
- Production: Deploy with Supabase PostgreSQL
- Real-time will work when backend writes to Supabase in production

**Option 3: Use Supabase REST API**
- Replace SQLAlchemy with Supabase Python client
- All database operations go through Supabase REST API
- More reliable but requires code refactoring

### Issue 3: "Could Not Validate Credentials"

**Solution:** Token expired. Login again to get new token.

---

## 📊 Verify Mock Data

Check if mock data exists in Supabase:

### Via Supabase Dashboard:
1. Go to: Table Editor
2. Click on `users` table
3. Should see 3 users (testuser1, testuser2, testuser3)

### Via Backend API:
```bash
# Login
curl -X POST http://localhost:8000/api/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser1&password=password123"

# Get expenses (using token from above)
curl http://localhost:8000/api/expenses \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Via Python Script:
```bash
cd backend
python test_supabase_api.py
```

Should show record counts for all tables.

---

## 🎮 Demo Scenario

**Perfect Demo Flow:**

1. **Preparation:**
   - Enable real-time (SQL command)
   - Start backend
   - Start frontend
   - Open 2 browser tabs

2. **Tab 1 (testuser1):**
   - Login
   - Go to Friends
   - See existing friend (testuser2)
   - Open DevTools console

3. **Tab 2 (testuser3):**
   - Login (separate tab/incognito)
   - Go to Friends → Requests tab
   - Wait for magic...

4. **Tab 1:**
   - Send friend request to testuser3
   - Watch console logs

5. **Tab 2:**
   - **BOOM! 💥** Request appears automatically!
   - Console shows: "🔔 Real-time update received"
   - Accept the request

6. **Tab 1:**
   - **BOOM AGAIN! 💥** testuser3 appears in friends!
   - All without clicking refresh!

---

## 📈 Performance Check

Real-time updates should be:
- **Fast:** < 500ms latency
- **Reliable:** 100% of changes detected
- **Efficient:** Minimal network usage

**Monitor in DevTools:**
- Network → WS tab → Check message sizes
- Console → Check for duplicate subscriptions
- Performance → Check for memory leaks

---

## 🚀 Next Steps

Once real-time works for friends, you can enable it for:

1. **Expenses** - See new expenses added by friends
2. **Split Expenses** - Live updates when friends split bills
3. **Balances** - Real-time balance calculations
4. **Notifications** - Toast notifications for real-time events

**To Add Real-time to Other Tables:**
```sql
-- Enable for more tables
ALTER PUBLICATION supabase_realtime ADD TABLE expenses;
ALTER PUBLICATION supabase_realtime ADD TABLE split_expenses;
ALTER PUBLICATION supabase_realtime ADD TABLE settlements;
```

Then add subscriptions in frontend components (same pattern as FriendList).

---

## 📚 Resources

- **Your Supabase Dashboard**: https://supabase.com/dashboard/project/hhncftvcjkqtpjsohksi
- **Real-time Docs**: https://supabase.com/docs/guides/realtime
- **Python Client Docs**: https://supabase.com/docs/reference/python/introduction
- **JavaScript Client Docs**: https://supabase.com/docs/reference/javascript/introduction

---

## ✅ Success Checklist

- [ ] Real-time enabled for friendships table (SQL command)
- [ ] Backend running (port 8000)
- [ ] Frontend running (port 5173)
- [ ] Logged in as testuser1
- [ ] Console shows "Real-time subscription active"
- [ ] Tested with 2 browser tabs
- [ ] Changes appear automatically without refresh
- [ ] Console logs show real-time events

**If all checked = SUCCESS! 🎉**

---

## 💡 Pro Tips

1. **Use Browser DevTools:** Console logs are your friend!
2. **Test in Incognito:** Easier to test with multiple users
3. **Watch Network Tab:** See WebSocket messages in real-time
4. **Check Supabase Logs:** Dashboard → Logs → Realtime logs
5. **Read Console Messages:** They tell you exactly what's happening

---

Need help? Check:
- `SUPABASE_SETUP.md` - Initial setup guide
- `ENABLE_REALTIME.md` - Real-time specific instructions
- Console logs - They're very descriptive!
