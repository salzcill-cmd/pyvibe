"""
App class — container utama untuk setiap aplikasi PyVibe.

Usage:
    app = App("My Website")
    app.route("/")
    def beranda():
        return tampil(judul("Halo!"))
    app.jalan()
"""

from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, Union
import json
import hashlib
from dataclasses import dataclass, field

from pyvibe.core.component import Component
from pyvibe.core.router import Router
from pyvibe.core.state import State
from pyvibe.core.renderer import Renderer


@dataclass
class Route:
    """Representasi satu route."""
    path: str
    handler: Callable
    methods: List[str] = field(default_factory=lambda: ["GET"])
    name: Optional[str] = None


class App:
    """
    Container utama aplikasi PyVibe.

    Semua route, state, dan configuration di-define di sini.
    """

    def __init__(self, name: str = "PyVibe App", **config):
        self.name = name
        self.config = {
            "name": name,
            "theme": config.get("theme", "default"),
            "language": config.get("language", "id"),
            "debug": config.get("debug", False),
            "port": config.get("port", 3000),
            "host": config.get("host", "localhost"),
            "title": config.get("title", name),
            "description": config.get("description", ""),
            "favicon": config.get("favicon", "🐍"),
            "primary_color": config.get("primary_color", "#7C3AED"),
            "secondary_color": config.get("secondary_color", "#06B6D4"),
            **config,
        }
        self.routes: Dict[str, Route] = {}
        self.middleware: List[Callable] = []
        self.router = Router()
        self.renderer = Renderer(self)
        self._state = State()
        self._on_load: Optional[Callable] = None
        self._on_error: Optional[Callable] = None

    def route(self, path: str, methods: Optional[List[str]] = None, name: Optional[str] = None):
        """
        Decorator untuk register route.

        Usage:
            @app.route("/")
            def beranda():
                return tampil(judul("Halo!"))
        """
        def decorator(handler: Callable):
            route = Route(
                path=path,
                handler=handler,
                methods=methods or ["GET"],
                name=name or handler.__name__,
            )
            self.routes[path] = route
            self.router.add_route(path, handler, methods)
            return handler
        return decorator

    def saat_muat(self, handler: Callable):
        """Decorator untuk on page load handler."""
        self._on_load = handler
        return handler

    def saat_error(self, handler: Callable):
        """Decorator untuk error handler."""
        self._on_error = handler
        return handler

    def tambah_middleware(self, middleware: Callable):
        """Add middleware."""
        self.middleware.append(middleware)
        return self

    def tampil(self, *children: Union[Component, str], **kwargs) -> str:
        """
        Render children ke HTML string.
        Bisa dipake langsung tanpa route, atau return dari route handler.

        Usage:
            app.tampil(judul("Halo"), paragraf("Dunia"))
        """
        return self.renderer.render(*children, **kwargs)

    def render_page(self, *children: Union[Component, str], **kwargs) -> str:
        """Render full page dengan HTML skeleton."""
        return self.renderer.render_page(*children, **kwargs)

    def jalan(self, **kwargs):
        """
        Jalankan development server.

        Usage:
            app.jalan()  # Default port 3000
            app.jalan(port=8080)  # Custom port
        """
        port = kwargs.get("port", self.config["port"])
        host = kwargs.get("host", self.config["host"])

        print(f"""
🐍 PyVibe Development Server
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 App: {self.name}
🌐 URL: http://{host}:{port}
🔥 Hot reload: ON
🎨 Theme: {self.config['theme']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ready! Buka browser dan mulai vibing~ 🚀
        """)

        # Generate HTML files untuk semua routes
        self.renderer.build_static()

        # Start dev server
        from pyvibe.dev.server import start_dev_server
        start_dev_server(host, port, self)

    def export(self, output_dir: str = "dist"):
        """Export ke static HTML files."""
        print(f"📦 Exporting ke {output_dir}...")
        self.renderer.build_static(output_dir)
        print(f"✅ Export selesai! Files ada di {output_dir}/")

    def get_state(self) -> State:
        """Get application state."""
        return self._state

    def set_state(self, key: str, value: Any):
        """Set state value."""
        self._state.set(key, value)

    def get_route(self, path: str) -> Optional[Route]:
        """Get route by path."""
        return self.routes.get(path)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize app config ke dictionary."""
        return {
            "name": self.name,
            "config": self.config,
            "routes": {path: {"name": r.name, "methods": r.methods} for path, r in self.routes.items()},
        }
