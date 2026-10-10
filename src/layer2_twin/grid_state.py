"""HYDRA-GRID Layer 2 - Grid state model."""
import hashlib
import time
from datetime import datetime


class Breaker:
    def __init__(self, bid):
        self.id = bid
        self.state = "CLOSED"

    def __repr__(self):
        return f"{self.id}:{self.state}"


class GridState:
    VOLTAGE_DROP_PER_OPEN = 0.30
    MIN_SAFE_VOLTAGE = 0.70

    def __init__(self, name="SUBSTATION_A", breaker_count=3):
        self.name = name
        self.breakers = {f"B{i}": Breaker(f"B{i}") for i in range(1, breaker_count + 1)}
        self.voltage = 1.0

    def open_count(self):
        return sum(1 for b in self.breakers.values() if b.state == "OPEN")

    def recompute_voltage(self):
        self.voltage = max(0.0, 1.0 - self.VOLTAGE_DROP_PER_OPEN * self.open_count())

    def apply(self, breaker_id, action):
        if breaker_id not in self.breakers:
            raise ValueError(f"Unknown breaker: {breaker_id}")
        b = self.breakers[breaker_id]
        if action == "OPEN":
            b.state = "OPEN"
        elif action == "CLOSE":
            b.state = "CLOSED"
        else:
            raise ValueError(f"Unknown action: {action}")
        self.recompute_voltage()

    def snapshot(self):
        return {
            "name": self.name,
            "voltage": round(self.voltage, 3),
            "breakers": {b.id: b.state for b in self.breakers.values()},
        }
