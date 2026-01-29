"""
End-to-End Integration Tests
Tests complete user workflows and system integration
"""
import pytest
import requests
from datetime import date, datetime
import time

BASE_URL = "http://localhost:8000"


class TestEndToEndWorkflows:
    """Complete user workflow tests"""
    
    @pytest.fixture(scope="class")
    def test_users(self):
        """Setup test users for the workflow"""
        users = {}
        test_accounts = [
            {"username": f"e2e_user1_{int(time.time())}", "email": f"e2e1_{int(time.time())}@test.com", "password": "test123"},
            {"username": f"e2e_user2_{int(time.time())}", "email": f"e2e2_{int(time.time())}@test.com", "password": "test123"},
            {"username": f"e2e_user3_{int(time.time())}", "email": f"e2e3_{int(time.time())}@test.com", "password": "test123"},
        ]
        
        for idx, account in enumerate(test_accounts):
            # Register
            reg_response = requests.post(f"{BASE_URL}/api/register", json=account)
            assert reg_response.status_code == 200
            
            # Login
            login_response = requests.post(
                f"{BASE_URL}/api/token",
                data={"username": account["username"], "password": account["password"]}
            )
            assert login_response.status_code == 200
            
            token = login_response.json()["access_token"]
            
            # Get user info
            user_response = requests.get(
                f"{BASE_URL}/api/users/me",
                headers={"Authorization": f"Bearer {token}"}
            )
            assert user_response.status_code == 200
            
            users[f"user{idx+1}"] = {
                "account": account,
                "token": token,
                "info": user_response.json(),
                "headers": {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
            }
        
        return users
    
    def test_complete_expense_tracking_workflow(self, test_users):
        """
        Test complete expense tracking workflow:
        1. User creates expenses
        2. Sets budgets
        3. Tracks debts
        4. Views analytics
        """
        user1 = test_users["user1"]
        
        print("\n" + "="*70)
        print("TEST: Complete Expense Tracking Workflow")
        print("="*70)
        
        # Step 1: Create multiple expenses
        print("\n1. Creating expenses...")
        expenses = []
        expense_data = [
            {"category": "Food", "amount": 500, "description": "Groceries"},
            {"category": "Transport", "amount": 200, "description": "Taxi"},
            {"category": "Food", "amount": 300, "description": "Restaurant"},
            {"category": "Shopping", "amount": 1500, "description": "Clothes"},
        ]
        
        for data in expense_data:
            data["date"] = str(date.today())
            response = requests.post(
                f"{BASE_URL}/api/expenses",
                headers=user1["headers"],
                json=data
            )
            assert response.status_code == 200
            expenses.append(response.json())
            print(f"   ✓ Created {data['category']}: ₹{data['amount']}")
        
        # Step 2: Set budgets
        print("\n2. Setting budgets...")
        budgets = []
        budget_data = [
            {"category": "Food", "limit_amount": 5000, "month": datetime.now().month, "year": datetime.now().year},
            {"category": "Transport", "limit_amount": 2000, "month": datetime.now().month, "year": datetime.now().year},
        ]
        
        for data in budget_data:
            response = requests.post(
                f"{BASE_URL}/api/budgets",
                headers=user1["headers"],
                json=data
            )
            assert response.status_code == 200
            budgets.append(response.json())
            print(f"   ✓ Set {data['category']}: ₹{data['limit_amount']}")
        
        # Step 3: Create debt
        print("\n3. Creating debt...")
        debt_data = {
            "name": "Credit Card",
            "principal_amount": 50000,
            "interest_rate": 18,
            "emi_amount": 5000,
            "emi_date": 5,
            "start_date": str(date.today())
        }
        
        debt_response = requests.post(
            f"{BASE_URL}/api/debts",
            headers=user1["headers"],
            json=debt_data
        )
        assert debt_response.status_code == 200
        debt = debt_response.json()
        print(f"   ✓ Created debt: {debt['name']} (₹{debt['principal_amount']})")
        
        # Step 4: List all expenses
        print("\n4. Viewing all expenses...")
        list_response = requests.get(
            f"{BASE_URL}/api/expenses",
            headers=user1["headers"]
        )
        assert list_response.status_code == 200
        all_expenses = list_response.json()
        print(f"   ✓ Total expenses: {len(all_expenses)}")
        
        # Step 5: List budgets
        print("\n5. Checking budgets...")
        budget_response = requests.get(
            f"{BASE_URL}/api/budgets",
            headers=user1["headers"]
        )
        assert budget_response.status_code == 200
        all_budgets = budget_response.json()
        print(f"   ✓ Total budgets: {len(all_budgets)}")
        
        print("\n✅ Expense tracking workflow completed successfully!")
    
    def test_complete_friendship_and_split_workflow(self, test_users):
        """
        Test complete friendship and split expense workflow:
        1. Send friend requests
        2. Accept requests
        3. Create split expenses
        4. View balances
        5. Settle up
        """
        user1 = test_users["user1"]
        user2 = test_users["user2"]
        user3 = test_users["user3"]
        
        print("\n" + "="*70)
        print("TEST: Complete Friendship & Split Expense Workflow")
        print("="*70)
        
        # Step 1: User1 sends friend requests
        print("\n1. Sending friend requests...")
        friend_requests = []
        for user in [user2, user3]:
            response = requests.post(
                f"{BASE_URL}/api/friends/request",
                headers=user1["headers"],
                json={"friend_username": user["account"]["username"]}
            )
            assert response.status_code == 200
            friend_requests.append(response.json())
            print(f"   ✓ Sent request to {user['account']['username']}")
        
        # Step 2: Accept friend requests
        print("\n2. Accepting friend requests...")
        for idx, user in enumerate([user2, user3]):
            # Get pending requests
            requests_response = requests.get(
                f"{BASE_URL}/api/friends/requests",
                headers=user["headers"]
            )
            assert requests_response.status_code == 200
            pending = requests_response.json()
            
            if pending:
                # Accept the first request
                accept_response = requests.post(
                    f"{BASE_URL}/api/friends/accept/{pending[0]['id']}",
                    headers=user["headers"]
                )
                assert accept_response.status_code == 200
                print(f"   ✓ {user['account']['username']} accepted request")
        
        # Step 3: Create split expense
        print("\n3. Creating split expense...")
        split_data = {
            "description": "Group dinner at restaurant",
            "total_amount": 3000,
            "category": "Food",
            "date": str(date.today()),
            "participant_usernames": [
                user2["account"]["username"],
                user3["account"]["username"]
            ]
        }
        
        split_response = requests.post(
            f"{BASE_URL}/api/split-expenses",
            headers=user1["headers"],
            json=split_data
        )
        assert split_response.status_code == 200
        split_expense = split_response.json()
        print(f"   ✓ Created split: ₹{split_expense['total_amount']}")
        print(f"   ✓ Participants: {len(split_expense['participants'])}")
        
        # Step 4: Check balances
        print("\n4. Checking balances...")
        for user_key, user in [("User1", user1), ("User2", user2), ("User3", user3)]:
            balance_response = requests.get(
                f"{BASE_URL}/api/split-expenses/balances",
                headers=user["headers"]
            )
            assert balance_response.status_code == 200
            balances = balance_response.json()
            print(f"   ✓ {user_key}: {len(balances)} balance entries")
        
        # Step 5: Create settlement
        print("\n5. Settling up...")
        # User2 settles with User1
        settlement_data = {
            "to_username": user1["account"]["username"],
            "amount": 1000
        }
        
        settle_response = requests.post(
            f"{BASE_URL}/api/split-expenses/settle",
            headers=user2["headers"],
            json=settlement_data
        )
        assert settle_response.status_code == 200
        print(f"   ✓ Settlement created: ₹{settlement_data['amount']}")
        
        print("\n✅ Friendship and split workflow completed successfully!")
    
    def test_complete_group_workflow(self, test_users):
        """
        Test complete group workflow:
        1. Create group
        2. Invite members
        3. Accept invitations
        4. Create group expenses
        5. View balances
        6. Create settlements
        """
        user1 = test_users["user1"]
        user2 = test_users["user2"]
        user3 = test_users["user3"]
        
        print("\n" + "="*70)
        print("TEST: Complete Group Management Workflow")
        print("="*70)
        
        # Step 1: Create group
        print("\n1. Creating group...")
        group_data = {
            "name": "Weekend Trip",
            "description": "Group for our weekend getaway",
            "currency": "INR"
        }
        
        group_response = requests.post(
            f"{BASE_URL}/api/groups",
            headers=user1["headers"],
            json=group_data
        )
        assert group_response.status_code == 201
        group = group_response.json()
        group_id = group["id"]
        print(f"   ✓ Created group: {group['name']} (ID: {group_id})")
        
        # Step 2: Invite members (only friends can be invited)
        print("\n2. Inviting members...")
        invite_response = requests.post(
            f"{BASE_URL}/api/groups/{group_id}/invite",
            headers=user1["headers"],
            json={"usernames": [user2["account"]["username"], user3["account"]["username"]]}
        )
        assert invite_response.status_code == 200
        print(f"   ✓ {invite_response.json()['message']}")
        
        # Step 3: Check and accept invitations
        print("\n3. Accepting invitations...")
        for user_key, user in [("User2", user2), ("User3", user3)]:
            # Check pending invitations
            pending_response = requests.get(
                f"{BASE_URL}/api/groups/invitations/pending",
                headers=user["headers"]
            )
            assert pending_response.status_code == 200
            pending = pending_response.json()
            
            if pending:
                # Accept the group invitation
                accept_response = requests.post(
                    f"{BASE_URL}/api/groups/{group_id}/join",
                    headers=user["headers"]
                )
                assert accept_response.status_code == 200
                print(f"   ✓ {user_key} joined the group")
        
        # Step 4: Create group expenses
        print("\n4. Creating group expenses...")
        expense_data = {
            "description": "Hotel booking",
            "total_amount": 6000,
            "category": "Accommodation",
            "date": str(date.today()),
            "split_type": "equal",
            "participant_ids": [
                user1["info"]["id"],
                user2["info"]["id"],
                user3["info"]["id"]
            ]
        }
        
        expense_response = requests.post(
            f"{BASE_URL}/api/groups/{group_id}/expenses",
            headers=user1["headers"],
            json=expense_data
        )
        assert expense_response.status_code == 200
        group_expense = expense_response.json()
        print(f"   ✓ Created expense: {group_expense['description']}")
        print(f"   ✓ Total: ₹{group_expense['total_amount']}")
        print(f"   ✓ Split among: {len(group_expense['participants'])} members")
        
        # Step 5: View group balances
        print("\n5. Checking group balances...")
        balance_response = requests.get(
            f"{BASE_URL}/api/groups/{group_id}/balances",
            headers=user1["headers"]
        )
        assert balance_response.status_code == 200
        balances = balance_response.json()
        print(f"   ✓ Balance entries: {len(balances)}")
        for user_id, balance_info in balances.items():
            print(f"      - {balance_info.get('username', 'User')}: ₹{balance_info.get('net_balance', 0)}")
        
        # Step 6: Get settlement suggestions
        print("\n6. Getting settlement suggestions...")
        suggestions_response = requests.get(
            f"{BASE_URL}/api/groups/{group_id}/settlements/suggestions",
            headers=user1["headers"]
        )
        assert suggestions_response.status_code == 200
        suggestions = suggestions_response.json()
        print(f"   ✓ Settlement suggestions: {len(suggestions)}")
        for suggestion in suggestions:
            print(f"      - {suggestion.get('from_username')} → {suggestion.get('to_username')}: ₹{suggestion.get('amount')}")
        
        print("\n✅ Group workflow completed successfully!")
    
    def test_complete_user_journey(self, test_users):
        """
        Test complete user journey from registration to complex operations
        """
        print("\n" + "="*70)
        print("TEST: Complete User Journey")
        print("="*70)
        
        # Create a brand new user for this journey
        timestamp = int(time.time())
        new_user_data = {
            "username": f"journey_user_{timestamp}",
            "email": f"journey_{timestamp}@test.com",
            "password": "journey123"
        }
        
        print("\n1. New user registration...")
        reg_response = requests.post(f"{BASE_URL}/api/register", json=new_user_data)
        assert reg_response.status_code == 200
        print(f"   ✓ Registered: {new_user_data['username']}")
        
        print("\n2. User login...")
        login_response = requests.post(
            f"{BASE_URL}/api/login",
            data={"username": new_user_data["username"], "password": new_user_data["password"]}
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        print("   ✓ Login successful")
        
        print("\n3. Adding expenses...")
        for i in range(3):
            expense_response = requests.post(
                f"{BASE_URL}/api/expenses",
                headers=headers,
                json={
                    "category": "Food",
                    "amount": 100 + (i * 50),
                    "description": f"Expense {i+1}",
                    "date": str(date.today())
                }
            )
            assert expense_response.status_code == 200
        print("   ✓ Added 3 expenses")
        
        print("\n4. Setting budget...")
        budget_response = requests.post(
            f"{BASE_URL}/api/budgets",
            headers=headers,
            json={
                "category": "Food",
                "limit_amount": 5000,
                "month": datetime.now().month,
                "year": datetime.now().year
            }
        )
        assert budget_response.status_code == 200
        print("   ✓ Budget set")
        
        print("\n5. Sending friend request...")
        friend_response = requests.post(
            f"{BASE_URL}/api/friends/request",
            headers=headers,
            json={"friend_username": test_users["user1"]["account"]["username"]}
        )
        assert friend_response.status_code == 200
        print("   ✓ Friend request sent")
        
        print("\n6. Viewing profile...")
        profile_response = requests.get(f"{BASE_URL}/api/users/me", headers=headers)
        assert profile_response.status_code == 200
        profile = profile_response.json()
        print(f"   ✓ Profile: {profile['username']} ({profile['email']})")
        
        print("\n✅ Complete user journey successful!")


# ========================================
# MAIN TEST RUNNER
# ========================================

if __name__ == "__main__":
    """Run end-to-end tests with pytest"""
    import sys
    
    print("\n" + "="*70)
    print("END-TO-END INTEGRATION TEST SUITE")
    print("="*70)
    print("\nTesting complete user workflows and system integration...")
    print("\nMake sure the backend server is running at:", BASE_URL)
    print("="*70 + "\n")
    
    # Run with pytest
    pytest_args = [
        __file__,
        "-v",  # Verbose
        "-s",  # Show print statements
        "--tb=short",  # Short traceback format
        "--color=yes",  # Colored output
        "-k", "test_complete"  # Run only complete workflow tests
    ]
    
    sys.exit(pytest.main(pytest_args))
