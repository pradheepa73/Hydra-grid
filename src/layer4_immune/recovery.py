"""HYDRA-GRID Layer 4 - Golden Image Auto-Recovery."""
import hashlib
import json
import os
import time
from datetime import datetime


class GoldenImageRecovery:
    def __init__(self, snapshot_dir=".hydra_snapshots"):
        self.snapshot_dir = snapshot_dir
        os.makedirs(snapshot_dir, exist_ok=True)
        self.recovery_events = []

    def _path_for(self, node_id):
        return os.path.join(self.snapshot_dir, node_id + "_golden.json")

    def _hash_state(self, state):
        serialized = json.dumps(state, sort_keys=True).encode()
        return hashlib.sha256(serialized).hexdigest()[:16]

    def create_golden_image(self, node_id, clean_state):
        path = self._path_for(node_id)
        envelope = {
            "node_id": node_id,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "hash": self._hash_state(clean_state),
            "state": clean_state,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(envelope, f)
        return envelope["hash"]

    def verify_golden_image(self, node_id):
        path = self._path_for(node_id)
        if not os.path.exists(path):
            return False, "Golden image not found"
        try:
            with open(path, encoding="utf-8") as f:
                envelope = json.load(f)
        except (json.JSONDecodeError, ValueError) as e:
            return False, "Golden image corrupted - tampering detected: " + str(e)
        if "state" not in envelope or "hash" not in envelope:
            return False, "Golden image missing fields - tampering detected"
        expected_hash = self._hash_state(envelope["state"])
        if expected_hash != envelope["hash"]:
            return False, "Golden image hash mismatch - tampering detected"
        return True, envelope

    def restore(self, node_id, current_state=None):
        t0 = time.perf_counter()
        ok, result = self.verify_golden_image(node_id)
        if not ok:
            self.recovery_events.append({
                "ts": datetime.now().strftime("%H:%M:%S"),
                "node": node_id,
                "status": "FAILED",
            })
            return False, 0, None
        envelope = result
        elapsed_ms = (time.perf_counter() - t0) * 1000
        self.recovery_events.append({
            "ts": datetime.now().strftime("%H:%M:%S"),
            "node": node_id,
            "status": "RESTORED",
            "elapsed_ms": round(elapsed_ms, 2),
        })
        return True, elapsed_ms, envelope["state"]

    def simulate_attack(self, node_id):
        path = self._path_for(node_id)
        if os.path.exists(path):
            with open(path, "a", encoding="utf-8") as f:
                f.write("\n# COMPROMISED")
        return True

    def summary(self):
        total = len(self.recovery_events)
        succeeded = sum(1 for e in self.recovery_events if e["status"] == "RESTORED")
        return {
            "total_recoveries": total,
            "succeeded": succeeded,
            "failed": total - succeeded,
        }


if __name__ == "__main__":
    print("HYDRA-GRID Golden Image Recovery Demo\n")
    r = GoldenImageRecovery()
    state = {"breakers": {"B1": "CLOSED", "B2": "CLOSED", "B3": "CLOSED"}, "voltage": 1.0}
    h = r.create_golden_image("SUBSTATION_A", state)
    print("[GOLDEN] Image created. Hash: " + h)
    ok, _ = r.verify_golden_image("SUBSTATION_A")
    print("[GOLDEN] Integrity check: " + str(ok))
    print("[ATTACK] Attacker compromises SUBSTATION_A ...")
    r.simulate_attack("SUBSTATION_A")
    time.sleep(0.5)
    success, ms, restored = r.restore("SUBSTATION_A")
    print("[RECOVER] Status: " + str(success) + ", Elapsed: " + str(round(ms, 2)) + " ms")
    print("[SUMMARY] " + str(r.summary()))
