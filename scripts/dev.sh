#!/usr/bin/env bash
# Aura Local Dev — one command to start everything
# Usage: ./scripts/dev.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APPS="$ROOT/../aura-apps"

echo "🚀 Starting Aura local dev..."
echo ""

# Backend
echo "  Backend  → http://localhost:3000"
cd "$APPS/apps/backend"
mkdir -p data
[ -f .env ] || echo "DATABASE_URL=file:./data/aura.db
AURA_JWT_SECRET=dev-secret-change-in-production
PORT=3000
NODE_ENV=development" > .env
bun run --watch src/serve.ts &
BACKEND_PID=$!

# Farm (Capacitor SPA)
echo "  Farm     → http://localhost:5173"
cd "$APPS/apps/farm-capacitor"
npx vite --port 5173 --host &
FARM_PID=$!

# Card (SPA)
echo "  Card     → http://localhost:5174"
cd "$APPS/apps/card"
npx vite --port 5174 --host &
CARD_PID=$!

echo ""
echo "✅ All services starting..."
echo "   Backend: http://localhost:3000/health"
echo "   Farm:    http://localhost:5173"
echo "   Card:    http://localhost:5174"
echo ""
echo "Press Ctrl+C to stop all."

trap "kill $BACKEND_PID $FARM_PID $CARD_PID 2>/dev/null; echo '🛑 Stopped.'" EXIT
wait
