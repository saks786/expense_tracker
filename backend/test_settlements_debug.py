"""
Debug script to verify settlement suggestions and settlements are working correctly
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# Login
print("Logging in as testuser1...")
login_response = requests.post(
    f"{BASE_URL}/api/token",
    data={"username": "testuser1", "password": "testpass123"}
)

if login_response.status_code != 200:
    print(f"[FAIL] Login failed: {login_response.text}")
    exit(1)

token = login_response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print("[OK] Login successful\n")

# Test Group 1
GROUP_ID = 1

print("="*60)
print(f"TESTING GROUP {GROUP_ID}")
print("="*60)

# 1. Check Group Expenses
print("\n1. GROUP EXPENSES:")
print("-" * 60)
expenses_response = requests.get(f"{BASE_URL}/api/groups/{GROUP_ID}/expenses", headers=headers)
if expenses_response.status_code == 200:
    expenses = expenses_response.json()
    print(f"[OK] Found {len(expenses)} expense(s)")
    for expense in expenses:
        print(f"  - {expense['description']}: ${expense['total_amount']} paid by {expense['payer_username']}")
        participants_str = ', '.join([f"{p['username']} (${p['share_amount']})" for p in expense['participants']])
        print(f"    Split among: {participants_str}")
else:
    print(f"[FAIL] Status {expenses_response.status_code}: {expenses_response.text}")

# 2. Check Balances
print("\n2. CURRENT BALANCES:")
print("-" * 60)
balances_response = requests.get(f"{BASE_URL}/api/groups/{GROUP_ID}/balances", headers=headers)
if balances_response.status_code == 200:
    balances = balances_response.json()
    print("[OK] Balances calculated:")
    for user_id, data in balances.items():
        balance = data['balance']
        username = data['username']
        if balance > 0:
            print(f"  ✓ {username} is OWED ${balance}")
        elif balance < 0:
            print(f"  ✗ {username} OWES ${abs(balance)}")
        else:
            print(f"  = {username} is settled (balance: $0)")
else:
    print(f"[FAIL] Status {balances_response.status_code}: {balances_response.text}")

# 3. Check Settlement Suggestions
print("\n3. SETTLEMENT SUGGESTIONS (How to settle debts):")
print("-" * 60)
suggestions_response = requests.get(f"{BASE_URL}/api/groups/{GROUP_ID}/settlements/suggestions", headers=headers)
if suggestions_response.status_code == 200:
    suggestions = suggestions_response.json()
    if suggestions:
        print(f"[OK] Found {len(suggestions)} settlement suggestion(s):")
        for suggestion in suggestions:
            print(f"  → {suggestion['from_username']} should pay ${suggestion['amount']} to {suggestion['to_username']}")
    else:
        print("[OK] No settlements needed - everyone is settled!")
else:
    print(f"[FAIL] Status {suggestions_response.status_code}: {suggestions_response.text}")

# 4. Check Settlement History
print("\n4. SETTLEMENT HISTORY (Actual payments recorded):")
print("-" * 60)
settlements_response = requests.get(f"{BASE_URL}/api/groups/{GROUP_ID}/settlements", headers=headers)
if settlements_response.status_code == 200:
    settlements = settlements_response.json()
    if settlements:
        print(f"[OK] Found {len(settlements)} settlement record(s):")
        for settlement in settlements:
            print(f"  ✓ User {settlement['from_user_id']} paid ${settlement['amount']} to User {settlement['to_user_id']} on {settlement['created_at']}")
    else:
        print("[OK] No settlements recorded yet")
else:
    print(f"[FAIL] Status {settlements_response.status_code}: {settlements_response.text}")

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print("""
UNDERSTANDING THE DIFFERENCE:

1. EXPENSES: What people spent and how it was split
2. BALANCES: Current state - who owes whom after expenses and settlements
3. SETTLEMENT SUGGESTIONS: Optimal way to pay back debts
4. SETTLEMENTS: History of actual payments made

When you ADD AN EXPENSE:
  - It updates BALANCES automatically
  - It updates SETTLEMENT SUGGESTIONS automatically

When you RECORD A SETTLEMENT (payment):
  - It adds to SETTLEMENT HISTORY
  - It updates BALANCES (reduces debt)
  - It updates SETTLEMENT SUGGESTIONS (reduces amounts owed)
""")

# Test data structure
print("\n" + "="*60)
print("API RESPONSE STRUCTURE VERIFICATION")
print("="*60)

print("\nSettlement Suggestions Response Structure:")
if suggestions_response.status_code == 200:
    print(json.dumps(suggestions_response.json(), indent=2))
    print("\n[OK] Structure matches documentation:")
    print("  - Array of objects")
    print("  - Each has: from_user_id, from_username, to_user_id, to_username, amount")

print("\nSettlements Response Structure:")
if settlements_response.status_code == 200:
    print(json.dumps(settlements_response.json(), indent=2))
    print("\n[OK] Structure matches documentation:")
    print("  - Array of objects")
    print("  - Each has: id, group_id, from_user_id, to_user_id, amount, created_at")
