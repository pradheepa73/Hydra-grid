"""HYDRA-GRID Layer 3 - Markov chain sequence anomaly detector."""
import math
from collections import defaultdict


class MarkovDetector:
    """
    Learns normal transitions (B1_OPEN -> B1_CLOSE) from training logs.
    Flags low-probability sequences as anomalies.
    """

    def __init__(self, anomaly_threshold=3.0):
        self.transitions = defaultdict(lambda: defaultdict(int))
        self.state_counts = defaultdict(int)
        self.anomaly_threshold = anomaly_threshold

    def train(self, commands):
        """commands: list of dicts like {"breaker": "B1", "action": "OPEN"}"""
        for i in range(len(commands) - 1):
            cur = (commands[i]["breaker"], commands[i]["action"])
            nxt = (commands[i + 1]["breaker"], commands[i + 1]["action"])
            self.transitions[cur][nxt] += 1
            self.state_counts[cur] += 1

    def score(self, commands):
        """
        Returns (anomaly_score, is_anomaly, reason).
        Higher score = more anomalous.
        """
        if len(commands) < 2:
            return 0.0, False, "Not enough commands to score."

        log_prob = 0.0
        for i in range(len(commands) - 1):
            cur = (commands[i]["breaker"], commands[i]["action"])
            nxt = (commands[i + 1]["breaker"], commands[i + 1]["action"])

            if self.state_counts[cur] == 0:
                return 100.0, True, f"Unseen transition from {cur}."
            prob = self.transitions[cur][nxt] / self.state_counts[cur]
            if prob == 0:
                return 100.0, True, f"Unseen transition {cur} -> {nxt}."
            log_prob += math.log(prob)

        score = -log_prob / max(len(commands) - 1, 1)
        is_anom = score > self.anomaly_threshold
        reason = f"Sequence score {score:.2f} (threshold {self.anomaly_threshold})."
        return score, is_anom, reason
