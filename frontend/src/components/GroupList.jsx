import React, { useState, useEffect } from "react";
import toast from "react-hot-toast";
import { getGroups, createGroup, getCurrentUser, getGroupInvitations, joinGroup, getFriends, inviteGroupMembers } from "../api";

export default function GroupList({ onSelectGroup }) {
  const [groups, setGroups] = useState([]);
  const [invitations, setInvitations] = useState([]);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [loading, setLoading] = useState(true);
  const [currentUser, setCurrentUser] = useState(null);

  useEffect(() => {
    fetchGroups();
    fetchInvitations();
    fetchCurrentUser();
  }, []);

  async function fetchGroups() {
    try {
      setLoading(true);
      const data = await getGroups();
      setGroups(data);
    } catch (error) {
      console.error("Failed to fetch groups:", error);
    } finally {
      setLoading(false);
    }
  }

  async function fetchInvitations() {
    try {
      const data = await getGroupInvitations();
      console.log('📨 Invitations received:', data);
      console.log('📊 Total invitations:', data.length);
      
      // Debug: log each invitation's structure
      if (data.length > 0) {
        console.log('🔍 First invitation structure:', {
          id: data[0].id,
          group_id: data[0].group_id,
          name: data[0].name,
          group_name: data[0].group_name,
          members: data[0].members?.length
        });
      }
      
      setInvitations(data);
    } catch (error) {
      console.error("❌ Failed to fetch invitations:", error);
      setInvitations([]);
    }
  }

  async function fetchCurrentUser() {
    try {
      const user = await getCurrentUser();
      setCurrentUser(user);
    } catch (error) {
      console.error("Failed to fetch current user:", error);
    }
  }

  async function handleCreateGroup(groupData) {
    try {
      const newGroup = await createGroup(groupData);
      await fetchGroups();
      setShowCreateModal(false);
      return newGroup; // Return the created group for member invitations
    } catch (error) {
      console.error("Failed to create group:", error);
      toast.error("Failed to create group. Please try again.");
      throw error;
    }
  }

  async function handleJoinGroup(groupId) {
    try {
      await joinGroup(groupId);
      await fetchGroups();
      await fetchInvitations();
    } catch (error) {
      console.error("Failed to join group:", error);
      toast.error("Failed to join group. Please try again.");
    }
  }

  if (loading) {
    return (
      <div className="groups-page">
        <p>Loading groups...</p>
      </div>
    );
  }

  return (
    <div className="groups-page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Groups</h1>
          <p className="page-subtitle">Manage shared expenses with friends</p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowCreateModal(true)}>
          <svg className="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Create Group
        </button>
      </div>

      {/* Pending Invitations - Prominent Display */}
      {invitations.length > 0 && (
        <div className="invitations-section">
          <div className="invitations-header">
            <div className="invitations-title">
              <svg className="invitations-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 19v-8.93a2 2 0 01.89-1.664l7-4.666a2 2 0 012.22 0l7 4.666A2 2 0 0121 10.07V19M3 19a2 2 0 002 2h14a2 2 0 002-2M3 19l6.75-4.5M21 19l-6.75-4.5M3 10l6.75 4.5M21 10l-6.75 4.5m0 0l-1.14.76a2 2 0 01-2.22 0l-1.14-.76" />
              </svg>
              <h2>Group Invitations</h2>
              <span className="badge-count">{invitations.length}</span>
            </div>
            <p className="invitations-subtitle">You've been invited to join these groups</p>
          </div>
          <div className="groups-grid">
            {invitations.map(invitation => (
              <GroupInvitationCard 
                key={invitation.id} 
                invitation={invitation} 
                onJoin={handleJoinGroup}
              />
            ))}
          </div>
        </div>
      )}

      {/* My Groups */}
      <div className="my-groups-section">
        <h2 className="section-title">
          <svg className="section-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          My Groups
          {groups.length > 0 && <span className="badge-count-secondary">{groups.length}</span>}
        </h2>
        <div className="groups-grid">
          {groups.length === 0 ? (
            <div className="empty-state">
              <svg className="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              <h3>No groups yet</h3>
              <p>Create your first group to start splitting expenses with friends!</p>
              <button className="btn btn-primary" onClick={() => setShowCreateModal(true)}>
                <svg className="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                Create Your First Group
              </button>
            </div>
          ) : (
            groups.map(group => (
              <GroupCard 
                key={group.id} 
                group={group} 
                onSelect={() => onSelectGroup(group.id)} 
              />
            ))
          )}
        </div>
      </div>

      {showCreateModal && (
        <CreateGroupModal 
          onClose={() => setShowCreateModal(false)} 
          onCreate={handleCreateGroup}
        />
      )}
    </div>
  );
}

