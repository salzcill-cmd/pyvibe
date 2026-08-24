"""
App class — container utama untuk setiap aplikasi PyVibe.

v2: Enhanced with middleware, hooks, better config, and production-ready features.

Usage:
    app = App("My Website")
    
    @app.route("/")
    def beranda():
        return tampil(judul("Halo!"))
    
    app.jalan()
"""

from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, Union
import json
import hashlib
import os
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
    middleware: List[Callable] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)


class App:
    """
    Container utama aplikasi PyVibe.
    
    Semua route, state, dan configuration di-define di sini.

    Usage:
        app = App("My Website", theme="dark", debug=True)
        
        @app.route("/")
        def beranda():
            return tampil(judul("Halo!"))
        
        app.jalan(port=8080)
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
            "base_url": config.get("base_url", ""),
            "static_dir": config.get("static_dir", "static"),
            "output_dir": config.get("output_dir", "dist"),
            "auto_reload": config.get("auto_reload", True),
            "minify": config.get("minify", False),
            **config,
        }
        self.routes: Dict[str, Route] = {}
        self.middleware: List[Callable] = []
        self._middleware_stack: List[Callable] = []
        self.router = Router()
        self.renderer = Renderer(self)
        self._state = State()
        self._on_load: Optional[Callable] = None
        self._on_error: Optional[Callable] = None
        self._hooks: Dict[str, List[Callable]] = {
            "before_request": [],
            "after_request": [],
            "before_render": [],
            "after_render": [],
            "on_startup": [],
            "on_shutdown": [],
        }
        self._error_handlers: Dict[int, Callable] = {}
        self._plugins: List[Any] = []

    def route(self, path: str, methods: Optional[List[str]] = None, name: Optional[str] = None, **meta):
        """
        Decorator untuk register route.

        Usage:
            @app.route("/")
            def beranda():
                return tampil(judul("Halo!"))
            
            @app.route("/api/users", methods=["GET", "POST"], name="users")
            def users():
                return {"data": "users"}
        """
        def decorator(handler: Callable):
            route = Route(
                path=path,
                handler=handler,
                methods=methods or ["GET"],
                name=name or handler.__name__,
                meta=meta,
            )
            self.routes[path] = route
            self.router.add_route(path, handler, methods)
            return handler
        return decorator

    def get(self, path: str, name: Optional[str] = None):
        """Shortcut for GET route."""
        return self.route(path, methods=["GET"], name=name)

    def post(self, path: str, name: Optional[str] = None):
        """Shortcut for POST route."""
        return self.route(path, methods=["POST"], name=name)

    def put(self, path: str, name: Optional[str] = None):
        """Shortcut for PUT route."""
        return self.route(path, methods=["PUT"], name=name)

    def delete(self, path: str, name: Optional[str] = None):
        """Shortcut for DELETE route."""
        return self.route(path, methods=["DELETE"], name=name)

    def patch(self, path: str, name: Optional[str] = None):
        """Shortcut for PATCH route."""
        return self.route(path, methods=["PATCH"], name=name)

    def api(self, path: str, methods: Optional[List[str]] = None, name: Optional[str] = None):
        """Shortcut for API routes (returns JSON)."""
        def decorator(handler: Callable):
            @self.route(path, methods=methods, name=name)
            def api_handler(*args, **kwargs):
                result = handler(*args, **kwargs)
                if isinstance(result, (dict, list)):
                    return json.dumps(result)
                return result
            return handler
        return decorator

    # ==================== Lifecycle Hooks ====================

    def saat_muat(self, handler: Callable):
        """Decorator untuk on page load handler."""
        self._on_load = handler
        return handler

    def saat_error(self, handler: Callable):
        """Decorator untuk error handler."""
        self._on_error = handler
        return handler

    def before_request(self, func: Callable):
        """Decorator for before request hook."""
        self._hooks["before_request"].append(func)
        return func

    def after_request(self, func: Callable):
        """Decorator for after request hook."""
        self._hooks["after_request"].append(func)
        return func

    def before_render(self, func: Callable):
        """Decorator for before render hook."""
        self._hooks["before_render"].append(func)
        return func

    def after_render(self, func: Callable):
        """Decorator for after render hook."""
        self._hooks["after_render"].append(func)
        return func

    def on_startup(self, func: Callable):
        """Decorator for startup hook."""
        self._hooks["on_startup"].append(func)
        return func

    def on_shutdown(self, func: Callable):
        """Decorator for shutdown hook."""
        self._hooks["on_shutdown"].append(func)
        return func

    def error_handler(self, status_code: int):
        """Decorator for custom error handlers."""
        def decorator(func: Callable):
            self._error_handlers[status_code] = func
            return func
        return decorator

    # ==================== Middleware ====================

    def tambah_middleware(self, middleware: Callable):
        """Add middleware."""
        self.middleware.append(middleware)
        return self

    def use(self, middleware_or_plugin: Any):
        """Add middleware or plugin."""
        if hasattr(middleware_or_plugin, "process_request"):
            self.middleware.append(middleware_or_plugin)
        elif hasattr(middleware_or_plugin, "setup"):
            middleware_or_plugin.setup(self)
            self._plugins.append(middleware_or_plugin)
        return self

    # ==================== State Management ====================

    def get_state(self) -> State:
        """Get application state."""
        return self._state

    def set_state(self, key: str, value: Any):
        """Set state value."""
        self._state.set(key, value)

    def get_route(self, path: str) -> Optional[Route]:
        """Get route by path."""
        return self.routes.get(path)

    # ==================== Rendering ====================

    def tampil(self, *children: Union[Component, str], **kwargs) -> str:
        """
        Render children ke HTML string.

        Usage:
            app.tampil(judul("Halo"), paragraf("Dunia"))
        """
        # Run before_render hooks
        for hook in self._hooks["before_render"]:
            try:
                hook(children)
            except Exception:
                pass

        result = self.renderer.render(*children, **kwargs)

        # Run after_render hooks
        for hook in self._hooks["after_render"]:
            try:
                hook(result)
            except Exception:
                pass

        return result

    def render_page(self, *children: Union[Component, str], **kwargs) -> str:
        """Render full page dengan HTML skeleton."""
        return self.renderer.render_page(*children, **kwargs)

    # ==================== Server ====================

    def jalan(self, **kwargs):
        """
        Jalankan development server.

        Usage:
            app.jalan()  # Default port 3000
            app.jalan(port=8080)  # Custom port
            app.jalan(host="0.0.0.0")  # Expose to network
        """
        port = kwargs.get("port", self.config["port"])
        host = kwargs.get("host", self.config["host"])

        # Run startup hooks
        for hook in self._hooks["on_startup"]:
            try:
                hook()
            except Exception:
                pass

        print(f"""
