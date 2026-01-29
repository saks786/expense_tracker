# 💰 Expense Tracker - Backend API

A comprehensive expense tracking and group expense management system with features for personal finance management, split expenses, and group settlements.

---

## 🚀 Features

### Personal Finance Management
- ✅ Track expenses by category and date
- ✅ Set and monitor category budgets
- ✅ Manage debts with EMI calculations
- ✅ View spending analytics

### Social Features  
- ✅ Friend system with requests and approvals
- ✅ Split expenses with friends
- ✅ Automatic balance calculations
- ✅ Smart settlement suggestions

### Group Management
- ✅ Create and manage expense groups
- ✅ Invite friends to groups (friendship required for security)
- ✅ Track shared group expenses
- ✅ Calculate group balances automatically
- ✅ Optimize group settlements
- ✅ View and accept pending invitations

### Additional Features
- ✅ JWT authentication with secure tokens
- ✅ Email notifications (SendGrid integration)
- ✅ Payment gateway (Stripe integration)
- ✅ RESTful API with OpenAPI docs
- ✅ Comprehensive test suite (45+ tests)
- ✅ PostgreSQL/Supabase support

---

## 📋 Prerequisites

- Python 3.8 or higher
- PostgreSQL database (Supabase recommended) or SQLite for development
- pip package manager

---

## 🛠️ Quick Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/expense_tracker

# JWT Authentication
JWT_SECRET_KEY=your-super-secret-key-change-this
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30

# Email (Optional)
SENDGRID_API_KEY=your-sendgrid-api-key
FROM_EMAIL=noreply@yourapp.com

# Payment Gateway (Optional)
STRIPE_SECRET_KEY=sk_test_your_stripe_secret
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_public

# Frontend URL
FRONTEND_URL=http://localhost:3000
```

### 3. Initialize Database

**For Supabase/PostgreSQL:**
```bash
# Run supabase_migration.sql in Supabase SQL Editor
# The file contains all table definitions and indexes
```

**For SQLite (Development):**
```bash
# Database will be auto-created on first run
# No migration needed
```

### 4. Run the Server

```bash
python -m uvicorn app.main:app --reload
```

Server starts at: **http://localhost:8000**

### 5. Test the API

Visit: **http://localhost:8000/docs** for interactive API documentation

---

## 🧪 Running Tests

### Quick Test Run

```bash
# Install test dependencies
pip install pytest pytest-cov requests

# Run all tests
python run_tests.py
```

### Advanced Testing

```bash
# All tests with verbose output
pytest tests/ -v

# Specific test file
pytest tests/test_backend.py -v

# With coverage report
pytest tests/ --cov=app --cov-report=html

# End-to-end tests only
pytest tests/test_e2e.py -v -s
```

**See [TESTING_GUIDE.md](TESTING_GUIDE.md) for complete testing documentation**

---

## 📚 API Endpoints Overview

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - Login and get JWT token
- `GET /api/users/me` - Get current user profile

### Expenses
- `GET/POST /api/expenses` - List/create expenses
- `GET/PUT/DELETE /api/expenses/{id}` - Manage specific expense

### Budgets
- `GET/POST /api/budgets` - List/create budgets
- `GET/PUT/DELETE /api/budgets/{id}` - Manage specific budget

### Debts
- `GET/POST /api/debts` - List/create debts
- `POST /api/debts/{id}/pay-emi` - Pay EMI installment

### Friends
- `POST /api/friends/request` - Send friend request
- `GET /api/friends/requests` - List pending requests
- `POST /api/friends/accept/{id}` - Accept request
- `GET /api/friends` - List all friends

### Split Expenses
- `POST /api/split-expenses` - Create split expense
- `GET /api/split-expenses` - List all splits
- `GET /api/split-expenses/balances` - Get balances
- `POST /api/split-expenses/settle` - Settle balance

### Groups
- `POST /api/groups` - Create group
- `GET /api/groups` - List user's groups
- `POST /api/groups/{id}/invite` - Invite friends (must be friends first!)
- `GET /api/groups/invitations/pending` - View pending invitations
- `POST /api/groups/{id}/join` - Accept invitation
- `POST /api/groups/{id}/expenses` - Create group expense
- `GET /api/groups/{id}/balances` - Get group balances
- `GET /api/groups/{id}/settlements/suggestions` - Get settlement suggestions

**Full API documentation:** http://localhost:8000/docs

---

## 📂 Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry
│   ├── auth.py              # JWT authentication
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic validation schemas
│   ├── routes.py            # Main API routes
│   ├── routes_groups.py     # Group management routes
│   ├── payments.py          # Stripe payment integration
│   ├── email_service.py     # SendGrid email service
│   └── supabase_client.py   # Supabase client (optional)
├── tests/
│   ├── conftest.py          # Pytest configuration & fixtures
│   ├── test_backend.py      # Backend API tests (30+ tests)
│   └── test_e2e.py          # End-to-end integration tests
├── .env                     # Environment variables (create this)
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
├── pytest.ini              # Pytest configuration
├── run_tests.py            # Convenient test runner
├── supabase_migration.sql  # Database schema migration
├── Readme.md               # This file
├── TESTING_GUIDE.md        # Complete testing documentation
├── GROUP_INVITATION_SYSTEM.md  # Group system documentation
└── QUICK_REFERENCE_GROUP_INVITATIONS.md  # Quick reference
```

