"""
PyVibe Testing — testing utilities.

Usage:
    from pyvibe.testing import TestCase, Client

    class TestApp(TestCase):
        def setup(self):
            self.app = App("Test")
            self.client = Client(self.app)

        def test_home(self):
            response = self.client.get("/")
            self.assert_status(response, 200)
            self.assert_contains(response, "Halo")

        def test_components(self):
            html = self.client.render(judul("Hello"))
            self.assert_contains(html, "<h1")
"""

from __future__ import annotations
import json
from typing import Any, Dict, List, Optional, Union
from pyvibe.core.app import App
from pyvibe.core.component import Component
from pyvibe.core.renderer import tampil


class Client:
    """Test client untuk PyVibe apps."""

    def __init__(self, app: App):
        self.app = app

    def get(self, path: str) -> Dict[str, Any]:
        """Simulate GET request."""
        route = self.app.get_route(path)
        if route:
            try:
                result = route.handler()
                if isinstance(result, list):
                    html = self.app.tampil(*result)
                elif isinstance(result, Component):
                    html = result.render()
                else:
                    html = str(result)
                return {"status": 200, "body": html, "headers": {}}
            except Exception as e:
                return {"status": 500, "body": str(e), "headers": {}}
        return {"status": 404, "body": "Not Found", "headers": {}}

    def post(self, path: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Simulate POST request."""
        return self.get(path)  # Simplified

    def render(self, *components: Union[Component, str]) -> str:
        """Render components to HTML."""
        return self.app.tampil(*components)

    def render_page(self, *components: Union[Component, str]) -> str:
        """Render full page."""
        return self.app.render_page(*components)


class TestCase:
    """
    Base test case untuk PyVibe apps.

    Usage:
        class TestApp(TestCase):
            def setup(self):
                self.app = App("Test")
                self.client = Client(self.app)

            def test_home(self):
                response = self.client.get("/")
                self.assert_status(response, 200)
    """

    def setup(self):
        """Setup test."""
        pass

    def teardown(self):
        """Teardown test."""
        pass

    def assert_status(self, response: Dict, status: int):
        """Assert response status."""
        assert response["status"] == status, f"Expected status {status}, got {response['status']}"

    def assert_contains(self, response: Union[Dict, str], text: str):
        """Assert response contains text."""
        body = response["body"] if isinstance(response, dict) else response
        assert text in body, f"Expected '{text}' in response"

    def assert_not_contains(self, response: Union[Dict, str], text: str):
        """Assert response does not contain text."""
        body = response["body"] if isinstance(response, dict) else response
        assert text not in body, f"Unexpected '{text}' in response"

    def assert_json(self, response: Dict, data: Any):
        """Assert response JSON."""
        body = response["body"] if isinstance(response, dict) else response
        if isinstance(body, str):
            body = json.loads(body)
        assert body == data, f"Expected {data}, got {body}"

    def assert_true(self, condition: bool, message: str = ""):
        """Assert condition is true."""
        assert condition, message or "Expected True"

    def assert_false(self, condition: bool, message: str = ""):
        """Assert condition is false."""
        assert not condition, message or "Expected False"

    def assert_equal(self, first: Any, second: Any, message: str = ""):
        """Assert equality."""
        assert first == second, message or f"Expected {second}, got {first}"

    def assert_not_equal(self, first: Any, second: Any, message: str = ""):
        """Assert inequality."""
        assert first != second, message or f"Expected not {second}"


# ==================== Component Tests ====================

def test_components():
    """Test semua components."""
    from pyvibe.components.basic import judul, paragraf, badge
    from pyvibe.components.input import tombol
    from pyvibe.components.layout import kartu, grid, baris
    from pyvibe.components.navigation import navbar, footer
    from pyvibe.components.feedback import alert, loader
    from pyvibe.components.data import tabel
    from pyvibe.components.advanced import modal, accordion

    print("Testing components...")

    # Basic
    assert judul("Hello").tag == "h1"
    assert paragraf("Hello").tag == "p"
    assert tombol("Click").tag == "button"
    assert badge("NEW").tag == "span"

    # Layout
    assert kartu().tag == "div"
    assert grid().tag == "div"
    assert baris().tag == "div"

    # Navigation
    assert navbar().tag == "nav"
    assert footer().tag == "footer"

    # Feedback
    assert alert("Info").tag == "div"
    assert loader().tag == "div"

    # Data
    assert tabel(data=[{"a": 1}]).tag == "div"

    # Advanced
    assert modal("Title").tag == "div"
    assert accordion(("Q", paragraf("A"))).tag == "div"

    print("✅ All component tests passed!")


if __name__ == "__main__":
    test_components()
