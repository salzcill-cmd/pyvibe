"""
Development Server — simple HTTP server untuk development.

Features:
- Auto-serves HTML files
- WebSocket hot reload (auto-refresh browser on file change)
- Live preview
- Syntax highlighting in terminal logs
"""

import http.server
import socketserver
import os
import threading
import time
import json
import hashlib
from pathlib import Path
from typing import Optional, Set


# ==================== WebSocket Hot Reload ====================

# Minimal WebSocket server (RFC 6455) — zero dependencies
WS_MAGIC = "258EAFA5-E914-47DA-95CA-5AB9D19027C8"

import struct
import socket as _socket


class WebSocketServer:
    """Minimal WebSocket server untuk hot reload."""

    def __init__(self, host: str = "localhost", port: int = 8080):
        self.host = host
        self.port = port
        self.clients: Set = set()
        self._running = False
        self._server_socket: Optional[_socket.socket] = None
        self._thread: Optional[threading.Thread] = None

    def start(self):
        """Start WebSocket server."""
        import base64
        import hashlib

        self._running = True
        self._server_socket = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
        self._server_socket.setsockopt(_socket.SOL_SOCKET, _socket.SO_REUSEADDR, 1)
        self._server_socket.settimeout(1.0)

        try:
            self._server_socket.bind((self.host, self.port))
            self._server_socket.listen(5)
        except OSError as e:
            print(f"  ⚠️ WebSocket port {self.port} occupied: {e}")
            return

        self._thread = threading.Thread(target=self._accept_loop, daemon=True)
        self._thread.start()
        print(f"  🔌 WebSocket hot reload: ws://{self.host}:{self.port}")

    def stop(self):
        """Stop WebSocket server."""
        self._running = False
        for client in self.clients:
            try:
                client.close()
            except:
                pass
        self.clients.clear()
        if self._server_socket:
            try:
                self._server_socket.close()
            except:
                pass

    def broadcast(self, message: str):
        """Send message to all connected clients."""
        for client in list(self.clients):
            try:
                self._ws_send(client, message)
            except:
                self.clients.discard(client)

    def reload(self):
        """Trigger browser reload."""
        self.broadcast(json.dumps({"type": "reload"}))

    def _accept_loop(self):
        """Accept incoming WebSocket connections."""
        while self._running:
            try:
                client_socket, addr = self._server_socket.accept()
                threading.Thread(
                    target=self._handle_client,
                    args=(client_socket,),
                    daemon=True,
                ).start()
            except _socket.timeout:
                continue
            except OSError:
                break

    def _handle_client(self, client_socket: _socket.socket):
        """Handle WebSocket client handshake and messages."""
        try:
            request = client_socket.recv(4096).decode("utf-8", errors="ignore")

            # WebSocket handshake
            if "Upgrade: websocket" not in request and "upgrade: websocket" not in request:
                client_socket.close()
                return

            # Extract Sec-WebSocket-Key
            key = None
            for line in request.split("\r\n"):
                if line.lower().startswith("sec-websocket-key:"):
                    key = line.split(":", 1)[1].strip()
                    break

            if not key:
                client_socket.close()
                return

            import base64
            accept_key = base64.b64encode(
                hashlib.sha1((key + WS_MAGIC).encode()).digest()
            ).decode()

            # Send handshake response
            response = (
                "HTTP/1.1 101 Switching Protocols\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n"
                f"Sec-WebSocket-Accept: {accept_key}\r\n"
                "\r\n"
            )
            client_socket.sendall(response.encode())
            self.clients.add(client_socket)

            # Keep connection alive — read loop
            while self._running:
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                except:
                    break
        except:
            pass
        finally:
            self.clients.discard(client_socket)
            try:
                client_socket.close()
            except:
                pass

    def _ws_send(self, sock: _socket.socket, message: str):
        """Send a WebSocket text frame."""
        payload = message.encode("utf-8")
        length = len(payload)

        # Build frame: FIN=1 + opcode=1 (text) + mask bit=0 (server to client)
        frame = bytearray()
        frame.append(0x81)  # FIN + TEXT

        if length < 126:
            frame.append(length)
        elif length < 65536:
            frame.append(126)
            frame.extend(struct.pack("!H", length))
        else:
            frame.append(127)
            frame.extend(struct.pack("!Q", length))

        frame.extend(payload)
        sock.sendall(bytes(frame))


