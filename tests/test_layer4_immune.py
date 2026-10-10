"""HYDRA-GRID Layer 4 tests."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.layer4_immune import ImmuneLearner, Signature, SignatureStore


def test_signature_hash_stable():
    s1 = Signature([("B1", "OPEN"), ("B2", "OPEN")])
    s2 = Signature([("B1", "OPEN"), ("B2", "OPEN")])
    assert s1.hash == s2.hash


def test_signature_different_sequences_differ():
    s1 = Signature([("B1", "OPEN")])
    s2 = Signature([("B2", "OPEN")])
    assert s1.hash != s2.hash


def test_unknown_signature_not_known():
    learner = ImmuneLearner(auto_approve=True)
    known, _, _ = learner.check([("B1", "OPEN")])
    assert known is False


def test_learned_signature_known():
    learner = ImmuneLearner(auto_approve=True)
    learner.observe_attack([("B1", "OPEN"), ("B2", "OPEN")])
    known, _, _ = learner.check([("B1", "OPEN"), ("B2", "OPEN")])
    assert known is True


def test_human_approval_gate():
    learner = ImmuneLearner(auto_approve=False)
    sig, status = learner.observe_attack([("B1", "OPEN")])
    assert status == "proposed"
    known, _, _ = learner.check([("B1", "OPEN")])
    assert known is False  # not approved yet
    learner.approve(sig.hash)
    known, _, _ = learner.check([("B1", "OPEN")])
    assert known is True
