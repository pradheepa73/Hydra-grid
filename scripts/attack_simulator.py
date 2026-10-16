"""HYDRA-GRID - Attack Simulator.

Launches scripted attacks against the HYDRA-GRID pipeline for demo purposes.
Each scenario mirrors a documented real-world incident.
"""
import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.layer5_council import HydraGrid


SCENARIOS = [
    ("SCADA_MASTER", "B1", "OPEN", "Legitimate operator"),
    ("IT_NET",       "B3", "OPEN", "IT network breach (Colonial 2021)"),
    ("SCADA_MASTER", "B1", "OPEN", "Redundant command (replay)"),
    ("SCADA_MASTER", "B2", "OPEN", "Cascade attack (Ukraine 2016)"),
    ("SCADA_MASTER", "B2", "OPEN", "Repeat attack - IMMUNE should block"),
]


def run():
    print("\n" + "=" * 64)
    print("  HYDRA-GRID - ATTACK SIMULATOR")
    print("=" * 64 + "\n")

    grid = HydraGrid(demo_mode=True)

    for source, breaker, action, label in SCENARIOS:
        print("--- " + label + " ---")
        result = grid.process(source, breaker, action)
        print("  Verdict: " + result["verdict"])
        print("  Layer:   " + result["layer"])
        print("  Reason:  " + result["reason"])
        time.sleep(0.3)
        print()

    print("=" * 64)
    print("  FINAL GRID STATE")
    print("  " + str(grid.snapshot()["grid"]))
    print("  IMMUNE: " + str(grid.snapshot()["immune_stats"]))
    print("=" * 64 + "\n")


if __name__ == "__main__":
    run()
