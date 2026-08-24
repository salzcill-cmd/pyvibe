"""
🐍 PyVibe SSR — Server-Side Rendering & Streaming.

"Render di server, tampil di browser — cepat & SEO-friendly."

Features:
- SSRRenderer — Render components on server
- StreamingRenderer — Stream HTML chunks to client
- Hydration — Client-side hydration support
- Incremental Streaming — Stream components as they render
- Cache — SSR cache for performance
- Pre-render — Pre-render pages at build time

Usage:
    from pyvibe.ssr import SSRRenderer, StreamingRenderer, hydrate_script

    # Server-Side Rendering
    ssr = SSRRenderer(app)
    html = ssr.render_route("/")
    full_page = ssr.render_page("/", title="My App")

    # Streaming
    stream = StreamingRenderer(app)
    for chunk in stream.stream_route("/"):
        response.write(chunk)

    # Hydration
    script = hydrate_script("app-root")
"""

from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, Union
from dataclasses import dataclass, field
import time
import hashlib
import json
import os


# ==================== SSR Renderer ====================

class SSRRenderer:
    """
    Server-Side Renderer — render PyVibe components to HTML on server.

    Usage:
        from pyvibe import App, judul, paragraf
        from pyvibe.ssr import SSRRenderer

        app = App("My App")

        @app.route("/")
        def home():
            return tampil(judul("Halo!"), paragraf("Ini SSR"))

        ssr = SSRRenderer(app)
        html = ssr.render_route("/")
    """

    def __init__(self, app=None, cache_enabled: bool = True,
                 cache_ttl: int = 300):
        self.app = app
        self.cache_enabled = cache_enabled
        self.cache_ttl = cache_ttl
        self._cache: Dict[str, Dict] = {}
        self._stats = {"renders": 0, "cache_hits": 0, "total_time": 0}

    def render_route(self, path: str, context: Optional[Dict] = None) -> str:
        """Render a route to HTML string."""
        start = time.time()

        # Check cache
        cache_key = self._cache_key(path, context)
        if self.cache_enabled and cache_key in self._cache:
            entry = self._cache[cache_key]
            if time.time() - entry["time"] < self.cache_ttl:
                self._stats["cache_hits"] += 1
                return entry["html"]

        # Get route handler
        html = ""
        if self.app and path in self.app.routes:
            route = self.app.routes[path]
            try:
                result = route.handler()
                if isinstance(result, str):
                    html = result
                elif hasattr(result, "render"):
                    html = result.render()
                else:
                    html = str(result)
            except Exception as e:
                html = self._error_page(str(e), path)
        else:
            html = self._not_found_page(path)

        # Cache result
        if self.cache_enabled:
            self._cache[cache_key] = {"html": html, "time": time.time()}

        self._stats["renders"] += 1
        self._stats["total_time"] += time.time() - start

        return html

    def render_page(self, path: str, title: str = "",
                    meta: Optional[Dict] = None,
                    scripts: Optional[List[str]] = None,
                    styles: Optional[List[str]] = None,
                    context: Optional[Dict] = None) -> str:
        """Render a full HTML page with SSR content."""
        body = self.render_route(path, context)

        meta_tags = ""
        if meta:
            for key, value in meta.items():
                meta_tags += f'<meta name="{key}" content="{value}">\n'

        script_tags = ""
        if scripts:
            for src in scripts:
                script_tags += f'<script src="{src}"></script>\n'

        style_tags = ""
        if styles:
            for href in styles:
                style_tags += f'<link rel="stylesheet" href="{href}">\n'

        title = title or "PyVibe SSR App"

        return f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {meta_tags}
    {style_tags}
</head>
<body>
    <div id="app">{body}</div>
    <script>window.__SSR__ = true;</script>
    <script>window.__INITIAL_STATE__ = {json.dumps(context or {})}</script>
    {script_tags}
