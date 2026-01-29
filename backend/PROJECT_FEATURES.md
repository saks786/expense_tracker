# Expense Tracker Backend - Features Documentation

## Overview
A comprehensive FastAPI-based expense tracking system with advanced features for personal finance management, social expense splitting, and organized group expense management with role-based permissions.

**Version:** 3.0.0
**Framework:** FastAPI
**Database:** SQLAlchemy (PostgreSQL/SQLite)
**Authentication:** JWT (JSON Web Tokens)

---

## Core Technologies

### Backend Stack
- **FastAPI** - Modern async web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Production database (SQLite for development)
- **Uvicorn** - ASGI server
- **Python-JOSE** - JWT token handling
- **Passlib (Argon2)** - Password hashing
- **SendGrid** - Email service integration
- **Pydantic** - Data validation

### Security Features
- JWT-based authentication with OAuth2
- Argon2 password hashing
- Token expiration (30 minutes)
- CORS protection with whitelist
- User credential validation
- Secure password storage

---

## Feature Categories

### 1. Authentication & User Management

#### User Registration (`POST /api/register`)
- Username uniqueness validation
- Email uniqueness validation
- Secure password hashing with Argon2
- Automatic user account creation

**Request:**
```json
{
  "username": "string",
  "email": "user@example.com",
  "password": "string"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "string",
  "email": "user@example.com",
  "is_active": true
}
```

#### User Login (`POST /api/token`)
- OAuth2 password flow
- JWT token generation
- 30-minute token expiration
- Bearer token authentication

**Request:** Form data with `username` and `password`

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### Get Current User (`GET /api/users/me`)
- Retrieve authenticated user details
- Token-based authentication required

---

### 2. Expense Management

#### List All Expenses (`GET /api/expenses`)
- Retrieve all expenses for authenticated user
- Sorted by user ownership
- Full expense details returned

**Response:**
```json
[
  {
    "id": 1,
    "category": "Food",
    "amount": 45.99,
    "description": "Grocery shopping",
    "date": "2025-01-15",
    "user_id": 1
  }
]
```

#### Add Expense (`POST /api/expenses`)
- Create new expense entry
- Automatic date defaulting to today
- Category-based organization

**Request:**
```json
{
  "category": "Food",
  "amount": 45.99,
  "description": "Grocery shopping",
  "date": "2025-01-15"
}
```

#### Update Expense (`PUT /api/expenses/{expense_id}`)
- Partial update support
- User ownership validation
- Only owner can modify expenses

**Request:**
```json
{
  "category": "Groceries",
  "amount": 50.00,
  "description": "Updated description"
}
```

#### Delete Expense (`DELETE /api/expenses/{expense_id}`)
- Permanent expense removal
- User ownership validation
- Confirmation message returned

---

### 3. Analytics & Reporting

#### Category Analytics (`GET /api/analytics/category`)
- Expense totals grouped by category
- User-specific data
- Aggregated spending insights

**Response:**
```json
[
  {
    "category": "Food",
    "total": 450.75
  },
  {
    "category": "Transport",
    "total": 120.50
  }
]
```

#### Monthly Analytics (`GET /api/analytics/monthly`)
- Monthly spending trends
- Date-based aggregation
- Chronological ordering
- Month format: YYYY-MM

**Response:**
```json
[
  {
    "month": "2025-01",
    "total": 1250.99
  },
  {
    "month": "2024-12",
    "total": 980.50
  }
]
```

---

### 4. Budget Management (Planned Feature)

#### Data Model
- Category-based budgets
- Monthly/yearly tracking
- Limit amount enforcement
- User ownership

**Schema:**
```json
{
  "id": 1,
  "category": "Food",
  "limit_amount": 500.00,
  "month": 1,
  "year": 2025,
  "user_id": 1
}
```

---

### 5. Debt Management

#### Data Model
- Debt/loan tracking
- EMI calculations
- Interest rate management
- Payment scheduling
- Status tracking (active/paid)

