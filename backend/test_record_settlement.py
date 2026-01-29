"""
Test recording a settlement and verify balances update correctly
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# Login
print("Logging in as testuser2...")
login_response = requests.post(
    f"{BASE_URL}/api/token",
    data={"username": "testuser2", "password": "testpass123"}
)

if login_response.status_code != 200:
    print(f"[FAIL] Login failed. Creating testuser2...")
    # Try to register
    register_response = requests.post(
        f"{BASE_URL}/api/register",
        json={"username": "testuser2", "email": "testuser2@example.com", "password": "testpass123"}
    )
    if register_response.status_code == 200:
        print("[OK] User created")
        login_response = requests.post(f"{BASE_URL}/api/token", data={"username": "testuser2", "password": "testpass123"})
    else:
        print(f"[FAIL] Could not create user")
        exit(1)

token = login_response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print("[OK] Login successful\n")

GROUP_ID = 1

print("="*60)
print("BEFORE RECORDING SETTLEMENT")
print("="*60)

# Check balances before
print("\nCurrent Balances:")
balances_response = requests.get(f"{BASE_URL}/api/groups/{GROUP_ID}/balances", headers=headers)
if balances_response.status_code == 200:
    balances = balances_response.json()
    for user_id, data in balances.items():
        print(f"  User {user_id} ({data['username']}): ${data['balance']}")
else:
    print(f"[FAIL] Status {balances_response.status_code}")

print("\nCurrent Settlement Suggestions:")
suggestions_response = requests.get(f"{BASE_URL}/api/groups/{GROUP_ID}/settlements/suggestions", headers=headers)
if suggestions_response.status_code == 200:
    suggestions = suggestions_response.json()
    for s in suggestions:
        print(f"  {s['from_username']} → {s['to_username']}: ${s['amount']}")

# Record a settlement - testuser2 pays testuser1 $100
print("\n" + "="*60)
print("RECORDING SETTLEMENT: testuser2 pays testuser1 $100")
print("="*60)

settlement_data = {
    "to_user_id": 1,  # testuser1
    "amount": 100.0
}

settlement_response = requests.post(
    f"{BASE_URL}/api/groups/{GROUP_ID}/settlements",
    headers=headers,
    json=settlement_data
)

print(f"\nPOST /api/groups/{GROUP_ID}/settlements")
print(f"Request: {json.dumps(settlement_data, indent=2)}")
print(f"Status: {settlement_response.status_code}")
print(f"Response: {json.dumps(settlement_response.json(), indent=2) if settlement_response.status_code in [200, 201] else settlement_response.text}")

if settlement_response.status_code not in [200, 201]:
    print("\n[FAIL] Settlement recording failed!")
    exit(1)

# Check balances after
print("\n" + "="*60)
print("AFTER RECORDING SETTLEMENT")
print("="*60)

print("\nUpdated Balances:")
balances_response = requests.get(f"{BASE_URL}/api/groups/{GROUP_ID}/balances", headers=headers)
if balances_response.status_code == 200:
    balances = balances_response.json()
    for user_id, data in balances.items():
        print(f"  User {user_id} ({data['username']}): ${data['balance']}")
else:
    print(f"[FAIL] Status {balances_response.status_code}")

print("\nUpdated Settlement Suggestions:")
suggestions_response = requests.get(f"{BASE_URL}/api/groups/{GROUP_ID}/settlements/suggestions", headers=headers)
if suggestions_response.status_code == 200:
    suggestions = suggestions_response.json()
    if suggestions:
        for s in suggestions:
            print(f"  {s['from_username']} → {s['to_username']}: ${s['amount']}")
    else:
        print("  No settlements needed - all balanced!")

print("\nAll Settlements History:")
settlements_response = requests.get(f"{BASE_URL}/api/groups/{GROUP_ID}/settlements", headers=headers)
if settlements_response.status_code == 200:
    settlements = settlements_response.json()
    for settlement in settlements:
        print(f"  Settlement {settlement['id']}: User {settlement['from_user_id']} → User {settlement['to_user_id']}: ${settlement['amount']}")

print("\n" + "="*60)
print("VERIFICATION")
print("="*60)
print("""
Expected behavior:
1. testuser2's balance should INCREASE by $100 (debt reduced)
2. testuser1's balance should DECREASE by $100 (credit reduced)
3. Settlement should appear in history
4. Settlement suggestions should update to reflect new balances
""")
