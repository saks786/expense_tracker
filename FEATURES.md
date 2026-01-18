# Expense Tracker - Features Documentation

## Overview
A comprehensive expense tracking application with personal finance management, debt tracking, friend expense splitting, and analytics capabilities. Built with React frontend and FastAPI backend.

---

## 🎯 Core Features

### 1. User Authentication & Authorization
**Status**: ✅ Fully Implemented

- **User Registration**
  - Username and email validation
  - Secure password hashing
  - Duplicate username/email prevention

- **User Login**
  - JWT-based authentication
  - OAuth2 password flow
  - Token expiration handling

- **User Profile**
  - Current user information retrieval
  - Session management
  - Secure logout functionality

**Technical Implementation**:
- Backend: JWT tokens with configurable expiration
- Frontend: Token storage in localStorage
- Security: Password hashing with industry-standard algorithms

---

### 2. Personal Expense Management
**Status**: ✅ Fully Implemented

#### Expense CRUD Operations
- **Create Expenses**
  - Category selection
  - Amount tracking
  - Description/notes
  - Date selection (defaults to current date)

- **Read/List Expenses**
  - View all personal expenses
  - Filter by category
  - Sorted display

- **Update Expenses**
  - Edit any expense field
  - Modal-based editing interface
  - Real-time validation

- **Delete Expenses**
  - Confirmation dialog
  - Permanent deletion
  - Immediate UI update

#### Expense Categories
Common categories include:
- Food & Dining
- Transportation
- Shopping
- Entertainment
- Bills & Utilities
- Healthcare
- Education
- Others (Custom categories supported)

**Technical Implementation**:
- Backend: RESTful API endpoints (`/api/expenses`)
- Database: SQLite with SQLAlchemy ORM
- Frontend: React state management with real-time updates

---

### 3. Analytics & Insights
**Status**: ✅ Fully Implemented

#### Statistics Dashboard
- **Total Expenses**: Cumulative spending across all time
- **Monthly Total**: Current month's spending
- **Average Expense**: Mean expense amount
- **Total Count**: Number of tracked expenses

#### Visual Analytics
**Category Distribution (Pie Chart)**
- Spending breakdown by category
- Percentage visualization
- Interactive chart with hover details
- Powered by Recharts library

**Monthly Trends (Line Chart)**
- Spending patterns over time
- Month-by-month comparison
- Trend identification
- Historical data visualization

**Analytics API Endpoints**:
- `/api/analytics/category` - Category-wise aggregation
- `/api/analytics/monthly` - Month-wise spending trends

**Technical Implementation**:
- Backend: SQL aggregation with GROUP BY
- Frontend: Recharts for data visualization
- Auto-displays when 3+ expenses exist

---

### 4. Debt Management
**Status**: 🟡 Frontend Implemented, Backend Missing Routes

#### Debt Tracking Features
- **Add Debts/Loans**
  - Debt name/description
  - Principal amount
  - Interest rate (% per annum)
  - EMI amount
  - EMI date (day of month)
  - Start date tracking

- **Debt Dashboard**
  - Active vs Paid status
  - Remaining amount calculation
  - Months remaining estimation
  - EMI schedule tracking

- **Payment Recording**
  - Record partial/full payments
  - Automatic remaining balance update
  - Status auto-update when paid off
  - Payment history tracking

- **Debt Deletion**
  - Remove closed/irrelevant debts
  - Confirmation dialogs

#### Debt Metrics
- Principal amount
- Interest rate
- EMI amount and date
- Remaining balance
- Calculated months to payoff
- Active/Paid status

**Technical Implementation**:
- Frontend: Complete UI with DebtForm and DebtList components
- Backend: Models defined, **Routes need implementation**
- Database: Debt table with relationships

**⚠️ Note**: Backend API routes for debts need to be implemented in `routes.py`

---

### 5. Friend Management
**Status**: 🟡 Frontend Implemented, Backend Routes Partial

#### Friend System Features
- **Send Friend Requests**
  - Search by username
  - Send connection requests

- **Manage Friend Requests**
  - View pending requests
  - Accept friend requests
  - Decline unwanted requests

- **Friend List**
  - View all connected friends
  - Remove friends
  - Friend status tracking

#### Friendship States
- **Pending**: Request sent, awaiting acceptance
- **Accepted**: Active friendship connection
- **Blocked**: (Future feature)

**Technical Implementation**:
- Frontend: FriendList component with request management
- Backend: Friendship model with bidirectional relationships
- Database: Friendships table with status tracking

**⚠️ Note**: Some friendship routes may need completion/testing

---

### 6. Split Expenses
**Status**: ✅ Fully Implemented

#### Group Expense Features
- **Create Split Expenses**
  - Expense description
  - Total amount
  - Category selection
  - Date tracking
  - Select participants from friend list

- **Automatic Split Calculation**
  - Equal split among participants
  - Per-person amount calculation
  - Creator tracking

- **Balance Tracking**
  - Who owes whom
  - Net balance per person
  - Consolidated view

- **Settlement Suggestions**
  - Optimized payment recommendations
  - Minimize number of transactions
  - Clear settlement paths

