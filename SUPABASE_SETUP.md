# Supabase Integration Setup Guide

## ✅ Completed Steps

### Backend Configuration
- ✅ Installed Supabase Python client (`supabase`, `psycopg2-binary`)
- ✅ Created `.env` file with Supabase credentials
- ✅ Configured database URL for Supabase PostgreSQL
- ✅ Created `app/supabase_client.py` for Supabase Python client

### Frontend Configuration
- ✅ Installed `@supabase/supabase-js` package
- ✅ Created `frontend/.env` with Supabase configuration
- ✅ Created `src/supabaseClient.js` for Supabase client initialization
- ✅ Configured authentication and real-time features

### Database Migration
- ✅ Created `supabase_migration.sql` with all table schemas
- ✅ Includes Row Level Security (RLS) policies
- ✅ Added performance indexes

---

## 🔧 Required Actions

### Step 1: Create Database Tables in Supabase

**IMPORTANT:** You must run the SQL migration script to create all tables!

1. Go to **Supabase Dashboard**: https://supabase.com/dashboard/project/hhncftvcjkqtpjsohksi
2. Click **SQL Editor** in the left sidebar
3. Click **"New Query"**
4. Open `backend/supabase_migration.sql` in a text editor
5. **Copy the entire SQL script**
6. Paste it into the Supabase SQL Editor
7. Click **"Run"** (or press Ctrl+Enter)
8. Verify success message appears

**Expected Output:**
```
✅ Database migration completed successfully!
📋 All tables, indexes, and RLS policies have been created.
```

### Step 2: Verify Tables Were Created

1. In Supabase Dashboard, click **Table Editor**
2. You should see these tables:
   - `users`
   - `expenses`
   - `budgets`
   - `debts`
   - `friendships`
   - `split_expenses`
   - `split_participants`
   - `settlements`
   - `transactions`

---

## 📋 What Was Configured

### Environment Variables

**Backend** (`.env`):
```env
SUPABASE_URL=https://hhncftvcjkqtpjsohksi.supabase.co
SUPABASE_ANON_KEY=sb_publishable_uqBGzTgotx-rKo2JHAQurg_Z5jxaTDb
SUPABASE_SERVICE_ROLE_KEY=sb_secret_vP26rjhdGeMQAlO29EYOoQ_XxZxKaNP
DATABASE_URL=postgresql://postgres:HArsh%401905%23%40@db.hhncftvcjkqtpjsohksi.supabase.co:5432/postgres
```

**Frontend** (`.env`):
```env
VITE_SUPABASE_URL=https://hhncftvcjkqtpjsohksi.supabase.co
VITE_SUPABASE_ANON_KEY=sb_publishable_uqBGzTgotx-rKo2JHAQurg_Z5jxaTDb
```

### Key Features Enabled

1. **PostgreSQL Database**: Cloud-hosted, scalable database
2. **Authentication System**: Built-in user authentication (ready to implement)
3. **Real-time Subscriptions**: Live data updates across clients
4. **Row Level Security (RLS)**: User-based data access control
5. **REST API**: Automatic API generation from database schema

---

## 🚀 Next Steps

### Option 1: Keep Current Backend (FastAPI + SQLAlchemy)
Continue using your existing FastAPI backend with Supabase as the database.

**Pros:**
- Minimal code changes
- Keep all existing logic
- Gradual migration path

**Cons:**
- PostgreSQL connection issues on some networks (IPv6)
- Not using Supabase's built-in features fully

**To Use:**
- Tables created ✅
- Backend will connect to Supabase PostgreSQL
- May need to troubleshoot network/DNS issues

### Option 2: Migrate to Supabase Auth + Postgrest (Recommended)
Use Supabase's built-in authentication and auto-generated REST API.

**Pros:**
- Better reliability (no PostgreSQL connection issues)
- Built-in auth (email/password, social logins)
- Real-time out of the box
- Reduced backend code

**Cons:**
- Need to refactor auth endpoints
- Learning curve for Supabase APIs

**To Implement:**
I can help you:
1. Replace JWT auth with Supabase Auth
2. Update API calls to use Supabase REST API
3. Enable real-time for friends/expenses

---

## 🧪 Testing Supabase Connection

### Test Frontend Connection

Create a test file: `frontend/src/testSupabase.js`
```javascript
import { supabase } from './supabaseClient.js'

// Test connection
async function testConnection() {
  const { data, error } = await supabase.from('users').select('count')

  if (error) {
    console.error('❌ Connection failed:', error.message)
  } else {
    console.log('✅ Supabase connected!', data)
  }
}

testConnection()
```

### Test Backend Connection

Run in backend directory:
```bash
python -c "from app.supabase_client import get_supabase; print(get_supabase())"
```

Expected output:
```
✅ Supabase client initialized successfully
<supabase._sync.client.Client object at 0x...>
```

---

## 🛠️ Troubleshooting

### Issue: "could not translate host name" Error

**Cause:** Windows DNS/IPv6 resolution issue with direct PostgreSQL connection

**Solutions:**
1. **Use Supabase REST API** (recommended)
   - Already configured in `app/supabase_client.py`
   - More reliable than direct PostgreSQL

2. **Enable IPv4 Connection Pooling**
   - In Supabase Dashboard → Settings → Database
   - Use "Connection Pooling" URL instead
   - Mode: "Transaction" for better compatibility

3. **Add to hosts file** (Windows)
   - Edit `C:\Windows\System32\drivers\etc\hosts`
   - Add: `<IP_ADDRESS> db.hhncftvcjkqtpjsohksi.supabase.co`
   - Get IP: `nslookup db.hhncftvcjkqtpjsohksi.supabase.co`

### Issue: RLS Policies Block Access

**Cause:** Row Level Security is enabled but policies aren't matching

**Solution:**
- Disable RLS temporarily for testing:
  ```sql
  ALTER TABLE users DISABLE ROW LEVEL SECURITY;
  ```
- Or use service role key in backend (bypasses RLS)

---

## 📚 Resources

- **Supabase Documentation**: https://supabase.com/docs
- **Python Client Docs**: https://supabase.com/docs/reference/python/introduction
- **JavaScript Client Docs**: https://supabase.com/docs/reference/javascript/introduction
- **Your Project Dashboard**: https://supabase.com/dashboard/project/hhncftvcjkqtpjsohksi

---

## ✨ What You Can Do Next

Once tables are created, you have these options:

### A. Test Existing Backend with Supabase DB
```bash
cd backend
python -m uvicorn app.main:app --reload
```
Then test endpoints as usual.

### B. Migrate to Full Supabase Stack
I can help you:
- Replace auth system with Supabase Auth
- Use Supabase client instead of SQLAlchemy
- Enable real-time features for live updates
- Set up social login (Google, GitHub, etc.)

### C. Create Mock Data in Supabase
Run your existing mock data endpoint:
```bash
curl -X POST http://localhost:8000/api/create-mock-data
```

This will populate Supabase with test data!

---

## 🤝 Need Help?

**Common next steps:**
1. ✅ Run the SQL migration script (MUST DO FIRST)
2. Test backend connection
3. Test frontend connection
4. Decide: Keep FastAPI or migrate to Supabase APIs
5. Enable real-time features

Let me know which path you want to take!
