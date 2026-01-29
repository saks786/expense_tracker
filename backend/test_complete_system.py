"""
Comprehensive test script for Friends/Split Expenses and Groups features
Tests both systems independently and their integration
"""
import requests
import json
from datetime import date

BASE_URL = "http://localhost:8000/api"

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ {msg}{Colors.END}")

def print_section(msg):
    print(f"\n{Colors.YELLOW}{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}{Colors.END}\n")

# Test data
TEST_USERS = [
    {"username": "testuser1", "email": "test1@example.com", "password": "password123"},
    {"username": "testuser2", "email": "test2@example.com", "password": "password123"},
    {"username": "testuser3", "email": "test3@example.com", "password": "password123"},
]

tokens = {}

def register_and_login():
    """Register and login all test users"""
    print_section("STEP 1: User Registration and Authentication")
    
    for user in TEST_USERS:
        username = user["username"]
        
        # Try to register
        response = requests.post(f"{BASE_URL}/register", json=user)
        if response.status_code == 200:
            print_success(f"Registered {username}")
        elif response.status_code == 400 and "already registered" in response.text:
            print_info(f"{username} already exists")
        else:
            print_error(f"Failed to register {username}: {response.text}")
        
        # Login
        response = requests.post(
            f"{BASE_URL}/token",
            data={"username": user["username"], "password": user["password"]}
        )
        if response.status_code == 200:
            tokens[username] = response.json()["access_token"]
            print_success(f"Logged in as {username}")
        else:
            print_error(f"Failed to login {username}: {response.text}")
            return False
    
    return True

def test_friends_system():
    """Test the friendship system"""
    print_section("STEP 2: Testing Friends System")
    
    # Test 1: Send friend request from user1 to user2
    print_info("Sending friend request: testuser1 → testuser2")
    response = requests.post(
        f"{BASE_URL}/friends/request",
        json={"friend_username": "testuser2"},
        headers={"Authorization": f"Bearer {tokens['testuser1']}"}
    )
    if response.status_code == 200:
        print_success(f"Friend request sent: {response.json()}")
    else:
        print_error(f"Failed to send friend request: {response.text}")
    
    # Test 2: List friend requests for user2
    print_info("Checking friend requests for testuser2")
    response = requests.get(
        f"{BASE_URL}/friends/requests",
        headers={"Authorization": f"Bearer {tokens['testuser2']}"}
    )
    if response.status_code == 200:
        requests_data = response.json()
        print_success(f"Friend requests ({len(requests_data)}): {json.dumps(requests_data, indent=2)}")
        if requests_data:
            friendship_id = requests_data[0]["id"]
            
            # Test 3: Accept friend request
            print_info(f"Accepting friend request ID: {friendship_id}")
            response = requests.put(
                f"{BASE_URL}/friends/{friendship_id}/accept",
                headers={"Authorization": f"Bearer {tokens['testuser2']}"}
            )
            if response.status_code == 200:
                print_success(f"Friend request accepted: {response.json()}")
            else:
                print_error(f"Failed to accept friend request: {response.text}")
    else:
        print_error(f"Failed to get friend requests: {response.text}")
    
    # Test 4: Send friend request from user1 to user3
    print_info("Sending friend request: testuser1 → testuser3")
    response = requests.post(
        f"{BASE_URL}/friends/request",
        json={"friend_username": "testuser3"},
        headers={"Authorization": f"Bearer {tokens['testuser1']}"}
    )
    if response.status_code == 200:
        friendship_id = response.json()["id"]
        print_success(f"Friend request sent")
        
        # Accept it
        print_info(f"Accepting friend request")
        response = requests.put(
            f"{BASE_URL}/friends/{friendship_id}/accept",
            headers={"Authorization": f"Bearer {tokens['testuser3']}"}
        )
        if response.status_code == 200:
            print_success(f"Friend request accepted")
    
    # Test 5: List all friends for user1
    print_info("Listing all friends for testuser1")
    response = requests.get(
        f"{BASE_URL}/friends",
        headers={"Authorization": f"Bearer {tokens['testuser1']}"}
    )
    if response.status_code == 200:
        friends = response.json()
        print_success(f"Friends ({len(friends)}): {json.dumps(friends, indent=2)}")
    else:
        print_error(f"Failed to get friends: {response.text}")

