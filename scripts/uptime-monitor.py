#!/usr/bin/env python3
"""
Aura uptime monitor — pings the landing page, logs response times, alerts on downtime.
Zero dependencies. Run as a cron job every 5 minutes.

Usage: python3 uptime-monitor.py [--alert-webhook URL]
  Without --alert-webhook: prints status to stdout (cron output)
  With --alert-webhook: POSTs alerts to the webhook URL on state changes
"""
import urllib.request
import urllib.error
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

TARGET = "https://sergio-pb.github.io/aura-workspace/"
STATE_FILE = os.path.expanduser("~/aura-workspace/logs/uptime-state.json")
LOG_FILE = os.path.expanduser("~/aura-workspace/logs/uptime-log.jsonl")
TIMEOUT_SEC = 15
ALERT_AFTER_FAILURES = 2  # consecutive failures before alerting

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"consecutive_failures": 0, "last_alerted_failures": 0, "last_status": None}

def save_state(s):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(s, f, indent=2)

def log_entry(entry):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

def ping():
    start = time.monotonic()
    try:
        req = urllib.request.Request(TARGET, method="HEAD")
        resp = urllib.request.urlopen(req, timeout=TIMEOUT_SEC)
        elapsed = round((time.monotonic() - start) * 1000)
        return {"status": resp.status, "ms": elapsed, "error": None}
    except urllib.error.HTTPError as e:
        elapsed = round((time.monotonic() - start) * 1000)
        return {"status": e.code, "ms": elapsed, "error": f"HTTP {e.code}"}
    except Exception as e:
        elapsed = round((time.monotonic() - start) * 1000)
        return {"status": 0, "ms": elapsed, "error": str(e)[:200]}

def main():
    webhook = None
    args = sys.argv[1:]
    if len(args) >= 2 and args[0] == "--alert-webhook":
        webhook = args[1]

    state = load_state()
    now = datetime.now(timezone.utc)
    result = ping()

    entry = {
        "timestamp": now.isoformat(),
        "target": TARGET,
        "status": result["status"],
        "ms": result["ms"],
        "error": result["error"],
    }
    log_entry(entry)

    is_up = result["status"] == 200

    if is_up:
        state["consecutive_failures"] = 0
        state["last_status"] = "up"
        print(f"UP — {result['ms']}ms")
    else:
        state["consecutive_failures"] += 1
        state["last_status"] = "down"
        print(f"DOWN — {result['error']} ({result['ms']}ms) — failures: {state['consecutive_failures']}")

    # Alert on state transitions
    should_alert = False
    alert_msg = ""

    if state["consecutive_failures"] == ALERT_AFTER_FAILURES:
        should_alert = True
        alert_msg = f"DOWN: {TARGET} unreachable after {ALERT_AFTER_FAILURES} consecutive failures. Last error: {result['error']}"
    elif state["consecutive_failures"] == 0 and state.get("last_alerted_failures", 0) > 0:
        should_alert = True
        alert_msg = f"RECOVERED: {TARGET} is back up ({result['ms']}ms)"

    if should_alert:
        state["last_alerted_failures"] = state["consecutive_failures"]
        print(f"ALERT: {alert_msg}")
        if webhook:
            try:
                data = json.dumps({"text": alert_msg, "timestamp": now.isoformat()}).encode()
                req = urllib.request.Request(webhook, data=data, headers={"Content-Type": "application/json"})
                urllib.request.urlopen(req, timeout=10)
            except Exception as e:
                print(f"Webhook delivery failed: {e}")

    save_state(state)

if __name__ == "__main__":
    main()
