"""
Quick script to test all failing test cases and document fixes needed
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# Setup test user
username = "fix_tester"
password = "password123"
email = "fixtester@example.com"

# Register and login
requests.post(f"{BASE_URL}/api/register", json={"username": username, "email": email, "password": password})
login_response = requests.post(f"{BASE_URL}/api/token", data={"username": username, "password": password})
token = login_response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

print("\n" + "="*70)
print("TESTING FAILING TEST CASES")
print("="*70)

# Test 1: Get expense by ID (expecting 405 - Method not allowed)
print("\n1. Test get expense by ID:")
exp_response = requests.post(f"{BASE_URL}/api/expenses", json={"category": "Test", "amount": 100}, headers=headers)
if exp_response.status_code == 200:
    exp_id = exp_response.json()["id"]
    get_response = requests.get(f"{BASE_URL}/api/expenses/{exp_id}", headers=headers)
    print(f"   GET /api/expenses/{exp_id}: {get_response.status_code}")
    if get_response.status_code == 405:
        print("   ❌ ISSUE: Endpoint does not exist (405 Method Not Allowed)")
    else:
        print("   ✓ Works correctly")

# Test 2: Delete expense (expecting 204 but getting 200)
print("\n2. Test delete expense:")
exp_response = requests.post(f"{BASE_URL}/api/expenses", json={"category": "Test", "amount": 100}, headers=headers)
if exp_response.status_code == 200:
    exp_id = exp_response.json()["id"]
    del_response = requests.delete(f"{BASE_URL}/api/expenses/{exp_id}", headers=headers)
    print(f"   DELETE /api/expenses/{exp_id}: {del_response.status_code}")
    if del_response.status_code == 200:
        print("   ⚠️  Returns 200 instead of 204 (no content)")
    elif del_response.status_code == 204:
        print("   ✓ Works correctly")

# Test 3: Create debt (422 error)
print("\n3. Test create debt:")
debt_data = {
    "name": "Test Loan",
    "principal_amount": 10000.0,
    "interest_rate": 10.0,
    "emi_amount": 1000.0,
    "emi_date": 5
}
debt_response = requests.post(f"{BASE_URL}/api/debts", json=debt_data, headers=headers)
print(f"   POST /api/debts: {debt_response.status_code}")
if debt_response.status_code != 200:
    print(f"   ❌ ERROR: {debt_response.json()}")
else:
    print("   ✓ Works correctly")

# Test 4: Send friend request (400 error)
print("\n4. Test send friend request:")
# Create another user first
friend_username = "friend_test_user"
requests.post(f"{BASE_URL}/api/register", json={"username": friend_username, "email": "friend@example.com", "password": "password123"})

friend_req_response = requests.post(
    f"{BASE_URL}/api/friends/request",
    json={"friend_username": friend_username},
    headers=headers
)
print(f"   POST /api/friends/request: {friend_req_response.status_code}")
if friend_req_response.status_code != 200:
    print(f"   ❌ ERROR: {friend_req_response.json()}")
else:
    print("   ✓ Works correctly")

# Test 5: Create split expense (422 error)
print("\n5. Test create split expense:")
split_data = {
    "description": "Test split",
    "total_amount": 1000.0,
    "category": "Food",
    "participant_usernames": [friend_username]
}
split_response = requests.post(f"{BASE_URL}/api/split-expenses", json=split_data, headers=headers)
print(f"   POST /api/split-expenses: {split_response.status_code}")
if split_response.status_code != 200:
    print(f"   ❌ ERROR: {split_response.json()}")
else:
    print("   ✓ Works correctly")

# Test 6: Create group expense (422 error)
print("\n6. Test create group expense:")
# Create a group first
group_response = requests.post(f"{BASE_URL}/api/groups", json={"name": "Test Group"}, headers=headers)
if group_response.status_code in [200, 201]:
    group_id = group_response.json()["id"]
    
    # Get user IDs
    me_response = requests.get(f"{BASE_URL}/api/users/me", headers=headers)
    my_id = me_response.json()["id"]
    
    group_exp_data = {
        "description": "Group test",
        "total_amount": 2000.0,
        "category": "Food",
        "split_type": "equal",
        "participant_ids": [my_id]
    }
    group_exp_response = requests.post(f"{BASE_URL}/api/groups/{group_id}/expenses", json=group_exp_data, headers=headers)
    print(f"   POST /api/groups/{group_id}/expenses: {group_exp_response.status_code}")
    if group_exp_response.status_code != 200:
        print(f"   ❌ ERROR: {group_exp_response.json()}")
    else:
        print("   ✓ Works correctly")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print("Run this script to see specific API issues with test cases")
print("="*70)