**Schema:**
```json
{
  "id": 1,
  "name": "Car Loan",
  "principal_amount": 20000.00,
  "interest_rate": 5.5,
  "emi_amount": 450.00,
  "emi_date": 15,
  "start_date": "2024-01-15",
  "remaining_amount": 18000.00,
  "status": "active",
  "user_id": 1
}
```

---

### 6. Social Features

#### Friendship System
- Friend request management
- Pending/accepted status tracking
- Bidirectional relationships
- User discovery by username

**Data Model:**
```json
{
  "id": 1,
  "user_id": 1,
  "friend_id": 2,
  "status": "pending",
  "created_at": "2025-01-15T10:30:00",
  "friend_username": "john_doe"
}
```

---

### 7. Split Expenses

#### Create Split Expense
- Multi-participant expense sharing
- Equal split calculation
- Category-based organization
- Date tracking

**Schema:**
```json
{
  "id": 1,
  "description": "Dinner at restaurant",
  "total_amount": 150.00,
  "category": "Food",
  "date": "2025-01-15",
  "created_by": 1,
  "created_at": "2025-01-15T20:30:00",
  "participants": [1, 2, 3],
  "split_amount": 50.00
}
```

#### Features
- Automatic equal split calculation
- Multiple participant support
- Creator tracking
- Participant management via many-to-many relationship

---

### 8. Groups System (Advanced Expense Management)

#### Overview
Comprehensive group expense management system for organized trips, events, shared living, and team expenses with role-based permissions, custom splits, and settlement tracking.

#### Create Group (`POST /api/groups`)
- Creates a new expense group
- Creator automatically becomes admin
- Custom currency support (default: INR)

**Request:**
```json
{
  "name": "Trip to Goa",
  "description": "Planning our vacation expenses",
  "currency": "INR",
  "image_url": "https://example.com/image.jpg"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Trip to Goa",
  "description": "Planning our vacation expenses",
  "currency": "INR",
  "image_url": "https://example.com/image.jpg",
  "is_active": true,
  "created_by": 1,
  "created_at": "2026-01-27T10:00:00",
  "members": [
    {
      "id": 1,
      "user_id": 1,
      "username": "john_doe",
      "role": "admin",
      "status": "accepted",
      "joined_at": "2026-01-27T10:00:00"
    }
  ]
}
```

#### List Groups (`GET /api/groups`)
- Returns all groups where user is a member
- Shows member count and user's role

#### Invite Members (`POST /api/groups/{group_id}/invite`)
- Any group member can invite users
- Invitations require acceptance
- Prevents duplicate invitations

**Request:**
```json
{
  "usernames": ["user2", "user3"]
}
```

**Response:**
```json
{
  "message": "Successfully invited 2 user(s). Users not found: none. Already members: none"
}
```

#### Accept Invitation (`POST /api/groups/{group_id}/join`)
- User accepts pending invitation
- Changes status from "pending" to "accepted"

#### Group Expenses with Custom Splits (`POST /api/groups/{group_id}/expenses`)
- Add expenses with custom split amounts
- Track who paid and who owes what
- Supports unequal splits

**Request:**
```json
{
  "description": "Hotel booking for 3 nights",
  "total_amount": 12000.0,
  "category": "Accommodation",
  "paid_by": 1,
  "participants": [
    {"user_id": 1, "share_amount": 4000.0},
    {"user_id": 2, "share_amount": 4000.0},
    {"user_id": 3, "share_amount": 4000.0}
  ],
  "date": "2026-01-27"
}
```

**Validation:**
- Sum of share_amounts must equal total_amount
- All participants must be group members
- Paid_by user must be a group member

#### Group Balances (`GET /api/groups/{group_id}/balances`)
- Calculate net balances for all members
- Shows who owes whom within the group
- Real-time calculation based on expenses and settlements

