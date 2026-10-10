"""HYDRA-GRID - Unified logging helper."""
import hashlib
import time
from datetime import datetime


class HydraLogger:
    def __init__(self, name="HYDRA-GRID"):
        self.name = name
        self.entries = []

    def log(self, layer, event_type, source, details, verdict):
        raw = f"{layer}|{event_type}|{source}|{details}|{verdict}|{time.time()}"
        entry = {
            "ts": datetime.now().strftime("%H:%M:%S"),
            "layer": layer,
            "type": event_type,
            "source": source,
            "details": details,
            "verdict": verdict,
            "hash": hashlib.sha256(raw.encode()).hexdigest()[:16],
        }
        self.entries.append(entry)
        return entry
