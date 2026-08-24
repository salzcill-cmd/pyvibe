"""
🐍 PyVibe PWA — Progressive Web App support.

"Install di HP, offline juga bisa jalan."

Features:
- PWAManifest — Generate manifest.json
- ServiceWorker — Generate service worker
- OfflinePage — Offline fallback page
- Icons — Generate PWA icons config
- Install prompt — Add to home screen

Usage:
    from pyvibe.pwa import PWAManifest, ServiceWorker, OfflinePage

    # Generate manifest.json
    manifest = PWAManifest(
        name="My App",
        short_name="MyApp",
        description="My awesome app",
        theme_color="#7C3AED",
        background_color="#FFFFFF",
    )
    manifest.save("manifest.json")

    # Generate service worker
    sw = ServiceWorker()
    sw.add_cache("static", ["/style.css", "/app.js"])
    sw.add_network_first("/api/")
    sw.save("sw.js")

    # Offline page
    offline = OfflinePage()
    offline.save("offline.html")
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
import json
import os


# ==================== PWA Manifest ====================

@dataclass
class PWAManifest:
    """
    Generate web manifest.json for PWA.

    Usage:
        manifest = PWAManifest(
            name="My App",
            short_name="MyApp",
            start_url="/",
            theme_color="#7C3AED",
        )
        manifest.save("manifest.json")
    """
    name: str = "PyVibe App"
    short_name: str = "PyVibe"
    description: str = ""
    start_url: str = "/"
    display: str = "standalone"
    background_color: str = "#FFFFFF"
    theme_color: str = "#7C3AED"
    orientation: str = "portrait-primary"
    scope: str = "/"
    lang: str = "id"
    icons: List[Dict] = field(default_factory=list)
    categories: List[str] = field(default_factory=lambda: ["webapp"])
    shortcuts: List[Dict] = field(default_factory=list)
    screenshots: List[Dict] = field(default_factory=list)
    extra: Dict = field(default_factory=dict)

    def add_icon(self, src: str, sizes: str = "192x192",
                 purpose: str = "any", type: str = "image/png"):
        """Add an icon."""
        self.icons.append({
            "src": src,
            "sizes": sizes,
            "type": type,
            "purpose": purpose,
        })
        return self

    def add_default_icons(self, prefix: str = "/icons"):
        """Add common PWA icon sizes."""
        sizes = ["72x72", "96x96", "128x128", "144x144",
                 "152x152", "192x192", "384x384", "512x512"]
        for size in sizes:
            w, h = size.split("x")
            self.add_icon(f"{prefix}/icon-{size}.png", size)
        return self

    def add_shortcut(self, name: str, url: str, description: str = "",
                     icons: Optional[List[Dict]] = None):
        """Add a shortcut."""
        shortcut = {"name": name, "url": url}
        if description:
            shortcut["description"] = description
        if icons:
            shortcut["icons"] = icons
        self.shortcuts.append(shortcut)
        return self

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        d = {
            "name": self.name,
            "short_name": self.short_name,
            "start_url": self.start_url,
            "display": self.display,
            "background_color": self.background_color,
            "theme_color": self.theme_color,
            "orientation": self.orientation,
            "scope": self.scope,
            "lang": self.lang,
        }
        if self.description:
            d["description"] = self.description
        if self.icons:
            d["icons"] = self.icons
        if self.categories:
            d["categories"] = self.categories
        if self.shortcuts:
            d["shortcuts"] = self.shortcuts
        d.update(self.extra)
        return d

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def save(self, path: str = "manifest.json"):
        """Save manifest to file."""
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_json())

    def render_link(self) -> str:
        """Render HTML link tag for manifest."""
        return '<link rel="manifest" href="/manifest.json">'

    def render_meta_tags(self) -> str:
        """Render PWA meta tags."""
        return f"""<meta name="theme-color" content="{self.theme_color}">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="{self.short_name}">
