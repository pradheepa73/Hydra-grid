"""HYDRA-GRID Layer 3 - PATTERN demo."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.layer2_twin import GridState
from src.layer3_pattern import PhysicsRules, MarkovDetector


def run():
    print("\n" + "=" * 64)
    print("  HYDRA-GRID 2026 - LAYER 3: PATTERN DEMO")
    print("=" * 64 + "\n")

    # ---- Train Markov on normal sequences ----
    normal_training = [
        {"breaker": "B1", "action": "OPEN"},
        {"breaker": "B1", "action": "CLOSE"},
        {"breaker": "B2", "action": "OPEN"},
        {"breaker": "B2", "action": "CLOSE"},
        {"breaker": "B3", "action": "OPEN"},
        {"breaker": "B3", "action": "CLOSE"},
    ]
    markov = MarkovDetector(anomaly_threshold=2.0)
    markov.train(normal_training)
    print("Markov detector trained on normal sequences.\n")

    # ---- Scenario 1: Physics rules ----
    print("=== Scenario 1: Physics Rules ===")
    grid = GridState()
    print(f"Source ATTACKER: {PhysicsRules.check_source('ATTACKER')}")
    print(f"Source SCADA_MASTER: {PhysicsRules.check_source('SCADA_MASTER')}")
    print(f"Voltage OK: {PhysicsRules.check_voltage(grid)}")
    print(f"Cascade OK: {PhysicsRules.check_cascade(grid)}\n")

    # ---- Scenario 2: Markov scores normal vs attack ----
    print("=== Scenario 2: Markov Sequence Scoring ===")

    normal_seq = [
        {"breaker": "B1", "action": "OPEN"},
        {"breaker": "B1", "action": "CLOSE"},
    ]
    score, is_anom, reason = markov.score(normal_seq)
    print(f"Normal sequence: score={score:.2f}, anomaly={is_anom}")
    print(f"  -> {reason}")

    attack_seq = [
        {"breaker": "B1", "action": "OPEN"},
        {"breaker": "B2", "action": "OPEN"},
        {"breaker": "B3", "action": "OPEN"},
    ]
    score, is_anom, reason = markov.score(attack_seq)
    print(f"Attack sequence: score={score:.2f}, anomaly={is_anom}")
    print(f"  -> {reason}\n")

    print("=" * 64)
    print("  LAYER 3 WORKING")
    print("=" * 64 + "\n")


if __name__ == "__main__":
    run()
