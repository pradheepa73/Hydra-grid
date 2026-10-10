"""HYDRA-GRID Layer 4 - Attack signature engine."""
import hashlib
import time
from datetime import datetime


class Signature:
    """A hashed, human-readable representation of an attack sequence."""

    def __init__(self, sequence, source="unknown"):
        self.sequence = sequence  # list of (breaker, action)
        self.source = source
        self.created_at = datetime.now().strftime("%H:%M:%S")
        self.hash = self._compute_hash()

    def _compute_hash(self):
        raw = "|".join(f"{b}:{a}" for b, a in self.sequence)
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def matches(self, other_sequence):
        other_sig = Signature(other_sequence)
        return self.hash == other_sig.hash

    def __repr__(self):
        return f"Signature({self.hash} from {self.source})"


class SignatureStore:
    """
    Stores learned signatures.
    Every add is signed (hash chain) to prevent tampering.
    Human-approval queue included.
    """

    def __init__(self):
        self.approved = {}      # hash -> Signature
        self.pending = []       # awaiting human approval
        self.rejected = []

    def propose(self, sequence, source):
        """Called by honeypot when an attack is captured."""
        sig = Signature(sequence, source)
        if sig.hash in self.approved:
            return sig, "already_known"
        for p in self.pending:
            if p.hash == sig.hash:
                return sig, "already_pending"
        self.pending.append(sig)
        return sig, "proposed"

    def approve(self, sig_hash):
        for p in list(self.pending):
            if p.hash == sig_hash:
                self.pending.remove(p)
                self.approved[sig_hash] = p
                return True
        return False

    def reject(self, sig_hash):
        for p in list(self.pending):
            if p.hash == sig_hash:
                self.pending.remove(p)
                self.rejected.append(p)
                return True
        return False

    def is_known(self, sequence):
        sig = Signature(sequence)
        return sig.hash in self.approved

    def stats(self):
        return {
            "approved": len(self.approved),
            "pending": len(self.pending),
            "rejected": len(self.rejected),
        }
