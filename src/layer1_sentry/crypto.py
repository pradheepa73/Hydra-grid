"""HYDRA-GRID Layer 1 - Signing + Nonce."""
import hashlib
import hmac


class KeyStore:
    def __init__(self):
        self.keys = {
            "SCADA_MASTER":   b"hydra-scada-master-secret-key-32b",
            "OPERATOR_ALICE": b"hydra-operator-alice-secret-key-32",
            "OPERATOR_BOB":   b"hydra-operator-bob-secret-key-3232",
        }

    def get(self, source):
        return self.keys.get(source)


class CommandSigner:
    def __init__(self, keystore):
        self.keystore = keystore
        self.seen_nonces = set()

    def sign(self, source, command, nonce):
        key = self.keystore.get(source)
        if key is None:
            return None
        msg = f"{source}|{command}|{nonce}".encode()
        return hmac.new(key, msg, hashlib.sha256).hexdigest()

    def verify(self, source, command, nonce, signature):
        if nonce in self.seen_nonces:
            return False, "Nonce already used - replay attack detected."
        key = self.keystore.get(source)
        if key is None:
            return False, f"Unknown source: {source}"
        expected = self.sign(source, command, nonce)
        if not hmac.compare_digest(expected, signature):
            return False, "Signature mismatch - command not authentic."
        self.seen_nonces.add(nonce)
        return True, "Signature verified."