**Response:**
```json
{
  "1": {"username": "john_doe", "balance": 8000.0},
  "2": {"username": "jane_smith", "balance": -4000.0},
  "3": {"username": "bob_jones", "balance": -4000.0}
}
```

**Balance Interpretation:**
- Positive balance: Others owe you this amount
- Negative balance: You owe others this amount
- Zero balance: All settled up

#### Settlement Suggestions (`GET /api/groups/{group_id}/settlements/suggestions`)
- Automated payment recommendations
- Minimizes number of transactions using greedy algorithm
- Simplifies complex multi-person debts

**Response:**
```json
[
  {
    "from_username": "jane_smith",
    "to_username": "john_doe",
    "amount": 4000.0
  },
  {
    "from_username": "bob_jones",
    "to_username": "john_doe",
    "amount": 4000.0
  }
]
```

#### Record Settlement (`POST /api/groups/{group_id}/settlements`)
- Record payments between group members
- Updates balance calculations automatically
- Maintains settlement history

**Request:**
```json
{
  "from_user_id": 2,
  "to_user_id": 1,
  "amount": 4000.0
}
```

#### Role-Based Permissions
- **Admin**: Full control - edit group, manage members, edit/delete all expenses
- **Member**: Create expenses, invite others, view balances, record settlements

#### Additional Group Features
- Update group details (admin only)
- Archive groups (admin only)
- Update member roles (admin only)
- Remove members (admin only)
- List all group expenses
- Update/delete expenses (creator or admin)

---

### 9. Balance & Settlement System

#### Get Balances (`GET /api/balances`)
- Calculate net balances between users
- Shows who owes whom
- Real-time balance computation
- Based on split expenses

**Response:**
```json
{
  "you": 25.50,
  "john_doe": -15.00,
  "jane_smith": 10.00
}
```

**Interpretation:**
- Positive value: Others owe you
- Negative value: You owe others
- "you" key shows your net balance

#### Settlement Suggestions (`GET /api/settlements/suggestions`)
- Automated settlement recommendations
- Simplified payment suggestions
- User-friendly format

**Response:**
```json
[
  {
    "from": "john_doe",
    "to": "you",
    "amount": 15.00
  },
  {
    "from": "you",
    "to": "jane_smith",
    "amount": 10.00
  }
]
```

#### Create Settlement (`POST /api/settlements`)
- Record payment between users
- Settlement history tracking
- User validation

**Request:**
```json
{
  "to_username": "john_doe",
  "amount": 15.00
}
```

**Response:**
```json
{
  "id": 1,
  "from_user_id": 1,
  "to_user_id": 2,
  "amount": 15.00,
  "created_at": "2025-01-15T21:00:00"
}
```

---

### 10. Email Notifications

#### SendGrid Integration
- Email service via SendGrid API
- HTML email support
- Configurable sender email
- Error handling and logging

#### Test Email Endpoint (`GET /api/test-email`)
- Test SendGrid configuration
- Verify email delivery
- HTML content support

**Configuration Required:**
- `SENDGRID_API_KEY` environment variable
- `FROM_EMAIL` environment variable

---

## Database Schema

### Tables Overview

1. **users**
   - id (Primary Key)
   - username (Unique)
   - email (Unique)
   - password (Hashed)
   - is_active (Boolean)

2. **expenses**
   - id (Primary Key)
   - category
   - amount
   - date
   - description
   - user_id (Foreign Key)

3. **budgets**
   - id (Primary Key)
   - category
   - limit_amount
   - month
   - year
   - user_id (Foreign Key)

4. **debts**
   - id (Primary Key)
   - name
   - principal_amount
   - interest_rate
   - emi_amount
   - emi_date
   - start_date
   - remaining_amount
   - status
   - user_id (Foreign Key)

5. **friendships**
   - id (Primary Key)
   - user_id (Foreign Key)
   - friend_id (Foreign Key)
   - status
   - created_at

6. **split_expenses**
   - id (Primary Key)
   - description
   - total_amount
   - category
   - date
   - created_by (Foreign Key)
   - created_at

