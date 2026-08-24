"""
PyVibe Fetch — data fetching utilities.

Usage:
    from pyvibe.fetch import Fetch, api_get, api_post

    # Simple fetch
    data = await api_get("https://api.example.com/users")

    # With options
    fetch = Fetch("https://api.example.com")
    data = await fetch.get("/users")
    result = await fetch.post("/users", json={"name": "Andi"})
"""

from __future__ import annotations
from typing import Any, Dict, Optional
import json


class Fetch:
    """
    HTTP fetch client.

    Usage:
        client = Fetch("https://api.example.com")
        users = await client.get("/users")
        user = await client.post("/users", json={"name": "Andi"})
    """

    def __init__(self, base_url: str = "", headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.token: Optional[str] = None

    def set_token(self, token: str):
        """Set authorization token."""
        self.token = token
        self.headers["Authorization"] = f"Bearer {token}"

    def _build_url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _build_headers(self) -> Dict[str, str]:
        headers = {**self.headers}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def get(self, path: str, **kwargs) -> str:
        """Generate JavaScript fetch GET code."""
        url = self._build_url(path)
        return f"""fetch('{url}', {{
    method: 'GET',
    headers: {json.dumps(self._build_headers())}
}}).then(r => r.json())"""

    def post(self, path: str, data: Optional[Dict] = None, **kwargs) -> str:
        """Generate JavaScript fetch POST code."""
        url = self._build_url(path)
        body = json.dumps(data) if data else "null"
        return f"""fetch('{url}', {{
    method: 'POST',
    headers: {{
        ...{json.dumps(self._build_headers())},
        'Content-Type': 'application/json'
    }},
    body: JSON.stringify({body})
}}).then(r => r.json())"""

    def put(self, path: str, data: Optional[Dict] = None, **kwargs) -> str:
        """Generate JavaScript fetch PUT code."""
        url = self._build_url(path)
        body = json.dumps(data) if data else "null"
        return f"""fetch('{url}', {{
    method: 'PUT',
    headers: {{
        ...{json.dumps(self._build_headers())},
        'Content-Type': 'application/json'
    }},
    body: JSON.stringify({body})
}}).then(r => r.json())"""

    def delete(self, path: str, **kwargs) -> str:
        """Generate JavaScript fetch DELETE code."""
        url = self._build_url(path)
        return f"""fetch('{url}', {{
    method: 'DELETE',
    headers: {json.dumps(self._build_headers())}
}}).then(r => r.json())"""


def api_get(url: str, headers: Optional[Dict[str, str]] = None) -> str:
    """Generate JavaScript fetch GET code."""
    return f"""fetch('{url}', {{
    method: 'GET',
    headers: {json.dumps(headers or {})}
}}).then(r => r.json())"""


def api_post(url: str, data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None) -> str:
    """Generate JavaScript fetch POST code."""
    body = json.dumps(data) if data else "null"
    return f"""fetch('{url}', {{
    method: 'POST',
    headers: {{
        ...{json.dumps(headers or {})},
        'Content-Type': 'application/json'
    }},
    body: JSON.stringify({body})
}}).then(r => r.json())"""


def api_put(url: str, data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None) -> str:
    """Generate JavaScript fetch PUT code."""
    body = json.dumps(data) if data else "null"
    return f"""fetch('{url}', {{
    method: 'PUT',
    headers: {{
        ...{json.dumps(headers or {})},
        'Content-Type': 'application/json'
    }},
    body: JSON.stringify({body})
}}).then(r => r.json())"""


def api_delete(url: str, headers: Optional[Dict[str, str]] = None) -> str:
    """Generate JavaScript fetch DELETE code."""
    return f"""fetch('{url}', {{
    method: 'DELETE',
    headers: {json.dumps(headers or {})}
}}).then(r => r.json())"""