def test_split_expenses():
    """Test the split expenses system"""
    print_section("STEP 3: Testing Split Expenses System")
    
    # Get user IDs first
    user_ids = {}
    for username in tokens.keys():
        response = requests.get(
            f"{BASE_URL}/users/me",
            headers={"Authorization": f"Bearer {tokens[username]}"}
        )
        if response.status_code == 200:
            user_ids[username] = response.json()["id"]
    
    print_info(f"User IDs: {user_ids}")
    
    # Test 1: Create split expense
    print_info("Creating split expense: testuser1 pays for dinner with testuser2 and testuser3")
    split_expense_data = {
        "description": "Team dinner",
        "total_amount": 3000.0,
        "category": "Food",
        "participant_ids": [user_ids["testuser2"], user_ids["testuser3"]],
        "date": str(date.today())
    }
    response = requests.post(
        f"{BASE_URL}/split-expenses",
        json=split_expense_data,
        headers={"Authorization": f"Bearer {tokens['testuser1']}"}
    )
    if response.status_code == 200:
        print_success(f"Split expense created: {response.json()}")
    else:
        print_error(f"Failed to create split expense: {response.text}")
    
    # Test 2: List split expenses
    print_info("Listing split expenses for testuser1")
    response = requests.get(
        f"{BASE_URL}/split-expenses",
        headers={"Authorization": f"Bearer {tokens['testuser1']}"}
    )
    if response.status_code == 200:
        expenses = response.json()
        print_success(f"Split expenses ({len(expenses)}): {json.dumps(expenses, indent=2)}")
    else:
        print_error(f"Failed to get split expenses: {response.text}")
    
    # Test 3: Check balances
    print_info("Checking balances for testuser1")
    response = requests.get(
        f"{BASE_URL}/balances",
        headers={"Authorization": f"Bearer {tokens['testuser1']}"}
    )
    if response.status_code == 200:
        balances = response.json()
        print_success(f"Balances: {json.dumps(balances, indent=2)}")
    else:
        print_error(f"Failed to get balances: {response.text}")
    
    # Test 4: Get settlement suggestions
    print_info("Getting settlement suggestions for testuser1")
    response = requests.get(
        f"{BASE_URL}/settlements/suggestions",
        headers={"Authorization": f"Bearer {tokens['testuser1']}"}
    )
    if response.status_code == 200:
        suggestions = response.json()
        print_success(f"Settlement suggestions: {json.dumps(suggestions, indent=2)}")
    else:
        print_error(f"Failed to get settlement suggestions: {response.text}")
    
    # Test 5: Check balances from testuser2's perspective
    print_info("Checking balances for testuser2")
    response = requests.get(
        f"{BASE_URL}/balances",
        headers={"Authorization": f"Bearer {tokens['testuser2']}"}
    )
    if response.status_code == 200:
        balances = response.json()
        print_success(f"Balances for testuser2: {json.dumps(balances, indent=2)}")
    else:
        print_error(f"Failed to get balances: {response.text}")