function GroupCard({ group, onSelect }) {
  // Calculate balance from group data (will come from API)
  const yourBalance = group.your_balance || 0;
  const memberCount = group.member_count || group.members?.length || 0;
  const totalSpend = group.total_expenses || 0;
  
  const balanceColor = yourBalance > 0 ? 'balance-positive' : 
                       yourBalance < 0 ? 'balance-negative' : 
                       'balance-neutral';
  
  const balanceText = yourBalance > 0 ? `You are owed ₹${Math.abs(yourBalance).toFixed(2)}` :
                      yourBalance < 0 ? `You owe ₹${Math.abs(yourBalance).toFixed(2)}` :
                      'All settled up';

  return (
    <div className="group-card">
      <div className="group-card-header">
        <h3 className="group-name">{group.name}</h3>
        <span className="member-count">
          <svg className="member-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          {memberCount} members
        </span>
      </div>
      
      <div className="group-card-stats">
        <div className="group-stat">
          <span className="stat-label">Total Spend</span>
          <span className="stat-value">₹{totalSpend.toLocaleString('en-IN')}</span>
        </div>
        <div className={`group-balance ${balanceColor}`}>
          <span className="balance-label">Your Balance</span>
          <span className="balance-value">{balanceText}</span>
        </div>
      </div>

      <button className="btn btn-secondary btn-block" onClick={onSelect}>
        View Group
      </button>
    </div>
  );
}

