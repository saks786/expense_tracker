# Expense Tracker - Testing Guide

## 📋 Overview

Comprehensive testing suite for the Expense Tracker backend API covering:
- ✅ Unit tests for all endpoints
- ✅ Integration tests for workflows
- ✅ End-to-end user journey tests
- ✅ Authentication and authorization tests

---

## 🚀 Quick Start

### 1. Install Testing Dependencies

```bash
pip install pytest pytest-cov requests
```

### 2. Start the Backend Server

```bash
python -m uvicorn app.main:app --reload
```

### 3. Run All Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_backend.py -v

# Run specific test class
pytest tests/test_backend.py::TestAuthentication -v

# Run specific test
pytest tests/test_backend.py::TestAuthentication::test_login -v
```

---

## 📂 Test Structure

```
tests/
├── conftest.py              # Test configuration and fixtures
├── test_backend.py          # Complete backend API tests
├── test_e2e.py             # End-to-end integration tests
└── .gitignore              # Test artifacts to ignore
```

---

## 🧪 Test Files

### 1. `test_backend.py` - Complete Backend API Tests

**Coverage:**
- ✅ Authentication (register, login, get user)
- ✅ Expenses (CRUD operations)
- ✅ Budgets (create, update, list)
- ✅ Debts (create, pay EMI, manage)
- ✅ Friendships (request, accept, list)
- ✅ Split Expenses (create, view balances, settle)
- ✅ Groups (create, invite, join, expenses, balances)

**Run:**
```bash
pytest tests/test_backend.py -v -s
```

**Output:**
```
TestAuthentication::test_register_new_user PASSED
TestAuthentication::test_login PASSED
TestAuthentication::test_get_current_user PASSED
TestExpenses::test_create_expense PASSED
TestExpenses::test_list_expenses PASSED
...
```

---

### 2. `test_e2e.py` - End-to-End Integration Tests

**Coverage:**
- ✅ Complete expense tracking workflow
- ✅ Friendship and split expense workflow
- ✅ Group management workflow
- ✅ Complete user journey from registration to complex operations

**Run:**
```bash
pytest tests/test_e2e.py -v -s
```

**Workflows Tested:**

#### Workflow 1: Expense Tracking
1. Create multiple expenses
2. Set budgets for categories
3. Create debts
4. View analytics

#### Workflow 2: Friendship & Splits
1. Send friend requests
2. Accept requests
3. Create split expenses
4. View balances
5. Settle up

#### Workflow 3: Group Management
1. Create group
2. Invite members (must be friends)
3. Accept invitations
4. Create group expenses
5. View balances
6. Get settlement suggestions

#### Workflow 4: Complete User Journey
1. Register new user
2. Login
3. Add expenses
4. Set budgets
5. Send friend requests
6. View profile

---

### 3. `conftest.py` - Test Configuration

**Provides:**
- ✅ Test fixtures for authentication
- ✅ Helper functions for creating test users
- ✅ Server connectivity checks
- ✅ Cleanup utilities

**Key Fixtures:**
```python
# Single authenticated user
def test_with_user(test_user):
    # test_user has: username, email, token, user_id, headers
    pass

# Multiple test users
def test_with_multiple_users(multiple_test_users):
    # multiple_test_users = {user1: {...}, user2: {...}, user3: {...}}
    pass

# Just auth headers
def test_with_auth(auth_headers):
    # auth_headers = {"Authorization": "Bearer token", "Content-Type": "..."}
    pass
```

---

## 🎯 Running Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run with Coverage
```bash
pytest tests/ --cov=app --cov-report=html
```

### Run Specific Category
```bash
# Only authentication tests
pytest tests/test_backend.py::TestAuthentication -v

# Only expense tests
pytest tests/test_backend.py::TestExpenses -v

