"""HYDRA-GRID - Honeypot tests."""
import socket
import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.layer1_sentry.honeypot import ModbusHoneypot


def test_honeypot_starts_and_captures():
    h = ModbusHoneypot(port=15020)
    assert h.start() is True
    time.sleep(0.5)
    try:
        s = socket.socket()
        s.connect(("127.0.0.1", 15020))
        s.send(b"\x01\x05\x00\x01\xff\x00")
        time.sleep(0.3)
        s.close()
    except Exception:
        pass
    time.sleep(0.3)
    h.stop()
    assert h.summary()["total_captured"] >= 1


def test_honeypot_signature_returned():
    h = ModbusHoneypot(port=15021)
    h.start()
    time.sleep(0.3)
    try:
        s = socket.socket()
        s.connect(("127.0.0.1", 15021))
        s.send(b"\x01\x06\x00\x02\x00\x10")
        time.sleep(0.3)
        s.close()
    except Exception:
        pass
    time.sleep(0.3)
    h.stop()
    assert h.get_signature() is not None
