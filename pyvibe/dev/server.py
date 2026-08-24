"""
Development Server — simple HTTP server untuk development.

Features:
- Auto-serves HTML files
- Hot reload on file changes
- Live preview
"""

import http.server
import socketserver
import os
import threading
import time
from pathlib import Path
from typing import Optional


class PyVibeHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler untuk PyVibe."""

    def __init__(self, *args, directory: str = ".pyvibe", **kwargs):
        self.serve_dir = directory
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self):
        # Try to serve the requested file
        path = self.path.split("?")[0]  # Remove query string

        # Try exact path
        file_path = os.path.join(self.serve_dir, path.lstrip("/"))
        if os.path.isfile(file_path):
            super().do_GET()
            return

        # Try index.html in directory
        index_path = os.path.join(self.serve_dir, path.lstrip("/"), "index.html")
        if os.path.isfile(index_path):
            self.path = path.rstrip("/") + "/index.html"
            super().do_GET()
            return

        # Try root index
        root_index = os.path.join(self.serve_dir, "index.html")
        if os.path.isfile(root_index):
            self.path = "/index.html"
            super().do_GET()
            return

        # 404
        self.send_error(404, f"File not found: {path}")

    def log_message(self, format, *args):
        """Custom log format."""
        print(f"  🐍 {args[0]}")


class FileWatcher:
    """Watch for file changes and trigger reload."""

    def __init__(self, watch_dir: str, callback, interval: float = 1.0):
        self.watch_dir = watch_dir
        self.callback = callback
        self.interval = interval
        self._running = False
        self._last_check = {}
        self._thread: Optional[threading.Thread] = None

    def start(self):
        """Start watching files."""
        self._running = True
        self._thread = threading.Thread(target=self._watch_loop, daemon=True)
        self._thread.start()
        print("  👀 File watcher started")

    def stop(self):
        """Stop watching files."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)

    def _watch_loop(self):
        """Main watch loop."""
        while self._running:
            self._check_files()
            time.sleep(self.interval)

    def _check_files(self):
        """Check for file modifications."""
        current_times = {}
        for root, dirs, files in os.walk(self.watch_dir):
            # Skip hidden dirs
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for f in files:
                if f.endswith((".py", ".html", ".css", ".js")):
                    path = os.path.join(root, f)
                    try:
                        mtime = os.path.getmtime(path)
                        current_times[path] = mtime
                        if path in self._last_check:
                            if mtime > self._last_check[path]:
                                print(f"  🔄 File changed: {os.path.relpath(path, self.watch_dir)}")
                                self.callback()
                        else:
                            print(f"  📄 Watching: {os.path.relpath(path, self.watch_dir)}")
                    except OSError:
                        pass
        self._last_check = current_times


def start_dev_server(host: str = "localhost", port: int = 3000, app=None):
    """
    Start PyVibe development server.

    Features:
    - Serves HTML files
    - Watches for changes
    - Auto-rebuilds on change
    """
    serve_dir = ".pyvibe"

    # Ensure serve directory exists
    os.makedirs(serve_dir, exist_ok=True)

    # Build initial output
    if app:
        print("  🔨 Building...")
        app.renderer.build_static(serve_dir)
        print("  ✅ Build complete!")

    # Start file watcher
    def on_change():
        if app:
            print("  🔨 Rebuilding...")
            app.renderer.build_static(serve_dir)
            print("  ✅ Rebuild complete!")

    watcher = FileWatcher(".", on_change, interval=1.5)
    watcher.start()

    # Start server
    handler = lambda *args: PyVibeHandler(*args, directory=serve_dir)

    try:
        with socketserver.TCPServer((host, port), handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  👋 Server stopped. Happy vibing!")
        watcher.stop()
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\n  ⚠️ Port {port} sudah dipake. Coba port lain:")
            print(f"     python app.py --port {port + 1}")
        else:
            raise
