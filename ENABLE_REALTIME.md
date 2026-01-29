# Enable Real-time for Friendships Table

## Step 1: Enable Real-time in Supabase Dashboard

Real-time needs to be enabled for specific tables in Supabase.

### Via Supabase Dashboard:

1. Go to: https://supabase.com/dashboard/project/hhncftvcjkqtpjsohksi
2. Click **Database** → **Replication** (or **Publications**)
3. Find the **`supabase_realtime`** publication
4. Make sure **`friendships`** table is checked/enabled
5. If not, click **"Insert a table into publication"** and add `friendships`

### Via SQL Editor (Easier):

1. Go to: https://supabase.com/dashboard/project/hhncftvcjkqtpjsohksi
2. Click **SQL Editor**
3. Run this SQL:

```sql
-- Enable real-time for friendships table
ALTER PUBLICATION supabase_realtime ADD TABLE friendships;

-- Verify it's enabled
SELECT * FROM pg_publication_tables WHERE pubname = 'supabase_realtime';
```

Expected output: You should see `friendships` in the list.

## Step 2: Verify Real-time is Working

### Frontend Console Logs:
When the FriendList component loads, you should see:
```
🔄 Setting up real-time subscription for friendships...
✅ Real-time subscription active for friendships!
```

### Test Real-time:
1. **Open two browser tabs** with your app logged in as different users
2. **Tab 1:** Login as `testuser1`
3. **Tab 2:** Login as `testuser2`
4. **Tab 1:** Send a friend request to `testuser3`
5. **Tab 2:** Should see the request appear automatically! 🎉
6. **Tab 2:** Accept the request
7. **Tab 1:** Should see friend list update automatically! 🎉

## How Real-time Works

```
User Action (Tab 1)
    ↓
Backend API (FastAPI)
    ↓
Supabase PostgreSQL (friendships table updated)
    ↓
Supabase Realtime Server (detects change)
    ↓
WebSocket Push to All Subscribed Clients
    ↓
Frontend (Tab 2) receives update
    ↓
Auto-refresh friends list!
```

## Troubleshooting

### Issue: "Real-time subscription not active"

**Check:**
1. Is real-time enabled for `friendships` table? (Run SQL above)
2. Check browser console for errors
3. Verify Supabase client initialized (check console logs)

### Issue: "Changes not appearing in real-time"

**Possible causes:**
1. Backend is still using SQLite (dev.db) instead of Supabase
2. Real-time not enabled for the table
3. WebSocket connection blocked by firewall/network

**To fix backend connection to Supabase:**
- Backend should use Supabase PostgreSQL (already configured in .env)
- Restart backend: `uvicorn app.main:app --reload`
- Check logs for "Connected to PostgreSQL" message

### Issue: "Backend connection failed"

If backend can't connect to Supabase PostgreSQL directly due to network issues, you have options:

**Option 1:** Use Supabase Connection Pooler (recommended for Windows)
1. Go to: Database Settings → Connection Pooling
2. Use the "Transaction" mode URL instead
3. Update DATABASE_URL in .env

**Option 2:** Keep using SQLite locally + Supabase for production
- Use SQLite for development (dev.db)
- Deploy to production with Supabase PostgreSQL

## Testing Script

Create `frontend/test-realtime.html`:
```html
<!DOCTYPE html>
<html>
<head>
  <title>Test Supabase Real-time</title>
  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
</head>
<body>
  <h1>Supabase Real-time Test</h1>
  <div id="status">Connecting...</div>
  <div id="events"></div>

  <script>
    const supabase = window.supabase.createClient(
      'https://hhncftvcjkqtpjsohksi.supabase.co',
      'sb_publishable_uqBGzTgotx-rKo2JHAQurg_Z5jxaTDb'
    );

    const channel = supabase
      .channel('test-friendships')
      .on('postgres_changes', {
        event: '*',
        schema: 'public',
        table: 'friendships'
      }, (payload) => {
        document.getElementById('events').innerHTML +=
          `<p>Event: ${payload.eventType} - ${JSON.stringify(payload.new || payload.old)}</p>`;
      })
      .subscribe((status) => {
        document.getElementById('status').textContent =
          status === 'SUBSCRIBED' ? '✅ Connected!' : 'Connecting...';
      });
  </script>
</body>
</html>
```

Open this file in your browser and watch for real-time events!