# Only group tests
pytest tests/test_backend.py::TestGroups -v
```

### Run E2E Tests Only
```bash
pytest tests/test_e2e.py -v -s
```

### Run with Verbose Output
```bash
pytest tests/ -v -s
```

### Run and Stop on First Failure
```bash
pytest tests/ -x
```

### Run in Parallel (faster)
```bash
pip install pytest-xdist
pytest tests/ -n auto
```

---

## 📊 Test Coverage

### Generate Coverage Report
```bash
pytest tests/ --cov=app --cov-report=term-missing
```

### Generate HTML Coverage Report
```bash
pytest tests/ --cov=app --cov-report=html
# Open htmlcov/index.html in browser
```

---

## 🔧 Configuration

### Update Test Server URL

Edit `conftest.py`:
```python
BASE_URL = "http://localhost:8000"  # Change if needed
```

### Update Test Users

Edit `conftest.py`:
```python
DEFAULT_TEST_USERS = {
    "user1": {"username": "testuser1", "email": "test1@example.com", "password": "password123"},
    "user2": {"username": "testuser2", "email": "test2@example.com", "password": "password123"},
    # Add more users as needed
}
```

---

## ✅ Test Checklist

Before deploying, ensure all tests pass:

- [ ] **Authentication Tests**
  - [ ] Register new user
  - [ ] Login with valid credentials
  - [ ] Get current user info
  - [ ] Reject invalid credentials

- [ ] **Expense Tests**
  - [ ] Create expense
  - [ ] List all expenses
  - [ ] Get expense by ID
  - [ ] Update expense
  - [ ] Delete expense

- [ ] **Budget Tests**
  - [ ] Create budget
  - [ ] List budgets
  - [ ] Update budget

- [ ] **Debt Tests**
  - [ ] Create debt
  - [ ] List debts
  - [ ] Pay EMI

- [ ] **Friendship Tests**
  - [ ] Send friend request
  - [ ] List friend requests
  - [ ] Accept friend request
  - [ ] List friends

- [ ] **Split Expense Tests**
  - [ ] Create split expense
  - [ ] List split expenses
  - [ ] Get balances
  - [ ] Create settlement

- [ ] **Group Tests**
  - [ ] Create group
  - [ ] List groups
  - [ ] Invite to group
  - [ ] Get pending invitations
  - [ ] Accept invitation
  - [ ] Create group expense
  - [ ] Get group balances

- [ ] **E2E Workflows**
  - [ ] Complete expense tracking workflow
  - [ ] Complete friendship workflow
  - [ ] Complete group workflow
  - [ ] Complete user journey

---

## 🐛 Debugging Tests

### Show Print Statements
```bash
pytest tests/ -v -s
```

### Show Full Error Tracebacks
```bash
pytest tests/ -v --tb=long
```

### Run Specific Test with Debugging
```bash
pytest tests/test_backend.py::TestGroups::test_create_group -v -s --tb=long
```

### Use PDB Debugger
```bash
pytest tests/ --pdb  # Drop into debugger on failure
```

---

## 🎨 Example Test Output

```
================================ test session starts ================================
platform win32 -- Python 3.11.0, pytest-7.4.0
collected 45 items

tests/test_backend.py::TestAuthentication::test_register_new_user PASSED    [  2%]
tests/test_backend.py::TestAuthentication::test_login PASSED                [  4%]
tests/test_backend.py::TestAuthentication::test_get_current_user PASSED     [  6%]
tests/test_backend.py::TestExpenses::test_create_expense PASSED             [  8%]
tests/test_backend.py::TestExpenses::test_list_expenses PASSED              [ 11%]
tests/test_backend.py::TestExpenses::test_get_expense_by_id PASSED          [ 13%]
tests/test_backend.py::TestGroups::test_create_group PASSED                 [ 91%]
tests/test_backend.py::TestGroups::test_invite_to_group PASSED              [ 93%]
tests/test_backend.py::TestGroups::test_accept_group_invitation PASSED      [ 95%]

================================ 45 passed in 12.34s ================================
```

---

## 📝 Writing New Tests

### Basic Test Structure

```python
import pytest
import requests

class TestMyFeature:
    """Test my new feature"""
    
    def test_something(self, test_user):
        """Test description"""
        # Arrange
        data = {"key": "value"}
        
        # Act
        response = requests.post(
            f"{BASE_URL}/api/my-endpoint",
            headers=test_user["headers"],
            json=data
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["key"] == "value"
```

### Using Fixtures

```python
def test_with_multiple_users(multiple_test_users):
    user1 = multiple_test_users["user1"]
    user2 = multiple_test_users["user2"]
    
    # Test interaction between users
    pass
```

---

## 🚨 Common Issues

### Issue: "Cannot connect to backend server"
**Solution:** Start the backend server:
```bash
python -m uvicorn app.main:app --reload
```

### Issue: "Test user already exists"
**Solution:** Tests handle this automatically. Users are reused if they exist.

### Issue: "Token expired"
**Solution:** Tokens are refreshed for each test session automatically.

### Issue: Tests fail with "422 Unprocessable Entity"
**Solution:** Check the request data format matches the API schema.

---

## 🎯 Continuous Integration

### GitHub Actions Example

```yaml
name: Run Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        python -m uvicorn app.main:app &
        sleep 5
        pytest tests/ -v --cov=app
```

---

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Requests Library](https://requests.readthedocs.io/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

---

## ✨ Best Practices

1. **Run tests before committing**: `pytest tests/ -v`
2. **Keep tests independent**: Each test should work alone
3. **Use fixtures**: Reuse setup code with fixtures
4. **Test edge cases**: Test error conditions too
5. **Keep tests fast**: Mock external services
6. **Write descriptive test names**: Clear what's being tested
7. **Use assertions**: Check actual vs expected results
8. **Clean up after tests**: Use fixtures for cleanup

---

## 🎉 Success!

If all tests pass, you're ready to deploy! 🚀

```bash
$ pytest tests/ -v

================================ 45 passed in 12.34s ================================

✅ All tests passed! Your backend is ready!
```
