"""HYDRA-GRID Layer 1 - SENTRY orchestrator."""
import hmac
from datetime import datetime, time as dtime

from src.core.constants import ALLOWED_COMMAND_SOURCES, MAINTENANCE_WINDOW
from src.layer1_sentry.crypto import KeyStore, CommandSigner
from src.layer1_sentry.rate_limit import RateLimiter
from src.layer1_sentry.firmware import FirmwareIntegrity
from src.layer1_sentry.merkle_log import MerkleAuditLog
from src.layer1_sentry.self_monitor import SelfIntegrityMonitor


BANNED_CREDENTIALS = {
    ("admin", "admin"), ("admin", "password"), ("admin", "1234"),
    ("root", "root"), ("root", "toor"), ("user", "user"),
    ("guest", "guest"), ("admin", ""), ("root", ""),
}


class SentryLayer:
    def __init__(self, demo_mode=False):
        self.keystore = KeyStore()
        self.signer = CommandSigner(self.keystore)
        self.rate_limiter = RateLimiter()
        self.firmware = FirmwareIntegrity()
        self.log = MerkleAuditLog()
        self.self_monitor = SelfIntegrityMonitor()
        self.blocks = 0
        self.allows = 0

    def _reject(self, source, command, reason):
        self.blocks += 1
        self.log.append("REJECT", source, command, reason)
        print(f"[BLOCK] [SENTRY] {source} -> {command}")
        print(f"        -> {reason}")
        return False

    def _accept(self, source, command, reason):
        self.allows += 1
        self.log.append("ACCEPT", source, command, reason)
        print(f"[ALLOW] [SENTRY] {source} -> {command}  ({reason})")
        return True

    def process_command(self, source, command, nonce, signature,
                        username, password):
        ok, reason = self.self_monitor.check()
        if not ok:
            return self._reject(source, command, reason)

        u_lower = username.lower()
        p_lower = password.lower()
        for banned_u, banned_p in BANNED_CREDENTIALS:
            u_match = hmac.compare_digest(u_lower, banned_u)
            p_match = hmac.compare_digest(p_lower, banned_p)
            if u_match and p_match:
                return self._reject(source, command,
                    f"Default credential blocked: {username}/*")

        now = datetime.now().time()
        start = dtime(MAINTENANCE_WINDOW[0], 0)
        end = dtime(MAINTENANCE_WINDOW[1], 0)
        if not (start <= now <= end):
            return self._reject(source, command,
                f"Outside maintenance window ({now.strftime('%H:%M')})")

        ok, reason = self.rate_limiter.check(source)
        if not ok:
            return self._reject(source, command, reason)

        ok, reason = self.signer.verify(source, command, nonce, signature)
        if not ok:
            return self._reject(source, command, reason)

        return self._accept(source, command, reason)

    def verify_firmware(self, plc_id, content):
        ok, reason = self.firmware.verify(plc_id, content)
        self.log.append("FIRMWARE", plc_id, reason, "OK" if ok else "FAIL")
        print(f"[{'OK' if ok else 'FAIL'}] [SENTRY] {reason}")
        return ok

    def summary(self):
        print("\n" + "=" * 64)
        print("  SENTRY LAYER SUMMARY")
        print(f"  Allowed: {self.allows}   Blocked: {self.blocks}")
        print(f"  Log entries: {len(self.log.entries)}")
        print(f"  Merkle root: {self.log.merkle_root()}")
        print("=" * 64 + "\n")