# ==================== File Watcher ====================

class FileWatcher:
    """Watch for file changes and trigger reload."""

    def __init__(self, watch_dir: str, callback, interval: float = 1.0):
        self.watch_dir = watch_dir
        self.callback = callback
        self.interval = interval
        self._running = False
        self._last_hashes: dict = {}
        self._thread: Optional[threading.Thread] = None

    def start(self):
        """Start watching files."""
        self._running = True
        self._thread = threading.Thread(target=self._watch_loop, daemon=True)
        self._thread.start()
        print("  👀 File watcher started (hot reload enabled)")

    def stop(self):
        """Stop watching files."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)

    def _watch_loop(self):
        """Main watch loop — uses file hashing for reliable change detection."""
        while self._running:
            self._check_files()
            time.sleep(self.interval)

    def _file_hash(self, path: str) -> str:
        """Compute file content hash for change detection."""
        try:
            h = hashlib.md5()
            with open(path, "rb") as f:
                h.update(f.read(8192))  # Read first 8KB for speed
            return h.hexdigest()
        except:
            return ""

    def _check_files(self):
        """Check for file modifications using content hashing."""
        current_hashes = {}
        for root, dirs, files in os.walk(self.watch_dir):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]
            for f in files:
                if f.endswith((".py", ".html", ".css", ".js", ".json")):
                    path = os.path.join(root, f)
                    file_hash = self._file_hash(path)
                    current_hashes[path] = file_hash

        # Detect changes
        changed_files = []
        for path, file_hash in current_hashes.items():
            if path in self._last_hashes:
                if file_hash != self._last_hashes[path]:
                    changed_files.append(os.path.relpath(path, self.watch_dir))
            else:
                pass  # New file, skip

        if changed_files:
            self.callback(changed_files)

        self._last_hashes = current_hashes


# ==================== HTTP Handler ====================

class PyVibeHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler dengan WebSocket support."""

    def __init__(self, *args, directory: str = ".pyvibe", ws_port: int = 8080, **kwargs):
        self.serve_dir = directory
        self.ws_port = ws_port
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self):
        path = self.path.split("?")[0]

        # Try exact file
        file_path = os.path.join(self.serve_dir, path.lstrip("/"))
        if os.path.isfile(file_path):
            self._serve_with_reload_script(file_path)
            return

        # Try index.html in directory
        index_path = os.path.join(self.serve_dir, path.lstrip("/"), "index.html")
        if os.path.isfile(index_path):
            self._serve_with_reload_script(index_path)
            return

        # Root index
        root_index = os.path.join(self.serve_dir, "index.html")
        if os.path.isfile(root_index):
            self._serve_with_reload_script(root_index)
            return

        self.send_error(404, f"File tidak ditemukan: {path}")

    def _serve_with_reload_script(self, file_path: str):
        """Serve file with hot reload script injected for HTML files."""
        try:
            with open(file_path, "rb") as f:
                content = f.read()

            if file_path.endswith(".html"):
                # Inject WebSocket hot reload script
                reload_script = f"""
<script>
(function() {{
    const ws = new WebSocket('ws://{self.client_address[0]}:{self.ws_port}');
    ws.onmessage = function(e) {{
        const msg = JSON.parse(e.data);
        if (msg.type === 'reload') {{
            console.log('🔄 PyVibe hot reload...');
            location.reload();
        }}
    }};
    ws.onclose = function() {{
        setTimeout(() => location.reload(), 2000);
    }};
}})();
</script>"""
                content_str = content.decode("utf-8", errors="ignore")
                # Inject before </body>
                if "</body>" in content_str:
                    content_str = content_str.replace("</body>", reload_script + "\n</body>")
                else:
                    content_str += reload_script
                content = content_str.encode("utf-8")

            # Send response
            self.send_response(200)
            self.send_header("Content-Length", str(len(content)))

            # Set content type
            ext = os.path.splitext(file_path)[1].lower()
            content_types = {
                ".html": "text/html; charset=utf-8",
                ".css": "text/css; charset=utf-8",
                ".js": "application/javascript; charset=utf-8",
                ".json": "application/json; charset=utf-8",
                ".png": "image/png",
                ".jpg": "image/jpeg",
                ".svg": "image/svg+xml",
                ".ico": "image/x-icon",
            }
            self.send_header("Content-Type", content_types.get(ext, "text/plain"))

            # No caching for dev
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            self.wfile.write(content)

        except Exception as e:
            self.send_error(500, f"Error: {e}")

    def log_message(self, format, *args):
        """Custom log format."""
        status_code = args[1] if len(args) > 1 else ""
        method = args[0].split()[0] if args else ""
        path = args[0].split()[1] if len(args[0].split()) > 1 else ""

        status_colors = {
            "200": "\033[92m",  # green
            "304": "\033[93m",  # yellow
            "404": "\033[91m",  # red
            "500": "\033[91m",  # red
        }
        reset = "\033[0m"
        color = status_colors.get(str(status_code), "")

        print(f"  {color}●{reset} {method} {path} → {color}{status_code}{reset}")