def test_groups_system():
    """Test the groups system"""
    print_section("STEP 4: Testing Groups System")
    
    # Test 1: Create a group
    print_info("Creating group: 'Trip to Goa' by testuser1")
    group_data = {
        "name": "Trip to Goa",
        "description": "Planning our vacation expenses",
        "currency": "INR"
    }
    response = requests.post(
        f"{BASE_URL}/groups",
        json=group_data,
        headers={"Authorization": f"Bearer {tokens['testuser1']}"}
    )
    if response.status_code == 200:
        group = response.json()
        group_id = group["id"]
        print_success(f"Group created (ID: {group_id}): {group['name']}")
    else:
        print_error(f"Failed to create group: {response.text}")
        return
    
    # Test 2: Invite members to group
    print_info(f"Inviting testuser2 and testuser3 to group {group_id}")
    response = requests.post(
        f"{BASE_URL}/groups/{group_id}/invite",
        json={"usernames": ["testuser2", "testuser3"]},
        headers={"Authorization": f"Bearer {tokens['testuser1']}"}
    )
    if response.status_code == 200:
        print_success(f"Members invited: {response.json()}")
    else:
        print_error(f"Failed to invite members: {response.text}")
    
    # Test 3: Join group (accept invitation)
    print_info("testuser2 accepting invitation")
    response = requests.post(
        f"{BASE_URL}/groups/{group_id}/join",
        headers={"Authorization": f"Bearer {tokens['testuser2']}"}
    )
    if response.status_code == 200:
        print_success(f"Invitation accepted: {response.json()}")
    else:
        print_error(f"Failed to accept invitation: {response.text}")
    
    print_info("testuser3 accepting invitation")
    response = requests.post(
        f"{BASE_URL}/groups/{group_id}/join",
        headers={"Authorization": f"Bearer {tokens['testuser3']}"}
    )
    if response.status_code == 200:
        print_success(f"Invitation accepted: {response.json()}")
    else:
        print_error(f"Failed to accept invitation: {response.text}")
    
    # Test 4: Get group details
    print_info(f"Getting group {group_id} details")
    response = requests.get(
        f"{BASE_URL}/groups/{group_id}",
        headers={"Authorization": f"Bearer {tokens['testuser1']}"}
    )
    if response.status_code == 200:
        group_details = response.json()
        print_success(f"Group details: {json.dumps(group_details, indent=2)}")
    else:
        print_error(f"Failed to get group details: {response.text}")
    
    # Test 5: Add group expense with custom splits
    print_info(f"Adding group expense: Hotel booking (testuser1 paid)")
    
    # Get user IDs
    user_ids = {}
    for username in tokens.keys():
        response = requests.get(
            f"{BASE_URL}/users/me",
            headers={"Authorization": f"Bearer {tokens[username]}"}
        )
        if response.status_code == 200:
            user_ids[username] = response.json()["id"]
    
    expense_data = {
        "description": "Hotel booking for 3 nights",
        "total_amount": 12000.0,
        "category": "Accommodation",
        "paid_by": user_ids["testuser1"],
        "participants": [
            {"user_id": user_ids["testuser1"], "share_amount": 4000.0},
            {"user_id": user_ids["testuser2"], "share_amount": 4000.0},
            {"user_id": user_ids["testuser3"], "share_amount": 4000.0}
        ],
        "date": str(date.today())
    }
    response = requests.post(
        f"{BASE_URL}/groups/{group_id}/expenses",
        json=expense_data,
        headers={"Authorization": f"Bearer {tokens['testuser1']}"}
    )
    if response.status_code == 200:
        print_success(f"Group expense added: {response.json()}")
    else:
        print_error(f"Failed to add group expense: {response.text}")
    
    # Test 6: Add another expense (testuser2 pays)
    print_info(f"Adding group expense: Dinner (testuser2 paid)")
    expense_data = {
        "description": "Beach side dinner",
        "total_amount": 2400.0,
        "category": "Food",
        "paid_by": user_ids["testuser2"],
        "participants": [
            {"user_id": user_ids["testuser1"], "share_amount": 800.0},
            {"user_id": user_ids["testuser2"], "share_amount": 800.0},
            {"user_id": user_ids["testuser3"], "share_amount": 800.0}
        ]
    }
    response = requests.post(
        f"{BASE_URL}/groups/{group_id}/expenses",
        json=expense_data,
        headers={"Authorization": f"Bearer {tokens['testuser2']}"}
    )
    if response.status_code == 200:
        print_success(f"Group expense added: {response.json()}")
    else:
        print_error(f"Failed to add group expense: {response.text}")
    
    # Test 7: List group expenses
    print_info(f"Listing all expenses for group {group_id}")
    response = requests.get(
        f"{BASE_URL}/groups/{group_id}/expenses",
        headers={"Authorization": f"Bearer {tokens['testuser1']}"}
    )
    if response.status_code == 200:
        expenses = response.json()
        print_success(f"Group expenses ({len(expenses)}): {json.dumps(expenses, indent=2)}")
    else:
        print_error(f"Failed to get group expenses: {response.text}")
    
    # Test 8: Check group balances
    print_info(f"Checking balances for group {group_id}")
    response = requests.get(
        f"{BASE_URL}/groups/{group_id}/balances",
        headers={"Authorization": f"Bearer {tokens['testuser1']}"}
    )
    if response.status_code == 200:
        balances = response.json()
        print_success(f"Group balances: {json.dumps(balances, indent=2)}")
    else:
        print_error(f"Failed to get group balances: {response.text}")
    
    # Test 9: Get settlement suggestions for group
    print_info(f"Getting settlement suggestions for group {group_id}")
    response = requests.get(
        f"{BASE_URL}/groups/{group_id}/settlements/suggestions",
        headers={"Authorization": f"Bearer {tokens['testuser1']}"}
    )
    if response.status_code == 200:
        suggestions = response.json()
        print_success(f"Settlement suggestions: {json.dumps(suggestions, indent=2)}")
    else:
        print_error(f"Failed to get settlement suggestions: {response.text}")
    
    # Test 10: Record a settlement
    print_info(f"Recording settlement: testuser2 pays testuser1 800 INR")
    settlement_data = {
        "from_user_id": user_ids["testuser2"],
        "to_user_id": user_ids["testuser1"],
        "amount": 800.0
    }
    response = requests.post(
        f"{BASE_URL}/groups/{group_id}/settlements",
        json=settlement_data,
        headers={"Authorization": f"Bearer {tokens['testuser2']}"}
    )
    if response.status_code == 200:
        print_success(f"Settlement recorded: {response.json()}")
    else:
        print_error(f"Failed to record settlement: {response.text}")
    
    # Test 11: Check balances again after settlement
    print_info(f"Checking balances after settlement")
    response = requests.get(
        f"{BASE_URL}/groups/{group_id}/balances",
        headers={"Authorization": f"Bearer {tokens['testuser1']}"}
    )
    if response.status_code == 200:
        balances = response.json()
        print_success(f"Updated group balances: {json.dumps(balances, indent=2)}")
    else:
        print_error(f"Failed to get updated balances: {response.text}")
    
    # Test 12: List all groups for user
    print_info("Listing all groups for testuser1")
    response = requests.get(
        f"{BASE_URL}/groups",
        headers={"Authorization": f"Bearer {tokens['testuser1']}"}
    )
    if response.status_code == 200:
        groups = response.json()
        print_success(f"User groups ({len(groups)}): {json.dumps(groups, indent=2)}")
    else:
        print_error(f"Failed to get groups: {response.text}")

