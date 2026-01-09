#!/bin/sh
echo "Starting Vite dev server..."
echo "Node version: $(node --version)"
echo "Running vite..."
# Disable output buffering and run vite
NODE_ENV=development exec node node_modules/vite/bin/vite.js --host 0.0.0.0 --port 5413 --clearScreen false
