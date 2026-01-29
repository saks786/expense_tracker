import React, { useState, useEffect } from "react";
import toast from "react-hot-toast";
import {
  getGroupDetails,
  getGroupExpenses,
  getGroupBalances,
  getGroupSettlementSuggestions,
  addGroupExpense,
  inviteGroupMember,
  removeGroupMember,
  recordGroupSettlement,
  getCurrentUser,
} from "../api";

export default function GroupDashboard({ groupId, onBack }) {
  const [activeTab, setActiveTab] = useState("expenses");
  const [showAddExpense, setShowAddExpense] = useState(false);
  const [showInviteMember, setShowInviteMember] = useState(false);
  const [group, setGroup] = useState(null);
  const [expenses, setExpenses] = useState([]);
  const [balances, setBalances] = useState([]);
  const [settlements, setSettlements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentUser, setCurrentUser] = useState(null);

  useEffect(() => {
    fetchGroupData();
    fetchCurrentUser();
  }, [groupId]);

  async function fetchCurrentUser() {
    try {
      const user = await getCurrentUser();
      setCurrentUser(user);
    } catch (error) {
      console.error("Failed to fetch current user:", error);
    }
  }

  async function fetchGroupData() {
    try {
      setLoading(true);
      const [groupData, expensesData, balancesData, settlementsData] = await Promise.all([
        getGroupDetails(groupId),
        getGroupExpenses(groupId),
        getGroupBalances(groupId),
        getGroupSettlementSuggestions(groupId),
      ]);
      
      console.log('RAW balancesData from API:', balancesData);
      console.log('RAW settlementsData from API:', settlementsData);
      
      setGroup(groupData);
      setExpenses(expensesData);
      // Extract balances array from the response object
      const balancesArray = balancesData?.balances || [];
      const settlementsArray = settlementsData?.settlements || [];
      
      console.log('Extracted balances:', balancesArray);
      console.log('Extracted settlements:', settlementsArray);
      
      setBalances(balancesArray);
      setSettlements(settlementsArray);
    } catch (error) {
      console.error("Failed to fetch group data:", error);
      toast.error("Failed to load group data");
    } finally {
      setLoading(false);
    }
  }

  async function handleAddExpense(expenseData) {
    try {
      await addGroupExpense(groupId, expenseData);
      // Small delay to ensure backend processes the expense
      await new Promise(resolve => setTimeout(resolve, 500));
      await fetchGroupData();
      setShowAddExpense(false);
      toast.success("Expense added successfully!");
    } catch (error) {
      console.error("Failed to add expense:", error);
      toast.error(error?.message || "Failed to add expense. Please try again.");
    }
  }

  async function handleInviteMember(username) {
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('🔵 INVITE MEMBER FLOW STARTED');
    console.log('Username to invite:', username);
    console.log('Group ID:', groupId);
    console.log('Current User:', currentUser);
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    
    try {
      const result = await inviteGroupMember(groupId, username);
      await fetchGroupData();
      setShowInviteMember(false);
      toast.success(`Successfully invited ${username} to the group!`);
    } catch (error) {
      console.error('Error inviting member:', error);
      toast.error(`Failed to invite member: ${error.message || 'Please try again.'}`);
    }
  }

  async function handleRecordSettlement(settlement) {
    try {
      await recordGroupSettlement(groupId, settlement);
      await fetchGroupData();
      toast.success("Settlement recorded successfully!");
    } catch (error) {
      console.error("Failed to record settlement:", error);
      toast.error("Failed to record settlement. Please try again.");
    }
  }

  const isAdmin = group?.members?.find(m => m.user_id === currentUser?.id)?.role === 'admin';

  if (loading || !group) {
    return (
      <div className="group-dashboard">
        <p>Loading group...</p>
      </div>
    );
  }

  return (
    <div className="group-dashboard">
      {/* Back Button */}
      {onBack && (
        <button className="btn btn-secondary" onClick={onBack} style={{ marginBottom: '1rem' }}>
          ← Back to Groups
        </button>
      )}

      {/* Group Header */}
      <div className="group-header">
        <div className="group-info">
          <h1 className="group-title">{group.name}</h1>
          <div className="member-avatars">
            {group.members?.map(member => (
              <div key={member.id} className="avatar" title={member.username || member.name}>
                {(member.username || member.name || 'U')[0].toUpperCase()}
              </div>
            ))}
          </div>
        </div>
        <button className="btn btn-primary" onClick={() => setShowAddExpense(true)}>
          <svg className="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Add Expense
        </button>
      </div>

      {/* Stats Cards */}
      <div className="group-stats">
        <div className="group-stat-card">
          <span className="stat-label">Total Group Spend</span>
          <span className="stat-value">₹{(group.total_expenses || 0).toLocaleString('en-IN')}</span>
        </div>
        <div className="group-stat-card">
          <span className="stat-label">Your Balance</span>
          <span className={`stat-value ${(group.your_balance || 0) > 0 ? 'text-green' : (group.your_balance || 0) < 0 ? 'text-red' : ''}`}>
            {(group.your_balance || 0) > 0 
              ? `You are owed ₹${Math.abs(group.your_balance).toFixed(2)}` 
              : (group.your_balance || 0) < 0 
                ? `You owe ₹${Math.abs(group.your_balance).toFixed(2)}`
                : 'All settled up'}
          </span>
        </div>
        <div className="group-stat-card">
          <span className="stat-label">Total Expenses</span>
          <span className="stat-value">{expenses.length}</span>
        </div>
      </div>

      {/* Tabs */}
      <div className="group-tabs">
        <button
          className={`tab ${activeTab === 'expenses' ? 'active' : ''}`}
          onClick={() => setActiveTab('expenses')}
        >
          Expenses
        </button>
        <button
          className={`tab ${activeTab === 'balances' ? 'active' : ''}`}
          onClick={() => setActiveTab('balances')}
        >
          Balances
        </button>
        <button
          className={`tab ${activeTab === 'settlements' ? 'active' : ''}`}
          onClick={() => setActiveTab('settlements')}
        >
          Settlements
        </button>
        <button
          className={`tab ${activeTab === 'members' ? 'active' : ''}`}
          onClick={() => setActiveTab('members')}
        >
          Members
        </button>
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {activeTab === 'expenses' && <ExpensesTab expenses={expenses} />}
        {activeTab === 'balances' && <BalancesTab balances={balances} />}
        {activeTab === 'settlements' && <SettlementsTab settlements={settlements} onRecordSettlement={handleRecordSettlement} />}
        {activeTab === 'members' && <MembersTab members={group.members || []} isAdmin={isAdmin} onInvite={() => setShowInviteMember(true)} />}
      </div>

      {showAddExpense && (
        <AddGroupExpenseModal
          groupMembers={group.members || []}
          currentUserId={currentUser?.id}
          onClose={() => setShowAddExpense(false)}
          onSubmit={handleAddExpense}
        />
      )}
      
      {showInviteMember && (
        <InviteMemberModal
          onClose={() => setShowInviteMember(false)}
          onInvite={handleInviteMember}
        />
      )}
    </div>
  );
}

