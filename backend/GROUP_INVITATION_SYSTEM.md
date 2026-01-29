# Group Invitation System - Complete Guide

## Overview
The group invitation system has been updated to ensure proper user relationships and security. Users can now only invite their **friends** to groups, and invited users will see pending invitations in their profile.

---

## Key Features

### ✅ Friendship Validation
- **Only friends can be invited** to groups
- System checks if users have an accepted friendship before creating invitation
- Case-insensitive username lookup for better user experience

### ✅ Pending Invitations Endpoint
- Users can view all pending group invitations
- New endpoint: `GET /api/groups/invitations/pending`
- Returns full group details for each pending invitation

### ✅ Proper ID Resolution
- Usernames are converted to user IDs automatically
- System validates that user exists before creating invitation
- Prevents duplicate invitations

---

## API Endpoints

### 1. Get Pending Invitations

**Endpoint:** `GET /api/groups/invitations/pending`

**Description:** Get all pending group invitations for the logged-in user

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "Trip to Goa",
    "description": "Planning our vacation",
    "currency": "INR",
    "image_url": "https://example.com/image.jpg",
    "is_active": true,
    "created_by": 2,
    "created_at": "2026-01-27T10:00:00",
    "members": [
      {
        "id": 1,
        "user_id": 2,
        "username": "john_doe",
        "role": "admin",
        "status": "accepted",
        "joined_at": "2026-01-27T10:00:00"
      },
      {
        "id": 2,
        "user_id": 1,
        "username": "jane_smith",
        "role": "member",
        "status": "pending",
        "joined_at": "2026-01-27T11:00:00"
      }
    ]
  }
]
```

---

### 2. Invite Members to Group

**Endpoint:** `POST /api/groups/{group_id}/invite`

**Description:** Invite friends to join a group. **Only friends can be invited.**

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "usernames": ["friend1", "friend2", "friend3"]
}
```

**Response (200):**

**Success:**
```json
{
  "message": "Successfully invited 2 user(s)"
}
```

**Partial Success:**
```json
{
  "message": "Successfully invited 1 user(s). Not friends with: user2. You can only invite friends to groups. Users not found: user3"
}
```

**All Failed:**
```json
{
  "message": "Not friends with: user1, user2. You can only invite friends to groups"
}
```

---

### 3. Accept Group Invitation

**Endpoint:** `POST /api/groups/{group_id}/join`

**Description:** Accept a pending group invitation

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "message": "Successfully joined the group"
}
```

**Error (404):**
```json
{
  "detail": "No pending invitation found"
}
```

---

## Complete Flow Example

### Step 1: User A and User B become friends

```javascript
// User A sends friend request
POST /api/friends/request
{
  "friend_username": "userB"
}

// User B accepts friend request
POST /api/friends/accept/{friendship_id}
```

---

### Step 2: User A creates a group

```javascript
POST /api/groups
{
  "name": "Weekend Getaway",
  "description": "Planning our trip",
  "currency": "INR"
}

// Response
{
  "id": 5,
  "name": "Weekend Getaway",
  "members": [
    {
      "user_id": 1,
      "username": "userA",
      "role": "admin",
      "status": "accepted"
    }
  ]
}
```

---

### Step 3: User A invites User B (their friend)

```javascript
POST /api/groups/5/invite
{
  "usernames": ["userB"]
}

// Response
{
  "message": "Successfully invited 1 user(s)"
}
```

---

### Step 4: User B checks pending invitations

```javascript
GET /api/groups/invitations/pending

// Response
[
  {
    "id": 5,
    "name": "Weekend Getaway",
    "description": "Planning our trip",
    "members": [
      {
        "user_id": 1,
        "username": "userA",
        "role": "admin",
        "status": "accepted"
      },
      {
        "user_id": 2,
        "username": "userB",
        "role": "member",
        "status": "pending"  // ⬅️ This is the invitation
      }
    ]
  }
]
```

---

### Step 5: User B accepts the invitation

```javascript
POST /api/groups/5/join

// Response
{
  "message": "Successfully joined the group"
}
```

---

### Step 6: User B now sees the group in their groups list

```javascript
GET /api/groups

