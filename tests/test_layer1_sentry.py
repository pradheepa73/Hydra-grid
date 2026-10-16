"""HYDRA-GRID Layer 1 tests."""
import secrets, sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.layer1_sentry import SentryLayer


def _sign(s, source, command):
    nonce = secrets.token_hex(8)
    sig = s.signer.sign(source, command, nonce)
    return nonce, sig


def test_legit_allowed():
    s = SentryLayer()
    n, sig = _sign(s, "OPERATOR_ALICE", "OPEN_B1")
    assert s.process_command("OPERATOR_ALICE", "OPEN_B1", n, sig, "alice", "S3cure!Pass") is True


def test_unknown_blocked():
    s = SentryLayer()
    assert s.process_command("ATTACKER", "OPEN_B1", "x", "x", "a", "b") is False


def test_replay_blocked():
    s = SentryLayer()
    n, sig = _sign(s, "OPERATOR_ALICE", "OPEN_B1")
    s.process_command("OPERATOR_ALICE", "OPEN_B1", n, sig, "alice", "S3cure!Pass")
    assert s.process_command("OPERATOR_ALICE", "OPEN_B1", n, sig, "alice", "S3cure!Pass") is False


def test_default_cred_blocked():
    s = SentryLayer()
    n, sig = _sign(s, "OPERATOR_BOB", "OPEN_B3")
    assert s.process_command("OPERATOR_BOB", "OPEN_B3", n, sig, "admin", "admin") is False


def test_firmware_ok():
    s = SentryLayer()
    assert s.verify_firmware("PLC_001", "firmware-plc001-v2.4.1") is True


def test_firmware_tampered():
    s = SentryLayer()
    assert s.verify_firmware("PLC_002", "evil") is False