---

## 🔐 Security Features

- ✅ JWT-based authentication with token expiration
- ✅ Password hashing using bcrypt
- ✅ Row-level security (RLS) policies in Supabase
- ✅ CORS configuration for frontend
- ✅ Input validation with Pydantic schemas
- ✅ SQL injection prevention via SQLAlchemy ORM
- ✅ Friendship requirement for group invitations

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [TESTING_GUIDE.md](TESTING_GUIDE.md) | Complete testing guide with examples |
| [GROUP_INVITATION_SYSTEM.md](GROUP_INVITATION_SYSTEM.md) | Group invitation system docs |
| [QUICK_REFERENCE_GROUP_INVITATIONS.md](QUICK_REFERENCE_GROUP_INVITATIONS.md) | Quick reference diagrams |
| [ACTION_ITEMS.md](ACTION_ITEMS.md) | Development roadmap |
| [PROJECT_FEATURES.md](PROJECT_FEATURES.md) | Feature list |

---

## 🚀 Deployment

### Docker Deployment

```bash
# Build image
docker build -t expense-tracker-backend .

# Run container
docker run -p 8000:8000 --env-file .env expense-tracker-backend
```

### Heroku Deployment

```bash
heroku create expense-tracker-api
heroku config:set DATABASE_URL=your-postgresql-url
heroku config:set JWT_SECRET_KEY=your-secret-key
git push heroku main
```

---

## 🧪 Test Coverage

Current test coverage: **45+ tests**

- ✅ Authentication tests (4 tests)
- ✅ Expense CRUD tests (5 tests)
- ✅ Budget management tests (3 tests)
- ✅ Debt management tests (3 tests)
- ✅ Friendship system tests (4 tests)
- ✅ Split expense tests (3 tests)
- ✅ Group management tests (8 tests)
- ✅ End-to-end workflow tests (4 comprehensive workflows)

Run tests with: `python run_tests.py --coverage`

---

## 🐛 Troubleshooting

### Database Connection Error
```bash
# Check DATABASE_URL in .env file
# Ensure PostgreSQL server is running
# For Supabase, verify connection string format
```

### Import Errors
```bash
pip install -r requirements.txt --force-reinstall
```

### Test Failures
```bash
# 1. Start backend server in one terminal
python -m uvicorn app.main:app --reload

# 2. Run tests in another terminal
pytest tests/ -v
```

### Group Invitation Issues
See [GROUP_INVITATION_SYSTEM.md](GROUP_INVITATION_SYSTEM.md) for troubleshooting group invitations.

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Write tests for new features
- Update documentation
- Keep commits focused and atomic

---

## 📞 Support

- 📖 Check documentation files
- 🔍 Review `/docs` for API reference
- 🐛 Report issues on GitHub
- 💬 Contact maintainers

---

## 📄 License

MIT License - See LICENSE file for details

---

## ✨ Built With

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern web framework
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - SQL toolkit and ORM
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Data validation
- **[Pytest](https://docs.pytest.org/)** - Testing framework
- **[Supabase](https://supabase.com/)** - PostgreSQL database
- **[SendGrid](https://sendgrid.com/)** - Email service
- **[Stripe](https://stripe.com/)** - Payment processing

---

## 🎯 Quick Command Reference

```bash
# Setup
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration

# Run server
python -m uvicorn app.main:app --reload

# Run tests
python run_tests.py
# or
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# API Documentation
# http://localhost:8000/docs
```

---

## 📊 Key Metrics

- 🧪 **45+ automated tests**
- 📝 **50+ API endpoints**
- 🔐 **JWT authentication**
- 👥 **Group & friend management**
- 💰 **Split expense tracking**
- 📧 **Email notifications**
- 💳 **Payment integration**

---

**Happy tracking! 💰🚀**

For detailed information, see the documentation files in this directory.
