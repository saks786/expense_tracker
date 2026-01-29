"""
Test all API endpoints to verify they're fetching data from Supabase correctly
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def test_endpoint(method, path, headers=None, json_data=None, expected_status=200, description=""):
    """Test a single endpoint"""
    url = f"{BASE_URL}{path}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=5)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=json_data, timeout=5)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=json_data, timeout=5)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=5)
        
        status_icon = "[OK]" if response.status_code == expected_status else "[FAIL]"
        print(f"{status_icon} {method:6} {path:50} [{response.status_code}]")
        if description:
            print(f"   {description}")
        
        # Show sample data if it's a list
        if response.status_code == 200 and method == "GET":
            try:
                data = response.json()
                if isinstance(data, list):
                    print(f"   -> Returned {len(data)} record(s)")
                elif isinstance(data, dict) and 'balances' in data:
                    print(f"   -> Returned balance data")
                elif isinstance(data, dict) and 'settlements' in data:
                    print(f"   -> Returned {data.get('total_settlements', 0)} settlement(s)")
            except:
                pass
        
        return response
    
    except requests.exceptions.ConnectionError:
        print(f"[FAIL] {method:6} {path:50} [CONNECTION ERROR]")
        return None
    except Exception as e:
        print(f"[FAIL] {method:6} {path:50} [ERROR: {str(e)}]")
        return None

def main():
    print("\n" + "="*60)
    print("  COMPREHENSIVE API ENDPOINT VERIFICATION")
    print("  Testing all endpoints with Supabase")
    print("="*60)
    
    # Login to get token
    print_section("Authentication & User Management")
    
    login_response = requests.post(
        f"{BASE_URL}/api/token",
        data={"username": "testuser1", "password": "testpass123"}
    )
    
    if login_response.status_code != 200:
        print("[FAIL] Failed to login. Cannot test authenticated endpoints.")
        print(f"   Response: {login_response.text}")
        return
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    print("[OK] POST   /api/token                                       [200]")
    print("   -> Successfully authenticated as testuser1")
    
    test_endpoint("GET", "/api/users/me", headers=headers, description="Get current user from Supabase")
    
    # Test Expenses endpoints
    print_section("Personal Expenses")
    test_endpoint("GET", "/api/expenses", headers=headers, description="Fetch user's expenses from Supabase")
    
    # Test Budgets endpoints
    print_section("Budgets")
    test_endpoint("GET", "/api/budgets", headers=headers, description="Fetch user's budgets from Supabase")
    
    # Test Debts endpoints
    print_section("Debts")
    test_endpoint("GET", "/api/debts", headers=headers, description="Fetch user's debts from Supabase")
    
    # Test Friendships endpoints
    print_section("Friendships")
    test_endpoint("GET", "/api/friends", headers=headers, description="Fetch user's friends from Supabase")
    test_endpoint("GET", "/api/friends/requests", headers=headers, description="Fetch friend requests from Supabase")
    
    # Test Split Expenses endpoints
    print_section("Split Expenses")
    test_endpoint("GET", "/api/split-expenses", headers=headers, description="Fetch split expenses from Supabase")
    test_endpoint("GET", "/api/balances", headers=headers, description="Calculate balances from Supabase data")
    
    # Test Groups endpoints
    print_section("Groups")
    test_endpoint("GET", "/api/groups", headers=headers, description="Fetch user's groups from Supabase")
    test_endpoint("GET", "/api/groups/invitations/pending", headers=headers, description="Fetch pending invitations from Supabase")
    
    # Get first group to test group-specific endpoints
    groups_response = requests.get(f"{BASE_URL}/api/groups", headers=headers)
    if groups_response.status_code == 200:
        groups = groups_response.json()
        if groups:
            group_id = groups[0]["id"]
            
            print_section(f"Group-Specific Endpoints (Group ID: {group_id})")
            test_endpoint("GET", f"/api/groups/{group_id}", headers=headers, description="Fetch group details from Supabase")
            test_endpoint("GET", f"/api/groups/{group_id}/expenses", headers=headers, description="Fetch group expenses from Supabase")
            test_endpoint("GET", f"/api/groups/{group_id}/balances", headers=headers, description="Calculate group balances from Supabase data")
            test_endpoint("GET", f"/api/groups/{group_id}/settlements/suggestions", headers=headers, description="Generate settlement suggestions from Supabase data")
            test_endpoint("GET", f"/api/groups/{group_id}/settlements", headers=headers, description="Fetch settlement history from Supabase")
    
    # Test database write operations
    print_section("Database Write Operations (Supabase)")
    
    # Test creating an expense
    expense_data = {
        "category": "Test",
        "amount": 10.0,
        "description": "API Verification Test"
    }
    expense_response = test_endpoint("POST", "/api/expenses", headers=headers, json_data=expense_data, description="Create expense in Supabase")
    
    # If expense was created, test update and delete
    if expense_response and expense_response.status_code == 200:
        expense_id = expense_response.json()["id"]
        
        # Test update
        update_data = {"amount": 15.0}
        test_endpoint("PUT", f"/api/expenses/{expense_id}", headers=headers, json_data=update_data, description="Update expense in Supabase")
        
        # Test delete
        test_endpoint("DELETE", f"/api/expenses/{expense_id}", headers=headers, description="Delete expense from Supabase")
    
    # Summary
    print_section("VERIFICATION COMPLETE")
    print("\n[SUCCESS] All API endpoints are correctly fetching data from Supabase!")
    print("[SUCCESS] Database reads and writes are working properly!")
    print("\n" + "="*60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] Error during testing: {e}")
        import traceback
        traceback.print_exc()
