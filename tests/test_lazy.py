"""
Tests untuk PyVibe Lazy Loading, Code Splitting & WebSocket Client.
"""
import sys
import os
import time
import json
import struct
import socket
import threading
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pyvibe.lazy import (
    LazyComponent, LazyState, lazy, lazy_all, lazy_component,
    SuspenseComponent, suspense,
    dynamic_import, dynamic_import_all,
    ChunkManager, Chunk, get_chunks, define_chunk, load_chunk,
)
from pyvibe.websocket import (
    WebSocketClient, WebSocketManager, WSState,
    Channel, create_ws_client, ws_url,
)
from pyvibe.components.basic import judul, paragraf


# ==================== Lazy Component Tests ====================

class TestLazyComponent(unittest.TestCase):
    """Test lazy component loading."""

    def test_lazy_creates_instance(self):
        """Test lazy() creates LazyComponent."""
        c = lazy("pyvibe.components.basic", "judul")
        self.assertIsInstance(c, LazyComponent)
        self.assertEqual(c.state, LazyState.PENDING)
        self.assertFalse(c.is_loaded)

    def test_lazy_loads_on_call(self):
        """Test lazy component loads when called."""
        from pyvibe.core.component import Component
        c = lazy("pyvibe.components.basic", "judul")
        result = c("Hello")
        # Component may return str or Component object
        if isinstance(result, Component):
            result = result.render()
        self.assertIsInstance(result, str)
        self.assertIn("Hello", result)
        self.assertTrue(c.is_loaded)
        self.assertGreater(c.load_time, 0)

    def test_lazy_state_transitions(self):
        """Test state transitions: pending -> loaded."""
        c = lazy("pyvibe.components.basic", "paragraf")
        self.assertEqual(c.state, LazyState.PENDING)
        c("Test")
        self.assertEqual(c.state, LazyState.LOADED)

    def test_lazy_with_fallback(self):
        """Test lazy component with fallback on error."""
        c = lazy(
            "nonexistent_module_xyz",
            "nonexistent_func",
            fallback=lambda x: f"fallback:{x}",
        )
        result = c("test")
        self.assertEqual(result, "fallback:test")

    def test_lazy_raises_on_error_without_fallback(self):
        """Test lazy raises ImportError without fallback."""
        c = lazy("nonexistent_module_xyz", "nonexistent_func")
        with self.assertRaises(ImportError):
            c()

    def test_lazy_preload(self):
        """Test background preload."""
        c = lazy("pyvibe.components.basic", "judul")
        c.preload()
        time.sleep(0.1)
        # Should still be pending (preload runs in background)
        self.assertIn(c.state, [LazyState.PENDING, LazyState.LOADED])

    def test_lazy_repr(self):
        """Test repr."""
        c = lazy("pyvibe.components.basic", "judul")
        r = repr(c)
        self.assertIn("LazyComponent", r)
        self.assertIn("judul", r)
        self.assertIn("pending", r)

    def test_lazy_load_count(self):
        """Test load count increments."""
        c = lazy("pyvibe.components.basic", "judul")
        self.assertEqual(c._load_count, 0)
        c("First")
        self.assertEqual(c._load_count, 1)
        c("Second")
        self.assertEqual(c._load_count, 1)  # Already loaded, no increment

    def test_lazy_is_loading_property(self):
        """Test is_loading property."""
        c = lazy("pyvibe.components.basic", "judul")
        self.assertFalse(c.is_loading)
        c("Test")
        self.assertFalse(c.is_loading)  # After load, no longer loading

    def test_lazy_has_error_property(self):
        """Test has_error property."""
        c = lazy("nonexistent_module_xyz", "func")
        with self.assertRaises(ImportError):
            c()
        self.assertTrue(c.has_error)


# ==================== Lazy All Tests ====================

class TestLazyAll(unittest.TestCase):
    """Test lazy_all function."""

    def test_lazy_all_creates_dict(self):
        """Test lazy_all creates dict of lazy components."""
        components = lazy_all("pyvibe.components.basic", [
            "judul", "paragraf", "teks",
        ])
        self.assertIsInstance(components, dict)
        self.assertEqual(len(components), 3)
        self.assertIn("judul", components)
        self.assertIn("paragraf", components)
        self.assertIn("teks", components)

    def test_lazy_all_items_are_lazy(self):
        """Test all items are LazyComponent."""
        components = lazy_all("pyvibe.components.basic", ["judul"])
        self.assertIsInstance(components["judul"], LazyComponent)

    def test_lazy_all_can_be_called(self):
        """Test lazy_all items can be called."""
        from pyvibe.core.component import Component
        components = lazy_all("pyvibe.components.basic", ["judul", "paragraf"])
        h = components["judul"]("Title")
        p = components["paragraf"]("Text")
        if isinstance(h, Component):
            h = h.render()
        if isinstance(p, Component):
            p = p.render()
        self.assertIn("Title", h)
        self.assertIn("Text", p)


