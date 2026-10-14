"""HYDRA-GRID - Recovery tests."""
import sys
import os
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.layer4_immune.recovery import GoldenImageRecovery


def test_create_golden_image():
    r = GoldenImageRecovery(snapshot_dir=".hydra_test_snapshots")
    h = r.create_golden_image("TEST_NODE", {"voltage": 1.0})
    assert h is not None
    shutil.rmtree(".hydra_test_snapshots", ignore_errors=True)


def test_verify_integrity():
    r = GoldenImageRecovery(snapshot_dir=".hydra_test_snapshots")
    r.create_golden_image("TEST_NODE", {"voltage": 1.0})
    ok, _ = r.verify_golden_image("TEST_NODE")
    assert ok is True
    shutil.rmtree(".hydra_test_snapshots", ignore_errors=True)


def test_restore_returns_state():
    r = GoldenImageRecovery(snapshot_dir=".hydra_test_snapshots")
    state = {"breakers": {"B1": "CLOSED"}, "voltage": 1.0}
    r.create_golden_image("TEST_NODE", state)
    success, ms, restored = r.restore("TEST_NODE")
    assert success is True
    assert restored == state
    assert ms >= 0
    shutil.rmtree(".hydra_test_snapshots", ignore_errors=True)
