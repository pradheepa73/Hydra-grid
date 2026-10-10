"""HYDRA-GRID Layer 2 - Digital Twin pre-execution simulator."""
import copy

from src.layer2_twin.grid_state import GridState


class DigitalTwin:
    def __init__(self, real_grid):
        self.real_grid = real_grid

    def simulate(self, breaker_id, action):
        reasons = []

        try:
            twin = copy.deepcopy(self.real_grid)
        except Exception as e:
            return False, [f"Twin copy failed: {e}"], None

        try:
            twin.apply(breaker_id, action)
        except Exception as e:
            return False, [f"Twin apply failed: {e}"], None

        if twin.voltage < GridState.MIN_SAFE_VOLTAGE:
            reasons.append(
                f"Projected voltage {twin.voltage:.2f} pu "
                f"(safe floor: {GridState.MIN_SAFE_VOLTAGE})"
            )

        if twin.open_count() >= 3:
            reasons.append(f"Cascade risk: {twin.open_count()} breakers open")

        if action == "OPEN" and self.real_grid.breakers[breaker_id].state == "OPEN":
            reasons.append(f"Breaker {breaker_id} already OPEN (redundant command)")

        if action == "CLOSE" and self.real_grid.breakers[breaker_id].state == "CLOSED":
            reasons.append(f"Breaker {breaker_id} already CLOSED (redundant command)")

        safe = len(reasons) == 0
        return safe, reasons, twin.snapshot()
