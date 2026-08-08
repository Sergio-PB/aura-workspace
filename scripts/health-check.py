#!/usr/bin/env python3
"""
Aura health check — one script, three modes. Zero AI tokens.
  pulse:    tracks pulse failures, outputs KEY=VALUE for LLM context
  watchdog: system health (disk, memory, git, OpenCode, errors), human output
  heartbeat: checks pulse liveness, human output

Watchdog and heartbeat modes: silent (empty stdout) when healthy.
Usage: python3 health-check.py [pulse|watchdog|heartbeat]
"""
import sqlite3, json, os, sys, subprocess, shutil
from datetime import datetime, timezone, timedelta
from pathlib import Path

DB = os.path.expanduser("~/.hermes/cron/executions.db")
JOB_ID = "bf744ee67796"
STATE_FILE = os.path.expanduser("~/aura-workspace/logs/pulse-state.json")
COOLDOWN_HOURS = 4
TIMEOUT_THRESHOLD = 3
WORKSPACE = os.path.expanduser("~/aura-workspace")
ERROR_LOG = os.path.join(WORKSPACE, "logs", "errors.md")

# ── pulse mode (data collection for LLM) ──────────────────────────

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
        "last_5_statuses": [],
    }

def save_state(s):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(s, f, indent=2)

def pulse_mode():
    state = load_state()
    now = datetime.now(timezone.utc)

    con = sqlite3.connect(DB)
    rows = con.execute(
        "SELECT status, error, finished_at FROM executions "
        "WHERE job_id = ? ORDER BY claimed_at DESC LIMIT 10",
        (JOB_ID,),
    ).fetchall()
    con.close()

    if not rows:
        print("NO_DATA")
        return

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

    cooldown_until = None
    if state.get("cooldown_until"):
        cooldown_until = datetime.fromisoformat(state["cooldown_until"])

    cooldown_active = False
    cooldown_remaining = 0

    if cooldown_until and now < cooldown_until:
        cooldown_active = True
        cooldown_remaining = int((cooldown_until - now).total_seconds() / 60)
    elif cooldown_until and now >= cooldown_until:
        cooldown_until = None
        print("COOLDOWN_EXPIRED=true")

    if not cooldown_active and consecutive_timeouts >= TIMEOUT_THRESHOLD:
        cooldown_until = now + timedelta(hours=COOLDOWN_HOURS)
        cooldown_active = True
        cooldown_remaining = COOLDOWN_HOURS * 60
        print("COOLDOWN_STARTED=true")

    should_alert = False
    alert_reason = ""
    last_alerted = state.get("last_alerted_failures", 0)

    if cooldown_active and not state.get("cooldown_until"):
        should_alert = True
        alert_reason = f"cooldown_started: {consecutive_timeouts} consecutive timeouts, pausing for {COOLDOWN_HOURS}h"
    elif consecutive_failures == 0 and last_alerted > 0:
        should_alert = True
        alert_reason = "recovery: pulse is healthy again"
    elif consecutive_failures > last_alerted and not cooldown_active:
        should_alert = True
        alert_reason = f"escalation: {consecutive_failures} consecutive failures (was {last_alerted}), type={last_error_type}"
    elif consecutive_failures > 0 and consecutive_failures == last_alerted:
        last_alerted_at = state.get("last_alerted_at")
        if last_alerted_at:
            last_at = datetime.fromisoformat(last_alerted_at)
            if (now - last_at) > timedelta(hours=2):
                should_alert = True
                alert_reason = f"reminder: {consecutive_failures} consecutive failures still ongoing (last alert >2h ago)"

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


# ── watchdog mode (system health, human output) ───────────────────