🐍 PyVibe Development Server
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 App: {self.name}
🌐 URL: http://{host}:{port}
🔥 Hot reload: {'ON' if self.config['auto_reload'] else 'OFF'}
🎨 Theme: {self.config['theme']}
📦 Routes: {len(self.routes)}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ready! Buka browser dan mulai vibing~ 🚀
        """)

        # Generate HTML files untuk semua routes
        self.renderer.build_static()

        # Start dev server
        from pyvibe.dev.server import start_dev_server
        start_dev_server(host, port, self)

    # ==================== Export ====================

    def export(self, output_dir: Optional[str] = None):
        """Export ke static HTML files."""
        output_dir = output_dir or self.config["output_dir"]
        print(f"📦 Exporting ke {output_dir}...")
        self.renderer.build_static(output_dir)
        print(f"✅ Export selesai! Files ada di {output_dir}/")
        return output_dir

    def to_dict(self) -> Dict[str, Any]:
        """Serialize app config ke dictionary."""
        return {
            "name": self.name,
            "config": self.config,
            "routes": {
                path: {
                    "name": r.name,
                    "methods": r.methods,
                    "meta": r.meta,
                }
                for path, r in self.routes.items()
            },
            "plugins": [p.__class__.__name__ for p in self._plugins],
        }

    def to_json(self) -> str:
        """Serialize app config ke JSON."""
        return json.dumps(self.to_dict(), indent=2)

    def __repr__(self) -> str:
        return f"<App name='{self.name}' routes={len(self.routes)}>"
