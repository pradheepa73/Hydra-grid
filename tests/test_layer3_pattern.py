"""HYDRA-GRID Layer 3 tests."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.layer2_twin import GridState
from src.layer3_pattern import PhysicsRules, MarkovDetector


def test_physics_blocks_it_net():
    ok, _ = PhysicsRules.check_source("IT_NET")
    assert ok is False


def test_physics_allows_scada():
    ok, _ = PhysicsRules.check_source("SCADA_MASTER")
    assert ok is True


def test_physics_voltage_floor():
    grid = GridState()
    grid.apply("B1", "OPEN")
    grid.apply("B2", "OPEN")
    ok, _ = PhysicsRules.check_voltage(grid)
    assert ok is False


def test_markov_normal_low_score():
    m = MarkovDetector(anomaly_threshold=2.0)
    m.train([
        {"breaker": "B1", "action": "OPEN"},
        {"breaker": "B1", "action": "CLOSE"},
    ])
    score, is_anom, _ = m.score([
        {"breaker": "B1", "action": "OPEN"},
        {"breaker": "B1", "action": "CLOSE"},
    ])
    assert is_anom is False


def test_markov_attack_high_score():
    m = MarkovDetector(anomaly_threshold=2.0)
    m.train([
        {"breaker": "B1", "action": "OPEN"},
        {"breaker": "B1", "action": "CLOSE"},
    ])
    score, is_anom, _ = m.score([
        {"breaker": "B1", "action": "OPEN"},
        {"breaker": "B2", "action": "OPEN"},
    ])
    assert is_anom is True
