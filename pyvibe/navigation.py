"""
PyVibe Navigation — router guards, params, navigation, and SEO helpers.

Usage:
    from pyvibe.navigation import Router, Guard, SEO, use_router, use_params

    # Router with guards
    router = Router()
    router.before_each(lambda to, from_: to["path"] != "/admin" or is_logged_in())
    
    # SEO
    seo = SEO(title="My Page", description="Desc", image="og.png")
    meta_tags = seo.render()
"""

from __future__ import annotations
import re
import json
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from urllib.parse import urlencode, parse_qs, urlparse


# ==================== Router Guards ====================

@dataclass
class RouteMeta:
    """Route metadata."""
    title: str = ""
    description: str = ""
    requires_auth: bool = False
    requires_role: Optional[str] = None
    layout: Optional[str] = None
    transition: str = "fade"
    props: Dict[str, Any] = field(default_factory=dict)
    middleware: List[str] = field(default_factory=list)


@dataclass
class NavigationGuard:
    """Navigation guard."""
    name: str
    handler: Callable
    redirect: Optional[str] = None


class Router:
    """
    Enhanced router with guards and middleware.
    
    Usage:
        router = Router()
        
        # Route guards
        @router.before_each
        def check_auth(to, from_):
            if to.meta.requires_auth and not is_logged_in():
                return "/login"
        
        @router.after_each
        def log_navigation(to, from_):
            print(f"Navigated to {to.path}")
    """

    def __init__(self):
        self.routes: Dict[str, Dict] = {}
        self.current_route: Optional[Dict] = None
        self.before_guards: List[Callable] = []
        self.after_guards: List[Callable] = []
        self._history: List[Dict] = []
        self._params: Dict[str, Any] = {}
        self._query: Dict[str, Any] = {}

    def add_route(self, path: str, handler: Callable, meta: Optional[RouteMeta] = None, **kwargs):
        """Add a route."""
        self.routes[path] = {
            "path": path,
            "handler": handler,
            "meta": meta or RouteMeta(),
            **kwargs,
        }

    def before_each(self, func: Callable):
        """Register before navigation guard."""
        self.before_guards.append(func)
        return func

    def after_each(self, func: Callable):
        """Register after navigation guard."""
        self.after_guards.append(func)
        return func

    def navigate(self, path: str, params: Optional[Dict] = None, query: Optional[Dict] = None) -> Dict:
        """
        Navigate to a path.
        
        Returns navigation result with status.
        """
        from_path = self.current_route["path"] if self.current_route else "/"
        to_route = self._match_route(path)
        
        if not to_route:
            return {"status": "error", "message": f"Route not found: {path}"}

        # Run before guards
        for guard in self.before_guards:
            result = guard(to_route, {"path": from_path})
            if result and isinstance(result, str):
                # Redirect
                return self.navigate(result, params, query)
            elif result is False:
                return {"status": "blocked", "message": "Navigation blocked by guard"}

        # Update route
        self._history.append(self.current_route or {"path": "/"})
        self.current_route = to_route
        self._params = params or {}
        self._query = query or {}

        # Run after guards
        for guard in self.after_guards:
            guard(to_route, {"path": from_path})

        return {"status": "ok", "path": path}

    def _match_route(self, path: str) -> Optional[Dict]:
        """Match path to registered route."""
        # Exact match
        if path in self.routes:
            return self.routes[path]
        
        # Pattern match (e.g., /users/:id)
        for route_path, route in self.routes.items():
            pattern = re.sub(r':(\w+)', r'(?P<\1>[^/]+)', route_path)
            match = re.match(f'^{pattern}$', path)
            if match:
                route["params"] = match.groupdict()
                return route
        
        return None

    def back(self) -> Dict:
        """Navigate back."""
        if self._history:
            prev = self._history.pop()
            self.current_route = prev
            return {"status": "ok", "path": prev["path"]}
        return {"status": "error", "message": "No history"}

    def get_params(self) -> Dict[str, Any]:
        """Get current route params."""
        return self._params

    def get_query(self) -> Dict[str, Any]:
        """Get current query params."""
        return self._query

    def generate_nav_code(self, path: str, text: str = "") -> str:
        """Generate JavaScript navigation code."""
        return f"window.location.href='{path}'"


