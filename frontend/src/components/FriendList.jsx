import React, { useState, useEffect } from "react";
import {
  getFriends,
  getFriendRequests,
  sendFriendRequest,
  acceptFriendRequest,
  removeFriend,
} from "../api";

export default function FriendList({ onUpdate }) {
  const [friends, setFriends] = useState([]);
  const [requests, setRequests] = useState([]);
  const [newFriendUsername, setNewFriendUsername] = useState("");
  const [activeTab, setActiveTab] = useState("friends"); // friends | requests

  const [loadingFriends, setLoadingFriends] = useState(false);
  const [loadingRequests, setLoadingRequests] = useState(false);
  const [sendingRequest, setSendingRequest] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    fetchFriends();
    fetchRequests();
  }, []);

  const fetchFriends = async () => {
    setLoadingFriends(true);
    setError("");
    try {
      const data = await getFriends();
      setFriends(data || []);
    } catch (err) {
      console.error(err);
      setError(err?.message || "Failed to load friends.");
    } finally {
      setLoadingFriends(false);
    }
  };

  const fetchRequests = async () => {
    setLoadingRequests(true);
    setError("");
    try {
      const data = await getFriendRequests();
      setRequests(data || []);
    } catch (err) {
      console.error(err);
      setError(err?.message || "Failed to load friend requests.");
    } finally {
      setLoadingRequests(false);
    }
  };

  const handleSendRequest = async (e) => {
    e.preventDefault();
    const username = newFriendUsername.trim();
    if (!username) return;

    setSendingRequest(true);
    setError("");
    setSuccess("");
    try {
      await sendFriendRequest(username);
      setNewFriendUsername("");
      setSuccess("Friend request sent.");
      fetchRequests();
    } catch (err) {
      setError(err?.message || "Failed to send friend request.");
    } finally {
      setSendingRequest(false);
    }
  };

  const handleAccept = async (friendshipId) => {
    setError("");
    setSuccess("");
    try {
      await acceptFriendRequest(friendshipId);
      await Promise.all([fetchFriends(), fetchRequests()]);
      setSuccess("Friend request accepted.");
      if (typeof onUpdate === "function") onUpdate();
    } catch (err) {
      setError(err?.message || "Failed to accept friend request.");
    }
  };

  const handleRemoveFriend = async (friendshipId) => {
    if (!window.confirm("Are you sure you want to remove this friend?")) return;
    setError("");
    setSuccess("");
    try {
      await removeFriend(friendshipId);
      await fetchFriends();
      setSuccess("Friend removed.");
      if (typeof onUpdate === "function") onUpdate();
    } catch (err) {
      setError(err?.message || "Failed to remove friend.");
    }
  };

  const handleRejectRequest = async (friendshipId) => {
    if (!window.confirm("Are you sure you want to reject this friend request?")) return;
    setError("");
    setSuccess("");
    try {
      await removeFriend(friendshipId);
      await fetchRequests();
      setSuccess("Friend request rejected.");
      if (typeof onUpdate === "function") onUpdate();
    } catch (err) {
      setError(err?.message || "Failed to reject request.");
    }
  };

  return (
    <div className="friend-management">
      <div className="list-header">
        <h3 className="list-title">👥 Friends & Requests</h3>

        <form onSubmit={handleSendRequest} className="add-friend-form" style={{ display: "flex", gap: 8 }}>
          <input
            type="text"
            placeholder="Enter username to add friend"
            value={newFriendUsername}
            onChange={(e) => setNewFriendUsername(e.target.value)}
            className="form-input"
          />
          <button
            type="submit"
            className="btn btn-primary"
            disabled={sendingRequest}
          >
            {sendingRequest ? "Sending..." : "Send Request"}
          </button>
        </form>
      </div>

      {(error || success) && (
        <div style={{ marginBottom: 16 }}>
          {error && (
            <div className="error-message" role="alert">
              {error}
            </div>
          )}
          {success && !error && (
            <div
              style={{
                background: "#ecfdf3",
                color: "#166534",
                padding: "12px 14px",
                borderRadius: 12,
                borderLeft: "4px solid #22c55e",
                fontSize: "0.9rem",
                marginTop: error ? 8 : 0,
              }}
            >
              {success}
            </div>
          )}
        </div>
      )}

      <div className="main-tabs" style={{ marginBottom: 20 }}>
        <button
          type="button"
          className={`main-tab ${activeTab === "friends" ? "active" : ""}`}
          onClick={() => setActiveTab("friends")}
        >
          Friends ({friends.length})
        </button>
        <button
          type="button"
          className={`main-tab ${activeTab === "requests" ? "active" : ""}`}
          onClick={() => setActiveTab("requests")}
        >
          Requests ({requests.length})
        </button>
      </div>

      {activeTab === "friends" && (
        <div className="friends-list">
          {loadingFriends ? (
            <p className="empty-state">Loading friends...</p>
          ) : friends.length === 0 ? (
            <p className="empty-state">No friends yet. Add some friends above!</p>
          ) : (
            friends.map((friendship) => (
              <div key={friendship.id} className="friend-card">
                <div className="friend-info" style={{ display: "flex", alignItems: "center", gap: 12 }}>
                  <div className="friend-avatar">
                    {friendship.friend_username?.[0]?.toUpperCase() || "👤"}
                  </div>
                  <div className="friend-details" style={{ display: "flex", flexDirection: "column" }}>
                    <span className="friend-name" style={{ fontWeight: 600 }}>
                      {friendship.friend_username}
                    </span>
                    <span className="friend-since" style={{ fontSize: "0.85rem", color: "#6b7280" }}>
                      Friends since{" "}
                      {friendship.created_at
                        ? new Date(friendship.created_at).toLocaleDateString()
                        : "-"}
                    </span>
                  </div>
                </div>
                <button
                  onClick={() => handleRemoveFriend(friendship.id)}
                  className="btn-remove"
                  type="button"
                >
                  Remove
                </button>
              </div>
            ))
          )}
        </div>
      )}

      {activeTab === "requests" && (
        <div className="requests-list">
          {loadingRequests ? (
            <p className="empty-state">Loading requests...</p>
          ) : requests.length === 0 ? (
            <p className="empty-state">No pending friend requests</p>
          ) : (
            requests.map((request) => (
              <div key={request.id} className="friend-card">
                <div className="friend-info" style={{ display: "flex", alignItems: "center", gap: 12 }}>
                  <div className="friend-avatar">
                    {request.friend_username?.[0]?.toUpperCase() || "👤"}
                  </div>
                  <div className="friend-details" style={{ display: "flex", flexDirection: "column" }}>
                    <span className="friend-name" style={{ fontWeight: 600 }}>
                      {request.friend_username}
                    </span>
                    <span className="request-time" style={{ fontSize: "0.85rem", color: "#6b7280" }}>
                      {request.created_at
                        ? new Date(request.created_at).toLocaleDateString()
                        : "-"}
                    </span>
                  </div>
                </div>
                <div className="request-actions" style={{ display: "flex", gap: 8 }}>
                  <button
                    onClick={() => handleAccept(request.id)}
                    className="btn-accept"
                    type="button"
                  >
                    Accept
                  </button>
                  <button
                    onClick={() => handleRejectRequest(request.id)}
                    className="btn-reject"
                    type="button"
                  >
                    Reject
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}
