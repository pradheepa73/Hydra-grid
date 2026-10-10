"""HYDRA-GRID - Startup self-test.

Verifies all critical components load. Raises RuntimeError on failure (fail-closed).
"""
import sys


def _try_import(module_path, symbol=None):
    try:
        mod = __import__(module_path, fromlist=["*"])
        if symbol is not None:
            getattr(mod, symbol)
        return True, None
    except Exception as e:
        return False, module_path + ("." + symbol if symbol else "") + ": " + str(e)


def run_startup_self_test(verbose=False):
    checks = [
        ("src.core.constants", None),
        ("src.core.exceptions", None),
        ("src.layer1_sentry.sentry", "SentryLayer"),
        ("src.layer1_sentry.crypto", "CommandSigner"),
        ("src.layer1_sentry.rate_limit", "RateLimiter"),
        ("src.layer1_sentry.firmware", "FirmwareIntegrity"),
        ("src.layer1_sentry.merkle_log", "MerkleAuditLog"),
        ("src.layer1_sentry.self_monitor", "SelfIntegrityMonitor"),
        ("src.layer2_twin.grid_state", "GridState"),
        ("src.layer2_twin.digital_twin", "DigitalTwin"),
        ("src.layer3_pattern.physics_rules", "PhysicsRules"),
        ("src.layer3_pattern.markov_chain", "MarkovDetector"),
        ("src.layer4_immune.signature", "SignatureStore"),
        ("src.layer4_immune.learner", "ImmuneLearner"),
        ("src.layer5_council.pipeline", "HydraGrid"),
    ]
    failures = []
    for module, symbol in checks:
        ok, err = _try_import(module, symbol)
        if not ok:
            failures.append(err)
        if verbose:
            status = "OK" if ok else "FAIL"
            print("  [" + status + "] " + module + ("." + symbol if symbol else ""))
    if failures:
        msg = "HYDRA-GRID STARTUP SELF-TEST FAILED (fail-closed):\n" + "\n".join("  - " + f for f in failures)
        raise RuntimeError(msg)
    if verbose:
        print("  All " + str(len(checks)) + " components loaded successfully.")
    return True


if __name__ == "__main__":
    print("Running HYDRA-GRID startup self-test...")
    try:
        run_startup_self_test(verbose=True)
        print("Startup self-test PASSED.")
    except RuntimeError as e:
        print("Startup self-test FAILED:")
        print(e)
        sys.exit(1)
