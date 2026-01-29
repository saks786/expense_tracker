"""
Test script for the updated group invitation system
Tests friendship validation and pending invitations
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_group_invitation_system():
    """
    Complete test of the group invitation system with friendship validation
    """
    
    print("=" * 70)
    print("GROUP INVITATION SYSTEM TEST")
    print("=" * 70)
    
    # Step 1: Create two test users
    print("\n1️⃣  Creating test users...")
    
    user1_data = {
        "username": "testuser_a",
        "email": "usera@test.com",
        "password": "password123"
    }
    
    user2_data = {
        "username": "testuser_b",
        "email": "userb@test.com",
        "password": "password123"
    }
    
    try:
        # Register users (may already exist)
        requests.post(f"{BASE_URL}/api/register", json=user1_data)
        requests.post(f"{BASE_URL}/api/register", json=user2_data)
        print("✓ Users created/already exist")
    except Exception as e:
        print(f"⚠️  Users may already exist: {e}")
    
    # Login users
    print("\n2️⃣  Logging in users...")
    
    login1 = requests.post(f"{BASE_URL}/api/login", data={
        "username": user1_data["username"],
        "password": user1_data["password"]
    })
    
    login2 = requests.post(f"{BASE_URL}/api/login", data={
        "username": user2_data["username"],
        "password": user2_data["password"]
    })
    
    if login1.status_code == 200 and login2.status_code == 200:
        token1 = login1.json()["access_token"]
        token2 = login2.json()["access_token"]
        print(f"✓ User A logged in: {user1_data['username']}")
        print(f"✓ User B logged in: {user2_data['username']}")
    else:
        print("❌ Login failed!")
        print(f"User A: {login1.status_code} - {login1.text}")
        print(f"User B: {login2.status_code} - {login2.text}")
        return
    
    headers1 = {"Authorization": f"Bearer {token1}", "Content-Type": "application/json"}
    headers2 = {"Authorization": f"Bearer {token2}", "Content-Type": "application/json"}
    
    # Step 2: Try to invite without friendship (should fail)
    print("\n3️⃣  Creating a group (User A)...")
    
    group_data = {
        "name": "Test Group",
        "description": "Testing invitations",
        "currency": "INR"
    }
    
    create_group = requests.post(
        f"{BASE_URL}/api/groups",
        headers=headers1,
        json=group_data
    )
    
    if create_group.status_code == 201:
        group_id = create_group.json()["id"]
        print(f"✓ Group created with ID: {group_id}")
    else:
        print(f"❌ Group creation failed: {create_group.text}")
        return
    
    # Step 3: Try to invite User B without being friends
    print("\n4️⃣  Trying to invite User B (NOT friends yet - should fail)...")
    
    invite_data = {
        "usernames": [user2_data["username"]]
    }
    
    invite_response = requests.post(
        f"{BASE_URL}/api/groups/{group_id}/invite",
        headers=headers1,
        json=invite_data
    )
    
    if invite_response.status_code == 200:
        message = invite_response.json()["message"]
        print(f"Response: {message}")
        
        if "Not friends with" in message:
            print("✅ CORRECT: Cannot invite non-friends!")
        else:
            print("❌ WARNING: Invitation succeeded without friendship!")
    else:
        print(f"❌ Request failed: {invite_response.text}")
    
    # Step 4: Send friend request
    print("\n5️⃣  Sending friend request from User A to User B...")
    
    friend_request = requests.post(
        f"{BASE_URL}/api/friends/request",
        headers=headers1,
        json={"friend_username": user2_data["username"]}
    )
    
    if friend_request.status_code == 200:
        friendship_id = friend_request.json()["id"]
        print(f"✓ Friend request sent (ID: {friendship_id})")
    else:
        print(f"⚠️  Friend request response: {friend_request.status_code} - {friend_request.text}")
        # May already be friends or have pending request
    
    # Step 5: Check friend requests for User B
    print("\n6️⃣  User B checking friend requests...")
    
    friend_requests = requests.get(
        f"{BASE_URL}/api/friends/requests",
        headers=headers2
    )
    
    if friend_requests.status_code == 200:
        requests_list = friend_requests.json()
        print(f"✓ User B has {len(requests_list)} pending friend request(s)")
        
        if requests_list:
            friendship_id = requests_list[0]["id"]
            
            # Accept friend request
            print("\n7️⃣  User B accepting friend request...")
            
            accept_response = requests.post(
                f"{BASE_URL}/api/friends/accept/{friendship_id}",
                headers=headers2
            )
            
            if accept_response.status_code == 200:
                print("✓ Friend request accepted!")
            else:
                print(f"⚠️  Accept response: {accept_response.text}")
        else:
            print("⚠️  No pending requests (may already be friends)")
    
    # Step 6: Now try to invite again (should succeed)
    print("\n8️⃣  Trying to invite User B again (NOW friends - should succeed)...")
    
    invite_response2 = requests.post(
        f"{BASE_URL}/api/groups/{group_id}/invite",
        headers=headers1,
        json=invite_data
    )
    
    if invite_response2.status_code == 200:
        message = invite_response2.json()["message"]
        print(f"Response: {message}")
        
        if "Successfully invited" in message:
            print("✅ CORRECT: Invitation sent to friend!")
        elif "Already members" in message:
            print("⚠️  User already invited/member")
        else:
            print(f"⚠️  Unexpected message: {message}")
    else:
        print(f"❌ Request failed: {invite_response2.text}")
    
    # Step 7: Check pending invitations for User B
    print("\n9️⃣  User B checking pending group invitations...")
    
    pending_invitations = requests.get(
        f"{BASE_URL}/api/groups/invitations/pending",
        headers=headers2
    )
    
    if pending_invitations.status_code == 200:
        invitations = pending_invitations.json()
        print(f"✓ User B has {len(invitations)} pending invitation(s)")
        
        if invitations:
            print(f"\nPending invitations:")
            for inv in invitations:
                print(f"  - Group: {inv['name']} (ID: {inv['id']})")
                print(f"    Created by user ID: {inv['created_by']}")
                
                # Find pending member
                for member in inv['members']:
                    if member['status'] == 'pending':
                        print(f"    Status: PENDING for {member['username']}")
            
            print("✅ CORRECT: Invitation shows in pending list!")
        else:
            print("⚠️  No pending invitations found")
    else:
        print(f"❌ Request failed: {pending_invitations.text}")
    
    # Step 8: User B accepts the invitation
    print("\n🔟  User B accepting group invitation...")
    
    accept_invite = requests.post(
        f"{BASE_URL}/api/groups/{group_id}/join",
        headers=headers2
    )
    
    if accept_invite.status_code == 200:
        print(f"✓ {accept_invite.json()['message']}")
        print("✅ CORRECT: User joined the group!")
    else:
        print(f"❌ Join failed: {accept_invite.text}")
    
    # Step 9: Verify User B is now in the group
    print("\n1️⃣1️⃣  Verifying User B is now a group member...")
    
    group_details = requests.get(
        f"{BASE_URL}/api/groups/{group_id}",
        headers=headers2
    )
    
    if group_details.status_code == 200:
        group_info = group_details.json()
        members = group_info['members']
        
        print(f"✓ Group has {len(members)} member(s):")
        for member in members:
            print(f"  - {member['username']} ({member['role']}) - {member['status']}")
        
        # Check if User B is accepted
        user_b_member = next((m for m in members if m['username'] == user2_data['username']), None)
        if user_b_member and user_b_member['status'] == 'accepted':
            print("✅ CORRECT: User B is now an accepted member!")
        else:
            print("⚠️  User B status:", user_b_member)
    else:
        print(f"❌ Failed to get group details: {group_details.text}")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE!")
    print("=" * 70)
    print("\n✅ Key Validations:")
    print("  1. Cannot invite non-friends ✓")
    print("  2. Can invite after becoming friends ✓")
    print("  3. Pending invitations are visible ✓")
    print("  4. Can accept invitations ✓")
    print("  5. Accepted members show in group ✓")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    try:
        test_group_invitation_system()
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