function CreateGroupModal({ onClose, onCreate }) {
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    currency: "INR",
  });
  const [friends, setFriends] = useState([]);
  const [selectedFriends, setSelectedFriends] = useState([]);
  const [submitting, setSubmitting] = useState(false);
  const [loadingFriends, setLoadingFriends] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [step, setStep] = useState(1); // 1: Group details, 2: Add members

  useEffect(() => {
    fetchFriends();
  }, []);

  async function fetchFriends() {
    try {
      setLoadingFriends(true);
      const data = await getFriends();
      setFriends(data || []);
    } catch (error) {
      console.error("Failed to fetch friends:", error);
    } finally {
      setLoadingFriends(false);
    }
  }

  const filteredFriends = friends.filter(friend => 
    friend.friend_username?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const toggleFriend = (friendId) => {
    setSelectedFriends(prev => 
      prev.includes(friendId) 
        ? prev.filter(id => id !== friendId)
        : [...prev, friendId]
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (step === 1) {
      // Move to member selection
      setStep(2);
      return;
    }

    // Step 2: Create group and invite members
    setSubmitting(true);
    try {
      const newGroup = await onCreate(formData);
      
      // If members were selected, invite them using the new API
      if (selectedFriends.length > 0 && newGroup?.id) {
        const usernamesToInvite = selectedFriends
          .map(friendId => {
            const friend = friends.find(f => f.id === friendId);
            return friend?.friend_username;
          })
          .filter(Boolean);
        
        if (usernamesToInvite.length > 0) {
          try {
            const result = await inviteGroupMembers(newGroup.id, usernamesToInvite);
            console.log('Invitation result:', result.message);
            
            // Show success/warning messages
            if (result.message) {
              if (result.message.includes('Successfully invited')) {
                const match = result.message.match(/Successfully invited (\d+) user/);
                if (match) {
                  toast.success(`Successfully invited ${match[1]} user(s) to the group`);
                }
              }
              
              // Check for warnings about non-friends
              if (result.message.includes('Not friends with')) {
                toast.warning('Some users could not be invited (not friends)');
              }
              
              if (result.message.includes('not found')) {
                toast.error('Some users were not found');
              }
            }
          } catch (inviteError) {
            console.error('Failed to invite some members:', inviteError);
            // Don't block the modal from closing - group was created successfully
          }
        }
      }
      
      onClose();
    } catch (error) {
      console.error("Failed to create group:", error);
    } finally {
      setSubmitting(false);
    }
  };

  const goBack = () => {
    setStep(1);
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content modal-large" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-header-content">
            {step === 2 && (
              <button className="btn-back" onClick={goBack}>
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>
            )}
            <div>
              <h2>{step === 1 ? 'Create New Group' : 'Add Members'}</h2>
              <p className="modal-subtitle">
                {step === 1 ? 'Step 1 of 2: Group Details' : 'Step 2 of 2: Invite Friends'}
              </p>
            </div>
          </div>
          <button className="modal-close" onClick={onClose}>
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          {step === 1 ? (
            // Step 1: Group Details
            <div className="modal-body">
              <div className="form-group">
                <label>
                  Group Name <span className="required">*</span>
                </label>
                <input
                  type="text"
                  placeholder="Weekend trip, Roommates, Office lunch, etc."
                  value={formData.name}
                  onChange={e => setFormData({...formData, name: e.target.value})}
                  required
                  autoFocus
                />
              </div>

              <div className="form-group">
                <label>Description</label>
                <textarea
                  placeholder="What's this group for? (Optional)"
                  value={formData.description}
                  onChange={e => setFormData({...formData, description: e.target.value})}
                  rows={3}
                />
              </div>

              <div className="form-group">
                <label>Currency</label>
                <select
                  value={formData.currency}
                  onChange={e => setFormData({...formData, currency: e.target.value})}
                >
                  <option value="INR">🇮🇳 INR (₹)</option>
                  <option value="USD">🇺🇸 USD ($)</option>
                  <option value="EUR">🇪🇺 EUR (€)</option>
                  <option value="GBP">🇬🇧 GBP (£)</option>
                </select>
              </div>
            </div>
          ) : (
            // Step 2: Add Members
            <div className="modal-body">
              <div className="members-selection">
                <div className="search-box">
                  <svg className="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                  <input
                    type="text"
                    placeholder="Search friends..."
                    value={searchQuery}
                    onChange={e => setSearchQuery(e.target.value)}
                    className="search-input"
                  />
                </div>

                {selectedFriends.length > 0 && (
                  <div className="selected-members">
                    <p className="selected-count">
                      {selectedFriends.length} friend{selectedFriends.length !== 1 ? 's' : ''} selected
                    </p>
                    <div className="selected-chips">
                      {selectedFriends.map(friendId => {
                        const friend = friends.find(f => f.id === friendId);
                        return (
                          <div key={friendId} className="chip">
                            <span>{friend?.friend_username}</span>
                            <button 
                              type="button" 
                              onClick={() => toggleFriend(friendId)}
                              className="chip-remove"
                            >
                              ×
                            </button>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}

                {loadingFriends ? (
                  <div className="loading-friends">
                    <p>Loading friends...</p>
                  </div>
                ) : filteredFriends.length === 0 ? (
                  <div className="no-friends">
                    <svg className="empty-icon-small" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                    <p>{searchQuery ? 'No friends found matching your search' : 'No friends yet. Add friends first to invite them to groups!'}</p>
                  </div>
                ) : (
                  <div className="friends-list">
                    {filteredFriends.map(friend => (
                      <label key={friend.id} className="friend-item">
                        <div className="friend-info">
                          <div className="friend-avatar">
                            {friend.friend_username?.[0]?.toUpperCase()}
                          </div>
                          <div className="friend-details">
                            <span className="friend-name">{friend.friend_username}</span>
                            <span className="friend-status">
                              {friend.friend_email || 'Friend'}
                            </span>
                          </div>
                        </div>
                        <input
                          type="checkbox"
                          checked={selectedFriends.includes(friend.id)}
                          onChange={() => toggleFriend(friend.id)}
                          className="friend-checkbox"
                        />
                      </label>
                    ))}
                  </div>
                )}
              </div>

              <div className="info-box">
                <svg className="info-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p>You can skip this step and add members later from the group page.</p>
              </div>
            </div>
          )}

          <div className="modal-footer">
            <button 
              type="button" 
              className="btn btn-secondary" 
              onClick={onClose}
              disabled={submitting}
            >
              Cancel
            </button>
            {step === 2 && (
              <button 
                type="button" 
                className="btn btn-outline" 
                onClick={goBack}
                disabled={submitting}
              >
                Back
              </button>
            )}
            <button 
              type="submit" 
              className="btn btn-primary"
              disabled={submitting || (step === 1 && !formData.name.trim())}
            >
              {submitting ? (
                <>
                  <svg className="btn-spinner" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Creating...
                </>
              ) : step === 1 ? (
                'Next: Add Members'
              ) : (
                `Create Group${selectedFriends.length > 0 ? ` & Invite ${selectedFriends.length}` : ''}`
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function GroupInvitationCard({ invitation, onJoin }) {
  const [joining, setJoining] = useState(false);

  const handleJoin = async () => {
    setJoining(true);
    try {
      // Support multiple possible ID field names from API
      const groupId = invitation.id || invitation.group_id;
      
      if (!groupId) {
        console.error('No group ID found in invitation:', invitation);
        toast.error('Unable to join group - invalid invitation data');
        return;
      }
      
      await onJoin(groupId);
    } finally {
      setJoining(false);
    }
  };

  // Find who invited the user (admin or first accepted member)
  const inviter = invitation.members?.find(m => m.role === 'admin' && m.status === 'accepted') 
    || invitation.members?.find(m => m.status === 'accepted');

  return (
    <div className="group-card invitation-card">
      <div className="invitation-badge">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 19v-8.93a2 2 0 01.89-1.664l7-4.666a2 2 0 012.22 0l7 4.666A2 2 0 0121 10.07V19M3 19a2 2 0 002 2h14a2 2 0 002-2M3 19l6.75-4.5M21 19l-6.75-4.5M3 10l6.75 4.5M21 10l-6.75 4.5m0 0l-1.14.76a2 2 0 01-2.22 0l-1.14-.76" />
        </svg>
        <span>Invitation</span>
      </div>
      
      <div className="group-card-header">
        <h3 className="group-name">{invitation.name}</h3>
        {inviter && (
          <div className="invitation-from">
            <svg className="user-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            <span>from <strong>{inviter.username}</strong></span>
          </div>
        )}
      </div>
      
      {invitation.description && (
        <p className="group-description">
          {invitation.description}
        </p>
      )}

      <div className="group-meta">
        <span className="meta-item">
          <svg className="meta-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          {invitation.members?.filter(m => m.status === 'accepted').length || 0} members
        </span>
        {invitation.currency && (
          <span className="meta-item">
            <svg className="meta-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {invitation.currency}
          </span>
        )}
      </div>

      <div className="invitation-actions">
        <button 
          className="btn btn-primary btn-block" 
          onClick={handleJoin}
          disabled={joining}
        >
          {joining ? (
            <>
              <svg className="btn-spinner" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Joining...
            </>
          ) : (
            <>
              <svg className="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Accept Invitation
            </>
          )}
        </button>
      </div>
    </div>
  );
}
