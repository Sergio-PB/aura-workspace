#!/usr/bin/env python3
"""
Pulse state tracker — runs before any LLM is invoked. Zero AI tokens.
Tracks consecutive failures, detects timeout/rate-limit patterns,
implements exponential cooldown, and deduplicates alerts.

Output: KEY=VALUE lines for the watchdog/pulse to consume.
State file: logs/pulse-state.json
"""
import sqlite3, json, os, sys
from datetime import datetime, timezone, timedelta

DB = "/Users/sergio/.hermes/cron/executions.db"
JOB_ID = "bf744ee67796"
STATE_FILE = "/Users/sergio/aura-workspace/logs/pulse-state.json"
COOLDOWN_HOURS = 4
TIMEOUT_THRESHOLD = 3  # consecutive timeouts before cooldown

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {
        "consecutive_failures": 0,
        "consecutive_timeouts": 0,
        "last_error_type": None,
        "last_error_message": None,
        "cooldown_until": None,
        "last_alerted_failures": 0,
        "last_alerted_at": None,
        "last_5_statuses": []
    }

def save_state(s):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(s, f, indent=2)

def classify_error(error_text):
    if not error_text:
        return "unknown", error_text
    msg = error_text.lower()
    if "timeout" in msg or "timed out" in msg:
        return "timeout", error_text
    if "rate limit" in msg or "429" in msg or "too many requests" in msg:
        return "rate_limit", error_text
    if "usage" in msg and ("exhausted" in msg or "exceeded" in msg or "limit" in msg):
        return "usage_exhausted", error_text
    if "connection" in msg or "refused" in msg or "network" in msg:
        return "network", error_text
    return "other", error_text

def main():
    state = load_state()
    now = datetime.now(timezone.utc)

    # Query last 10 runs
    con = sqlite3.connect(DB)
    rows = con.execute(
        "SELECT status, error, finished_at FROM executions "
        "WHERE job_id = ? ORDER BY claimed_at DESC LIMIT 10",
        (JOB_ID,)
    ).fetchall()
    con.close()

    if not rows:
        print("NO_DATA")
        return

    # Count consecutive failures and timeouts
    consecutive_failures = 0
    consecutive_timeouts = 0
    last_error = ""
    last_error_type = None
    statuses = []

    for status, error, finished_at in rows:
        s = status[0].upper() if status else "?"
        statuses.append(s)
        if status in ("failed", "error"):
            consecutive_failures += 1
            if not last_error:
                last_error = (error or "").strip()
                last_error_type, _ = classify_error(last_error)
                if last_error_type == "timeout":
                    consecutive_timeouts = consecutive_failures  # all consecutive failures are timeouts
        else:
            break

    # Re-count timeouts specifically
    consecutive_timeouts = 0
    for status, error, finished_at in rows:
        if status in ("failed", "error"):
            etype, _ = classify_error((error or "").strip())
            if etype == "timeout":
                consecutive_timeouts += 1
            else:
                break
        else:
            break

    # Check cooldown
    cooldown_until = None
    if state.get("cooldown_until"):
        cooldown_until = datetime.fromisoformat(state["cooldown_until"])
    
    cooldown_active = False
    cooldown_remaining = 0

    if cooldown_until and now < cooldown_until:
        cooldown_active = True
        cooldown_remaining = int((cooldown_until - now).total_seconds() / 60)
    elif cooldown_until and now >= cooldown_until:
        # Cooldown expired
        cooldown_until = None
        print("COOLDOWN_EXPIRED=true")

    # Should we enter cooldown?
    if not cooldown_active and consecutive_timeouts >= TIMEOUT_THRESHOLD:
        cooldown_until = now + timedelta(hours=COOLDOWN_HOURS)
        cooldown_active = True
        cooldown_remaining = COOLDOWN_HOURS * 60
        print(f"COOLDOWN_STARTED=true")

    # Determine if we should alert
    should_alert = False
    alert_reason = ""

    last_alerted = state.get("last_alerted_failures", 0)

    if cooldown_active and not state.get("cooldown_until"):
        # Just entered cooldown — alert once
        should_alert = True
        alert_reason = f"cooldown_started: {consecutive_timeouts} consecutive timeouts, pausing for {COOLDOWN_HOURS}h"
    elif consecutive_failures == 0 and last_alerted > 0:
        # Recovery
        should_alert = True
        alert_reason = "recovery: pulse is healthy again"
    elif consecutive_failures > last_alerted and not cooldown_active:
        # Situation got worse
        should_alert = True
        alert_reason = f"escalation: {consecutive_failures} consecutive failures (was {last_alerted}), type={last_error_type}"
    elif consecutive_failures > 0 and consecutive_failures == last_alerted:
        # Same state, no change — don't re-alert unless it's been >2 hours
        last_alerted_at = state.get("last_alerted_at")
        if last_alerted_at:
            last_at = datetime.fromisoformat(last_alerted_at)
            if (now - last_at) > timedelta(hours=2):
                should_alert = True
                alert_reason = f"reminder: {consecutive_failures} consecutive failures still ongoing (last alert >2h ago)"

    # Update state
    state["consecutive_failures"] = consecutive_failures
    state["consecutive_timeouts"] = consecutive_timeouts
    state["last_error_type"] = last_error_type
    state["last_error_message"] = last_error[:200] if last_error else None
    state["cooldown_until"] = cooldown_until.isoformat() if cooldown_until else None
    state["last_5_statuses"] = statuses[:5]
    if should_alert:
        state["last_alerted_failures"] = consecutive_failures
        state["last_alerted_at"] = now.isoformat()
    save_state(state)

    # Output
    print(f"CONSECUTIVE_FAILURES={consecutive_failures}")
    print(f"CONSECUTIVE_TIMEOUTS={consecutive_timeouts}")
    print(f"LAST_ERROR_TYPE={last_error_type or 'none'}")
    if last_error:
        print(f"LAST_ERROR={last_error.split(chr(10))[0][:200]}")
    print(f"COOLDOWN_ACTIVE={'true' if cooldown_active else 'false'}")
    if cooldown_active:
        print(f"COOLDOWN_REMAINING_MINUTES={cooldown_remaining}")
    print(f"SHOULD_ALERT={'true' if should_alert else 'false'}")
    if alert_reason:
        print(f"ALERT_REASON={alert_reason}")
    print(f"LAST_5={' '.join(statuses[:5])}")

if __name__ == "__main__":
    main()
