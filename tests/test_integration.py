"""HYDRA-GRID - Cross-layer integration tests.

Verifies all 5 layers work together as a system.
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.layer5_council import HydraGrid


def test_all_layers_present():
    g = HydraGrid(demo_mode=True)
    assert hasattr(g, "sentry")     # Layer 1
    assert hasattr(g, "twin")       # Layer 2
    assert hasattr(g, "markov")     # Layer 3
    assert hasattr(g, "immune")     # Layer 4


def test_end_to_end_legitimate():
    g = HydraGrid(demo_mode=True)
    result = g.process("SCADA_MASTER", "B1", "OPEN")
    assert result["verdict"] == "ALLOW"


def test_end_to_end_it_breach_blocked():
    g = HydraGrid(demo_mode=True)
    result = g.process("IT_NET", "B3", "OPEN")
    assert result["verdict"] == "BLOCK"


def test_end_to_end_cascade_blocked():
    g = HydraGrid(demo_mode=True)
    g.process("SCADA_MASTER", "B1", "OPEN")
    g.process("SCADA_MASTER", "B2", "OPEN")
    result = g.process("SCADA_MASTER", "B3", "OPEN")
    assert result["verdict"] == "BLOCK"


def test_snapshot_contains_all_keys():
    g = HydraGrid(demo_mode=True)
    g.process("SCADA_MASTER", "B1", "OPEN")
    snap = g.snapshot()
    assert "grid" in snap
    assert "events" in snap
    assert "immune_stats" in snap
