"""HYDRA-GRID Layer 1 - Encrypted Merkle audit log.

Two independent security guarantees:
  - Confidentiality: AES-256-GCM encrypts every entry. Attacker reading
    the log sees ciphertext, not commands.
  - Integrity: SHA-256 over ciphertext + Merkle root. Tampering breaks
    both the GCM auth tag and the Merkle root.
"""
import hashlib
import hmac
import json
import os
import time
from datetime import datetime

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class MerkleAuditLog:
    _HMAC_KEY = os.urandom(32)
    _KEY = os.urandom(32)
    _NONCE_LEN = 12

    def __init__(self):
        self.entries = []
        self._aes = AESGCM(self._KEY)

    def _encrypt(self, plaintext):
        nonce = os.urandom(self._NONCE_LEN)
        ciphertext = self._aes.encrypt(nonce, plaintext, associated_data=None)
        return ciphertext, nonce

    def _decrypt(self, ciphertext, nonce):
        return self._aes.decrypt(nonce, ciphertext, associated_data=None)

    def append(self, event_type, source, details, verdict):
        record = {
            "ts": datetime.now().strftime("%H:%M:%S"),
            "type": event_type,
            "source": source,
            "details": details,
            "verdict": verdict,
            "unix": time.time(),
        }
        plaintext = json.dumps(record, separators=(",", ":")).encode()
        ciphertext, nonce = self._encrypt(plaintext)
        entry_hash = hashlib.sha256(ciphertext).hexdigest()
        entry_mac = hmac.new(
            self._HMAC_KEY, ciphertext, hashlib.sha256
        ).hexdigest()
        self.entries.append({
            "nonce": nonce.hex(),
            "ciphertext": ciphertext.hex(),
            "hash": entry_hash,
            "mac": entry_mac,
            "ts": record["ts"],
        })

    def decrypt_entry(self, entry):
        try:
            ciphertext = bytes.fromhex(entry["ciphertext"])
            nonce = bytes.fromhex(entry["nonce"])
            return json.loads(self._decrypt(ciphertext, nonce))
        except Exception as e:
            return {"error": "decryption failed: " + str(e)}

    def merkle_root(self):
        if not self.entries:
            return "EMPTY"
        level = [e["hash"] for e in self.entries]
        while len(level) > 1:
            if len(level) % 2 == 1:
                level.append(level[-1])
            level = [
                hashlib.sha256((level[i] + level[i + 1]).encode()).hexdigest()
                for i in range(0, len(level), 2)
            ]
        return level[0][:16]

    def verify_integrity(self):
        for e in self.entries:
            ciphertext = bytes.fromhex(e["ciphertext"])
            expected_hash = hashlib.sha256(ciphertext).hexdigest()
            if expected_hash != e["hash"]:
                return False
            if "mac" in e:
                expected_mac = hmac.new(
                    self._HMAC_KEY, ciphertext, hashlib.sha256
                ).hexdigest()
                if not hmac.compare_digest(expected_mac, e["mac"]):
                    return False
        return True
