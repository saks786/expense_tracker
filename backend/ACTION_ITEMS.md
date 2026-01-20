# 🎯 Post-Migration Action Items

## Required Actions (You Must Do These)

### 1. ⚙️ Configure Environment Variables

**Choose One Method:**

#### Method A: Interactive Setup (Easiest) ✅
```powershell
python setup_migration.py
```
- Follow the wizard prompts
- Enter your Supabase credentials
- Auto-generates secure SECRET_KEY
- Creates .env file automatically

#### Method B: Manual Setup
```powershell
# Copy example file
Copy-Item .env.example .env

# Edit .env and update these values:
# - DATABASE_URL (from Supabase: Settings → Database → Connection String)
# - SUPABASE_URL (from Supabase: Settings → API → Project URL)
# - SUPABASE_KEY (from Supabase: Settings → API → anon/public key)
# - SECRET_KEY (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
```

---

### 2. 🗄️ Run Database Migration

1. **Open Supabase Dashboard**
   - Go to https://supabase.com/dashboard
   - Select your project

2. **Open SQL Editor**
   - Click "SQL Editor" in left sidebar
   - Click "New query"

3. **Run Migration Script**
   - Open `supabase_migration.sql` in your text editor
   - Copy ALL contents (203 lines)
   - Paste into Supabase SQL Editor
   - Click "Run" button

4. **Verify Success**
   - You should see: `✅ Database migration completed successfully!`
   - Check "Table Editor" to see all 9 tables

---

### 3. 📦 Install Dependencies

```powershell
pip install -r requirements.txt
```

**New packages added:**
- `supabase` - Supabase Python SDK
- `colorama` - Colored terminal output for test script

**Existing packages:**
- `fastapi`, `uvicorn`, `sqlalchemy`, `psycopg2-binary`, etc.

---

### 4. 🧪 Test Migration

```powershell
python test_migration.py
```

**What this tests:**
- ✅ Connection to Supabase PostgreSQL
- ✅ All 9 tables exist
- ✅ Indexes are created
- ✅ CRUD operations work

**Expected output:**
```
✅ Connected to Supabase PostgreSQL successfully!
✅ All required tables are present!
✅ All CRUD operations completed successfully!
✅ MIGRATION TEST PASSED!
```

---

### 5. 🚀 Start Application

```powershell
uvicorn app.main:app --reload --port 8000
```

**Expected output:**
```
INFO:     🔄 Connecting to Supabase PostgreSQL...
INFO:     ✅ Successfully connected to Supabase PostgreSQL!
INFO:     DB tables created/verified.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**If you see this, migration is complete!** ✅

---

## Optional Actions (Recommended)

### 6. 🎭 Create Mock Data (For Testing)

```powershell
curl -X POST http://localhost:8000/api/create-mock-data
```

**Or use the API docs:**
1. Visit http://localhost:8000/docs
2. Find `POST /api/create-mock-data`
3. Click "Try it out"
4. Click "Execute"

**What this creates:**
- 3 test users (testuser1, testuser2, testuser3)
- 20 expenses across different categories
- 4 budgets for different categories
- 2 debts with EMI details
- 2 friendships (1 accepted, 1 pending)
- 2 split expenses with participants
- 1 settlement between users

**Test user credentials:**
- Username: `testuser1` / Password: `password123`
- Username: `testuser2` / Password: `password123`
- Username: `testuser3` / Password: `password123`

---

### 7. 🧪 Test API Endpoints

Visit: http://localhost:8000/docs

**Try these endpoints:**

1. **Authentication:**
   - `POST /api/register` - Register new user
   - `POST /api/token` - Login (get JWT token)

2. **Expenses:**
   - `GET /api/expenses` - Get all expenses (requires auth)
   - `POST /api/expenses` - Create expense (requires auth)

3. **Budgets:**
   - `GET /api/budgets` - Get all budgets
   - `POST /api/budgets` - Create budget

4. **Development:**
   - `POST /api/create-mock-data` - Create test data

---

### 8. 🔗 Update Frontend Configuration

If you have a frontend application:

1. **Update API endpoint:**
   ```javascript
   const API_BASE_URL = 'http://localhost:8000/api';
   ```

2. **Update CORS in backend** (if needed):
   ```python
   # app/main.py
   frontend_origins = [
       "http://localhost:5173",  # Your frontend URL
   ]
   ```

3. **Test frontend login:**
   - Use mock user credentials
   - Verify all features work

---

### 9. 🔒 Configure Row Level Security (Production)

For production, you may want to update RLS policies:

1. **Go to Supabase Dashboard → Authentication**
2. **Enable Auth providers** (email, Google, GitHub, etc.)
3. **Update RLS policies** to use Supabase Auth
4. **Test with real user authentication**

Current RLS policies use `auth.uid()` which expects Supabase Auth.

---

### 10. 📊 Monitor Database

**Supabase Dashboard Features:**

1. **Table Editor:** View and edit data directly
2. **SQL Editor:** Run custom queries
3. **Database Logs:** Monitor queries and errors
4. **Database Health:** Check performance metrics
5. **Backups:** Configure automatic backups

---

## Verification Checklist

Use this to track your progress:

- [ ] ✅ Supabase project created
- [ ] ✅ `.env` file configured with credentials
- [ ] ✅ `supabase_migration.sql` executed successfully
- [ ] ✅ Dependencies installed (`pip install -r requirements.txt`)
- [ ] ✅ Migration test passed (`python test_migration.py`)
- [ ] ✅ Backend starts without errors
- [ ] ✅ Can access API docs (http://localhost:8000/docs)
- [ ] ✅ Mock data created (optional)
- [ ] ✅ API endpoints tested
- [ ] ✅ Frontend connected (optional)

---

## Quick Command Reference

```powershell
# Setup
python setup_migration.py              # Interactive .env setup
pip install -r requirements.txt        # Install dependencies

