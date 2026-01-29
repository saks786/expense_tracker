"""
Quick test script to verify self-invitation and transaction issues
"""
import requests

BASE_URL = "http://localhost:8000"

def test_self_invitation():
    """Test the self-invitation issue"""
    print("\n" + "="*70)
    print("TESTING SELF-INVITATION")
    print("="*70)
    
    # Register and login as user
    username = "selftest_user"
    password = "password123"
    email = "selftest@example.com"
    
    # Register
    reg_response = requests.post(
        f"{BASE_URL}/api/register",
        json={"username": username, "email": email, "password": password}
    )
    print(f"Register: {reg_response.status_code}")
    
    # Login
    login_response = requests.post(
        f"{BASE_URL}/api/token",
        data={"username": username, "password": password}
    )
    
    if login_response.status_code != 200:
        print(f"Login failed: {login_response.text}")
        return
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Create a group
    group_response = requests.post(
        f"{BASE_URL}/api/groups",
        json={"name": "Test Group", "description": "Testing self-invitation"},
        headers=headers
    )
    
    if group_response.status_code not in [200, 201]:
        print(f"Group creation failed: {group_response.text}")
        return
    
    group_data = group_response.json()
    group_id = group_data["id"]
    print(f"✓ Created group: {group_id}")
    print(f"  Members: {len(group_data.get('members', []))}")
    
    # Try to invite yourself
    print(f"\nAttempting to invite yourself ({username}) to the group...")
    invite_response = requests.post(
        f"{BASE_URL}/api/groups/{group_id}/invite",
        json={"usernames": [username]},
        headers=headers
    )
    
    print(f"Status: {invite_response.status_code}")
    print(f"Response: {invite_response.json()}")
    
    # Check the response
    data = invite_response.json()
    if "already_members" in data and username in data["already_members"]:
        print(f"\n❌ ISSUE FOUND: Self-invitation is categorized as 'already_members'")
        print(f"   Expected: A specific error like 'cannot_invite_self' or clearer message")
    elif "failed" in data and username in data["failed"]:
        print(f"\n✓ GOOD: Self-invitation is properly rejected in 'failed' list")
    else:
        print(f"\n? UNEXPECTED: Check the response format")


def test_transaction():
    """Test transaction functionality"""
    print("\n" + "="*70)
    print("TESTING TRANSACTION FUNCTIONALITY")
    print("="*70)
    
    print("NOTE: Transaction table exists in models.py")
    print("Transaction model fields:")
    print("  - id, user_id, stripe_payment_intent_id")
    print("  - amount, currency, payment_method")
    print("  - transaction_type, debt_id, split_expense_id")
    print("  - status, description, created_at, updated_at")
    print("\nTransaction functionality requires:")
    print("  1. Stripe API keys configured")
    print("  2. Payment endpoints (/api/payments/*)")
    print("  3. Create debt or split expense to associate transaction")
    
    # Check if the payments router is available
    docs_response = requests.get(f"{BASE_URL}/docs")
    if "payments" in docs_response.text.lower():
        print("\n✓ Payments routes are registered")
    else:
        print("\n❌ Payments routes may not be registered in main.py")


if __name__ == "__main__":
    # Start by checking server
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=2)
        if response.status_code == 200:
            print("✓ Backend server is running\n")
        else:
            print("❌ Backend server returned unexpected status")
            exit(1)
    except Exception as e:
        print(f"❌ Backend server is not running: {e}")
        print("Please start the server first: python -m uvicorn app.main:app --reload")
        exit(1)
    
    # Run tests
    test_self_invitation()
    test_transaction()
    
    print("\n" + "="*70)
    print("TESTING COMPLETE")
    print("="*70)