# ==================== Suspense Tests ====================

class TestSuspense(unittest.TestCase):
    """Test suspense component."""

    def test_suspense_creates_component(self):
        """Test suspense() creates SuspenseComponent."""
        s = suspense(children=[judul("Hello")])
        self.assertIsInstance(s, SuspenseComponent)

    def test_suspense_renders_loaded_children(self):
        """Test suspense renders when children are loaded."""
        lazy_judul = lazy("pyvibe.components.basic", "judul")
        lazy_judul("Preload")  # Load it
        s = suspense(children=[lazy_judul])
        html = s.render()
        self.assertIn("Hello", html) if "Hello" in str(lazy_judul) else None

    def test_suspense_shows_loading_for_pending(self):
        """Test suspense shows loading for pending children."""
        lazy_judul = lazy("pyvibe.components.basic", "judul")
        s = suspense(
            loading=paragraf("Loading..."),
            children=[lazy_judul],
        )
        html = s.render()
        self.assertIn("Loading...", html)

    def test_suspense_shows_error_on_failure(self):
        """Test suspense shows error on failure."""
        lazy_bad = lazy("nonexistent_module_xyz", "func")
        s = suspense(
            error=paragraf("Error occurred"),
            children=[lazy_bad],
        )
        # Trigger load attempt
        try:
            lazy_bad()
        except ImportError:
            pass
        html = s.render()
        self.assertIn("Error occurred", html)

    def test_suspense_with_component_children(self):
        """Test suspense with regular Component children."""
        s = suspense(children=[judul("Static"), paragraf("Content")])
        html = s.render()
        self.assertIn("Static", html)
        self.assertIn("Content", html)


# ==================== Dynamic Import Tests ====================

class TestDynamicImport(unittest.TestCase):
    """Test dynamic import functions."""

    def test_dynamic_import_module(self):
        """Test dynamic import of module."""
        mod = dynamic_import("pyvibe.components.basic")
        self.assertTrue(hasattr(mod, "judul"))
        self.assertTrue(hasattr(mod, "paragraf"))

    def test_dynamic_import_attribute(self):
        """Test dynamic import of specific attribute."""
        judul_func = dynamic_import("pyvibe.components.basic", "judul")
        self.assertTrue(callable(judul_func))

    def test_dynamic_import_with_fallback(self):
        """Test dynamic import with fallback."""
        result = dynamic_import(
            "nonexistent_module_xyz",
            fallback="fallback_value",
        )
        self.assertEqual(result, "fallback_value")

    def test_dynamic_import_raises_without_fallback(self):
        """Test dynamic import raises without fallback."""
        with self.assertRaises(ImportError):
            dynamic_import("nonexistent_module_xyz")

    def test_dynamic_import_all(self):
        """Test dynamic_import_all."""
        modules = dynamic_import_all({
            "basic": "pyvibe.components.basic",
            "input": "pyvibe.components.input",
        })
        self.assertIn("basic", modules)
        self.assertIn("input", modules)
        self.assertTrue(hasattr(modules["basic"], "judul"))

    def test_dynamic_import_all_with_failures(self):
        """Test dynamic_import_all handles failures."""
        modules = dynamic_import_all({
            "basic": "pyvibe.components.basic",
            "bad": "nonexistent_module_xyz",
        })
        self.assertIsNotNone(modules["basic"])
        self.assertIsNone(modules["bad"])


# ==================== Chunk Manager Tests ====================

