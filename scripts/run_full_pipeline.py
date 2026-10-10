"""HYDRA-GRID Layer 5 - Unified pipeline demo."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.layer5_council import HydraGrid


def run():
    print("\n" + "=" * 64)
    print("  HYDRA-GRID 2026 - FULL PIPELINE DEMO")
    print("=" * 64 + "\n")

    grid = HydraGrid(demo_mode=True)

    scenarios = [
        ("SCADA_MASTER", "B1", "OPEN", "Legitimate operator"),
        ("IT_NET",       "B3", "OPEN", "IT network breach (Colonial 2021)"),
        ("SCADA_MASTER", "B1", "OPEN", "Compromised operator - first step"),
        ("SCADA_MASTER", "B2", "OPEN", "Cascade blocked by TWIN"),
        ("SCADA_MASTER", "B2", "OPEN", "Repeat attack - IMMUNE blocks instantly"),
    ]

    for source, breaker, action, label in scenarios:
        print(f"--- {label} ---")
        result = grid.process(source, breaker, action)
        print(f"[{result['verdict']}] Layer: {result['layer']}")
        print(f"  Reason: {result['reason']}")
        if result.get("projected"):
            print(f"  Projected V: {result['projected']['voltage']} pu")
        print()

    print("=" * 64)
    print(f"  FINAL GRID: {grid.snapshot()['grid']}")
    print(f"  IMMUNE STATS: {grid.snapshot()['immune_stats']}")
    print("=" * 64 + "\n")


if __name__ == "__main__":
    run()
