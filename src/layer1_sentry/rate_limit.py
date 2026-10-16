"""HYDRA-GRID Layer 1 - Per-source rate limiter."""
import time
from collections import defaultdict

from src.core.constants import RATE_LIMIT_MAX, RATE_LIMIT_WINDOW_SECONDS


class RateLimiter:
    def __init__(self):
        self.history = defaultdict(list)

    def check(self, source):
        now = time.time()
        self.history[source] = [
            t for t in self.history[source]
            if now - t < RATE_LIMIT_WINDOW_SECONDS
        ]
        if len(self.history[source]) >= RATE_LIMIT_MAX:
            return False, f"Rate limit exceeded: {RATE_LIMIT_MAX}/{RATE_LIMIT_WINDOW_SECONDS}s"
        self.history[source].append(now)
        return True, f"Rate OK ({len(self.history[source])}/{RATE_LIMIT_MAX})."