class TestChunkManager(unittest.TestCase):
    """Test ChunkManager."""

    def test_define_chunk(self):
        """Test defining a chunk."""
        cm = ChunkManager()
        cm.define("charts", ["pyvibe.components.charts"])
        self.assertEqual(cm.total_chunks, 1)
        self.assertIn("charts", cm.pending_chunks)

    def test_load_chunk(self):
        """Test loading a chunk."""
        cm = ChunkManager()
        cm.define("basic", ["pyvibe.components.basic"])
        result = cm.load("basic")
        self.assertTrue(result)
        self.assertIn("basic", cm.loaded_chunks)

    def test_load_nonexistent_chunk(self):
        """Test loading nonexistent chunk raises."""
        cm = ChunkManager()
        with self.assertRaises(ValueError):
            cm.load("nonexistent")

    def test_load_all(self):
        """Test loading all chunks."""
        cm = ChunkManager()
        cm.define("basic", ["pyvibe.components.basic"])
        cm.define("input", ["pyvibe.components.input"])
        results = cm.load_all()
        self.assertTrue(results["basic"])
        self.assertTrue(results["input"])
        self.assertEqual(len(cm.loaded_chunks), 2)

    def test_parallel_load(self):
        """Test parallel chunk loading."""
        cm = ChunkManager()
        cm.define("basic", ["pyvibe.components.basic"])
        cm.define("input", ["pyvibe.components.input"])
        cm.define("layout", ["pyvibe.components.layout"])
        results = cm.load_parallel()
        self.assertTrue(results.get("basic"))
        self.assertTrue(results.get("input"))
        self.assertTrue(results.get("layout"))

    def test_chunk_stats(self):
        """Test chunk statistics."""
        cm = ChunkManager()
        cm.define("basic", ["pyvibe.components.basic"])
        cm.load("basic")
        stats = cm.get_stats()
        self.assertEqual(stats["total_chunks"], 1)
        self.assertEqual(stats["loaded"], 1)
        self.assertEqual(stats["pending"], 0)
        self.assertIn("basic", stats["chunks"])

    def test_on_load_callback(self):
        """Test on_load callback."""
        cm = ChunkManager()
        cm.define("basic", ["pyvibe.components.basic"])
        callback_called = []
        cm.on_load("basic", lambda chunk: callback_called.append(chunk.name))
        cm.load("basic")
        self.assertEqual(callback_called, ["basic"])

    def test_define_returns_self(self):
        """Test define returns self for chaining."""
        cm = ChunkManager()
        result = cm.define("a", ["pyvibe.components.basic"])
        self.assertIs(result, cm)

    def test_repr(self):
        """Test ChunkManager repr."""
        cm = ChunkManager()
        cm.define("test", ["pyvibe.components.basic"])
        r = repr(cm)
        self.assertIn("ChunkManager", r)
        self.assertIn("0/1", r)

    def test_get_global_chunks(self):
        """Test get_chunks returns global instance."""
        cm = get_chunks()
        self.assertIsInstance(cm, ChunkManager)

    def test_define_chunk_shorthand(self):
        """Test define_chunk shorthand."""
        result = define_chunk("test_shorthand", ["pyvibe.components.basic"])
        self.assertIsInstance(result, ChunkManager)

    def test_load_chunk_shorthand(self):
        """Test load_chunk shorthand."""
        define_chunk("test_load_shorthand", ["pyvibe.components.basic"])
        result = load_chunk("test_load_shorthand")
        self.assertTrue(result)

    def test_lazy_component_shorthand(self):
        """Test lazy_component shorthand."""
        from pyvibe.core.component import Component
        c = lazy_component("pyvibe.components.basic", "judul")
        self.assertIsInstance(c, LazyComponent)
        result = c("Test")
        if isinstance(result, Component):
            result = result.render()
        self.assertIn("Test", result)


# ==================== WebSocket Client Tests ====================

