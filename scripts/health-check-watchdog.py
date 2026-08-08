#!/usr/bin/env python3
"""Thin wrapper: run health-check.py in watchdog mode (scheduler passes no args)."""
import sys, runpy
sys.argv = ["health-check.py", "watchdog"]
runpy.run_path("/Users/sergio/.hermes/scripts/health-check.py", run_name="__main__")