</body>
</html>"""

    def render_component(self, component) -> str:
        """Render a single component to HTML."""
        if hasattr(component, "render"):
            return component.render()
        return str(component)

    def clear_cache(self):
        """Clear SSR cache."""
        self._cache.clear()

    def get_stats(self) -> Dict:
        """Get rendering statistics."""
        return {
            **self._stats,
            "cache_size": len(self._cache),
            "avg_time": (
                round(self._stats["total_time"] / self._stats["renders"], 4)
                if self._stats["renders"] > 0 else 0
            ),
        }

    def _cache_key(self, path: str, context: Optional[Dict]) -> str:
        """Generate cache key."""
        raw = f"{path}:{json.dumps(context or {}, sort_keys=True)}"
        return hashlib.md5(raw.encode()).hexdigest()

    def _error_page(self, error: str, path: str) -> str:
        """Render error page."""
        return f"""<div style="padding:40px;text-align:center;font-family:sans-serif;">
            <h1 style="color:#EF4444;">500 — Internal Server Error</h1>
            <p>Error rendering <code>{path}</code></p>
            <p style="color:#6B7280;">{error}</p>
        </div>"""

    def _not_found_page(self, path: str) -> str:
        """Render 404 page."""
        return f"""<div style="padding:40px;text-align:center;font-family:sans-serif;">
            <h1 style="color:#7C3AED;">404 — Halaman Tidak Ditemukan</h1>
            <p><code>{path}</code> tidak tersedia.</p>
        </div>"""


# ==================== Streaming Renderer ====================

class StreamingRenderer:
    """
    Streaming Renderer — stream HTML chunks to client.

    Usage:
        stream = StreamingRenderer(app)
        for chunk in stream.stream_route("/"):
            yield chunk  # Send chunk to client
    """

    def __init__(self, app=None, chunk_size: int = 1024):
        self.app = app
        self.chunk_size = chunk_size

    def stream_route(self, path: str, context: Optional[Dict] = None):
        """Stream route rendering as chunks."""
        # Stream document head
        yield self._head_html(context)
        yield "\n<!-- SSR Stream Start -->\n"

        # Stream body content
        if self.app and path in self.app.routes:
            route = self.app.routes[path]
            try:
                result = route.handler()
                html = result if isinstance(result, str) else (
                    result.render() if hasattr(result, "render") else str(result)
                )
                # Chunk the HTML
                for i in range(0, len(html), self.chunk_size):
                    yield html[i:i + self.chunk_size]
            except Exception as e:
                yield f'<div class="ssr-error">Error: {e}</div>'
        else:
            yield f'<div class="ssr-not-found">404: {path} not found</div>'

        # Stream tail
        yield "\n<!-- SSR Stream End -->\n"
        yield self._tail_html()

    def stream_components(self, components: List):
        """Stream a list of components."""
        yield self._head_html()
        for comp in components:
            html = comp.render() if hasattr(comp, "render") else str(comp)
            for i in range(0, len(html), self.chunk_size):
                yield html[i:i + self.chunk_size]
        yield self._tail_html()

    def _head_html(self, context: Optional[Dict] = None) -> str:
        """HTML head with streaming support."""
        return f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PyVibe SSR</title>
</head>
<body>
<div id="app">"""

    def _tail_html(self) -> str:
        """HTML tail."""
        return """</div>
<script>window.__SSR_STREAM__ = true;</script>
</body>
</html>"""


# ==================== Hydration ====================

def hydrate_script(root_id: str = "app", hydrate_fn: str = "PyVibe.hydrate") -> str:
    """
    Generate client-side hydration script.

    Usage:
        script = hydrate_script("app-root")
        # Add to HTML: <script>{script}</script>
    """
    return f"""
<script>
(function() {{
    var root = document.getElementById('{root_id}');
    if (!root) {{
        console.error('[PyVibe SSR] Root element #{root_id} not found');
        return;
    }}

    // Mark as hydrated
    root.setAttribute('data-hydrated', 'true');

    // Initialize PyVibe client
    if (typeof {hydrate_fn} === 'function') {{
        {hydrate_fn}(root, window.__INITIAL_STATE__ || {{}});
    }}

    // Dispatch hydration event
    root.dispatchEvent(new CustomEvent('pyvibe:hydrated', {{
        detail: {{ timestamp: Date.now() }}
    }}));

    console.log('[PyVibe SSR] Hydration complete ✓');
}})();
</script>"""


def ssr_meta_tags(title: str = "", description: str = "",
                  image: str = "", url: str = "") -> str:
    """Generate SSR-friendly meta tags."""
    tags = []
    if title:
        tags.append(f'<meta property="og:title" content="{title}">')
        tags.append(f'<title>{title}</title>')
    if description:
        tags.append(f'<meta name="description" content="{description}">')
        tags.append(f'<meta property="og:description" content="{description}">')
    if image:
        tags.append(f'<meta property="og:image" content="{image}">')
    if url:
        tags.append(f'<meta property="og:url" content="{url}">')
    tags.append('<meta property="og:type" content="website">')
    return "\n    ".join(tags)


# ==================== Pre-render ====================

class PreRenderer:
    """
    Pre-render pages at build time for static hosting.

    Usage:
        pre = PreRenderer(app)
        pre.add_route("/")
        pre.add_route("/about")
        pre.render_all("dist/")
    """

    def __init__(self, app=None):
        self.app = app
        self._routes: List[str] = []
        self._ssr = SSRRenderer(app)

    def add_route(self, path: str):
        """Add route to pre-render."""
        if path not in self._routes:
            self._routes.append(path)

    def add_routes(self, paths: List[str]):
        """Add multiple routes."""
        for path in paths:
            self.add_route(path)

    def render_all(self, output_dir: str = "dist") -> Dict[str, str]:
        """Pre-render all routes to files."""
        os.makedirs(output_dir, exist_ok=True)
        results = {}

        for path in self._routes:
            html = self._ssr.render_page(path)
            # Convert path to filename
            filename = path.strip("/").replace("/", "_") or "index"
            filepath = os.path.join(output_dir, f"{filename}.html")

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html)

            results[path] = filepath

        return results

    def render_sitemap(self) -> str:
        """Generate sitemap XML."""
        urls = "\n".join(
            f'  <url><loc>{path}</loc></url>'
            for path in self._routes
        )
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>"""