function ExpensesTab({ expenses }) {
  if (expenses.length === 0) {
    return <div className="empty-state"><p>No expenses yet. Add your first expense to get started!</p></div>;
  }

  return (
    <div className="expenses-list">
      {expenses.map(expense => (
        <div key={expense.id} className="expense-row">
          <div className="expense-info">
            <h4 className="expense-desc">{expense.description}</h4>
            <p className="expense-meta">
              Paid by {expense.paid_by_username} • {expense.category || 'Uncategorized'} • {new Date(expense.date || expense.created_at).toLocaleDateString()}
            </p>
            <p className="expense-meta" style={{ fontSize: '12px', color: '#6B7280' }}>
              {expense.split_method === 'equal' ? 'Split equally' : 'Custom split'} • {expense.participants?.length || 0} participants
            </p>
          </div>
          <div className="expense-amount">₹{expense.total_amount.toLocaleString('en-IN')}</div>
        </div>
      ))}
    </div>
  );
}

function BalancesTab({ balances }) {
  if (!balances || balances.length === 0) {
    return <div className="empty-state"><p>All settled up! No outstanding balances.</p></div>;
  }

  return (
    <div className="balances-list">
      {balances.map((balance, idx) => {
        const amount = Math.abs(balance.balance || 0);
        const isOwe = (balance.balance || 0) < 0;
        
        return (
          <div key={idx} className={`balance-row ${isOwe ? 'owe' : 'owed'}`}>
            <div className="balance-info">
              <div className="balance-avatar">{(balance.username || 'U')[0].toUpperCase()}</div>
              <div>
                <span className="balance-person" style={{ fontSize: '16px', fontWeight: '600', color: '#111827' }}>
                  {balance.username || 'Unknown User'}
                </span>
                <p className="balance-text" style={{ margin: '4px 0 0 0', fontSize: '14px', color: '#6B7280' }}>
                  {isOwe ? 'You owe' : 'Owes you'}
                </p>
              </div>
            </div>
            <span className={`balance-amount ${isOwe ? 'text-red' : 'text-green'}`} style={{ fontSize: '18px' }}>
              ₹{amount.toFixed(2)}
            </span>
          </div>
        );
      })}
    </div>
  );
}

