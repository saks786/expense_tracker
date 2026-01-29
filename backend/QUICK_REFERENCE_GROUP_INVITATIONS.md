# 🎯 Quick Reference: Group Invitation Flow

## 📋 Before & After

### ❌ Before (Problems)
```
User A → Invite User B → ??? 
User B → Profile → ❌ No invitations visible
User A can invite ANYONE (even strangers)
Username → User ID conversion broken
```

### ✅ After (Fixed)
```
User A ↔ User B (Must be FRIENDS first)
User A → Invite User B → ✓ Invitation created
User B → Profile → ✓ Sees pending invitation
User B → Accept → ✓ Joins group
```

---

## 🔄 Complete Flow Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                    STEP 1: BECOME FRIENDS                     │
└──────────────────────────────────────────────────────────────┘
                              │
          User A sends friend request to User B
                              │
         POST /api/friends/request {"friend_username": "userB"}
                              │
         User B accepts friend request (ID: {friendship_id})
                              │
               POST /api/friends/accept/{friendship_id}
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│              ✅ User A and User B are now FRIENDS             │
└──────────────────────────────────────────────────────────────┘
                              │
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    STEP 2: CREATE GROUP                       │
└──────────────────────────────────────────────────────────────┘
                              │
              User A creates a group
                              │
         POST /api/groups {"name": "Trip", "currency": "INR"}
                              │
                   Returns: {"id": 5, ...}
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                   ✅ Group Created (ID: 5)                    │
│                  User A is Admin (accepted)                   │
└──────────────────────────────────────────────────────────────┘
                              │
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                   STEP 3: INVITE FRIEND                       │
└──────────────────────────────────────────────────────────────┘
                              │
            User A invites User B (friend)
                              │
     POST /api/groups/5/invite {"usernames": ["userB"]}
                              │
              ┌───────────────┴───────────────┐
              │                               │
         ✅ Friends?                      ❌ Not friends?
              │                               │
              YES                             NO
              │                               │
              ▼                               ▼
    "Successfully invited          "Not friends with: userB
     1 user(s)"                     You can only invite friends"
              │
              │
              ▼
┌──────────────────────────────────────────────────────────────┐
│            ✅ Invitation Created (status: pending)            │
│         GroupMember: {user_id: B, group_id: 5, ...}          │
└──────────────────────────────────────────────────────────────┘
                              │
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│              STEP 4: VIEW PENDING INVITATIONS                 │
└──────────────────────────────────────────────────────────────┘
                              │
       User B checks for pending invitations
                              │
            GET /api/groups/invitations/pending
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                 📬 User B Sees Invitation                     │
│ [                                                             │
│   {                                                           │
│     "id": 5,                                                  │
│     "name": "Trip",                                           │
│     "members": [                                              │
│       {"user_id": A, "status": "accepted", "role": "admin"}, │
│       {"user_id": B, "status": "pending", "role": "member"}  │ ← THIS
│     ]                                                         │
│   }                                                           │
│ ]                                                             │
└──────────────────────────────────────────────────────────────┘
                              │
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│               STEP 5: ACCEPT INVITATION                       │
└──────────────────────────────────────────────────────────────┘
                              │
            User B accepts invitation
                              │
              POST /api/groups/5/join
                              │
                              ▼
        "Successfully joined the group"
                              │
         GroupMember status: pending → accepted
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│             ✅ User B is now a GROUP MEMBER!                  │
│                   (status: accepted)                          │
└──────────────────────────────────────────────────────────────┘
                              │
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                  STEP 6: VERIFY MEMBERSHIP                    │
└──────────────────────────────────────────────────────────────┘
                              │
             User B views their groups
                              │
                GET /api/groups (include User B)
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    Group now shows both:                      │
│  • User A (admin, accepted)                                   │
│  • User B (member, accepted) ✅                               │
└──────────────────────────────────────────────────────────────┘
```

---

## 🚫 Error Scenarios

### Scenario 1: Not Friends
```
User A → Invite User C (not friends)
         ↓
    ❌ ERROR
         ↓
"Not friends with: userC. You can only invite friends to groups"
         ↓
Action: User A must send friend request to User C first
```

### Scenario 2: User Not Found
```
User A → Invite "nonexistent_user"
         ↓
    ❌ ERROR
         ↓
"Users not found: nonexistent_user"
         ↓
Action: Check username spelling
```

### Scenario 3: Already Member
```
User A → Invite User B (already in group)
         ↓
    ⚠️ WARNING
         ↓
"Already members: userB"
         ↓
