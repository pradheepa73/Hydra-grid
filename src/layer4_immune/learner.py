"""HYDRA-GRID Layer 4 - Adaptive Immune Learner."""
import time

from src.layer4_immune.signature import SignatureStore


class ImmuneLearner:
    """
    Learns from attacks. Next attempt is blocked in <1ms.
    Safety gates:
      1. Human approval required before deployment
      2. Signatures hashed (tamper-evident)
      3. Learner isolated (no network access to real grid)
    """

    def __init__(self, auto_approve=False):
        self.store = SignatureStore()
        self.auto_approve = auto_approve
        self.events = []

    def observe_attack(self, sequence, source="MIRAGE_GRID"):
        """
        Called when the honeypot captures an attack.
        Returns (sig, status).
        """
        sig, status = self.store.propose(sequence, source)
        self.events.append({
            "ts": time.time(),
            "hash": sig.hash,
            "status": status,
            "sequence": sequence,
        })

        if self.auto_approve and status == "proposed":
            self.store.approve(sig.hash)
            status = "auto_approved"

        return sig, status

    def check(self, sequence):
        """
        Fast path — checked BEFORE the twin runs.
        Returns (is_known, reason, latency_ms).
        """
        t0 = time.perf_counter()
        known = self.store.is_known(sequence)
        latency_ms = (time.perf_counter() - t0) * 1000

        if known:
            return True, "Signature match — known attack blocked.", latency_ms
        return False, "No known signature.", latency_ms

    def approve(self, sig_hash):
        return self.store.approve(sig_hash)

    def reject(self, sig_hash):
        return self.store.reject(sig_hash)

    def stats(self):
        return self.store.stats()
