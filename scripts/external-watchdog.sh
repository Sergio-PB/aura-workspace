#!/bin/bash
# Aura External Watchdog — runs via launchd, completely outside Hermes
# Checks: Hermes gateway liveness, cron scheduler health, pulse heartbeat
# Alerts via Telegram if anything is wrong. Silent when healthy.

set -euo pipefail

BOT_TOKEN="8908466522:AAHUU_uuuVVtn62Jhm4SojXhCOoyl6KbXmk"
CHAT_ID="664767609"
HERMES_HOME="/Users/sergio/.hermes"
LOG_FILE="/Users/sergio/aura-workspace/logs/watchdog-external.log"
CRON_JOBS="$HERMES_HOME/cron/jobs.json"
MAX_PULSE_AGE_MINUTES=45
MAX_LOG_LINES=2000

log() {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $1" >> "$LOG_FILE"
    # ponytail: keep log bounded — truncate to last 1000 lines past 2000
    if [ "$(wc -l < "$LOG_FILE" 2>/dev/null || echo 0)" -gt "$MAX_LOG_LINES" ]; then
        tail -n 1000 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
    fi
}

alert() {
    local msg="$1"
    log "ALERT: $msg"
    curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
        -d "chat_id=${CHAT_ID}" \
        -d "text=${msg}" \
        -d "parse_mode=Markdown" \
        > /dev/null 2>&1
}

# 1. Check Hermes gateway is running
if ! pgrep -f "hermes_cli.main gateway run" > /dev/null 2>&1; then
    alert "🚨 *Hermes gateway is DOWN.* The agent can't receive messages or deliver cron output."
    exit 1
fi

# 2. Check cron jobs file exists
if [ ! -f "$CRON_JOBS" ]; then
    alert "⚠️ *Cron jobs file missing.* No cron jobs are scheduled."
    exit 1
fi

# 3. Check aura-pulse last run time
PULSE_LAST_RUN=$(python3 -c "
import json, sys
with open('$CRON_JOBS') as f:
    jobs = json.load(f).get('jobs', [])
for j in jobs:
    if j.get('name') == 'aura-pulse':
        lr = j.get('last_run_at')
        if lr:
            print(lr)
        break
" 2>/dev/null)

if [ -z "$PULSE_LAST_RUN" ]; then
    alert "⚠️ *aura-pulse has never run.* The autonomous agent hasn't started working yet."
    exit 0
fi

# Parse the ISO timestamp and compare
PULSE_EPOCH=$(date -j -f "%Y-%m-%dT%H:%M:%S" "${PULSE_LAST_RUN%%.*}" +%s 2>/dev/null || echo 0)
NOW_EPOCH=$(date +%s)
AGE_MINUTES=$(( (NOW_EPOCH - PULSE_EPOCH) / 60 ))

if [ "$AGE_MINUTES" -gt "$MAX_PULSE_AGE_MINUTES" ]; then
    alert "🚨 *PULSE MISSED.* aura-pulse last ran ${AGE_MINUTES} minutes ago (threshold: ${MAX_PULSE_AGE_MINUTES}). The autonomous agent may be stuck or the cron scheduler may be down."
    exit 1
fi

# 4. Check for RETRY-FAILED in error log
ERROR_LOG="/Users/sergio/aura-workspace/logs/errors.md"
if [ -f "$ERROR_LOG" ]; then
    RETRY_FAILED=$(grep -c '\[RETRY-FAILED\]' "$ERROR_LOG" 2>/dev/null | tr -d '[:space:]' || echo 0)
    RETRY_FAILED=${RETRY_FAILED:-0}
    if [ "$RETRY_FAILED" -gt 0 ] 2>/dev/null; then
        alert "⚠️ *Pulse errors require attention.* ${RETRY_FAILED} RETRY-FAILED entries in error log."
    fi
fi

# All clear — log and exit silently
log "All clear. Gateway: up, Pulse: ${AGE_MINUTES}m ago, Errors: ${RETRY_FAILED:-0}"