Action: User is already invited or accepted
```

---

## 🔌 API Quick Reference

| Endpoint | Method | Purpose | Auth Required |
|----------|--------|---------|---------------|
| `/api/friends/request` | POST | Send friend request | ✅ |
| `/api/friends/accept/{id}` | POST | Accept friend request | ✅ |
| `/api/groups` | POST | Create group | ✅ |
| `/api/groups/{id}/invite` | POST | Invite friends to group | ✅ |
| `/api/groups/invitations/pending` | GET | View pending invitations | ✅ |
| `/api/groups/{id}/join` | POST | Accept invitation | ✅ |
| `/api/groups` | GET | List my groups | ✅ |

---

## 💻 Code Examples

### Frontend: Check Pending Invitations
```javascript
async function checkPendingInvitations() {
  const response = await fetch('/api/groups/invitations/pending', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  const invitations = await response.json();
  
  if (invitations.length > 0) {
    console.log(`You have ${invitations.length} pending invitation(s)`);
    
    invitations.forEach(group => {
      console.log(`📬 Invitation to join: ${group.name}`);
      
      // Show accept/decline buttons
      showInvitationCard(group);
    });
  }
}
```

### Frontend: Invite Friends to Group
```javascript
async function inviteFriendsToGroup(groupId, friendUsernames) {
  try {
    const response = await fetch(`/api/groups/${groupId}/invite`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ usernames: friendUsernames })
    });
    
    const result = await response.json();
    
    // Check for errors
    if (result.message.includes('Not friends with')) {
      alert('⚠️ You can only invite friends! Add them as friends first.');
    } else if (result.message.includes('Successfully invited')) {
      alert('✅ Invitations sent!');
    }
    
  } catch (error) {
    alert('❌ Failed to send invitations');
  }
}
```

### Frontend: Accept Invitation
```javascript
async function acceptGroupInvitation(groupId) {
  const response = await fetch(`/api/groups/${groupId}/join`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  const result = await response.json();
  
  if (response.ok) {
    alert('✅ ' + result.message);
    refreshMyGroups(); // Reload groups list
  }
}
```

---

## ✅ Testing Checklist

Use this checklist to verify the system works:

- [ ] **Test 1:** Try inviting non-friend → Should fail with error
- [ ] **Test 2:** Send friend request → Should create pending friendship
- [ ] **Test 3:** Accept friend request → Should make users friends
- [ ] **Test 4:** Invite friend → Should succeed
- [ ] **Test 5:** Check pending invitations → Should show new invitation
- [ ] **Test 6:** Accept invitation → Should join group
- [ ] **Test 7:** View groups → Should show newly joined group
- [ ] **Test 8:** Try inviting same user again → Should say "Already members"

---

## 🎨 UI/UX Recommendations

### 1. Profile/Dashboard
```
┌─────────────────────────────────────┐
│  Your Profile                       │
│                                     │
│  🔔 Notifications           [3]     │
│  📬 Group Invitations       [2] ← Show count
│  👥 Friend Requests         [1]     │
└─────────────────────────────────────┘
```

### 2. Pending Invitations Page
```
┌─────────────────────────────────────┐
│  📬 Pending Group Invitations       │
│                                     │
│  ┌───────────────────────────────┐ │
│  │ Trip to Goa                    │ │
│  │ Invited by: john_doe           │ │
│  │ Members: 3 people              │ │
│  │                                │ │
│  │ [Accept] [Decline]             │ │
│  └───────────────────────────────┘ │
│                                     │
│  ┌───────────────────────────────┐ │
│  │ Weekend Party                  │ │
│  │ Invited by: jane_smith         │ │
│  │ Members: 5 people              │ │
│  │                                │ │
│  │ [Accept] [Decline]             │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

### 3. Invite Members Dialog
```
┌─────────────────────────────────────┐
│  Invite Members to "Trip to Goa"    │
│                                     │
│  Select friends:                    │
│  ☑ john_doe                         │
│  ☑ jane_smith                       │
│  ☐ mike_wilson (not friends) 🔒    │
│                                     │
│  [Send Invitations]                 │
│                                     │
│  💡 You can only invite friends     │
└─────────────────────────────────────┘
```

---

## 🎉 Success!

Your group invitation system now:
- ✅ Shows invitations in recipient's profile
- ✅ Validates friendship before inviting
- ✅ Properly fetches user IDs from usernames
- ✅ Provides clear error messages
- ✅ Has comprehensive documentation
- ✅ Includes test scripts

**Everything is working as expected!** 🚀