<link rel="apple-touch-icon" href="/icons/icon-192x192.png">"""


# ==================== Service Worker ====================

class ServiceWorker:
    """
    Generate service worker JavaScript for offline support.

    Usage:
        sw = ServiceWorker()
        sw.add_cache("static-v1", ["/style.css", "/app.js", "/logo.png"])
        sw.add_cache_first("/fonts/", "fonts-v1")
        sw.add_network_first("/api/", "api-cache")
        sw.add_stale_while_revalidate("/images/", "images-v1")
        sw.save("sw.js")
    """

    def __init__(self, cache_name: str = "pyvibe-cache-v1"):
        self.cache_name = cache_name
        self._caches: List[Dict] = []
        self._strategies: List[Dict] = []
        self._offline_fallback: str = "/offline.html"
        self._precache: List[str] = []

    def add_cache(self, name: str, urls: List[str]):
        """Add URLs to cache on install."""
        self._caches.append({"name": name, "urls": urls})
        return self

    def precache(self, urls: List[str]):
        """Add URLs to precache."""
        self._precache.extend(urls)
        return self

    def add_cache_first(self, pattern: str, cache_name: str = ""):
        """Add Cache-First strategy for a URL pattern."""
        self._strategies.append({
            "type": "cache_first",
            "pattern": pattern,
            "cache": cache_name or self.cache_name,
        })
        return self

    def add_network_first(self, pattern: str, cache_name: str = ""):
        """Add Network-First strategy for a URL pattern."""
        self._strategies.append({
            "type": "network_first",
            "pattern": pattern,
            "cache": cache_name or self.cache_name,
        })
        return self

    def add_stale_while_revalidate(self, pattern: str, cache_name: str = ""):
        """Add Stale-While-Revalidate strategy."""
        self._strategies.append({
            "type": "stale_while_revalidate",
            "pattern": pattern,
            "cache": cache_name or self.cache_name,
        })
        return self

    def set_offline_fallback(self, url: str):
        """Set offline fallback page."""
        self._offline_fallback = url
        return self

    def generate_js(self) -> str:
        """Generate service worker JavaScript."""
        # Build precache list
        precache_urls = []
        for cache in self._caches:
            for url in cache["urls"]:
                precache_urls.append(f'    "{url}"')
        for url in self._precache:
            precache_urls.append(f'    "{url}"')

        precache_list = ",\n".join(precache_urls)

        # Build strategy handlers
        strategy_code = ""
        for s in self._strategies:
            strategy_code += f"""
    // Strategy: {s['type'].replace('_', ' ').title()} for {s['pattern']}
    if (url.pathname.startsWith('{s["pattern"]}')) {{
        event.respondWith({self._strategy_fn(s['type'], s['cache'], s['pattern'])});
        return;
    }}
"""
        return f"""// PyVibe Service Worker
// Generated automatically — do not edit manually

const CACHE_NAME = '{self.cache_name}';
const OFFLINE_URL = '{self._offline_fallback}';

const PRECACHE_URLS = [
{precache_list}
];

// Install — cache assets
self.addEventListener('install', (event) => {{
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(PRECACHE_URLS))
            .then(() => self.skipWaiting())
    );
}});

// Activate — clean old caches
self.addEventListener('activate', (event) => {{
    event.waitUntil(
        caches.keys().then(names =>
            Promise.all(
                names.filter(name => name !== CACHE_NAME)
                     .map(name => caches.delete(name))
            )
        ).then(() => self.clients.claim())
    );
}});

