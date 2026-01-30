#!/bin/bash

# =========================
# Cron-safe environment
# =========================
export PATH=/usr/local/bin:/usr/bin:/bin

APP_DIR="/home/ubuntu/expense_tracker"
BRANCH="staging"
LOG="/home/ubuntu/deploy.log"
LOCK="/tmp/deploy.lock"

# =========================
# Prevent overlapping runs
# =========================
exec 9>"$LOCK" || exit 1
flock -n 9 || exit 0

echo "------------------------" >> "$LOG"
date >> "$LOG"

cd "$APP_DIR" || {
  echo "❌ App directory not found" >> "$LOG"
  exit 1
}

# =========================
# Git update
# =========================
/usr/bin/git fetch origin >> "$LOG" 2>&1

LOCAL=$(/usr/bin/git rev-parse HEAD)
REMOTE=$(/usr/bin/git rev-parse origin/$BRANCH)

if [ "$LOCAL" != "$REMOTE" ]; then
  echo "🚀 Changes detected. Deploying..." >> "$LOG"

  /usr/bin/git reset --hard origin/$BRANCH >> "$LOG" 2>&1

  # =========================
  # Docker compose deploy
  # =========================
  /usr/bin/docker compose down >> "$LOG" 2>&1
  /usr/bin/docker compose up -d --build >> "$LOG" 2>&1

  echo "✅ Deployment successful" >> "$LOG"
else
  echo "ℹ️ No changes" >> "$LOG"
fi
