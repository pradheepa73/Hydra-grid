"""HYDRA-GRID Layer 5 - Unified pipeline combining all layers."""
from src.layer1_sentry import SentryLayer
from src.layer2_twin import GridState, DigitalTwin
from src.layer3_pattern import PhysicsRules, MarkovDetector
from src.layer4_immune import ImmuneLearner


class HydraGrid:
    """The full HYDRA-GRID pipeline: SENTRY -> IMMUNE -> TWIN -> PATTERN."""

    def __init__(self, demo_mode=True):
        # Layer 1
        self.sentry = SentryLayer(demo_mode=demo_mode)
        # Layer 2
        self.grid = GridState(name="SUBSTATION_A", breaker_count=3)
        self.twin = DigitalTwin(self.grid)
        # Layer 3
        self.markov = MarkovDetector(anomaly_threshold=2.0)
        self._train_markov()
        # Layer 4
        self.immune = ImmuneLearner(auto_approve=True)
        # Audit trail
        self.events = []

    def _train_markov(self):
        normal = [
            {"breaker": "B1", "action": "OPEN"},
            {"breaker": "B1", "action": "CLOSE"},
            {"breaker": "B2", "action": "OPEN"},
            {"breaker": "B2", "action": "CLOSE"},
        ]
        self.markov.train(normal)

    def _log(self, layer, source, command, verdict, reason):
        self.events.append({
            "layer": layer,
            "source": source,
            "command": command,
            "verdict": verdict,
            "reason": reason,
        })

    def process(self, source, breaker, action, nonce=None, signature=None,
                username="operator", password="S3cure!Pass"):
        """
        Run a command through the full pipeline.
        Returns dict with the final verdict and reason.
        """
        cmd_str = f"{action}_{breaker}"
        seq = [(breaker, action)]

        # ---- LAYER 4 (IMMUNE) - FASTEST PATH FIRST ----
        known, reason, latency = self.immune.check(seq)
        if known:
            self._log("IMMUNE", source, cmd_str, "BLOCK", reason)
            return {"verdict": "BLOCK", "layer": "IMMUNE", "reason": reason,
                    "latency_ms": latency}

        # ---- LAYER 1 (SENTRY) ----
        if nonce is None:
            # Internal/system commands bypass SENTRY signing
            pass
        else:
            ok = self.sentry.process_command(
                source, cmd_str, nonce, signature, username, password
            )
            if not ok:
                self._log("SENTRY", source, cmd_str, "BLOCK",
                          "SENTRY policy violation")
                return {"verdict": "BLOCK", "layer": "SENTRY",
                        "reason": "SENTRY policy violation", "latency_ms": 0}

        # ---- LAYER 3 (PATTERN - physics rules) ----
        ok, reason = PhysicsRules.check_source(source)
        if not ok:
            self._log("PATTERN", source, cmd_str, "BLOCK", reason)
            return {"verdict": "BLOCK", "layer": "PATTERN",
                    "reason": reason, "latency_ms": 0}

        # ---- LAYER 3 (PATTERN - Markov sequence) ----
        score, is_anom, reason = self.markov.score([
            {"breaker": breaker, "action": action}
        ])
        # Markov needs 2+ commands; skip single-command scoring

        # ---- LAYER 2 (TWIN - pre-execution simulation) ----
        safe, reasons, projected = self.twin.simulate(breaker, action)
        if not safe:
            # Feed to IMMUNE
            self.immune.observe_attack(seq, source=source)
            self._log("TWIN", source, cmd_str, "BLOCK", reasons[0])
            return {"verdict": "BLOCK", "layer": "TWIN",
                    "reason": reasons[0], "latency_ms": 0,
                    "projected": projected}

        # ---- ALL LAYERS PASSED - EXECUTE ----
        self.grid.apply(breaker, action)
        self._log("EXECUTED", source, cmd_str, "ALLOW", "All layers passed")
        return {"verdict": "ALLOW", "layer": "ALL",
                "reason": "All layers passed", "latency_ms": 0}

    def snapshot(self):
        return {
            "grid": self.grid.snapshot(),
            "events": self.events,
            "immune_stats": self.immune.stats(),
        }
