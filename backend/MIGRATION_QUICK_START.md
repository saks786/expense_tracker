# 🚀 SQLite to Supabase Migration - Quick Start

This document provides a quick reference for migrating your Expense Tracker from SQLite to Supabase PostgreSQL.

## ⚡ Quick Migration (5 Minutes)

### Option 1: Interactive Setup (Recommended)

```powershell
# Run the interactive setup wizard
python setup_migration.py
```

This wizard will:
- Guide you through entering your Supabase credentials
- Generate a secure SECRET_KEY automatically
- Create your .env file with all required settings

### Option 2: Manual Setup

1. **Copy the example file:**
   ```powershell
   Copy-Item .env.example .env
   ```

2. **Edit .env and update these values:**
   ```env
   DATABASE_URL=postgresql://postgres:your_password@db.xxxxxxxxxxxxx.supabase.co:5432/postgres
   SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
   SUPABASE_KEY=your_supabase_anon_key_here
   ```

3. **Get credentials from Supabase:**
   - Go to https://supabase.com/dashboard
   - Select your project
   - Settings → Database → Copy "Connection String"
   - Settings → API → Copy "Project URL" and "anon key"

## 📊 Run Database Migration

1. **Open Supabase Dashboard:**
   - Go to your project → SQL Editor

2. **Copy and run migration script:**
   - Open `supabase_migration.sql` in your editor
   - Copy all contents (203 lines)
   - Paste into Supabase SQL Editor
   - Click "Run"

3. **Verify success:**
   - You should see: ✅ Database migration completed successfully!

## 🧪 Test the Migration

```powershell
# Install dependencies
pip install -r requirements.txt

# Run migration test
python test_migration.py
```

Expected output:
```
✅ Connected to Supabase PostgreSQL successfully!
✅ All required tables are present!
✅ All CRUD operations completed successfully!
✅ MIGRATION TEST PASSED!
```

## 🏃 Start the Application

```powershell
uvicorn app.main:app --reload --port 8000
```

Expected output:
```
INFO:     🔄 Connecting to Supabase PostgreSQL...
INFO:     ✅ Successfully connected to Supabase PostgreSQL!
INFO:     DB tables created/verified.
INFO:     Application startup complete.
```

## ✅ Verification Checklist

- [ ] Supabase project created
- [ ] .env file configured
- [ ] supabase_migration.sql executed in Supabase
- [ ] test_migration.py passes all tests
- [ ] Backend starts without errors
- [ ] Can create and retrieve data via API

## 🔧 What Changed?

### Files Modified:
1. **app/database.py** - Now only uses PostgreSQL (no SQLite fallback)
2. **requirements.txt** - Added `supabase` and `colorama` packages
3. **supabase_migration.sql** - Fixed typo in RLS policy

### Files Created:
1. **test_migration.py** - Comprehensive migration test script
2. **setup_migration.py** - Interactive .env setup wizard
3. **.env.example** - Example environment variables
4. **MIGRATION_GUIDE.md** - Detailed migration documentation
5. **MIGRATION_QUICK_START.md** - This file

### Database Changes:
- ✅ All data now stored in Supabase PostgreSQL
- ✅ Connection pooling enabled (10 base + 20 overflow)
- ✅ Row Level Security (RLS) enabled
- ✅ Indexes created for optimal performance
- ✅ Foreign key constraints enforced

## 🆘 Troubleshooting

### Error: "DATABASE_URL not found"
**Solution:** Run `python setup_migration.py` or create .env file manually

### Error: "Cannot connect to Supabase"
**Solution:** Check your DATABASE_URL format:
```
postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

### Error: "Table 'users' is MISSING"
**Solution:** Run the migration SQL script in Supabase SQL Editor

### Error: "Import error: No module named 'colorama'"
**Solution:** Install dependencies: `pip install -r requirements.txt`

## 📚 Full Documentation

For detailed information, see:
- **MIGRATION_GUIDE.md** - Complete migration guide with all details
- **supabase_migration.sql** - Database schema and RLS policies
- **test_migration.py** - Migration verification script

## 🎉 Success!

Once all tests pass, your application is fully migrated to Supabase PostgreSQL!

### Benefits:
- ✅ Professional PostgreSQL database
- ✅ Automatic backups
- ✅ Scalable infrastructure
- ✅ Real-time capabilities
- ✅ Row-level security
- ✅ 500MB free tier storage

### Next Steps:
1. Test all API endpoints with your frontend
2. Create mock data: `POST http://localhost:8000/api/create-mock-data`
3. Explore Supabase features (Auth, Storage, Real-time)
4. Deploy to production (Render, Railway, or Vercel)

## 📞 Need Help?

- Check **MIGRATION_GUIDE.md** for detailed troubleshooting
- Review Supabase docs: https://supabase.com/docs
- Check SQLAlchemy docs: https://docs.sqlalchemy.org

---

**Migration Status:** ✅ Complete - All files updated and tested

**Database:** Supabase PostgreSQL (Production-ready)

**Last Updated:** January 2026
