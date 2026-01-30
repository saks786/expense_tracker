#!/bin/bash
set -e

APP_DIR="/home/ubuntu/expense_tracker"
BRANCH="staging"
LOG="/home/ubuntu/deploy.log"

cd $APP_DIR

echo "------------------------" >> $LOG
date >> $LOG

git fetch origin

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/$BRANCH)

if [ "$LOCAL" != "$REMOTE" ]; then
  echo "🚀 Changes detected. Deploying..." >> $LOG

  git reset --hard origin/$BRANCH

  docker compose down
  docker compose up -d --build

  echo "✅ Deployment successful" >> $LOG
else
  echo "ℹ️ No changes" >> $LOG
fi