# ==================== Params & Query Helpers ====================

def use_params(path_pattern: str, actual_path: str) -> Dict[str, str]:
    """
    Extract params from URL pattern.
    
    Usage:
        params = use_params("/users/:id/posts/:post_id", "/users/123/posts/456")
        # {"id": "123", "post_id": "456"}
    """
    pattern = re.sub(r':(\w+)', r'(?P<\1>[^/]+)', path_pattern)
    match = re.match(f'^{pattern}$', actual_path)
    return match.groupdict() if match else {}


def use_query(url: str) -> Dict[str, List[str]]:
    """
    Parse query string from URL.
    
    Usage:
        query = use_query("/search?q=python&page=2")
        # {"q": ["python"], "page": ["2"]}
    """
    parsed = urlparse(url)
    return parse_qs(parsed.query)


def build_url(base: str, params: Optional[Dict] = None, query: Optional[Dict] = None) -> str:
    """Build URL with params and query."""
    url = base
    if params:
        for key, value in params.items():
            url = url.replace(f":{key}", str(value))
    if query:
        url += "?" + urlencode(query)
    return url


# ==================== Navigation Helpers ====================

def redirect(url: str) -> str:
    """Generate redirect HTML/JS."""
    return f'<script>window.location.href="{url}"</script>'


def redirect_meta(url: str) -> str:
    """Generate meta redirect."""
    return f'<meta http-equiv="refresh" content="0;url={url}">'


def preload(url: str) -> str:
    """Generate preload link."""
    return f'<link rel="preload" href="{url}" as="document">'


# ==================== SEO Helpers ====================

class SEO:
    """
    SEO helper for meta tags and structured data.
    
    Usage:
        seo = SEO(
            title="My Page | MySite",
            description="Description here",
            image="https://example.com/og.png",
            url="https://example.com/page",
        )
        html = seo.render()
    """

    def __init__(
        self,
        title: str = "",
        description: str = "",
        image: str = "",
        url: str = "",
        type: str = "website",
        site_name: str = "",
        locale: str = "id_ID",
        keywords: Optional[List[str]] = None,
        author: str = "",
        robots: str = "index, follow",
        canonical: str = "",
        structured_data: Optional[Dict] = None,
    ):
        self.title = title
        self.description = description
        self.image = image
        self.url = url
        self.type = type
        self.site_name = site_name
        self.locale = locale
        self.keywords = keywords or []
        self.author = author
        self.robots = robots
        self.canonical = canonical
        self.structured_data = structured_data

    def render(self) -> str:
        """Render SEO meta tags."""
        tags = []

        # Basic meta
        if self.title:
            tags.append(f'<title>{self._escape(self.title)}</title>')
            tags.append(f'<meta property="og:title" content="{self._escape(self.title)}">')
            tags.append(f'<meta name="twitter:title" content="{self._escape(self.title)}">')

        if self.description:
            tags.append(f'<meta name="description" content="{self._escape(self.description)}">')
            tags.append(f'<meta property="og:description" content="{self._escape(self.description)}">')
            tags.append(f'<meta name="twitter:description" content="{self._escape(self.description)}">')

        if self.image:
            tags.append(f'<meta property="og:image" content="{self._escape(self.image)}">')
            tags.append(f'<meta name="twitter:image" content="{self._escape(self.image)}">')
            tags.append(f'<meta name="twitter:card" content="summary_large_image">')

        if self.url:
            tags.append(f'<meta property="og:url" content="{self._escape(self.url)}">')

        # OG tags
        tags.append(f'<meta property="og:type" content="{self.type}">')
        if self.site_name:
            tags.append(f'<meta property="og:site_name" content="{self._escape(self.site_name)}">')
        tags.append(f'<meta property="og:locale" content="{self.locale}">')

        # Twitter
        tags.append(f'<meta name="twitter:card" content="summary_large_image">')

        # Other
        if self.keywords:
            tags.append(f'<meta name="keywords" content="{self._escape(", ".join(self.keywords))}">')
        if self.author:
            tags.append(f'<meta name="author" content="{self._escape(self.author)}">')
        tags.append(f'<meta name="robots" content="{self.robots}">')
        if self.canonical:
            tags.append(f'<link rel="canonical" href="{self._escape(self.canonical)}">')

        # Structured data
        if self.structured_data:
            ld_json = json.dumps(self.structured_data, indent=2)
            tags.append(f'<script type="application/ld+json">{ld_json}</script>')

        return "\n".join(tags)

    def render_og(self) -> str:
        """Render only OG tags."""
        tags = []
        if self.title:
            tags.append(f'<meta property="og:title" content="{self._escape(self.title)}">')
        if self.description:
            tags.append(f'<meta property="og:description" content="{self._escape(self.description)}">')
        if self.image:
            tags.append(f'<meta property="og:image" content="{self._escape(self.image)}">')
        if self.url:
            tags.append(f'<meta property="og:url" content="{self._escape(self.url)}">')
        tags.append(f'<meta property="og:type" content="{self.type}">')
        return "\n".join(tags)

    @staticmethod
    def _escape(text: str) -> str:
        """Escape HTML."""
        return text.replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')


