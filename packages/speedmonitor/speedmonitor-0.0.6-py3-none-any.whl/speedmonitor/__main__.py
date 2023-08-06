"""
"""
from speedmonitor.speedlib import run_local_monitor
import os


LOCATION = os.environ.get('SPEEDMONITOR_LOCATION', 'unknown')
INTERVAL_SECONDS = int(os.environ.get('SPEEDMONITOR_INTERVAL_SECONDS', '60'))
FILENAME = os.environ.get('SPEEDMONITOR_FILENAME', 'speedtest.json')
run_local_monitor(LOCATION, INTERVAL_SECONDS, FILENAME)