# ==================== Main Server ====================

def start_dev_server(host: str = "localhost", port: int = 3000, app=None):
    """
    Start PyVibe development server dengan WebSocket hot reload.

    Features:
    - Auto-rebuilds on file change
    - WebSocket hot reload (browser auto-refreshes)
    - Beautiful terminal output
    - File watching
    """
    serve_dir = ".pyvibe"
    ws_port = port + 1

    os.makedirs(serve_dir, exist_ok=True)

    # Logo
    print()
    print("  ╭─────────────────────────────────────╮")
    print("  │  🐍 PyVibe Development Server        │")
    print("  │  Hot reload: ON 🔥                   │")
    print("  ╰─────────────────────────────────────╯")
    print()

    # Build initial output
    if app:
        print("  🔨 Building...")
        app.renderer.build_static(serve_dir)
        print("  ✅ Build complete!")
        print()

    # Start WebSocket server
    ws_server = WebSocketServer(host, ws_port)
    ws_server.start()

    # File watcher with hot reload
    def on_change(changed_files):
        if app:
            print(f"\n  🔄 Files changed: {', '.join(changed_files)}")
            print("  🔨 Rebuilding...")
            app.renderer.build_static(serve_dir)
            print("  ✅ Rebuild complete!")
            ws_server.reload()  # Trigger browser reload!

    watcher = FileWatcher(".", on_change, interval=1.0)
    watcher.start()

    # Start HTTP server
    handler = lambda *args: PyVibeHandler(*args, directory=serve_dir, ws_port=ws_port)

    print(f"  🌐 Server:     http://{host}:{port}")
    print(f"  🔌 Hot reload: ws://{host}:{ws_port}")
    print(f"  📂 Watching:   {os.getcwd()}")
    print()
    print("  Press Ctrl+C to stop")
    print("  ─────────────────────────────────────")
    print()

    try:
        with socketserver.TCPServer((host, port), handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  👋 Server stopped. Happy vibing! 🐍")
        watcher.stop()
        ws_server.stop()
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\n  ⚠️ Port {port} sudah dipake. Coba port lain:")
            print(f"     python app.py --port {port + 1}")
        else:
            raise