function SettlementsTab({ settlements, onRecordSettlement }) {
  console.log('SettlementsTab received settlements:', settlements);
  console.log('Settlements count:', settlements?.length);
  
  if (!settlements || settlements.length === 0) {
    return <div className="empty-state"><p>No settlements needed. All balances are settled!</p></div>;
  }

  const handleMarkPaid = (settlement) => {
    if (window.confirm(`Confirm that ${settlement.from_username} paid ${settlement.to_username} ₹${settlement.amount.toFixed(2)}?`)) {
      onRecordSettlement({
        from_user_id: settlement.from_user_id,
        to_user_id: settlement.to_user_id,
        amount: settlement.amount
      });
    }
  };

  return (
    <div className="settlements-list">
      <p className="settlements-intro">Simplify balances with these suggested payments:</p>
      {settlements.map((settlement, idx) => {
        console.log(`Rendering settlement ${idx}:`, settlement);
        return (
          <div key={idx} className="settlement-card">
            <div className="settlement-text">
              <strong>{settlement.from_username}</strong> pays <strong>{settlement.to_username}</strong>
            </div>
            <div className="settlement-amount">₹{settlement.amount.toFixed(2)}</div>
            <button className="btn btn-sm btn-primary" onClick={() => handleMarkPaid(settlement)}>
              Mark as Paid
            </button>
          </div>
        );
      })}
    </div>
  );
}

function MembersTab({ members, isAdmin, onInvite }) {
  if (!members || members.length === 0) {
    return <div className="empty-state"><p>No members in this group yet.</p></div>;
  }

  return (
    <div className="members-list">
      {members.map(member => (
        <div key={member.user_id} className="member-row">
          <div className="member-avatar">{member.username[0].toUpperCase()}</div>
          <div className="member-info">
            <h4 className="member-name">{member.username}</h4>
            <p className="member-role">
              {member.role === 'admin' ? '👑 Admin' : 'Member'} • 
              {member.status === 'pending' ? ' Pending' : ' Active'}
            </p>
          </div>
          {isAdmin && member.role !== 'admin' && member.status === 'accepted' && (
            <button className="btn btn-sm btn-danger">Remove</button>
          )}
        </div>
      ))}
      {isAdmin && (
        <button className="btn btn-secondary" style={{ marginTop: '1rem' }} onClick={onInvite}>
          + Invite Member
        </button>
      )}
    </div>
  );
}

