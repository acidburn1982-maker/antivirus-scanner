#!/usr/bin/env python3
"""
Malware Signature Database Manager
Handles storage, retrieval, and updating of malware signatures
"""

import json
import os
from typing import Dict, Optional
from datetime import datetime


class SignatureDatabase:
    """Manages malware signature database"""

    def __init__(self, db_path: str = "data/signatures.json"):
        self.db_path = db_path
        self.signatures = {}
        self.last_updated = None
        self.load_signatures()

    def load_signatures(self):
        """Load signatures from local database"""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r") as f:
                    data = json.load(f)
                    self.signatures = data.get("signatures", {})
                    self.last_updated = data.get("last_updated", None)
            except json.JSONDecodeError:
                print(f"Error loading signatures")
                self.signatures = {}
        else:
            self._initialize_default_signatures()

    def _initialize_default_signatures(self):
        """Initialize with default malware signatures for testing"""
        default_signatures = {
            "5d41402abc4b2a76b9719d911017c592": {
                "name": "Trojan.GenericA",
                "type": "Trojan",
                "severity": "High",
                "description": "Generic trojan detected"
            },
            "6512bd43d9caa6e02c990b0a82652dca": {
                "name": "Worm.BasicWorm",
                "type": "Worm",
                "severity": "Critical",
                "description": "Generic worm detected"
            },
            "e4d909c290d0fb1ca068ffaddf22cbd0": {
                "name": "Ransom.CryptoLocker",
                "type": "Ransomware",
                "severity": "Critical",
                "description": "Ransomware variant detected"
            }
        }
        self.signatures = default_signatures
        self.save_signatures()

    def save_signatures(self):
        """Save signatures to database file"""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            data = {
                "signatures": self.signatures,
                "last_updated": datetime.now().isoformat(),
                "total_signatures": len(self.signatures)
            }
            with open(self.db_path, "w") as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Error saving signatures: {e}")

    def search_signature(self, file_hash: str) -> Optional[Dict]:
        """Search for signature by hash"""
        return self.signatures.get(file_hash, None)

    def add_signature(self, file_hash: str, threat_info: Dict):
        """Add new signature to database"""
        self.signatures[file_hash] = threat_info
        self.save_signatures()

    def get_statistics(self) -> Dict:
        """Get database statistics"""
        threat_types = {}
        for sig in self.signatures.values():
            threat_type = sig.get("type", "Unknown")
            threat_types[threat_type] = threat_types.get(threat_type, 0) + 1

        return {
            "total_signatures": len(self.signatures),
            "threat_types": threat_types,
            "last_updated": self.last_updated
        }


if __name__ == "__main__":
    db = SignatureDatabase()
    stats = db.get_statistics()
    print(f"Signature Database Statistics:")
    print(f"Total Signatures: {stats['total_signatures']}")
    print(f"Threat Types: {stats['threat_types']}")