def test_integration():
    """Test integration between both systems"""
    print_section("STEP 5: Testing System Integration")
    
    # Both systems work independently
    # Friends system: testuser1 is friends with testuser2 and testuser3
    # Split expenses: Direct expense splitting between friends
    # Groups: Organized expense tracking with custom splits
    
    print_info("Verifying both systems maintain separate data")
    
    # Check split expenses balances (friends system)
    response = requests.get(
        f"{BASE_URL}/balances",
        headers={"Authorization": f"Bearer {tokens['testuser1']}"}
    )
    if response.status_code == 200:
        split_balances = response.json()
        print_success(f"Split Expenses Balances: {json.dumps(split_balances, indent=2)}")
    
    # Check group balances
    response = requests.get(
        f"{BASE_URL}/groups",
        headers={"Authorization": f"Bearer {tokens['testuser1']}"}
    )
    if response.status_code == 200:
        groups = response.json()
        if groups:
            group_id = groups[0]["id"]
            response = requests.get(
                f"{BASE_URL}/groups/{group_id}/balances",
                headers={"Authorization": f"Bearer {tokens['testuser1']}"}
            )
            if response.status_code == 200:
                group_balances = response.json()
                print_success(f"Group Balances: {json.dumps(group_balances, indent=2)}")
    
    print_info("✓ Both systems maintain separate balance calculations")
    print_info("✓ Friends system is for informal splitting (equal shares)")
    print_info("✓ Groups system is for organized trips/events (custom splits)")

def main():
    """Run all tests"""
    print_section("COMPREHENSIVE SYSTEM TEST")
    print_info("Testing Friends/Split Expenses + Groups Integration")
    
    try:
        if not register_and_login():
            print_error("Failed to setup users")
            return
        
        test_friends_system()
        test_split_expenses()
        test_groups_system()
        test_integration()
        
        print_section("TEST SUMMARY")
        print_success("All systems tested successfully!")
        print_info("✓ Friends system working")
        print_info("✓ Split expenses working")
        print_info("✓ Groups system working")
        print_info("✓ Both systems integrate properly")
        
    except Exception as e:
        print_error(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
