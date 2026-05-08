#!/usr/bin/env python3
"""
Quarantine Management System
Handles safe storage and management of detected threats
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class QuarantineManager:
    """Manages quarantine of suspicious/malicious files"""

    def __init__(self, quarantine_dir: str = "data/quarantine"):
        self.quarantine_dir = quarantine_dir
        self.quarantine_index = os.path.join(quarantine_dir, "index.json")
        self._ensure_directory()
        self.load_index()

    def _ensure_directory(self):
        """Ensure quarantine directory exists"""
        os.makedirs(self.quarantine_dir, exist_ok=True)

    def load_index(self):
        """Load quarantine index"""
        if os.path.exists(self.quarantine_index):
            try:
                with open(self.quarantine_index, "r") as f:
                    self.quarantine_items = json.load(f)
            except json.JSONDecodeError:
                self.quarantine_items = []
        else:
            self.quarantine_items = []

    def save_index(self):
        """Save quarantine index"""
        with open(self.quarantine_index, "w") as f:
            json.dump(self.quarantine_items, f, indent=2)

    def quarantine_file(self, file_path: str, threat_info: Dict) -> bool:
        """Move file to quarantine"""
        try:
            if not os.path.exists(file_path):
                return False

            file_name = os.path.basename(file_path)
            timestamp = datetime.now().isoformat().replace(":", "-")
            quarantine_file = os.path.join(self.quarantine_dir, f"{timestamp}_{file_name}")

            shutil.move(file_path, quarantine_file)

            quarantine_record = {
                "original_path": file_path,
                "quarantine_path": quarantine_file,
                "threat_name": threat_info.get("name", "Unknown"),
                "threat_type": threat_info.get("type", "Unknown"),
                "severity": threat_info.get("severity", "Unknown"),
                "quarantine_date": datetime.now().isoformat(),
                "action": "quarantined"
            }
            self.quarantine_items.append(quarantine_record)
            self.save_index()

            return True
        except Exception as e:
            print(f"Error quarantining file: {e}")
            return False

    def restore_file(self, quarantine_path: str, restore_path: str = None) -> bool:
        """Restore file from quarantine"""
        try:
            if not os.path.exists(quarantine_path):
                return False

            for item in self.quarantine_items:
                if item["quarantine_path"] == quarantine_path:
                    restore_path = restore_path or item["original_path"]
                    break

            if not restore_path:
                return False

            os.makedirs(os.path.dirname(restore_path), exist_ok=True)
            shutil.copy2(quarantine_path, restore_path)

            for item in self.quarantine_items:
                if item["quarantine_path"] == quarantine_path:
                    item["action"] = "restored"
                    item["restore_date"] = datetime.now().isoformat()
                    break

            self.save_index()
            return True
        except Exception as e:
            print(f"Error restoring file: {e}")
            return False

    def delete_file(self, quarantine_path: str) -> bool:
        """Permanently delete file from quarantine"""
        try:
            if os.path.exists(quarantine_path):
                os.remove(quarantine_path)

            for item in self.quarantine_items:
                if item["quarantine_path"] == quarantine_path:
                    item["action"] = "deleted"
                    item["delete_date"] = datetime.now().isoformat()
                    break

            self.save_index()
            return True
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False

    def get_quarantine_list(self) -> List[Dict]:
        """Get list of quarantined files"""
        return [item for item in self.quarantine_items if item.get("action") == "quarantined"]

    def get_statistics(self) -> Dict:
        """Get quarantine statistics"""
        quarantined = [i for i in self.quarantine_items if i.get("action") == "quarantined"]
        threat_types = {}
        for item in quarantined:
            threat_type = item.get("threat_type", "Unknown")
            threat_types[threat_type] = threat_types.get(threat_type, 0) + 1

        return {
            "total_quarantined": len(quarantined),
            "threat_types": threat_types,
            "total_history": len(self.quarantine_items)
        }


if __name__ == "__main__":
    qm = QuarantineManager()
    stats = qm.get_statistics()
    print(f"Quarantine Statistics:")
    print(f"Total Quarantined: {stats['total_quarantined']}")
