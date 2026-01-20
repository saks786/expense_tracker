# Supabase Migration Guide

This guide will help you complete the migration from SQLite to Supabase PostgreSQL.

## 📋 Prerequisites

Before starting the migration, ensure you have:

1. **Supabase Account**: Sign up at https://supabase.com
2. **Supabase Project**: Create a new project in Supabase Dashboard
3. **Database Credentials**: Get your PostgreSQL connection string from Supabase

## 🚀 Migration Steps

### Step 1: Get Supabase Credentials

1. Go to your Supabase project dashboard
2. Navigate to **Settings** → **Database**
3. Find the **Connection String** section
4. Copy the connection string in the format:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
   ```

### Step 2: Update Environment Variables

1. Copy `.env.example` to `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Edit `.env` and update these values:
   ```env
   DATABASE_URL=postgresql://postgres:your_password@db.xxxxxxxxxxxxx.supabase.co:5432/postgres
   SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
   SUPABASE_KEY=your_supabase_anon_key_here
   ```

   **How to get these values:**
   - `DATABASE_URL`: From Settings → Database → Connection String
   - `SUPABASE_URL`: From Settings → API → Project URL
   - `SUPABASE_KEY`: From Settings → API → Project API keys → anon/public key

### Step 3: Run Database Migration Script

1. Open Supabase Dashboard → **SQL Editor**
2. Copy the entire contents of `supabase_migration.sql`
3. Paste into the SQL Editor
4. Click **Run** to execute the migration

This will create:
- All database tables (users, expenses, budgets, debts, etc.)
- Indexes for optimal performance
- Row Level Security (RLS) policies
- Foreign key constraints

### Step 4: Install Dependencies

Install the required Python packages:

```powershell
pip install -r requirements.txt
```

### Step 5: Test the Migration

Run the migration test script:

```powershell
python test_migration.py
```

This script will:
- ✅ Test connection to Supabase PostgreSQL
- ✅ Verify all tables exist
- ✅ Check indexes are created
- ✅ Test CRUD operations
- ✅ Confirm database is ready

### Step 6: Start the Application

Start your FastAPI backend:

```powershell
uvicorn app.main:app --reload --port 8000
```

You should see:
```
INFO:     🔄 Connecting to Supabase PostgreSQL...
INFO:     ✅ Successfully connected to Supabase PostgreSQL!
INFO:     DB tables created/verified.
```

## 🔍 Verification Checklist

- [ ] Supabase project created
- [ ] `.env` file configured with correct credentials
- [ ] Migration SQL script executed successfully in Supabase
- [ ] `test_migration.py` passes all tests
- [ ] Backend starts without errors
- [ ] SQLite fallback removed from code

## 📊 Database Schema

The migration creates the following tables:

1. **users** - User accounts and authentication
2. **expenses** - Personal expense records
3. **budgets** - Monthly budget limits per category
4. **debts** - Debt tracking with EMI details
5. **friendships** - Friend connections between users
6. **split_expenses** - Group expenses to split among friends
7. **split_participants** - Junction table for split expense participants
8. **settlements** - Payment settlements between users
9. **transactions** - Payment gateway transaction records

## 🔒 Security Features

The migration includes:

- **Row Level Security (RLS)**: Users can only access their own data
- **Authentication policies**: Integrated with Supabase Auth
- **Foreign key constraints**: Data integrity enforcement
- **Cascade deletes**: Clean up related data automatically

## 🎯 Key Changes from SQLite

### Before (SQLite):
```python
DATABASE_URL = "sqlite:///./dev.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
```

### After (Supabase PostgreSQL):
```python
DATABASE_URL = os.getenv("DATABASE_URL")  # PostgreSQL connection string
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)
```

### Database-Specific Changes:

1. **No more SQLite fallback** - Only PostgreSQL is supported
2. **Connection pooling** - Better performance for concurrent requests
3. **Native PostgreSQL features** - Better performance and scalability
4. **Supabase real-time** - Can enable real-time subscriptions
5. **Row Level Security** - Built-in data access control

## 🛠️ Troubleshooting

### Connection Error
```
❌ Cannot connect to Supabase PostgreSQL
```
**Solution**: Verify your `DATABASE_URL` is correct and your Supabase project is running

### Missing Tables Error
```
❌ Table 'expenses' is MISSING!
```
**Solution**: Run the `supabase_migration.sql` script in Supabase SQL Editor

### Authentication Error
```
❌ RLS policy violation
```
**Solution**: Disable RLS for development or update policies in Supabase Dashboard

### Pool Connection Error
```
❌ Too many connections
```
**Solution**: Check your Supabase plan limits and adjust pool settings

## 📚 Additional Resources

- [Supabase Documentation](https://supabase.com/docs)
- [SQLAlchemy PostgreSQL Docs](https://docs.sqlalchemy.org/en/14/dialects/postgresql.html)
- [FastAPI Database Guide](https://fastapi.tiangolo.com/tutorial/sql-databases/)

## 🎉 Migration Complete!

Once all tests pass, your application is fully migrated to Supabase PostgreSQL! 

The application now uses:
- ✅ Supabase PostgreSQL for all database operations
- ✅ Connection pooling for better performance
- ✅ Row Level Security for data protection
- ✅ Professional database hosting with automatic backups
- ✅ Scalable infrastructure ready for production

## 🚀 Next Steps

1. **Create mock data** (optional):
   ```bash
   curl -X POST http://localhost:8000/api/create-mock-data
   ```

2. **Test all API endpoints** in your frontend application

3. **Enable Supabase features**:
   - Real-time subscriptions
   - Authentication providers (Google, GitHub, etc.)
   - Storage for file uploads
   - Edge functions for serverless logic

4. **Monitor your database** in Supabase Dashboard → Database → Logs

5. **Set up backups** in Supabase Dashboard → Database → Backups
