"""Shadow Sentinel tests."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from shadow_sentinel import ShadowSentinel

LAYERS = ["SENTRY", "TWIN", "PATTERN", "IMMUNE", "COUNCIL"]

def test_normal_no_trigger():
    s = ShadowSentinel()
    for l in LAYERS:
        s.heartbeat(l); s.record_integrity(l, "hash_" + l); s.record_view(l, "state_A")
    fired, _, _ = s.evaluate(LAYERS, {l: "hash_" + l for l in LAYERS}, {l: "state_A" for l in LAYERS})
    assert fired is False

def test_two_signals_trigger():
    s = ShadowSentinel()
    s.record_integrity("SENTRY", "wrong_hash")
    fired, active, _ = s.evaluate(LAYERS, {l: "hash_" + l for l in LAYERS}, {l: "state_A" for l in LAYERS})
    assert fired is True
    assert len(active) >= 2

def test_human_approval_gate():
    s = ShadowSentinel()
    s.record_integrity("SENTRY", "wrong_hash")
    s.evaluate(LAYERS, {l: "hash_" + l for l in LAYERS}, {l: "state_A" for l in LAYERS})
    assert len(s.pending_alerts()) == 1
    assert s.approve(0, "operator_1") is True

def test_log_chain_integrity():
    s = ShadowSentinel()
    s._append_log("TEST", {"x": 1})
    s._append_log("TEST", {"x": 2})
    assert s.verify_log_chain() is True

def test_decision_contradiction():
    s = ShadowSentinel()
    s.record_expected("OPEN_B1", "BLOCK")
    s.record_observed("OPEN_B1", "ALLOW")
    fired, active, _ = s.evaluate(LAYERS, {l: "hash_" + l for l in LAYERS}, {l: "state_A" for l in LAYERS})
    assert "D_DecisionContradiction" in active