def run(cmd, timeout=10):
    """Run a command, return (stdout, stderr, exit_code)."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, shell=True)
        return r.stdout.strip(), r.stderr.strip(), r.returncode
    except subprocess.TimeoutExpired:
        return "", "timeout", -1
    except Exception as e:
        return "", str(e), -1

def check_disk():
    """Alert if any volume > 85%."""
    usage = shutil.disk_usage("/")
    pct = (usage.used / usage.total) * 100
    if pct > 85:
        return f"Disk {pct:.0f}% used ({usage.free // (1024**3)} GB free)"
    return None

def check_memory():
    """Alert if memory pressure is high."""
    out, _, _ = run("memory_pressure 2>&1 | head -1", timeout=5)
    if not out:
        out, _, _ = run("vm_stat 2>&1 | head -5", timeout=5)
        # ponytail: rough heuristic — if vm_stat is all we have, skip deep parsing
        return None
    if "critical" in out.lower():
        return f"Memory pressure CRITICAL: {out}"
    return None

def check_git():
    """Alert if uncommitted changes > 2h old."""
    out, _, rc = run(f"cd {WORKSPACE} && git status --porcelain", timeout=10)
    if rc != 0 or not out:
        return None
    # Check mtime of modified files
    now = datetime.now()
    stale = []
    for line in out.split("\n"):
        line = line.strip()
        if not line:
            continue
        # git status --porcelain: " M path" or "?? path"
        fpath = line[3:].strip().split(" -> ")[-1]  # handle renames
        full = os.path.join(WORKSPACE, fpath)
        if os.path.exists(full):
            mtime = datetime.fromtimestamp(os.path.getmtime(full))
            age_h = (now - mtime).total_seconds() / 3600
            if age_h > 2:
                stale.append(f"{fpath} ({age_h:.0f}h)")
    if stale:
        return f"Uncommitted changes >2h: {', '.join(stale[:5])}"
    return None

def check_opencode():
    """Alert if OpenCode is not functional."""
    out, _, rc = run("opencode models ollama 2>&1", timeout=15)
    if rc != 0 or "error" in out.lower():
        return f"OpenCode unhealthy: {out[:200]}"
    return None

def check_errors():
    """Alert if error log has recent RETRY-FAILED entries."""
    if not os.path.exists(ERROR_LOG):
        return None
    now = datetime.now()
    recent = []
    with open(ERROR_LOG) as f:
        for line in f:
            if "RETRY-FAILED" in line:
                # Extract timestamp: [2026-08-08T15:00:00]
                try:
                    ts_str = line.split("]")[0].lstrip("[")
                    ts = datetime.fromisoformat(ts_str)
                    age_h = (now - ts).total_seconds() / 3600
                    if age_h < 24:
                        recent.append(line.strip()[:200])
                except (ValueError, IndexError):
                    pass
    if recent:
        return f"Recent RETRY-FAILED ({len(recent)}):\n" + "\n".join(recent[-3:])
    return None

def watchdog_mode():
    issues = []
    for check_fn, label in [
        (check_disk, "Disk"),
        (check_memory, "Memory"),
        (check_git, "Git"),
        (check_opencode, "OpenCode"),
        (check_errors, "Errors"),
    ]:
        result = check_fn()
        if result:
            issues.append(f"{label}: {result}")

    if not issues:
        return  # silent when healthy

    print("Aura Watchdog Alert")
    print("=" * 40)
    for issue in issues:
        print(f"  {issue}")
    print(f"\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")


# ── heartbeat mode (pulse liveness) ───────────────────────────────

def heartbeat_mode():
    con = sqlite3.connect(DB)
    row = con.execute(
        "SELECT finished_at, status FROM executions "
        "WHERE job_id = ? ORDER BY claimed_at DESC LIMIT 1",
        (JOB_ID,),
    ).fetchone()
    con.close()

    if not row:
        print("Heartbeat: no pulse runs found")
        return

    finished_at, status = row
    if not finished_at:
        print("Heartbeat: pulse has never completed a run")
        return

    last_run = datetime.fromisoformat(finished_at)
    now = datetime.now(timezone.utc)
    age_min = (now - last_run).total_seconds() / 60

    if age_min > 45:
        print(f"Heartbeat: pulse last ran {age_min:.0f} min ago (status: {status})")
    # silent when healthy


# ── main ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "pulse"
    if mode == "pulse":
        pulse_mode()
    elif mode == "watchdog":
        watchdog_mode()
    elif mode == "heartbeat":
        heartbeat_mode()
    else:
        print(f"Unknown mode: {mode}. Use pulse, watchdog, or heartbeat.", file=sys.stderr)
        sys.exit(1)
