"""Test split expense creation"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

# First login to get token
login_data = {
    "username": "testuser1",
    "password": "password123"
}

print("Logging in...")
response = requests.post(f"{BASE_URL}/token", data=login_data)
if response.status_code == 200:
    token = response.json()["access_token"]
    print(f"✅ Login successful! Token: {token[:20]}...")
else:
    print(f"❌ Login failed: {response.status_code}")
    print(response.text)
    exit(1)

# Now try to create a split expense
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Test 1: With all required fields
print("\n--- Test 1: Complete data ---")
split_expense_data = {
    "description": "Dinner at restaurant",
    "total_amount": 150.50,
    "category": "Food",
    "date": "2026-01-20",
    "participant_usernames": ["testuser2", "testuser3"]
}

print(f"Request data: {json.dumps(split_expense_data, indent=2)}")
response = requests.post(f"{BASE_URL}/split-expenses", headers=headers, json=split_expense_data)
print(f"Response status: {response.status_code}")
print(f"Response: {response.text}")

# Test 2: Without date (should use default)
print("\n--- Test 2: Without date ---")
split_expense_data2 = {
    "description": "Movie tickets",
    "total_amount": 60.0,
    "category": "Entertainment",
    "participant_usernames": ["testuser2"]
}

print(f"Request data: {json.dumps(split_expense_data2, indent=2)}")
response2 = requests.post(f"{BASE_URL}/split-expenses", headers=headers, json=split_expense_data2)
print(f"Response status: {response2.status_code}")
print(f"Response: {response2.text}")

# Test 3: Check what validation error looks like with bad data
print("\n--- Test 3: Missing required field (should fail) ---")
split_expense_data3 = {
    "description": "Test",
    "category": "Food"
    # Missing total_amount
}

print(f"Request data: {json.dumps(split_expense_data3, indent=2)}")
response3 = requests.post(f"{BASE_URL}/split-expenses", headers=headers, json=split_expense_data3)
print(f"Response status: {response3.status_code}")
print(f"Response: {json.dumps(response3.json(), indent=2)}")
