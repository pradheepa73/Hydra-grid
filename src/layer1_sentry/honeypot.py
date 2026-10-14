"""HYDRA-GRID Layer 1 - Modbus TCP Honeypot."""
import hashlib
import socket
import threading
import time
from datetime import datetime


class ModbusHoneypot:
    def __init__(self, host="127.0.0.1", port=5020):
        self.host = host
        self.port = port
        self.running = False
        self.captured_commands = []
        self.sock = None
        self.thread = None

    def _handle_client(self, client_sock, address):
        try:
            client_sock.settimeout(5.0)
            while self.running:
                data = client_sock.recv(256)
                if not data:
                    break
                capture = {
                    "ts": datetime.now().strftime("%H:%M:%S"),
                    "source_ip": address[0],
                    "source_port": address[1],
                    "hex": data.hex(),
                    "length": len(data),
                    "sha256": hashlib.sha256(data).hexdigest()[:16],
                }
                self.captured_commands.append(capture)
                response = data[:2] + b"\x00\x00"
                client_sock.sendall(response)
        except socket.timeout:
            pass
        except Exception:
            pass
        finally:
            try:
                client_sock.close()
            except Exception:
                pass

    def _serve(self):
        while self.running:
            try:
                client_sock, address = self.sock.accept()
                t = threading.Thread(
                    target=self._handle_client,
                    args=(client_sock, address),
                    daemon=True,
                )
                t.start()
            except OSError:
                break

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(10)
        self.running = True
        self.thread = threading.Thread(target=self._serve, daemon=True)
        self.thread.start()
        return True

    def stop(self):
        self.running = False
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass

    def get_signature(self):
        if not self.captured_commands:
            return None
        return self.captured_commands[-1]["sha256"]

    def summary(self):
        return {
            "total_captured": len(self.captured_commands),
            "unique_sources": len(set(c["source_ip"] for c in self.captured_commands)),
        }


if __name__ == "__main__":
    print("Starting Modbus Honeypot on 127.0.0.1:5020 ...")
    honeypot = ModbusHoneypot()
    honeypot.start()
    print("Honeypot running. Press Ctrl+C to stop.\n")
    try:
        while True:
            time.sleep(3)
            print("[HONEYPOT] " + str(honeypot.summary()))
    except KeyboardInterrupt:
        honeypot.stop()
        print("Stopped.")
