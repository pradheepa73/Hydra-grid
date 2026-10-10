"""HYDRA-GRID Layer 1 - Merkle audit log."""
import hashlib
import time
from datetime import datetime


class MerkleAuditLog:
    def __init__(self):
        self.entries = []

    def append(self, event_type, source, details, verdict):
        raw = f"{event_type}|{source}|{details}|{verdict}|{time.time()}"
        entry_hash = hashlib.sha256(raw.encode()).hexdigest()
        self.entries.append({
            "ts": datetime.now().strftime("%H:%M:%S"),
            "type": event_type,
            "source": source,
            "details": details,
            "verdict": verdict,
            "hash": entry_hash,
        })

    def merkle_root(self):
        if not self.entries:
            return "EMPTY"
        level = [e["hash"] for e in self.entries]
        while len(level) > 1:
            if len(level) % 2 == 1:
                level.append(level[-1])
            level = [
                hashlib.sha256((level[i] + level[i + 1]).encode()).hexdigest()
                for i in range(0, len(level), 2)
            ]
        return level[0][:16]
