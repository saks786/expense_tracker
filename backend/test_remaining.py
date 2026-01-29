"""
Simple diagnostic for remaining test failures
"""
import requests
import json
from datetime import date

BASE_URL = "http://localhost:8000"

# Setup
username = "diag_user"
password = "password123"
email = "diag@example.com"

requests.post(f"{BASE_URL}/api/register", json={"username": username, "email": email, "password": password})
login_response = requests.post(f"{BASE_URL}/api/token", data={"username": username, "password": password})
token = login_response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

print("\nDiagnosing 3 remaining failures:")
print("="*70)

# Test 1: Create debt with start_date=None
print("\n1. CREATE DEBT:")
debt_data = {
    "name": "Personal Loan",
    "principal_amount": 50000.0,
    "remaining_amount": 50000.0,
    "interest_rate": 10.5,
    "emi_amount": 5000.0,
    "emi_date": 5,
    "start_date": None
}
response = requests.post(f"{BASE_URL}/api/debts", json=debt_data, headers=headers)
print(f"   Status: {response.status_code}")
if response.status_code != 200:
    error = response.json()
    print(f"   Error: {json.dumps(error, indent=6)}")

# Test 2: Send friend request
print("\n2. SEND FRIEND REQUEST:")
friend_username = "diag_friend"
requests.post(f"{BASE_URL}/api/register", json={"username": friend_username, "email": "diagfriend@example.com", "password": "password123"})

response = requests.post(
    f"{BASE_URL}/api/friends/request",
    json={"friend_username": friend_username},
    headers=headers
)
print(f"   Status: {response.status_code}")
if response.status_code != 200:
    error = response.json()
    print(f"   Error: {json.dumps(error, indent=6)}")

# Test 3: Create group expense  
print("\n3. CREATE GROUP EXPENSE:")
group_response = requests.post(f"{BASE_URL}/api/groups", json={"name": "Diag Group"}, headers=headers)
if group_response.status_code in [200, 201]:
    group_id = group_response.json()["id"]
    me_response = requests.get(f"{BASE_URL}/api/users/me", headers=headers)
    my_id = me_response.json()["id"]
    
    expense_data = {
        "description": "Group test",
        "total_amount": 2000.0,
        "category": "Food",
        "split_type": "equal",
        "paid_by": my_id,
        "participants": [
            {
                "user_id": my_id,
                "amount_owed": 2000.0
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/api/groups/{group_id}/expenses", json=expense_data, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code != 200:
        error = response.json()
        print(f"   Error: {json.dumps(error, indent=6)}")

print("\n" + "="*70)
