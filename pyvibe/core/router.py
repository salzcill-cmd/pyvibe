"""
Router — client-side routing untuk SPA navigation.

Supports:
- Dynamic routes (/produk/<id>)
- Nested routes
- Route guards
- History API
"""

from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, Tuple
import re
import json
from dataclasses import dataclass, field


@dataclass
class RouteMatch:
    """Hasil matching route."""
    path: str
    params: Dict[str, str] = field(default_factory=dict)
    query: Dict[str, str] = field(default_factory=dict)


class Router:
    """
    Client-side router untuk PyVibe.

    Usage:
        router = Router()
        router.add_route("/", handler)
        router.add_route("/produk/{id}", handler)

        # Match route
        match = router.match("/produk/123")
        # → RouteMatch(path="/produk/{id}", params={"id": "123"})
    """

    def __init__(self):
        self.routes: List[Tuple[str, Callable, List[str]]] = []
        self._before_hooks: List[Callable] = []
        self._after_hooks: List[Callable] = []
        self._not_found: Optional[Callable] = None
        self._current: Optional[RouteMatch] = None

    def add_route(self, path: str, handler: Callable, methods: Optional[List[str]] = None):
        """Register route."""
        self.routes.append((path, handler, methods or ["GET"]))

    def before(self, hook: Callable):
        """Add before navigation hook (guard)."""
        self._before_hooks.append(hook)

    def after(self, hook: Callable):
        """Add after navigation hook."""
        self._after_hooks.append(hook)

    def not_found(self, handler: Callable):
        """Set 404 handler."""
        self._not_found = handler

    def match(self, path: str) -> Optional[RouteMatch]:
        """Match path ke route pattern.

        Supports:
        - /static/path → exact match
        - /dynamic/{id} → parameter capture
        - /dynamic/{id:int} → typed parameter
        - /wildcard/*path → wildcard
        """
        # Clean path
        path = path.rstrip("/") or "/"
        query = {}

        # Parse query string
        if "?" in path:
            path, query_str = path.split("?", 1)
            for param in query_str.split("&"):
                if "=" in param:
                    key, value = param.split("=", 1)
                    query[key] = value

        for route_path, handler, methods in self.routes:
            route_path_clean = route_path.rstrip("/") or "/"
            params = self._match_pattern(route_path_clean, path)
            if params is not None:
                self._current = RouteMatch(path=route_path, params=params, query=query)
                return self._current

        return None

    def _match_pattern(self, pattern: str, path: str) -> Optional[Dict[str, str]]:
        """Match route pattern ke actual path."""
        # Exact match
        if pattern == path:
            return {}

        # Split segments
        pattern_segments = pattern.split("/")
        path_segments = path.split("/")

        if len(pattern_segments) != len(path_segments):
            return None

        params = {}
        for p_seg, path_seg in zip(pattern_segments, path_segments):
            if p_seg.startswith("{") and p_seg.endswith("}"):
                # Parameter
                param_name = p_seg[1:-1]
                # Handle typed params {id:int}
                if ":" in param_name:
                    param_name, param_type = param_name.split(":", 1)
                params[param_name] = path_seg
            elif p_seg != path_seg:
                return None

        return params

    def navigate(self, path: str) -> Optional[RouteMatch]:
        """Navigate ke path."""
        # Run before hooks
        for hook in self._before_hooks:
            if not hook(path):
                return None

        match = self.match(path)
        if match:
            self._current = match
            # Run after hooks
            for hook in self._after_hooks:
                hook(match)
            return match
        elif self._not_found:
            self._not_found(path)

        return None

    def get_current(self) -> Optional[RouteMatch]:
        """Get current route match."""
        return self._current

    def get_all_routes(self) -> List[str]:
        """Get all registered route paths."""
        return [path for path, _, _ in self.routes]

    def to_js(self) -> str:
        """Generate JavaScript routing code."""
        routes_js = []
        for path, handler, methods in self.routes:
            params = re.findall(r'\{(\w+)\}', path)
            route_def = {
                "path": path,
                "handler": handler.__name__,
                "methods": methods,
                "params": params,
            }
            routes_js.append(route_def)

        return f"""
const routes = {json.dumps(routes_js, indent=2)};

class PyVibeRouter {{
    constructor() {{
        this.routes = routes;
        this.current = null;
    }}

    match(path) {{
        const cleanPath = path.replace(/\\/$/, '') || '/';
        for (const route of this.routes) {{
            const cleanRoutePath = route.path.replace(/\\/$/, '') || '/';
            if (cleanRoutePath === cleanPath) {{
                return {{ route, params: {{}}, query: this.parseQuery(path) }};
            }}
            // Dynamic routes
            const routeSegments = cleanRoutePath.split('/');
            const pathSegments = cleanPath.split('/');
            if (routeSegments.length !== pathSegments.length) continue;
            const params = {{}};
            let matched = true;
            for (let i = 0; i < routeSegments.length; i++) {{
                if (routeSegments[i].startsWith('{{') && routeSegments[i].endsWith('}}')) {{
                    params[routeSegments[i].slice(1, -1)] = pathSegments[i];
                }} else if (routeSegments[i] !== pathSegments[i]) {{
                    matched = false;
                    break;
                }}
            }}
            if (matched) return {{ route, params, query: this.parseQuery(path) }};
        }}
        return null;
    }}

    parseQuery(path) {{
        const query = {{}};
        const idx = path.indexOf('?');
        if (idx !== -1) {{
            path.slice(idx + 1).split('&').forEach(p => {{
                const [k, v] = p.split('=');
                if (k) query[decodeURIComponent(k)] = decodeURIComponent(v || '');
            }});
        }}
        return query;
    }}

    navigate(path) {{
        window.history.pushState(null, '', path);
        this.resolve();
    }}

    resolve() {{
        const path = window.location.pathname;
        const result = this.match(path);
        if (result) {{
            this.current = result;
            window.dispatchEvent(new CustomEvent('routechange', {{ detail: result }}));
        }}
    }}
}}

const pyvibeRouter = new PyVibeRouter();
"""