function AddGroupExpenseModal({ groupMembers, currentUserId, onClose, onSubmit }) {
  const [formData, setFormData] = useState({
    description: "",
    total_amount: "",
    category: "Food",
    paid_by: currentUserId || "",
    split_method: "equal",
    participants: [],
    custom_splits: {},
    date: new Date().toISOString().split('T')[0],
  });
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate participants selected
    if (!formData.participants || formData.participants.length === 0) {
      toast.error("Please select at least one participant");
      return;
    }
    
    // Validate custom splits if custom method selected
    if (formData.split_method === 'custom') {
      const totalSplits = Object.values(formData.custom_splits).reduce((sum, val) => sum + parseFloat(val || 0), 0);
      const totalAmount = parseFloat(formData.total_amount);
      if (Math.abs(totalSplits - totalAmount) > 0.01) {
        toast.error(`Custom splits (₹${totalSplits.toFixed(2)}) must equal total amount (₹${totalAmount.toFixed(2)})`);
        return;
      }
    }
    
    setSubmitting(true);
    try {
      const totalAmount = parseFloat(formData.total_amount);
      const participantCount = formData.participants.length;
      
      // Calculate participants array with share_amount for each
      const participants = formData.split_method === 'equal' 
        ? formData.participants.map(id => ({ 
            user_id: parseInt(id),
            share_amount: parseFloat((totalAmount / participantCount).toFixed(2))
          }))
        : formData.participants.map(id => ({
            user_id: parseInt(id),
            share_amount: parseFloat(formData.custom_splits[id] || 0)
          }));
      
      const payload = {
        description: formData.description,
        total_amount: totalAmount,
        category: formData.category,
        paid_by: parseInt(formData.paid_by),
        participants: participants,
        ...(formData.date && { date: formData.date })
      };
      
      await onSubmit(payload);
    } catch (error) {
      console.error("Failed to add expense:", error);
    } finally {
      setSubmitting(false);
    }
  };

  const toggleParticipant = (memberId) => {
    setFormData(prev => {
      const newParticipants = prev.participants.includes(memberId)
        ? prev.participants.filter(id => id !== memberId)
        : [...prev.participants, memberId];
      
      // Remove custom split if participant is removed
      const newCustomSplits = { ...prev.custom_splits };
      if (!newParticipants.includes(memberId)) {
        delete newCustomSplits[memberId];
      }
      
      return {
        ...prev,
        participants: newParticipants,
        custom_splits: newCustomSplits
      };
    });
  };
  
  const updateCustomSplit = (memberId, amount) => {
    setFormData(prev => ({
      ...prev,
      custom_splits: {
        ...prev.custom_splits,
        [memberId]: amount
      }
    }));
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Add Group Expense</h2>
          <button className="modal-close" onClick={onClose}>
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Description</label>
            <input
              type="text"
              placeholder="What was this expense for?"
              value={formData.description}
              onChange={e => setFormData({...formData, description: e.target.value})}
              required
            />
          </div>

          <div className="form-group">
            <label>Amount</label>
            <input
              type="number"
              placeholder="0.00"
              value={formData.total_amount}
              onChange={e => setFormData({...formData, total_amount: e.target.value})}
              required
              step="0.01"
            />
          </div>

          <div className="form-group">
            <label>Category</label>
            <select
              value={formData.category}
              onChange={e => setFormData({...formData, category: e.target.value})}
            >
              <option value="Food">Food</option>
              <option value="Transportation">Transportation</option>
              <option value="Accommodation">Accommodation</option>
              <option value="Entertainment">Entertainment</option>
              <option value="Utilities">Utilities</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div className="form-group">
            <label>Paid By</label>
            <select
              value={formData.paid_by}
              onChange={e => setFormData({...formData, paid_by: e.target.value})}
              required
            >
              <option value="">Select who paid</option>
              {groupMembers.map(member => (
                <option key={member.id} value={member.id}>
                  {member.username || member.name}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Split Method</label>
            <select
              value={formData.split_method}
              onChange={e => setFormData({...formData, split_method: e.target.value})}
            >
              <option value="equal">Split Equally</option>
              <option value="custom">Custom Amounts</option>
            </select>
          </div>

          <div className="form-group">
            <label>Split Among</label>
            <div className="checkbox-group">
              {groupMembers.filter(m => m.status === 'accepted').map(member => (
                <div key={member.user_id} style={{ marginBottom: '8px' }}>
                  <label className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={formData.participants.includes(member.user_id)}
                      onChange={() => toggleParticipant(member.user_id)}
                    />
                    <span>{member.username}</span>
                  </label>
                  {formData.split_method === 'custom' && formData.participants.includes(member.user_id) && (
                    <input
                      type="number"
                      placeholder="Amount"
                      value={formData.custom_splits[member.user_id] || ''}
                      onChange={e => updateCustomSplit(member.user_id, e.target.value)}
                      step="0.01"
                      style={{ marginLeft: '30px', width: '120px', padding: '4px 8px' }}
                    />
                  )}
                </div>
              ))}
            </div>
            {formData.split_method === 'custom' && formData.participants.length > 0 && (
              <p className="form-hint">
                Total: ₹{Object.values(formData.custom_splits).reduce((sum, val) => sum + parseFloat(val || 0), 0).toFixed(2)} / ₹{formData.total_amount || '0.00'}
              </p>
            )}
          </div>

          <div className="modal-footer">
            <button 
              type="button" 
              className="btn btn-secondary" 
              onClick={onClose}
              disabled={submitting}
            >
              Cancel
            </button>
            <button 
              type="submit" 
              className="btn btn-primary"
              disabled={submitting}
            >
              {submitting ? "Adding..." : "Add Expense"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function InviteMemberModal({ onClose, onInvite }) {
  const [username, setUsername] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await onInvite(username);
    } catch (error) {
      console.error("Failed to invite member:", error);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Invite Member</h2>
          <button className="modal-close" onClick={onClose}>
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              placeholder="Enter username to invite"
              value={username}
              onChange={e => setUsername(e.target.value)}
              required
            />
            <p className="form-hint">The user will receive an invitation to join this group</p>
          </div>

          <div className="modal-footer">
            <button 
              type="button" 
              className="btn btn-secondary" 
              onClick={onClose}
              disabled={submitting}
            >
              Cancel
            </button>
            <button 
              type="submit" 
              className="btn btn-primary"
              disabled={submitting}
            >
              {submitting ? "Inviting..." : "Send Invitation"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
