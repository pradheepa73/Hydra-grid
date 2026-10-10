"""HYDRA-GRID Layer 2 tests."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.layer2_twin import GridState, DigitalTwin


def test_normal_open_safe():
    grid = GridState()
    twin = DigitalTwin(grid)
    safe, reasons, _ = twin.simulate("B1", "OPEN")
    assert safe is True
    assert reasons == []


def test_cascade_blocked():
    grid = GridState()
    twin = DigitalTwin(grid)
    grid.apply("B1", "OPEN")
    grid.apply("B2", "OPEN")
    safe, reasons, projected = twin.simulate("B3", "OPEN")
    assert safe is False
    assert any("Cascade" in r or "voltage" in r.lower() for r in reasons)


def test_voltage_floor_blocks():
    grid = GridState()
    twin = DigitalTwin(grid)
    grid.apply("B1", "OPEN")
    grid.apply("B2", "OPEN")
    safe, reasons, _ = twin.simulate("B3", "OPEN")
    assert safe is False


def test_redundant_open_blocked():
    grid = GridState()
    twin = DigitalTwin(grid)
    grid.apply("B1", "OPEN")
    safe, reasons, _ = twin.simulate("B1", "OPEN")
    assert safe is False
    assert any("redundant" in r.lower() for r in reasons)


def test_redundant_close_blocked():
    grid = GridState()
    twin = DigitalTwin(grid)
    safe, reasons, _ = twin.simulate("B1", "CLOSE")
    assert safe is False
    assert any("redundant" in r.lower() for r in reasons)
