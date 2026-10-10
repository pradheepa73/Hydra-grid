"""HYDRA-GRID Layer 5 tests."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.layer5_council import HydraGrid


def test_pipeline_blocks_it_net():
    g = HydraGrid(demo_mode=True)
    r = g.process("IT_NET", "B3", "OPEN")
    assert r["verdict"] == "BLOCK"


def test_pipeline_allows_scada():
    g = HydraGrid(demo_mode=True)
    r = g.process("SCADA_MASTER", "B1", "OPEN")
    assert r["verdict"] == "ALLOW"


def test_pipeline_twin_blocks_cascade():
    g = HydraGrid(demo_mode=True)
    g.process("SCADA_MASTER", "B1", "OPEN")
    g.process("SCADA_MASTER", "B2", "OPEN")
    r = g.process("SCADA_MASTER", "B3", "OPEN")
    assert r["verdict"] == "BLOCK"
    assert r["layer"] == "TWIN"


def test_pipeline_immune_learns():
    g = HydraGrid(demo_mode=True)
    g.process("SCADA_MASTER", "B1", "OPEN")
    g.process("SCADA_MASTER", "B2", "OPEN")  # blocked by TWIN, feeds IMMUNE
    # Second attempt at B2 should be caught by IMMUNE now
    r = g.process("SCADA_MASTER", "B2", "OPEN")
    assert r["verdict"] == "BLOCK"


def test_pipeline_snapshot_structure():
    g = HydraGrid(demo_mode=True)
    g.process("SCADA_MASTER", "B1", "OPEN")
    snap = g.snapshot()
    assert "grid" in snap
    assert "events" in snap
    assert "immune_stats" in snap