7. **split_participants** (Association Table)
   - split_expense_id (Foreign Key)
   - user_id (Foreign Key)

8. **settlements**
   - id (Primary Key)
   - from_user_id (Foreign Key)
   - to_user_id (Foreign Key)
   - amount
   - created_at

9. **groups**
   - id (Primary Key)
   - name
   - description
   - currency
   - image_url
   - is_active
   - created_by (Foreign Key)
   - created_at

10. **group_members**
    - id (Primary Key)
    - group_id (Foreign Key)
    - user_id (Foreign Key)
    - role (admin/member)
    - status (pending/accepted)
    - joined_at

11. **group_expenses**
    - id (Primary Key)
    - group_id (Foreign Key)
    - description
    - total_amount

### Groups (Advanced Expense Management)
- `GET /api/groups` - List all user's groups
- `POST /api/groups` - Create a new group
- `GET /api/groups/{group_id}` - Get group details
- `PUT /api/groups/{group_id}` - Update group (admin only)
- `DELETE /api/groups/{group_id}` - Archive group (admin only)
- `POST /api/groups/{group_id}/invite` - Invite members
- `POST /api/groups/{group_id}/join` - Accept invitation
- `PUT /api/groups/{group_id}/members/{user_id}` - Update member role (admin only)
- `DELETE /api/groups/{group_id}/members/{user_id}` - Remove member (admin only)
- `GET /api/groups/{group_id}/expenses` - List group expenses
- `POST /api/groups/{group_id}/expenses` - Add group expense
- `PUT /api/groups/{group_id}/expenses/{expense_id}` - Update expense (creator/admin)
- `DELETE /api/groups/{group_id}/expenses/{expense_id}` - Delete expense (creator/admin)
- `GET /api/groups/{group_id}/balances` - Get group balances
- `GET /api/groups/{group_id}/settlements/suggestions` - Get settlement suggestions
- `POST /api/groups/{group_id}/settlements` - Record settlement
    - category
    - paid_by (Foreign Key)
    - date
    - created_at

12. **group_expense_participants**
    - id (Primary Key)
    - group_expense_id (Foreign Key)
    - user_id (Foreign Key)
    - share_amount

13. **group_settlements**
    - id (Primary Key)
    - group_id (Foreign Key)
    - from_user_id (Foreign Key)
    - to_user_id (Foreign Key)
    - amount
    - created_at

---

## API Endpoints Summary

### Authentication
- `POST /api/register` - User registration
- `POST /api/token` - User login (OAuth2)
- `GET /api/users/me` - Get current user

### Expenses
- `GET /api/expenses` - List all expenses
- `POST /api/expenses` - Create expense
- `PUT /api/expenses/{expense_id}` - Update expense
- `DELETE /api/expenses/{expense_id}` - Delete expense

### Analytics
- `GET /api/analytics/category` - Category-wise spending
- `GET /api/analytics/monthly` - Monthly spending trends

### Social & Splitting
- `GET /api/balances` - Get user balances
- `GET /api/settlements/suggestions` - Settlement recommendations
- `POST /api/settlements` - Create settlement

### Utilities
- `GET /` - Root health check
- `GET /ping` - Simple ping endpoint
- `GET /api/test-email` - Test email service

---

## Environment Configuration

### Required Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Authentication
SECRET_KEY=your-secret-key-change-in-production

# Email Service
SENDGRID_API_KEY=your-sendgrid-api-key
FROM_EMAIL=noreply@yourdomain.com
```

### Development Defaults
- Database: `sqlite:///./dev.db` (fallback)
- Token expiration: 30 minutes
- CORS: Multiple origins supported

---

## CORS Configuration

### Allowed Origins
- `http://140.245.14.94:5413`
- `https://expense-tracker-one-eta-34.vercel.app`
- `http://localhost:5173`
- `http://localhost:5413`
- `http://localhost:5174`

