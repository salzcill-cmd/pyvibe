"""
PyVibe Core Tests
Tests untuk core framework components.
"""
import pytest
from pyvibe import *
from pyvibe.core.app import App
from pyvibe.core.state import State
from pyvibe.core.component import Component


class TestApp:
    """Tests untuk App class."""
    
    def test_create_app(self):
        app = App("Test App")
        assert app.name == "Test App"
    
    def test_app_with_theme(self):
        app = App("Test", theme="gelap")
        assert app.config["theme"] == "gelap"
    
    def test_app_routes(self):
        app = App("Test")
        
        @app.route("/")
        def home():
            return tampil(judul("Home"))
        
        assert "/" in app.routes
    
    def test_app_render(self):
        app = App("Test")
        html = app.tampil(judul("Hello"))
        assert len(html) > 0


class TestState:
    """Tests untuk State class."""
    
    def test_create_state(self):
        state = State(count=0, name="Test")
        assert state.count == 0
        assert state.name == "Test"
    
    def test_update_state(self):
        state = State(count=0)
        state.count = 1
        assert state.count == 1


class TestComponents:
    """Tests untuk basic components."""
    
    def test_judul(self):
        comp = judul("Test")
        assert comp is not None
        assert comp.content == "Test"
    
    def test_paragraf(self):
        comp = paragraf("Test text")
        assert comp is not None
        assert comp.content == "Test text"
    
    def test_tombol(self):
        comp = tombol("Click me")
        assert comp is not None
    
    def test_kartu(self):
        comp = kartu(paragraf("Card content"))
        assert comp is not None
    
    def test_grid(self):
        comp = grid(
            kartu(paragraf("1")),
            kartu(paragraf("2")),
            kartu(paragraf("3")),
            kolom=3,
        )
        assert comp is not None