# ==================== Sitemap Generator ====================

class SitemapGenerator:
    """
    Generate sitemap.xml.
    
    Usage:
        sitemap = SitemapGenerator("https://example.com")
        sitemap.add("/", priority=1.0, changefreq="daily")
        sitemap.add("/about", priority=0.8)
        xml = sitemap.render()
    """

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.urls: List[Dict] = []

    def add(self, path: str, priority: float = 0.5, changefreq: str = "monthly", lastmod: str = ""):
        """Add URL to sitemap."""
        self.urls.append({
            "url": f"{self.base_url}{path}",
            "priority": priority,
            "changefreq": changefreq,
            "lastmod": lastmod,
        })

    def render(self) -> str:
        """Render sitemap XML."""
        lines = ['<?xml version="1.0" encoding="UTF-8"?>']
        lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
        for url in self.urls:
            lines.append("  <url>")
            lines.append(f"    <loc>{url['url']}</loc>")
            if url.get("lastmod"):
                lines.append(f"    <lastmod>{url['lastmod']}</lastmod>")
            lines.append(f"    <changefreq>{url['changefreq']}</changefreq>")
            lines.append(f"    <priority>{url['priority']}</priority>")
            lines.append("  </url>")
        lines.append("</urlset>")
        return "\n".join(lines)

    def save(self, filepath: str = "sitemap.xml"):
        """Save sitemap to file."""
        with open(filepath, "w") as f:
            f.write(self.render())


# ==================== Robots.txt Generator ====================

class RobotsGenerator:
    """Generate robots.txt."""

    def __init__(self, sitemap_url: str = ""):
        self.rules: List[Dict] = []
        self.sitemap_url = sitemap_url

    def allow(self, path: str = "/", user_agent: str = "*"):
        """Add allow rule."""
        self.rules.append({"user_agent": user_agent, "path": path, "allow": True})

    def disallow(self, path: str, user_agent: str = "*"):
        """Add disallow rule."""
        self.rules.append({"user_agent": user_agent, "path": path, "allow": False})

    def render(self) -> str:
        """Render robots.txt."""
        lines = []
        for rule in self.rules:
            lines.append(f"User-agent: {rule['user_agent']}")
            if rule["allow"]:
                lines.append(f"Allow: {rule['path']}")
            else:
                lines.append(f"Disallow: {rule['path']}")
            lines.append("")
        if self.sitemap_url:
            lines.append(f"Sitemap: {self.sitemap_url}")
        return "\n".join(lines)
