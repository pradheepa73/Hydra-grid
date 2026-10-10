"""HYDRA-GRID Layer 4 - IMMUNE demo."""
import sys, os, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.layer4_immune import ImmuneLearner


def run():
    print("\n" + "=" * 64)
    print("  HYDRA-GRID 2026 - LAYER 4: IMMUNE DEMO")
    print("=" * 64 + "\n")

    learner = ImmuneLearner(auto_approve=True)

    attack_sequence = [("B1", "OPEN"), ("B2", "OPEN"), ("B3", "OPEN")]

    # ---- Attempt 1: Unknown attack ----
    print("=== ATTEMPT 1: Unknown Attack ===")
    known, reason, latency = learner.check(attack_sequence)
    print(f"[IMMUNE] Known? {known}  Latency: {latency:.4f} ms")
    print(f"         {reason}\n")

    # ---- Attack captured by honeypot ----
    print("=== Honeypot captures attack, feeds IMMUNE ===")
    sig, status = learner.observe_attack(attack_sequence, source="MIRAGE_GRID")
    print(f"[IMMUNE] Signature learned: {sig.hash}")
    print(f"         Status: {status}\n")

    # ---- Attempt 2: Same attack, now known ----
    print("=== ATTEMPT 2: Same Attack Repeated ===")
    known, reason, latency = learner.check(attack_sequence)
    print(f"[IMMUNE] Known? {known}  Latency: {latency:.4f} ms")
    print(f"         {reason}\n")

    # ---- Attempt 3: Slightly different attack ----
    print("=== ATTEMPT 3: Novel Attack (Unknown) ===")
    novel = [("B1", "CLOSE"), ("B2", "OPEN")]
    known, reason, latency = learner.check(novel)
    print(f"[IMMUNE] Known? {known}  Latency: {latency:.4f} ms")
    print(f"         {reason}\n")

    print("=" * 64)
    print(f"  LEARNER STATS: {learner.stats()}")
    print("=" * 64 + "\n")


if __name__ == "__main__":
    run()
