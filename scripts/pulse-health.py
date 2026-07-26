#!/usr/bin/env python3
"""Query cron execution history for aura-pulse failures. Zero AI tokens."""
import sqlite3, sys
from datetime import datetime, timezone

DB = "/Users/sergio/.hermes/cron/executions.db"
JOB_ID = "bf744ee67796"

def main():
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

    # Count consecutive failures from most recent
    consecutive = 0
    last_error = ""
    for status, error, finished_at in rows:
        if status in ("failed", "error"):
            consecutive += 1
            if not last_error:
                last_error = (error or "").strip()
        else:
            break

    print(f"CONSECUTIVE_FAILURES={consecutive}")
    if last_error:
        # Truncate to first line
        print(f"LAST_ERROR={last_error.split(chr(10))[0][:200]}")

    # Also print last 5 statuses for context
    statuses = [r[0][0].upper() for r in rows[:5]]  # F, C, R
    print(f"LAST_5={' '.join(statuses)}")

if __name__ == "__main__":
    main()