// Fetch — apply strategies
self.addEventListener('fetch', (event) => {{
    const url = new URL(event.request.url);
{strategy_code}
    // Default: Network first, fallback to cache
    event.respondWith(
        fetch(event.request)
            .then(response => {{
                const clone = response.clone();
                caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
                return response;
            }})
            .catch(() => caches.match(event.request))
    );
}});
"""

    def _strategy_fn(self, strategy: str, cache: str, pattern: str) -> str:
        """Generate strategy function code."""
        if strategy == "cache_first":
            return f"""caches.match(event.request)
            .then(cached => cached || fetch(event.request).then(response => {{
                const clone = response.clone();
                caches.open('{cache}').then(c => c.put(event.request, clone));
                return response;
            }}))"""
        elif strategy == "network_first":
            return f"""fetch(event.request)
            .then(response => {{
                const clone = response.clone();
                caches.open('{cache}').then(c => c.put(event.request, clone));
                return response;
            }})
            .catch(() => caches.match(event.request))"""
        elif strategy == "stale_while_revalidate":
            return f"""caches.match(event.request).then(cached => {{
                const fetchPromise = fetch(event.request).then(response => {{
                    const clone = response.clone();
                    caches.open('{cache}').then(c => c.put(event.request, clone));
                    return response;
                }});
                return cached || fetchPromise;
            }})"""
        return "fetch(event.request)"

    def save(self, path: str = "sw.js"):
        """Save service worker to file."""
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.generate_js())

    def render_script_tag(self) -> str:
        """Render script tag to register service worker."""
        return """<script>
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js')
        .then(reg => console.log('[PyVibe] SW registered:', reg.scope))
        .catch(err => console.error('[PyVibe] SW registration failed:', err));
}
</script>"""


# ==================== Offline Page ====================

class OfflinePage:
    """
    Generate offline fallback page.

    Usage:
        offline = OfflinePage(title="Offline", message="No internet connection")
        offline.save("offline.html")
    """

    def __init__(self, title: str = "Offline",
                 message: str = "Tidak ada koneksi internet.",
                 theme_color: str = "#7C3AED"):
        self.title = title
        self.message = message
        self.theme_color = theme_color

    def generate_html(self) -> str:
        """Generate offline page HTML."""
        return f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #F9FAFB;
            color: #1F2937;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 24px;
        }}
        .offline-container {{
            text-align: center;
            max-width: 400px;
        }}
        .offline-icon {{
            font-size: 64px;
            margin-bottom: 16px;
        }}
        h1 {{
            font-size: 24px;
            margin-bottom: 8px;
            color: {self.theme_color};
        }}
        p {{
            color: #6B7280;
            margin-bottom: 24px;
            line-height: 1.6;
        }}
        .retry-btn {{
            background: {self.theme_color};
            color: white;
            border: none;
            padding: 12px 32px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: opacity 0.2s;
        }}
        .retry-btn:hover {{ opacity: 0.9; }}
    </style>
</head>
<body>
    <div class="offline-container">
        <div class="offline-icon">📡</div>
        <h1>{self.title}</h1>
        <p>{self.message}</p>
        <button class="retry-btn" onclick="location.reload()">
            🔄 Coba Lagi
        </button>
    </div>
</body>
</html>"""

    def save(self, path: str = "offline.html"):
        """Save offline page to file."""
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.generate_html())


# ==================== PWA Builder ====================

class PWABuilder:
    """
    All-in-one PWA setup.

    Usage:
        pwa = PWABuilder(
            name="My App",
            short_name="MyApp",
            theme_color="#7C3AED",
        )
        pwa.setup("dist/")
    """

    def __init__(self, name: str = "PyVibe App",
                 short_name: str = "PyVibe",
                 theme_color: str = "#7C3AED",
                 **kwargs):
        self.manifest = PWAManifest(
            name=name, short_name=short_name,
            theme_color=theme_color, **kwargs,
        )
        self.sw = ServiceWorker()
        self.offline = OfflinePage(
            title=f"{name} — Offline",
            theme_color=theme_color,
        )

    def setup(self, output_dir: str = "dist") -> Dict[str, str]:
        """Generate all PWA files."""
        os.makedirs(output_dir, exist_ok=True)
        files = {}

        # Manifest
        manifest_path = os.path.join(output_dir, "manifest.json")
        self.manifest.save(manifest_path)
        files["manifest"] = manifest_path

        # Service Worker
        sw_path = os.path.join(output_dir, "sw.js")
        self.sw.save(sw_path)
        files["service_worker"] = sw_path

        # Offline page
        offline_path = os.path.join(output_dir, "offline.html")
        self.offline.save(offline_path)
        files["offline"] = offline_path

        return files

    def get_html_tags(self) -> str:
        """Get all HTML tags needed for PWA."""
        return (
            self.manifest.render_link() + "\n" +
            self.manifest.render_meta_tags() + "\n" +
            self.sw.render_script_tag()
        )
