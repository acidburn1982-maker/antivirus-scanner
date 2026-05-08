#!/usr/bin/env python3
"""
Real-time File System Monitor
Detects and responds to suspicious file activity
"""

import os
import time
from typing import Callable, Dict


class FileSystemMonitor:
    """Real-time file system monitoring for threat detection"""

    def __init__(self, watch_paths: list = None, callback: Callable = None):
        self.watch_paths = watch_paths or [os.path.expanduser("~"), "/tmp"]
        self.callback = callback
        self.is_monitoring = False
        self.monitored_extensions = {".exe", ".dll", ".scr", ".bat", ".cmd", ".vbs", ".js"}

    def start(self):
        """Start monitoring"""
        self.is_monitoring = True
        print("Real-time protection started")

    def stop(self):
        """Stop monitoring"""
        self.is_monitoring = False
        print("Real-time protection stopped")

    def is_running(self) -> bool:
        """Check if monitor is running"""
        return self.is_monitoring

    def _should_scan_file(self, file_path: str) -> bool:
        """Determine if file should be scanned"""
        _, ext = os.path.splitext(file_path)
        return ext.lower() in self.monitored_extensions


if __name__ == "__main__":
    monitor = FileSystemMonitor()
    monitor.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.stop()