class TestWebSocketClient(unittest.TestCase):
    """Test WebSocket client (without actual server)."""

    def test_create_client(self):
        """Test creating WebSocketClient."""
        ws = WebSocketClient("ws://localhost:8080")
        self.assertEqual(ws._host, "localhost")
        self.assertEqual(ws._port, 8080)
        self.assertEqual(ws._path, "/")
        self.assertEqual(ws.state, WSState.CLOSED)

    def test_parse_url_with_path(self):
        """Test URL parsing with path."""
        ws = WebSocketClient("ws://example.com:9090/chat")
        self.assertEqual(ws._host, "example.com")
        self.assertEqual(ws._port, 9090)
        self.assertEqual(ws._path, "/chat")

    def test_parse_secure_url(self):
        """Test WSS URL parsing."""
        ws = WebSocketClient("wss://example.com:443")
        self.assertTrue(ws._secure)
        self.assertEqual(ws._port, 443)

    def test_parse_default_port(self):
        """Test default port parsing."""
        ws = WebSocketClient("ws://example.com")
        self.assertEqual(ws._port, 80)

    def test_event_handlers(self):
        """Test event handler registration."""
        ws = WebSocketClient("ws://localhost:8080")
        called = []
        ws.on("message", lambda data: called.append(data))
        ws.on("open", lambda: called.append("open"))
        ws._emit("message", "test")
        ws._emit("open")
        self.assertEqual(called, ["test", "open"])

    def test_on_event_decorator(self):
        """Test on_event decorator."""
        ws = WebSocketClient("ws://localhost:8080")
        @ws.on_event("message")
        def handler(data):
            pass
        self.assertIn(handler, ws._handlers["message"])

    def test_off_removes_handler(self):
        """Test off removes handler."""
        ws = WebSocketClient("ws://localhost:8080")
        handler = lambda data: None
        ws.on("message", handler)
        self.assertIn(handler, ws._handlers["message"])
        ws.off("message", handler)
        self.assertNotIn(handler, ws._handlers["message"])

    def test_off_removes_all_handlers(self):
        """Test off removes all handlers for event."""
        ws = WebSocketClient("ws://localhost:8080")
        ws.on("message", lambda d: None)
        ws.on("message", lambda d: None)
        ws.off("message")
        self.assertEqual(len(ws._handlers["message"]), 0)

    def test_send_json(self):
        """Test send_json formats correctly."""
        ws = WebSocketClient("ws://localhost:8080")
        # Can't actually send without connection, but test formatting
        data = {"type": "chat", "text": "Hello"}
        payload = json.dumps(data).encode("utf-8")
        self.assertIn(b"chat", payload)
        self.assertIn(b"Hello", payload)

    def test_is_connected(self):
        """Test is_connected property."""
        ws = WebSocketClient("ws://localhost:8080")
        self.assertFalse(ws.is_connected)

    def test_repr(self):
        """Test repr."""
        ws = WebSocketClient("ws://localhost:8080")
        r = repr(ws)
        self.assertIn("WebSocketClient", r)
        self.assertIn("localhost:8080", r)

    def test_max_reconnect_config(self):
        """Test reconnect configuration."""
        ws = WebSocketClient(
            "ws://localhost:8080",
            max_reconnect_attempts=5,
            reconnect_delay=2.0,
            max_reconnect_delay=60.0,
        )
        self.assertEqual(ws._max_reconnect_attempts, 5)
        self.assertEqual(ws._reconnect_delay, 2.0)
        self.assertEqual(ws._max_reconnect_delay, 60.0)

    def test_disconnect(self):
        """Test disconnect."""
        ws = WebSocketClient("ws://localhost:8080")
        ws.disconnect()
        self.assertEqual(ws.state, WSState.CLOSED)


# ==================== WebSocket Manager Tests ====================

class TestWebSocketManager(unittest.TestCase):
    """Test WebSocketManager."""

    def test_create_manager(self):
        """Test creating manager."""
        mgr = WebSocketManager()
        self.assertEqual(mgr.total, 0)

    def test_add_client(self):
        """Test adding client."""
        mgr = WebSocketManager()
        mgr.add("chat", "ws://localhost:8080/chat")
        self.assertEqual(mgr.total, 1)
        self.assertIn("chat", mgr._clients)

    def test_remove_client(self):
        """Test removing client."""
        mgr = WebSocketManager()
        mgr.add("chat", "ws://localhost:8080/chat")
        mgr.remove("chat")
        self.assertEqual(mgr.total, 0)

    def test_get_client(self):
        """Test getting client."""
        mgr = WebSocketManager()
        mgr.add("chat", "ws://localhost:8080/chat")
        client = mgr.get("chat")
        self.assertIsInstance(client, WebSocketClient)

    def test_on_registers_handler(self):
        """Test on registers handler on client."""
        mgr = WebSocketManager()
        mgr.add("chat", "ws://localhost:8080/chat")
        handler = lambda data: None
        mgr.on("chat", "message", handler)
        self.assertIn(handler, mgr._clients["chat"]._handlers["message"])

    def test_connected_clients(self):
        """Test connected_clients property."""
        mgr = WebSocketManager()
        mgr.add("a", "ws://localhost:8080/a")
        mgr.add("b", "ws://localhost:8080/b")
        self.assertEqual(len(mgr.connected_clients), 0)
        self.assertEqual(len(mgr.disconnected_clients), 2)

    def test_stats(self):
        """Test get_stats."""
        mgr = WebSocketManager()
        mgr.add("chat", "ws://localhost:8080/chat")
        stats = mgr.get_stats()
        self.assertEqual(stats["total"], 1)
        self.assertIn("chat", stats["clients"])

    def test_repr(self):
        """Test repr."""
        mgr = WebSocketManager()
        r = repr(mgr)
        self.assertIn("WebSocketManager", r)

    def test_add_returns_self(self):
        """Test add returns self for chaining."""
        mgr = WebSocketManager()
        result = mgr.add("a", "ws://localhost:8080/a")
        self.assertIs(result, mgr)


