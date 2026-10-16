"""HYDRA-GRID Layer 3 - Physics rules detector."""
from src.layer2_twin.grid_state import GridState


class PhysicsRules:
    """Fast path - hard rules applied before the twin."""

    BANNED_SOURCES = {"IT_NET", "UNKNOWN", "ATTACKER"}
    MAX_OPEN_IN_WINDOW = 3
    WINDOW_SECONDS = 2.0

    @classmethod
    def check_source(cls, source):
        if source in cls.BANNED_SOURCES:
            return False, f"Zero Trust: source '{source}' is not authorized."
        return True, "Source allowed."

    @classmethod
    def check_voltage(cls, grid):
        if grid.voltage < GridState.MIN_SAFE_VOLTAGE:
            return False, f"Current voltage {grid.voltage:.2f} pu below safe floor."
        return True, "Voltage OK."

    @classmethod
    def check_cascade(cls, grid):
        if grid.open_count() >= cls.MAX_OPEN_IN_WINDOW:
            return False, f"Cascade: {grid.open_count()} breakers already open."
        return True, "No cascade."