// Response
[
  {
    "id": 5,
    "name": "Weekend Getaway",
    "members": [
      {
        "user_id": 1,
        "username": "userA",
        "role": "admin",
        "status": "accepted"
      },
      {
        "user_id": 2,
        "username": "userB",
        "role": "member",
        "status": "accepted"  // ⬅️ Now accepted
      }
    ]
  }
]
```

---

## Error Handling

### Not Friends Error
```json
{
  "message": "Not friends with: userX. You can only invite friends to groups"
}
```
**Solution:** Users must first send and accept friend requests before inviting to groups.

---

### User Not Found Error
```json
{
  "message": "Users not found: invalidUsername"
}
```
**Solution:** Verify the username is correct and the user exists.

---

### Already Member Error
```json
{
  "message": "Already members: userX"
}
```
**Solution:** User is already in the group (either pending or accepted).

---

### Not a Group Member Error (403)
```json
{
  "detail": "You are not a member of this group"
}
```
**Solution:** Only group members can invite others to the group.

---

## Frontend Integration Tips

### Display Pending Invitations Badge

```javascript
// Fetch pending invitations count
async function getPendingInvitationsCount() {
  const response = await fetch('/api/groups/invitations/pending', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  const invitations = await response.json();
  return invitations.length;
}

// Show badge in UI
const count = await getPendingInvitationsCount();
if (count > 0) {
  showNotificationBadge(count);
}
```

---

### Show Invite Button Only for Friends

```javascript
async function canInviteUser(username) {
  // Get user's friends list
  const response = await fetch('/api/friends', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  const friends = await response.json();
  
  // Check if username is in friends list
  return friends.some(f => f.friend_username === username);
}

// In UI
if (await canInviteUser(username)) {
  showInviteButton();
} else {
  showAddFriendButton();
}
```

---

### Handle Invitation Response

```javascript
async function inviteToGroup(groupId, usernames) {
  try {
    const response = await fetch(`/api/groups/${groupId}/invite`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ usernames })
    });
    
    const result = await response.json();
    
    // Parse the message
    if (result.message.includes('Successfully invited')) {
      showSuccess(result.message);
    }
    
    if (result.message.includes('Not friends with')) {
      showWarning('Some users are not your friends. Add them as friends first.');
    }
    
    if (result.message.includes('not found')) {
      showError('Some users were not found.');
    }
    
  } catch (error) {
    showError('Failed to send invitations');
  }
}
```

---

## Database Schema

### GroupMember Table
```sql
CREATE TABLE group_members (
    id INTEGER PRIMARY KEY,
    group_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    role VARCHAR DEFAULT 'member',  -- 'admin' or 'member'
    status VARCHAR DEFAULT 'pending',  -- 'pending' or 'accepted'
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES groups(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Friendship Table
```sql
CREATE TABLE friendships (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    friend_id INTEGER NOT NULL,
    status VARCHAR DEFAULT 'pending',  -- 'pending' or 'accepted'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (friend_id) REFERENCES users(id)
);
```

---

## Testing Checklist

- [ ] User can see pending invitations in their profile
- [ ] User can only invite friends to groups
- [ ] Inviting non-friend shows appropriate error message
- [ ] Username lookup is case-insensitive
- [ ] Duplicate invitations are prevented
- [ ] User can accept pending invitations
- [ ] Accepted invitations move from pending to active groups
- [ ] Non-existent users show error message
- [ ] Group members can invite others (not just admins)

---

## Migration Notes

If you have existing group invitations without friendship validation:

1. **Option A:** Allow existing pending invitations to be accepted
2. **Option B:** Clear all pending invitations and require re-invitation with friendship check

To clear pending invitations (if needed):
```sql
DELETE FROM group_members WHERE status = 'pending';
```

---

## Security Features

✅ **Friendship Required:** Prevents spam invitations from strangers  
✅ **Case-Insensitive Lookup:** Better user experience  
✅ **Duplicate Prevention:** No duplicate invitations  
✅ **Proper Authorization:** Only group members can invite  
✅ **ID Resolution:** Usernames properly converted to user IDs  

---

## Summary

The updated group invitation system now requires:
1. **Users must be friends first** before group invitations
2. **Pending invitations are visible** via the new endpoint
3. **Proper user ID resolution** from usernames
4. **Clear error messages** for all failure scenarios

This ensures a secure, user-friendly group management experience! 🎉