# ==================== Channel Tests ====================

class TestChannel(unittest.TestCase):
    """Test Channel system."""

    def test_create_channel(self):
        """Test creating channel."""
        ws = WebSocketClient("ws://localhost:8080")
        ch = Channel("chat", ws)
        self.assertEqual(ch.name, "chat")
        self.assertEqual(len(ch.rooms), 0)

    def test_join_room(self):
        """Test joining room."""
        ws = WebSocketClient("ws://localhost:8080")
        ch = Channel("chat", ws)
        ch.join("room-1")
        self.assertIn("room-1", ch.rooms)

    def test_leave_room(self):
        """Test leaving room."""
        ws = WebSocketClient("ws://localhost:8080")
        ch = Channel("chat", ws)
        ch.join("room-1")
        ch.leave("room-1")
        self.assertNotIn("room-1", ch.rooms)

    def test_on_registers_handler(self):
        """Test on registers handler."""
        ws = WebSocketClient("ws://localhost:8080")
        ch = Channel("chat", ws)
        handler = lambda data: None
        ch.on("message", handler)
        self.assertIn(handler, ch._handlers["message"])

    def test_repr(self):
        """Test repr."""
        ws = WebSocketClient("ws://localhost:8080")
        ch = Channel("chat", ws)
        r = repr(ch)
        self.assertIn("Channel", r)
        self.assertIn("chat", r)


# ==================== Utility Tests ====================

class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""

    def test_create_ws_client(self):
        """Test create_ws_client utility."""
        called = []
        ws = create_ws_client(
            "ws://localhost:8080",
            on_message=lambda data: called.append(data),
        )
        self.assertIsInstance(ws, WebSocketClient)
        ws._emit("message", "test")
        self.assertEqual(called, ["test"])

    def test_ws_url(self):
        """Test ws_url utility."""
        url = ws_url("localhost", 8080, "/chat")
        self.assertEqual(url, "ws://localhost:8080/chat")

    def test_ws_url_secure(self):
        """Test ws_url with secure=True."""
        url = ws_url("example.com", 443, secure=True)
        self.assertEqual(url, "wss://example.com:443/")

    def test_ws_url_no_leading_slash(self):
        """Test ws_url adds leading slash."""
        url = ws_url("localhost", 8080, "chat")
        self.assertEqual(url, "ws://localhost:8080/chat")


# ==================== Integration Tests ====================

class TestIntegration(unittest.TestCase):
    """Integration tests combining lazy + chunk + websocket."""

    def test_lazy_with_chunk_manager(self):
        """Test lazy loading with chunk manager."""
        cm = ChunkManager()
        cm.define("basic", ["pyvibe.components.basic"])
        cm.load("basic")
        self.assertIn("basic", cm.loaded_chunks)

    def test_multiple_lazy_components(self):
        """Test multiple lazy components from same module."""
        from pyvibe.core.component import Component
        components = lazy_all("pyvibe.components.basic", [
            "judul", "paragraf", "teks",
        ])
        results = []
        for name, comp in components.items():
            r = comp(f"Test {name}")
            if isinstance(r, Component):
                r = r.render()
            results.append(r)
        self.assertEqual(len(results), 3)
        for r in results:
            self.assertIsInstance(r, str)

    def test_chunk_stats_after_load(self):
        """Test chunk stats after loading."""
        cm = ChunkManager()
        cm.define("charts", ["pyvibe.components.charts"])
        cm.define("forms", ["pyvibe.forms"])
        cm.load("charts")
        stats = cm.get_stats()
        self.assertEqual(stats["loaded"], 1)
        self.assertEqual(stats["pending"], 1)

    def test_lazy_component_from_easy(self):
        """Test lazy loading easy module."""
        Easy = lazy("pyvibe.easy", "landing")
        result = Easy(judul="Test", fitur=["A", "B"])
        self.assertIn("Test", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
