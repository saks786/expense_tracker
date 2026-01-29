# Expense Tracker Backend

FastAPI backend for the Expense Tracker application with Supabase PostgreSQL database.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Supabase account and project
- pip (Python package manager)

### Migration from SQLite

**🎯 This application now uses Supabase PostgreSQL exclusively.**

If you're migrating from SQLite, see:
- **MIGRATION_QUICK_START.md** - 5-minute quick start guide
- **MIGRATION_GUIDE.md** - Detailed migration documentation

### Setup

1. **Run the interactive setup wizard:**
   ```powershell
   python setup_migration.py
   ```

2. **Or manually configure .env:**
   ```powershell
   Copy-Item .env.example .env
   # Edit .env with your Supabase credentials
   ```

3. **Run database migration in Supabase:**
   - Open Supabase Dashboard → SQL Editor
   - Copy contents of `supabase_migration.sql`
   - Paste and run in SQL Editor

4. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Test the migration:**
   ```powershell
   python test_migration.py
   ```

6. **Start the server:**
   ```powershell
   uvicorn app.main:app --reload --port 8000
   ```

## 📋 Features

- ✅ User authentication with JWT tokens
- ✅ Expense tracking and categorization
- ✅ Budget management per category
- ✅ Debt tracking with EMI calculations
- ✅ Friend management and split expenses
- ✅ Payment integration (Stripe)
- ✅ Email notifications (SendGrid)
- ✅ Supabase PostgreSQL database
- ✅ Row Level Security (RLS)
- ✅ Real-time capabilities

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **Database:** Supabase PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT (python-jose)
- **Password Hashing:** Argon2 (passlib)
- **Payment Gateway:** Stripe
- **Email Service:** SendGrid

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database connection (PostgreSQL)
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── routes.py            # API endpoints
│   ├── auth.py              # Authentication logic
│   ├── payments.py          # Stripe integration
│   ├── email_service.py     # SendGrid integration
│   └── supabase_client.py   # Supabase client
├── supabase_migration.sql   # Database migration script
├── test_migration.py        # Migration test script
├── setup_migration.py       # Interactive setup wizard
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment variables
├── MIGRATION_GUIDE.md      # Detailed migration guide
├── MIGRATION_QUICK_START.md # Quick start guide
└── README.md               # This file
```

## 🌐 API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/token` - Login and get access token

### Expenses
- `GET /api/expenses` - Get all expenses
- `POST /api/expenses` - Create new expense
- `PUT /api/expenses/{id}` - Update expense
- `DELETE /api/expenses/{id}` - Delete expense

### Budgets
- `GET /api/budgets` - Get all budgets
- `POST /api/budgets` - Create budget
- `GET /api/budgets/alerts` - Get budget alerts

### Debts
- `GET /api/debts` - Get all debts
- `POST /api/debts` - Create debt
- `PUT /api/debts/{id}` - Update debt

### Friends & Split Expenses
- `POST /api/friends/request` - Send friend request
- `GET /api/friends` - Get friends list
- `POST /api/split-expenses` - Create split expense
- `POST /api/settlements` - Create settlement

### Payments
- `POST /api/payments/create-payment-intent` - Create Stripe payment intent

### Development
- `POST /api/create-mock-data` - Create test data (dev only)

## 🧪 Testing

### Test Migration
```powershell
python test_migration.py
```

### Test API Endpoints
```powershell
# Start server
uvicorn app.main:app --reload

# Test in browser
http://localhost:8000/docs
```

### Create Mock Data
```powershell
curl -X POST http://localhost:8000/api/create-mock-data
```

## 🔐 Environment Variables

Required variables in `.env`:

```env
# Database
DATABASE_URL=postgresql://postgres:password@db.xxx.supabase.co:5432/postgres

# Supabase
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=your_anon_key

# Authentication
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Optional Services
SENDGRID_API_KEY=your_sendgrid_key
STRIPE_SECRET_KEY=your_stripe_key
```

## 🚀 Deployment

### Deploy to Render

1. Connect your GitHub repository
2. Set environment variables in Render dashboard
3. Deploy with:
   ```
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

### Deploy to Railway

1. Connect your GitHub repository
2. Set environment variables
3. Railway will auto-detect and deploy

## 📊 Database Schema

See `supabase_migration.sql` for complete schema including:
- Users, Expenses, Budgets, Debts
- Friendships, Split Expenses, Settlements
- Transactions (payment records)
- Indexes and RLS policies

## 🔒 Security Features

- JWT token-based authentication
- Argon2 password hashing
- Row Level Security (RLS) in Supabase
- CORS configuration
- Environment variable security

## 📝 Development Notes

### Database Connection
- Uses SQLAlchemy ORM with PostgreSQL
- Connection pooling enabled (10 base + 20 overflow)
- Automatic connection health checks (pool_pre_ping)
- Connections recycled every hour

### Authentication Flow
1. User registers → Password hashed with Argon2
2. User logs in → JWT token generated
3. Protected endpoints require Bearer token
4. Token expires after 30 minutes (configurable)

## 🆘 Troubleshooting

### Cannot connect to database
- Check DATABASE_URL format in .env
- Verify Supabase project is running
- Test connection: `python test_migration.py`

### Import errors
- Install dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version` (3.8+ required)

### API errors
- Check FastAPI logs in terminal
- Visit `/docs` for interactive API documentation
- Verify JWT token is included in request headers

## 📚 Documentation

- **API Docs:** http://localhost:8000/docs (when running)
- **Migration Guide:** See MIGRATION_GUIDE.md
- **Quick Start:** See MIGRATION_QUICK_START.md

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational purposes.

---

**Status:** ✅ Production-ready with Supabase PostgreSQL

**Last Updated:** January 2026
