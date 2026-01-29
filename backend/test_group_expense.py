"""
Test script for group expense creation
Run this to verify the API endpoint works and see detailed error messages
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# First, login to get a token
def login(username="testuser", password="testpass123"):
    response = requests.post(
        f"{BASE_URL}/api/token",
        data={"username": username, "password": password}
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Login failed: {response.status_code}")
        print(response.text)
        return None

# Test creating a group expense
def test_create_group_expense(token, group_id=1):
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test data - adjust user IDs as needed
    expense_data = {
        "description": "Test Grocery shopping",
        "total_amount": 2000.0,
        "category": "Groceries",
        "paid_by": 1,  # Make sure this user ID exists and is a member
        "participants": [
            {
                "user_id": 1,
                "share_amount": 1000.0
            },
            {
                "user_id": 2,
                "share_amount": 1000.0
            }
        ]
    }
    
    print(f"\nTesting POST /api/groups/{group_id}/expenses")
    print(f"Request body:")
    print(json.dumps(expense_data, indent=2))
    
    response = requests.post(
        f"{BASE_URL}/api/groups/{group_id}/expenses",
        headers=headers,
        json=expense_data
    )
    
    print(f"\nResponse Status: {response.status_code}")
    print(f"Response Body:")
    print(json.dumps(response.json(), indent=2))
    
    return response.status_code == 201

if __name__ == "__main__":
    print("=== Group Expense Creation Test ===\n")
    
    # Get credentials
    username = input("Enter username (default: testuser): ").strip() or "testuser"
    password = input("Enter password (default: testpass123): ").strip() or "testpass123"
    group_id = input("Enter group ID (default: 1): ").strip() or "1"
    
    # Login
    print(f"\nLogging in as {username}...")
    token = login(username, password)
    
    if not token:
        print("\n❌ Login failed. Please check credentials.")
        exit(1)
    
    print("✓ Login successful")
    
    # Test expense creation
    success = test_create_group_expense(token, int(group_id))
    
    if success:
        print("\n✓ Group expense created successfully!")
    else:
        print("\n❌ Failed to create group expense. Check error above.")