# Testing
python test_migration.py               # Test migration
python create_mock_data.py             # Create mock data (alternative)

# Running
uvicorn app.main:app --reload          # Start dev server
uvicorn app.main:app --port 8000       # Start on specific port

# Database
# Run supabase_migration.sql in Supabase Dashboard

# API Testing
curl -X POST http://localhost:8000/api/create-mock-data  # Create mock data
# Or visit: http://localhost:8000/docs
```

---

## Common Issues & Solutions

### ❌ Error: "DATABASE_URL not found"
**Solution:** Run `python setup_migration.py` or create `.env` manually

### ❌ Error: "Cannot connect to Supabase"
**Solution:** Check DATABASE_URL format in `.env`:
```
postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

### ❌ Error: "Table 'users' is MISSING"
**Solution:** Run `supabase_migration.sql` in Supabase SQL Editor

### ❌ Error: "ModuleNotFoundError: No module named 'colorama'"
**Solution:** Run `pip install -r requirements.txt`

### ❌ Error: "RLS policy violation"
**Solution:** For development, disable RLS in Supabase Dashboard (Table → Settings → Disable RLS)

---

## Files Reference

| File | Purpose | Action Required |
|------|---------|----------------|
| **setup_migration.py** | Interactive setup wizard | ✅ Run this first |
| **supabase_migration.sql** | Database schema | ✅ Run in Supabase |
| **test_migration.py** | Migration verification | ✅ Run after setup |
| **.env.example** | Example config | 📄 Reference only |
| **MIGRATION_QUICK_START.md** | Quick start guide | 📖 Read if needed |
| **MIGRATION_GUIDE.md** | Detailed guide | 📖 Read for details |
| **MIGRATION_COMPLETE.md** | Migration summary | 📖 Read for overview |
| **ACTION_ITEMS.md** | This file | 📋 Follow checklist |

---

## Success Indicators

You'll know the migration is successful when:

✅ `python test_migration.py` shows all green checkmarks
✅ Backend starts with "Successfully connected to Supabase PostgreSQL!"
✅ You can access API docs at http://localhost:8000/docs
✅ You can create and retrieve data via API
✅ No errors in terminal when running application

---

## Next Steps After Migration

1. **Deploy to Production:** Use Render, Railway, or Vercel
2. **Enable Supabase Features:** Auth providers, Storage, Real-time
3. **Set Up Monitoring:** Configure error logging and alerts
4. **Configure Backups:** Enable automatic daily backups
5. **Optimize Performance:** Review slow queries in Supabase dashboard

---

## Support & Documentation

- **Quick Start:** MIGRATION_QUICK_START.md
- **Full Guide:** MIGRATION_GUIDE.md
- **Summary:** MIGRATION_COMPLETE.md
- **Supabase Docs:** https://supabase.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com

---

**Migration Status:** ✅ Code changes complete - Ready for configuration

**Your Action:** Follow steps 1-5 above to complete the migration

**Time Required:** ~10-15 minutes

---

*Last Updated: January 2026*

*Good luck with your migration! 🚀*
