"""
Test Configuration and Utilities
"""
import pytest
import requests
from typing import Dict, Any

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_TIMEOUT = 30  # seconds

# Test user credentials
DEFAULT_TEST_USERS = {
    "user1": {"username": "testuser1", "email": "test1@example.com", "password": "password123"},
    "user2": {"username": "testuser2", "email": "test2@example.com", "password": "password123"},
    "user3": {"username": "testuser3", "email": "test3@example.com", "password": "password123"},
}


def create_test_user(username: str, email: str, password: str) -> Dict[str, Any]:
    """
    Create a test user and return their credentials and token
    
    Returns:
        dict with keys: username, email, password, token, user_id
    """
    # Register user (may already exist)
    requests.post(
        f"{BASE_URL}/api/register",
        json={"username": username, "email": email, "password": password}
    )
    
    # Login to get token
    login_response = requests.post(
        f"{BASE_URL}/api/token",
        data={"username": username, "password": password},
        timeout=TEST_TIMEOUT
    )
    
    if login_response.status_code != 200:
        raise Exception(f"Failed to login test user: {login_response.text}")
    
    token = login_response.json()["access_token"]
    
    # Get user info
    user_response = requests.get(
        f"{BASE_URL}/api/users/me",
        headers={"Authorization": f"Bearer {token}"},
        timeout=TEST_TIMEOUT
    )
    
    if user_response.status_code != 200:
        raise Exception(f"Failed to get user info: {user_response.text}")
    
    user_info = user_response.json()
    
    return {
        "username": username,
        "email": email,
        "password": password,
        "token": token,
        "user_id": user_info["id"],
        "headers": {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    }


def cleanup_test_data(token: str):
    """
    Clean up test data for a user
    Note: This doesn't delete the user, just their data
    """
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Delete expenses
        expenses_response = requests.get(f"{BASE_URL}/api/expenses", headers=headers)
        if expenses_response.status_code == 200:
            for expense in expenses_response.json():
                requests.delete(f"{BASE_URL}/api/expenses/{expense['id']}", headers=headers)
        
        # Delete budgets
        budgets_response = requests.get(f"{BASE_URL}/api/budgets", headers=headers)
        if budgets_response.status_code == 200:
            for budget in budgets_response.json():
                requests.delete(f"{BASE_URL}/api/budgets/{budget['id']}", headers=headers)
        
        # Delete debts
        debts_response = requests.get(f"{BASE_URL}/api/debts", headers=headers)
        if debts_response.status_code == 200:
            for debt in debts_response.json():
                requests.delete(f"{BASE_URL}/api/debts/{debt['id']}", headers=headers)
    except Exception as e:
        print(f"Warning: Error during cleanup: {e}")


@pytest.fixture(scope="session")
def base_url():
    """Provide base URL for tests"""
    return BASE_URL


@pytest.fixture(scope="session")
def check_server():
    """Check if server is running before tests"""
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code != 200:
            pytest.exit("Backend server is not running! Start it with: python -m uvicorn app.main:app --reload")
    except requests.exceptions.ConnectionError:
        pytest.exit(f"Cannot connect to backend server at {BASE_URL}! Make sure it's running.")
    
    print(f"\n✓ Backend server is running at {BASE_URL}")


@pytest.fixture(scope="function")
def auth_headers():
    """Provide authentication headers for a test user"""
    user = create_test_user("testuser1", "test1@example.com", "password123")
    return user["headers"]


@pytest.fixture(scope="function")
def test_user():
    """Provide a complete test user with authentication"""
    return create_test_user("testuser1", "test1@example.com", "password123")


@pytest.fixture(scope="function")
def multiple_test_users():
    """Provide multiple test users"""
    users = {}
    for key, data in DEFAULT_TEST_USERS.items():
        users[key] = create_test_user(data["username"], data["email"], data["password"])
    return users