### CORS Settings
- Credentials: Enabled
- Methods: All
- Headers: All

---

## Security Features

### Authentication
- JWT tokens with HS256 algorithm
- 30-minute token expiration
- OAuth2 password flow
- Bearer token scheme

### Password Security
- Argon2 hashing algorithm
- No plain-text password storage
- Password verification on login

### Data Protection
- User ownership validation
- CORS whitelist protection
- SQL injection prevention via ORM
- Input validation with Pydantic

---

## Database Features

### ORM Capabilities
- SQLAlchemy relationships
- Cascade delete operations
- Foreign key constraints
- Index optimization

### Connection Management
- Pool pre-ping for cloud databases
- Session factory pattern
- Automatic table creation on startup
- PostgreSQL and SQLite support

---

## Deployment Features

### Docker Support
- Dockerfile included
- Container-ready configuration
- Environment variable support

### Cloud Deployment
- Vercel serverless compatibility (`api/varcel.py`)
- Render.com ready
- PostgreSQL cloud database support
- Health check endpoints

### Logging
- Structured logging with Python's logging module
- Startup event logging
- Error tracking and reporting
- Database connection monitoring

---

## API Response Standards

### Success Responses
- 200 OK - Successful GET/PUT/DELETE
- 201 Created - Successful POST (implicit)

### Error Responses
- 400 Bad Request - Validation errors, duplicate entries
- 401 Unauthorized - Authentication failure
- 404 Not Found - Resource not found
- 422 Unprocessable Entity - Validation errors

### Response Format
All responses follow Pydantic schema validation with consistent structure.

---

## Development Features

### Hot Reload
- Uvicorn with `--reload` flag
- Automatic code change detection

### Database Migrations
- Automatic table creation on startup
- Schema evolution support via SQLAlchemy

### API Documentation
- Auto-generated OpenAPI docs at `/docs`
- ReDoc documentation at `/redoc`
- Interactive API testing interface

---

## Planned Features (Future Enhancements)

Based on the schema, these features are modeled but may need route implementation:

1. **Budget Alerts** - Notifications when spending exceeds limits
2. **Friend Management** - Complete friend request/accept workflow
3. **Debt Reminders** - EMI payment notifications
4. **Recurring Expenses** - Automatic expense creation
5. **Export Data** - CSV/PDF report generation
6. **Multi-currency** - Support for different currencies
7. **Expense Categories** - Custom category management
8. **Split Percentage** - Non-equal expense splitting

---

## Performance Considerations

### Database Optimization
- Indexed columns for quick lookups (username, email)
- Connection pooling with pre-ping
- Efficient query patterns with SQLAlchemy

### API Performance
- Async route handlers with FastAPI
- Lazy loading of relationships
- Minimal database queries per request

---

## Testing Endpoints

### Health Checks
- `GET /` - Backend status
- `GET /ping` - Simple connectivity test

### Email Testing
- `GET /api/test-email` - SendGrid integration verification

---

## Version History

**v3.0.0** (Current - January 2026)
- Complete Groups system with role-based permissions
- Custom expense splits with flexible share amounts
- Group balance calculation and settlement tracking
- Settlement optimization algorithm
- Member invitation and management
- Username-based member invitations
- Support for organized trips, events, and shared living

**v2.0.0**
- Complete expense management system
- Social features with split expenses
- Settlement system
- Analytics dashboard support
- Email integration
- JWT authentication
- Multi-user support

---

## Getting Started

### Installation
```bash
pip install -r requirements.txt
```

### Run Development Server
```bash
uvicorn app.main:app --reload
```

### Access API
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Support & Documentation

### API Documentation
- Interactive docs available at `/docs`
- Schema definitions in `app/schemas.py`
- Model definitions in `app/models.py`

### Error Handling
- Comprehensive HTTP exception handling
- Descriptive error messages
- Validation error details from Pydantic

---

**Last Updated:** January 2025
**Maintained By:** Expense Tracker Team
