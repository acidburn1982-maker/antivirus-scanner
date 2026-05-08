#!/usr/bin/env python3
"""
Core Antivirus Scanner Engine
Handles malware detection through signature matching and heuristic analysis
"""

import os
import hashlib
import json
import threading
from pathlib import Path
from typing import List, Dict, Tuple
import time


class MalwareScanner:
    """Main scanner class for detecting malware through signature matching"""

    def __init__(self, signature_db_path: str = "data/signatures.json"):
        self.signature_db_path = signature_db_path
        self.signatures = {}
        self.is_scanning = False
        self.scan_progress = 0
        self.total_files = 0
        self.files_scanned = 0
        self.threats_found = []
        self.load_signatures()

    def load_signatures(self):
        """Load signatures from local database"""
        if os.path.exists(self.signature_db_path):
            try:
                with open(self.signature_db_path, 'r') as f:
                    data = json.load(f)
                    self.signatures = data.get('signatures', {})
            except json.JSONDecodeError:
                print(f"Error loading signatures")
                self.signatures = {}

    def compute_file_hash(self, file_path: str) -> str:
        """Compute SHA-256 hash of a file"""
        hash_obj = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        except (IOError, OSError) as e:
            return None

    def check_file_signature(self, file_path: str) -> Tuple[bool, Dict]:
        """Check if file matches known malware signatures"""
        file_hash = self.compute_file_hash(file_path)
        if not file_hash:
            return False, {}

        threat_info = self.signatures.get(file_hash)
        if threat_info:
            threat_info['file_path'] = file_path
            threat_info['detected_time'] = time.time()
            return True, threat_info

        return False, {}

    def scan_file(self, file_path: str) -> bool:
        """Scan single file for malware"""
        try:
            if not os.path.isfile(file_path):
                return False

            is_threat, threat_info = self.check_file_signature(file_path)
            if is_threat:
                self.threats_found.append(threat_info)
                return True
            return False
        except Exception as e:
            return False

    def scan_directory(self, directory: str, recursive: bool = True) -> List[Dict]:
        """Recursively scan directory for malware"""
        self.is_scanning = True
        self.threats_found = []
        self.files_scanned = 0

        try:
            for file_path in Path(directory).rglob("*") if recursive else Path(directory).glob("*"):
                if not self.is_scanning:
                    break

                if file_path.is_file():
                    self.scan_file(str(file_path))
                    self.files_scanned += 1

        except Exception as e:
            print(f"Error scanning directory: {e}")
        finally:
            self.is_scanning = False

        return self.threats_found

    def quick_scan(self) -> List[Dict]:
        """Scan common system directories"""
        scan_dirs = []
        if os.name == "nt":
            scan_dirs = ["C:\\Users\\", "C:\\Windows\\Temp"]
        else:
            scan_dirs = [os.path.expanduser("~"), "/tmp"]

        all_threats = []
        for directory in scan_dirs:
            if os.path.exists(directory):
                threats = self.scan_directory(directory, recursive=True)
                all_threats.extend(threats)

        return all_threats

    def stop_scan(self):
        """Stop ongoing scan"""
        self.is_scanning = False

    def get_progress(self) -> Dict:
        """Get current scan progress"""
        return {
            "is_scanning": self.is_scanning,
            "progress": self.scan_progress,
            "files_scanned": self.files_scanned,
            "total_files": self.total_files,
            "threats_found": len(self.threats_found)
        }


if __name__ == "__main__":
    scanner = MalwareScanner()
    print("Scanner ready")
