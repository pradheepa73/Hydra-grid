"""Shadow Sentinel - Independent Watchdog for HYDRA-GRID.

Not a layer. A separate application that monitors the 5 primary layers.
Activates when 2+ of 5 danger signals (H-D-I-V-S) fire together.
"""
import hashlib
import time
from datetime import datetime


class ShadowSentinel:
    HEARTBEAT_TIMEOUT = 30
    TRIGGER_THRESHOLD = 2
    PATTERN_WINDOW = 60
    PATTERN_MIN_EVENTS = 5

    def __init__(self):
        self.layer_heartbeats = {}
        self.expected_decisions = []
        self.observed_decisions = []
        self.integrity_checks = {}
        self.view_reports = {}
        self.recent_events = []
        self.log = []
        self.alert_queue = []
        self.activated = False

    def heartbeat(self, layer):
        self.layer_heartbeats[layer] = time.time()

    def record_expected(self, command, expected_verdict):
        self.expected_decisions.append({"cmd": command, "expected": expected_verdict, "ts": time.time()})

    def record_observed(self, command, actual_verdict):
        self.observed_decisions.append({"cmd": command, "actual": actual_verdict, "ts": time.time()})

    def record_integrity(self, layer, state_hash):
        self.integrity_checks[layer] = state_hash

    def record_view(self, layer, view):
        self.view_reports[layer] = view

    def record_event(self, source, event_type, details=""):
        self.recent_events.append({"source": source, "type": event_type, "details": details, "ts": time.time()})

    def _check_heartbeat(self, layers):
        now = time.time()
        lost = [l for l in layers if self.layer_heartbeats.get(l) is None or (now - self.layer_heartbeats[l]) > self.HEARTBEAT_TIMEOUT]
        return len(lost) > 0, str(len(lost)) + " layer(s) missing heartbeat"

    def _check_decision(self):
        contradictions = 0
        for exp, obs in zip(self.expected_decisions, self.observed_decisions):
            if exp["cmd"] == obs["cmd"] and exp["expected"] != obs["actual"]:
                contradictions += 1
        return contradictions > 0, str(contradictions) + " decision contradiction(s)"

    def _check_integrity(self, expected_hashes):
        failures = 0
        for layer, expected in expected_hashes.items():
            actual = self.integrity_checks.get(layer)
            if actual is None or actual != expected:
                failures += 1
        return failures > 0, str(failures) + " integrity failure(s)"

    def _check_view(self, expected_views):
        mismatches = 0
        for layer, expected in expected_views.items():
            if self.view_reports.get(layer) != expected:
                mismatches += 1
        return mismatches > 0, str(mismatches) + " view mismatch(es)"

    def _check_pattern(self):
        now = time.time()
        recent = [e for e in self.recent_events if now - e["ts"] < self.PATTERN_WINDOW]
        return len(recent) >= self.PATTERN_MIN_EVENTS, str(len(recent)) + " events in window"

    def evaluate(self, layers, expected_hashes, expected_views):
        signals = {}
        signals["H_HeartbeatLoss"] = self._check_heartbeat(layers)
        signals["D_DecisionContradiction"] = self._check_decision()
        signals["I_IntegrityFailure"] = self._check_integrity(expected_hashes)
        signals["V_ViewMismatch"] = self._check_view(expected_views)
        signals["S_SustainedPattern"] = self._check_pattern()

        active = [n for n, (f, _) in signals.items() if f]
        self._append_log("EVALUATION", {"active": active, "count": len(active)})

        if len(active) >= self.TRIGGER_THRESHOLD:
            self._activate(active, signals)
            return True, active, signals
        return False, active, signals

    def _activate(self, active_signals, signals):
        self.activated = True
        alert = {
            "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "trigger_count": len(active_signals),
            "triggers": active_signals,
            "details": {n: signals[n][1] for n in active_signals},
            "action_required": "HUMAN_REVIEW",
            "status": "PENDING",
        }
        self.alert_queue.append(alert)
        self._append_log("ACTIVATION", alert)

    def _append_log(self, event_type, payload):
        prev = self.log[-1]["hash"] if self.log else "GENESIS"
        raw = str(prev) + "|" + event_type + "|" + str(payload) + "|" + str(time.time())
        h = hashlib.sha256(raw.encode()).hexdigest()[:16]
        self.log.append({"type": event_type, "payload": payload, "hash": h, "prev": prev, "ts": datetime.now().strftime("%H:%M:%S")})

    def verify_log_chain(self):
        prev = "GENESIS"
        for entry in self.log:
            if entry["prev"] != prev:
                return False
            prev = entry["hash"]
        return True

    def pending_alerts(self):
        return [a for a in self.alert_queue if a["status"] == "PENDING"]

    def approve(self, index, operator_id):
        if 0 <= index < len(self.alert_queue):
            self.alert_queue[index]["status"] = "APPROVED"
            self.alert_queue[index]["operator"] = operator_id
            self.alert_queue[index]["resolved_at"] = datetime.now().strftime("%H:%M:%S")
            self._append_log("APPROVED", {"operator": operator_id, "index": index})
            return True
        return False

    def reject(self, index, operator_id, reason=""):
        if 0 <= index < len(self.alert_queue):
            self.alert_queue[index]["status"] = "REJECTED"
            self.alert_queue[index]["operator"] = operator_id
            self.alert_queue[index]["reason"] = reason
            self.alert_queue[index]["resolved_at"] = datetime.now().strftime("%H:%M:%S")
            self._append_log("REJECTED", {"operator": operator_id, "index": index})
            return True
        return False

    def is_activated(self):
        return self.activated

    def summary(self):
        return {
            "activated": self.activated,
            "total_alerts": len(self.alert_queue),
            "pending": len(self.pending_alerts()),
            "log_entries": len(self.log),
            "log_integrity": self.verify_log_chain(),
        }


if __name__ == "__main__":
    s = ShadowSentinel()
    layers = ["SENTRY", "TWIN", "PATTERN", "IMMUNE", "COUNCIL"]
    print("Normal operation:")
    for l in layers:
        s.heartbeat(l)
        s.record_integrity(l, "hash_" + l)
        s.record_view(l, "state_A")
    fired, active, _ = s.evaluate(layers, {l: "hash_" + l for l in layers}, {l: "state_A" for l in layers})
    print("  Activated:", fired, "| Signals:", active)