#### Split Expense Workflow
1. User creates expense with total amount
2. Selects friends as participants
3. System auto-splits amount equally
4. Balances calculated and displayed
5. Settlement suggestions generated
6. Participants can view shared expenses

**Technical Implementation**:
- Backend: `/api/split-expenses`, `/api/balances`, `/api/settlements`
- Database: Many-to-many relationship with users
- Frontend: SplitExpenseForm and SplitExpenseList components
- Algorithm: Smart balance calculation and settlement optimization

---

## 🎨 User Interface Features

### Responsive Design
- Mobile-friendly interface
- Adaptive layouts
- Touch-optimized controls

### Tab-Based Navigation
- **💰 Expenses** - Personal expense tracking
- **💳 Debts** - Debt and loan management
- **👥 Friends** - Friend connections
- **🤝 Split** - Shared expense management

### Interactive Components
- Modal dialogs for editing
- Confirmation prompts for deletions
- Real-time form validation
- Loading states and error handling
- Empty state messages

### Visual Feedback
- Color-coded status indicators
- Smooth transitions and animations
- Hover effects and interactive elements
- Currency formatting (₹ symbol)
- Date formatting

---

## 🔧 Technical Architecture

### Frontend Stack
- **Framework**: React 18.2.0
- **Routing**: React Router DOM 6.20.0
- **Charts**: Recharts 2.10.0
- **HTTP Client**: Axios 1.6.0
- **Build Tool**: Vite 5.0.0
- **Styling**: Custom CSS with modern features

### Backend Stack
- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: SQLite (dev), PostgreSQL-ready
- **Authentication**: JWT with OAuth2
- **Password Security**: bcrypt hashing
- **Email Service**: SendGrid integration

### Database Schema
**Tables**:
- `users` - User accounts
- `expenses` - Personal expenses
- `debts` - Debt tracking
- `budgets` - Budget limits (model exists)
- `friendships` - Friend connections
- `split_expenses` - Shared expenses
- `split_participants` - Many-to-many for splits
- `settlements` - Payment settlements

### API Architecture
- RESTful design principles
- JWT Bearer token authentication
- CORS configured for frontend domains
- Request/Response validation with Pydantic
- Error handling and status codes

---

## 📊 Data Models

### User
```python
- id: Integer (Primary Key)
- username: String (Unique)
- email: String (Unique)
- password: String (Hashed)
- is_active: Boolean
```

### Expense
```python
- id: Integer (Primary Key)
- category: String
- amount: Float
- date: Date
- description: String
- user_id: Integer (Foreign Key)
```

### Debt
```python
- id: Integer (Primary Key)
- name: String
- principal_amount: Float
- interest_rate: Float
- emi_amount: Float
- emi_date: Integer (Day of month)
- start_date: Date
- remaining_amount: Float
- status: String (active/paid)
- user_id: Integer (Foreign Key)
```

### Friendship
```python
- id: Integer (Primary Key)
- user_id: Integer (Foreign Key)
- friend_id: Integer (Foreign Key)
- status: String (pending/accepted)
- created_at: DateTime
```

### SplitExpense
```python
- id: Integer (Primary Key)
- description: String
- total_amount: Float
- category: String
- date: Date
- created_by: Integer (Foreign Key)
- participants: Many-to-Many with Users
- created_at: DateTime
```

### Settlement
```python
- id: Integer (Primary Key)
- from_user_id: Integer (Foreign Key)
- to_user_id: Integer (Foreign Key)
- amount: Float
- created_at: DateTime
```

---

## 🚀 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register` | Create new user account |
| POST | `/api/token` | Login and get JWT token |
| GET | `/api/users/me` | Get current user info |

### Expenses
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/expenses` | List all user expenses |
| POST | `/api/expenses` | Create new expense |
| PUT | `/api/expenses/{id}` | Update expense |
| DELETE | `/api/expenses/{id}` | Delete expense |

### Analytics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/analytics/category` | Category-wise spending |
| GET | `/api/analytics/monthly` | Monthly spending trends |

### Split Expenses
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/split-expenses` | List split expenses |
| POST | `/api/split-expenses` | Create split expense |
| DELETE | `/api/split-expenses/{id}` | Delete split expense |
| GET | `/api/balances` | Get user balances |
| GET | `/api/settlements/suggestions` | Get settlement suggestions |
| POST | `/api/settlements` | Record settlement |

### Debts (⚠️ Routes need implementation)
| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/api/debts` | List user debts | 🔴 Missing |
| POST | `/api/debts` | Create new debt | 🔴 Missing |
| PUT | `/api/debts/{id}` | Update debt/payment | 🔴 Missing |
| DELETE | `/api/debts/{id}` | Delete debt | 🔴 Missing |

