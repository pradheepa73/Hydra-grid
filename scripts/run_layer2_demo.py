"""HYDRA-GRID Layer 2 - TWIN demo."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.layer2_twin import GridState, DigitalTwin


def run():
    print("\n" + "=" * 64)
    print("  HYDRA-GRID 2026 - LAYER 2: TWIN DEMO")
    print("=" * 64 + "\n")

    grid = GridState(name="SUBSTATION_A", breaker_count=3)
    twin = DigitalTwin(grid)

    def attempt(source, breaker, action):
        print(f"--- {source}: {action} {breaker} ---")
        safe, reasons, projected = twin.simulate(breaker, action)
        if safe:
            grid.apply(breaker, action)
            print(f"[ALLOW] [TWIN] Real grid updated. V={grid.voltage:.2f} pu")
        else:
            print(f"[BLOCK] [TWIN] Command blocked before execution.")
            for r in reasons:
                print(f"        -> {r}")
            print(f"        -> Projected V={projected['voltage']} pu")
        print()

    print("=== Scenario 1: Normal Operation ===")
    attempt("OPERATOR", "B1", "OPEN")
    attempt("OPERATOR", "B1", "CLOSE")

    print("=== Scenario 2: Redundant Commands ===")
    attempt("OPERATOR", "B2", "OPEN")
    attempt("OPERATOR", "B2", "OPEN")
    attempt("OPERATOR", "B2", "CLOSE")
    attempt("OPERATOR", "B2", "CLOSE")

    print("=== Scenario 3: Cascade Blocked (Money Shot) ===")
    attempt("ATTACKER", "B1", "OPEN")   # safe, V=0.70
    attempt("ATTACKER", "B2", "OPEN")   # blocked, would be V=0.40

    print("=" * 64)
    print(f"  FINAL GRID STATE")
    print(f"  {grid.snapshot()}")
    print("=" * 64 + "\n")


if __name__ == "__main__":
    run()
