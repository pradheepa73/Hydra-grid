"""HYDRA-GRID Layer 1 - Firmware integrity."""
import hashlib


class FirmwareIntegrity:
    def __init__(self):
        self.trusted = {
            "PLC_001": self._hash("firmware-plc001-v2.4.1"),
            "PLC_002": self._hash("firmware-plc002-v2.4.1"),
            "PLC_003": self._hash("firmware-plc003-v2.4.1"),
        }

    @staticmethod
    def _hash(content):
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def verify(self, plc_id, content):
        if plc_id not in self.trusted:
            return False, f"Unknown PLC: {plc_id}"
        if self._hash(content) != self.trusted[plc_id]:
            return False, f"Firmware mismatch on {plc_id} - possible tampering."
        return True, f"Firmware verified: {plc_id}"