### Friends (⚠️ Some routes need implementation)
| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/api/friends` | List friends | 🟡 Check |
| GET | `/api/friends/requests` | List pending requests | 🟡 Check |
| POST | `/api/friends/request` | Send friend request | 🟡 Check |
| PUT | `/api/friends/{id}/accept` | Accept request | 🟡 Check |
| DELETE | `/api/friends/{id}` | Remove friend | 🟡 Check |

---

## 🔐 Security Features

### Authentication Security
- JWT token-based authentication
- Secure password hashing (bcrypt)
- Token expiration and refresh
- OAuth2 password flow standard

### API Security
- Bearer token authentication
- CORS configuration
- Request validation
- SQL injection prevention (ORM)
- XSS protection

### Data Privacy
- User data isolation
- Relationship-based access control
- Friendship verification for splits
- Secure password storage

---

## 🎯 Future Enhancement Ideas

### Planned Features
1. **Budget Management**
   - Category-wise budget limits
   - Budget vs actual tracking
   - Overspending alerts

2. **Notifications**
   - Email notifications (SendGrid integrated)
   - EMI due date reminders
   - Settlement payment reminders
   - Budget limit warnings

3. **Recurring Expenses**
   - Monthly subscription tracking
   - Auto-create recurring expenses
   - Subscription management

4. **Export/Import**
   - CSV export
   - PDF reports
   - Data backup/restore

5. **Advanced Analytics**
   - Year-over-year comparison
   - Spending predictions
   - Custom date range filtering
   - Expense tags and labels

6. **Multi-Currency Support**
   - Currency selection
   - Exchange rate integration
   - Multi-currency expenses

7. **Receipt Management**
   - Upload receipt images
   - OCR for receipt parsing
   - Attachment storage

8. **Group Management**
   - Create expense groups
   - Group-based splitting
   - Group analytics

### Technical Improvements
- Database migration to PostgreSQL for production
- Redis caching for analytics
- WebSocket for real-time updates
- Mobile app (React Native)
- Progressive Web App (PWA)
- Automated testing suite
- CI/CD pipeline

---

## 📝 Development Status

### ✅ Completed Features
- User authentication and authorization
- Personal expense CRUD operations
- Category-based expense tracking
- Analytics dashboard with charts
- Split expense creation and management
- Balance calculation and settlement suggestions
- Friend system (frontend complete)

### 🟡 Partially Complete
- Debt management (frontend complete, backend routes needed)
- Friend management (verify backend routes)

### 🔴 Not Started
- Budget management (models exist, no UI/routes)
- Email notifications (service integrated, not used)
- Recurring expenses
- Receipt uploads
- Export functionality

---

## 🛠️ Setup & Configuration

### Environment Variables
**Backend (.env)**:
```env
DATABASE_URL=sqlite:///./dev.db
SECRET_KEY=your-secret-key-here
SENDGRID_API_KEY=your-sendgrid-key
```

**Frontend (.env)**:
```env
VITE_API_URL=http://localhost:8000
```

### Running the Application

**Backend**:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev
```

### Database Initialization
- Tables auto-created on first run
- SQLite database stored at `backend/dev.db`
- Models defined in `app/models.py`

---

## 📱 User Workflows

### Basic Expense Tracking Flow
1. User registers/logs in
2. Navigates to Expenses tab (default)
3. Fills expense form (amount, category, description, date)
4. Submits expense
5. Views expense in list below
6. Can edit/delete as needed
7. Views analytics on dashboard

### Split Expense Flow
1. User adds friends (Friends tab)
2. Navigates to Split tab
3. Creates split expense with description and amount
4. Selects participant friends
5. System calculates split and balances
6. Views settlement suggestions
7. Can record settlements when paid

### Debt Management Flow
1. User navigates to Debts tab
2. Adds debt with principal, rate, EMI details
3. Views debt dashboard with remaining amount
4. Records payments as EMI is paid
5. System updates remaining amount and status
6. Debt auto-marked as "paid" when settled

---

## 🎨 Design System

### Color Scheme
- Primary: Blue accent colors
- Success: Green for completed/paid
- Warning: Yellow for pending
- Danger: Red for deletion/errors
- Background: Clean white/light gray

### Typography
- Primary Font: System font stack
- Monospace: For currency amounts
- Font sizes: Hierarchical scaling

### Components
- Cards for data display
- Modal dialogs for editing
- Buttons with hover states
- Form inputs with validation
- Tab navigation
- Charts and graphs

---

## 📄 License & Credits

### Technologies Used
- React - MIT License
- FastAPI - MIT License
- Recharts - MIT License
- SQLAlchemy - MIT License

### Project Structure
```
expense_tracker/
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── api.js          # API client
│   │   └── App.jsx         # Main app
│   └── package.json
└── backend/
    ├── app/
    │   ├── models.py       # Database models
    │   ├── routes.py       # API routes
    │   ├── schemas.py      # Pydantic schemas
    │   ├── auth.py         # Authentication
    │   └── main.py         # FastAPI app
    └── requirements.txt
```

---

## 📞 Support & Contribution

### Known Issues
- Debt management backend routes need implementation
- Friend management routes need verification
- Budget feature incomplete

### Contribution Guidelines
1. Fork the repository
2. Create feature branch
3. Implement changes with tests
4. Submit pull request

### Contact
For issues and feature requests, please use the GitHub issue tracker.

---

**Last Updated**: January 2026
**Version**: 2.0.0
**Status**: Active Development
