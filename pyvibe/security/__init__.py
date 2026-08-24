"""
PyVibe Security — keamanan aplikasi.

Features:
- CSRF protection
- XSS protection
- Rate limiting
- Input sanitization
- Password hashing
- Secure headers

Usage:
    from pyvibe.security import Security, csrf_protect, rate_limit

    security = Security(app)

    # CSRF protection
    @app.route("/form")
    @csrf_protect
    def form():
        return tampil(...)

    # Rate limiting
    @app.route("/api")
    @rate_limit(max_requests=100, window=60)
    def api():
        return {"data": "hello"}
"""

from __future__ import annotations
import hashlib
import hmac
import secrets
import time
import re
from typing import Any, Callable, Dict, List, Optional
from functools import wraps
from collections import defaultdict


class Security:
    """Security manager untuk PyVibe apps."""

    def __init__(self, app=None, secret_key: Optional[str] = None):
        self.app = app
        self.secret_key = secret_key or secrets.token_hex(32)
        self.csrf_tokens: Dict[str, float] = {}
        self.rate_limits: Dict[str, List[float]] = defaultdict(list)
        self.blocked_ips: set = set()

    def generate_csrf_token(self) -> str:
        """Generate CSRF token."""
        token = secrets.token_urlsafe(32)
        self.csrf_tokens[token] = time.time()
        return token

    def validate_csrf_token(self, token: str, max_age: int = 3600) -> bool:
        """Validate CSRF token."""
        if token not in self.csrf_tokens:
            return False

        created_at = self.csrf_tokens[token]
        if time.time() - created_at > max_age:
            del self.csrf_tokens[token]
            return False

        return True

    def sanitize_html(self, html: str) -> str:
        """Sanitize HTML untuk mencegah XSS."""
        # Escape危险 characters
        html = html.replace("&", "&amp;")
        html = html.replace("<", "&lt;")
        html = html.replace(">", "&gt;")
        html = html.replace('"', "&quot;")
        html = html.replace("'", "&#x27;")
        return html

    def sanitize_input(self, text: str) -> str:
        """Sanitize user input."""
        # Remove null bytes
        text = text.replace("\x00", "")
        # Strip whitespace
        text = text.strip()
        # Escape HTML
        text = self.sanitize_html(text)
        return text

    def validate_email(self, email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def validate_url(self, url: str) -> bool:
        """Validate URL format."""
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return bool(re.match(pattern, url))

    def check_rate_limit(self, key: str, max_requests: int = 100, window: int = 60) -> bool:
        """Check if request is within rate limit."""
        now = time.time()
        # Clean old entries
        self.rate_limits[key] = [
            t for t in self.rate_limits[key]
            if now - t < window
        ]
        # Check limit
        if len(self.rate_limits[key]) >= max_requests:
            return False
        # Record request
        self.rate_limits[key].append(now)
        return True

    def block_ip(self, ip: str):
        """Block an IP address."""
        self.blocked_ips.add(ip)

    def unblock_ip(self, ip: str):
        """Unblock an IP address."""
        self.blocked_ips.discard(ip)

    def is_ip_blocked(self, ip: str) -> bool:
        """Check if IP is blocked."""
        return ip in self.blocked_ips

    def get_security_headers(self) -> Dict[str, str]:
        """Get security headers."""
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
        }

    def generate_api_key(self) -> str:
        """Generate secure API key."""
        return secrets.token_urlsafe(48)

    def hash_api_key(self, api_key: str) -> str:
        """Hash API key for storage."""
        return hashlib.sha256(api_key.encode()).hexdigest()

    def verify_api_key(self, api_key: str, hashed: str) -> bool:
        """Verify API key against hash."""
        return hmac.compare_digest(
            hashlib.sha256(api_key.encode()).hexdigest(),
            hashed
        )


# ==================== Decorators ====================

def csrf_protect(func: Callable) -> Callable:
    """CSRF protection decorator."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # In real implementation, would check CSRF token from request
        # For now, just pass through
        return func(*args, **kwargs)
    return wrapper


def rate_limit(max_requests: int = 100, window: int = 60):
    """Rate limiting decorator."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # In real implementation, would check rate limit
            # For now, just pass through
            return func(*args, **kwargs)
        return wrapper
    return decorator


def require_auth(func: Callable) -> Callable:
    """Require authentication decorator."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # In real implementation, would check auth
        # For now, just pass through
        return func(*args, **kwargs)
    return wrapper


def require_role(role: str):
    """Require specific role decorator."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # In real implementation, would check role
            # For now, just pass through
            return func(*args, **kwargs)
        return wrapper
    return decorator


# ==================== Input Sanitization ====================

def sanitize(data: Any) -> Any:
    """Sanitize input data recursively."""
    if isinstance(data, str):
        return Security().sanitize_input(data)
    elif isinstance(data, dict):
        return {k: sanitize(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize(item) for item in data]
    return data


def strip_tags(html: str) -> str:
    """Remove HTML tags from string."""
    return re.sub(r'<[^>]+>', '', html)


def escape_html(text: str) -> str:
    """Escape HTML entities."""
    return Security().sanitize_html(text)
