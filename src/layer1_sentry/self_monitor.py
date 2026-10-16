"""HYDRA-GRID Layer 1 - Self-integrity monitor."""
import hashlib

from src.core.constants import (
    MAINTENANCE_WINDOW, RATE_LIMIT_MAX, ALLOWED_COMMAND_SOURCES
)


class SelfIntegrityMonitor:
    def __init__(self):
        self.startup_fingerprint = self._fingerprint()

    def _fingerprint(self):
        policy = (
            f"{sorted(MAINTENANCE_WINDOW)}|"
            f"{RATE_LIMIT_MAX}|"
            f"{sorted(ALLOWED_COMMAND_SOURCES)}"
        )
        return hashlib.sha256(policy.encode()).hexdigest()[:16]

    def check(self):
        if self._fingerprint() != self.startup_fingerprint:
            return False, "SELF-INTEGRITY FAILURE - policy modified!"
        return True, "Self-integrity OK."
