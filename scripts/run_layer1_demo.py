"""HYDRA-GRID Layer 1 demo."""
import sys, os, secrets
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.layer1_sentry import SentryLayer


def legit(sentry, source, command):
    nonce = secrets.token_hex(8)
    sig = sentry.signer.sign(source, command, nonce)
    return nonce, sig


def run():
    print("\n" + "=" * 64)
    print("  HYDRA-GRID 2026 - LAYER 1: SENTRY DEMO")
    print("=" * 64 + "\n")

    sentry = SentryLayer()

    print("--- Scenario 1: Legitimate Operator ---")
    n, s = legit(sentry, "OPERATOR_ALICE", "OPEN_B1")
    sentry.process_command("OPERATOR_ALICE", "OPEN_B1", n, s, "alice", "S3cure!Pass")

    print("\n--- Scenario 2: Stolen Creds, No Signature ---")
    sentry.process_command("ATTACKER", "OPEN_B2", "fake", "fake", "alice", "S3cure!Pass")

    print("\n--- Scenario 3: Replay Attack ---")
    n, s = legit(sentry, "OPERATOR_ALICE", "OPEN_B1")
    sentry.process_command("OPERATOR_ALICE", "OPEN_B1", n, s, "alice", "S3cure!Pass")
    sentry.process_command("OPERATOR_ALICE", "OPEN_B1", n, s, "alice", "S3cure!Pass")

    print("\n--- Scenario 4: Default Credential ---")
    n, s = legit(sentry, "OPERATOR_BOB", "OPEN_B3")
    sentry.process_command("OPERATOR_BOB", "OPEN_B3", n, s, "admin", "admin")

    print("\n--- Scenario 5: Burst Attack ---")
    for i in range(7):
        n, s = legit(sentry, "OPERATOR_BOB", f"CMD_{i}")
        sentry.process_command("OPERATOR_BOB", f"CMD_{i}", n, s, "bob", "BobPass!")

    print("\n--- Scenario 6: Firmware Integrity ---")
    sentry.verify_firmware("PLC_001", "firmware-plc001-v2.4.1")
    sentry.verify_firmware("PLC_002", "firmware-plc002-v9.9.9")

    sentry.summary()


if __name__ == "__main__":
    run()
