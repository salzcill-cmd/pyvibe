"""
🐍 PyVibe Lazy — Lazy Loading, Code Splitting & Dynamic Imports.

"Gak perlu muat semua sekaligus, muat aja yang dibutuhkan."

Features:
- lazy() — Lazy load components
- suspense() — Show loading state while lazy components load
- dynamic_import() — Dynamic Python module import
- Code splitting — Split app into chunks
- Chunk loading — Load chunks on demand

Usage:
    from pyvibe.lazy import lazy, suspense, dynamic_import, ChunkManager

    # Lazy load a heavy component
    HeavyChart = lazy("pyvibe.components.charts", "chart_bar")

    # Wrap with suspense (shows loading while loading)
    page = suspense(
        loading=loader(),
        children=[HeavyChart(data=...)],
    )

    # Dynamic import
    module = dynamic_import("pyvibe.components.advanced_ui")
    calendar = module.calendar_component(year=2026)

    # Code splitting
    chunks = ChunkManager()
    chunks.define("charts", ["chart_bar", "chart_line", "chart_pie"])
    chunks.define("forms", ["Form", "FormBuilder", "Validators"])
    chunks.load("charts")  # Only load chart components
"""

from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, Union, Set
from dataclasses import dataclass, field
import sys
import importlib
import time
import threading


# ==================== Lazy Component ====================

@dataclass
class LazyState:
    """State of a lazy-loaded component."""
    PENDING = "pending"
    LOADING = "loading"
    LOADED = "loaded"
    ERROR = "error"


class LazyComponent:
    """
    Lazy-loaded component — only loads when first accessed.

    Usage:
        Chart = lazy("pyvibe.components.charts", "chart_bar")
        # Component not loaded yet

        html = Chart(data=[...])
        # Now it loads and renders
    """

    def __init__(self, module_path: str, component_name: str,
                 fallback: Optional[Any] = None):
        self.module_path = module_path
        self.component_name = component_name
        self.fallback = fallback
        self._state = LazyState.PENDING
        self._module = None
        self._component = None
        self._error = None
        self._load_time = 0.0
        self._load_count = 0
        self._last_result = None

    def _load(self):
        """Load the module and component."""
        if self._state == LazyState.LOADED:
            return

        self._state = LazyState.LOADING
        start = time.time()

        try:
            # Try to import the module
            if self.module_path in sys.modules:
                self._module = sys.modules[self.module_path]
            else:
                self._module = importlib.import_module(self.module_path)

            # Get the component
            self._component = getattr(self._module, self.component_name)
            self._state = LazyState.LOADED
            self._load_time = time.time() - start
            self._load_count += 1

        except Exception as e:
            self._state = LazyState.ERROR
            self._error = e
            self._load_time = time.time() - start

    def __call__(self, *args, **kwargs):
        """Call the lazy component."""
        self._load()

        if self._state == LazyState.ERROR:
            if self.fallback:
                return self.fallback(*args, **kwargs)
            raise ImportError(
                f"Gagal lazy load '{self.component_name}' dari "
                f"'{self.module_path}': {self._error}"
            )

        self._last_result = self._component(*args, **kwargs)
        return self._last_result

    def __getattr__(self, name):
        """Delegate attribute access to the loaded component."""
        self._load()
        if self._component:
            return getattr(self._component, name)
        raise AttributeError(f"Component not loaded: {name}")

    @property
    def state(self) -> str:
        """Get current state."""
        return self._state

    @property
    def is_loaded(self) -> bool:
        """Check if loaded."""
        return self._state == LazyState.LOADED

    @property
    def is_loading(self) -> bool:
        """Check if currently loading."""
        return self._state == LazyState.LOADING

    @property
    def has_error(self) -> bool:
        """Check if there was an error."""
        return self._state == LazyState.ERROR

    @property
    def load_time(self) -> float:
        """Get load time in seconds."""
        return self._load_time

    def preload(self):
        """Preload the component in background."""
        def _background_load():
            self._load()
        thread = threading.Thread(target=_background_load, daemon=True)
        thread.start()
        return self

    def __repr__(self):
        return (
            f"<LazyComponent '{self.component_name}' "
            f"state={self._state} load_time={self._load_time:.3f}s>"
        )


def lazy(module_path: str, component_name: str,
         fallback: Optional[Any] = None) -> LazyComponent:
    """
    Create a lazy-loaded component.

    Usage:
        Chart = lazy("pyvibe.components.charts", "chart_bar")
        Modal = lazy("pyvibe.components.advanced", "modal")

        # Later, when needed:
        html = Chart(data=[...])
    """
    return LazyComponent(module_path, component_name, fallback)


def lazy_all(module_path: str, component_names: List[str],
             fallback: Optional[Any] = None) -> Dict[str, LazyComponent]:
    """
    Create multiple lazy components from one module.

    Usage:
        charts = lazy_all("pyvibe.components.charts", [
            "chart_bar", "chart_line", "chart_pie", "chart_doughnut"
        ])
        html = charts["chart_bar"](data=[...])
    """
    return {
        name: LazyComponent(module_path, name, fallback)
        for name in component_names
    }


# ==================== Suspense ====================

from pyvibe.core.component import Component
from pyvibe.core.renderer import Renderer


class SuspenseComponent(Component):
    """
    Suspense wrapper — shows loading state while lazy components load.

    Usage:
        page = suspense(
            loading=loader(),  # Show this while loading
            error=alert("Gagal memuat!"),  # Show this on error
            children=[  # Lazy components
                lazy_chart(data=[...]),
                lazy_modal(),
            ],
        )
    """

    def __init__(self, loading: Optional[Component] = None,
                 error: Optional[Component] = None,
                 children: Optional[List[Any]] = None,
                 **kwargs):
        super().__init__(tag="div", **kwargs)
        self._loading_component = loading
        self._error_component = error
        self._children_raw = children or []

    def render(self) -> str:
        """Render with suspense handling."""
        from pyvibe.components.feedback import loader, alert

        # Check if all lazy components are loaded
        all_loaded = True
        has_error = False
        error_msg = ""

        for child in self._children_raw:
            if isinstance(child, LazyComponent):
                if child.has_error:
                    has_error = True
                    error_msg = str(child._error)
                    break
                elif not child.is_loaded:
                    all_loaded = False

        # Show loading state
        if not all_loaded:
            loading = self._loading_component or loader()
            renderer = Renderer()
            return renderer.render(loading)

        # Show error state
        if has_error:
            error = self._error_component or alert(
                f"Error: {error_msg}", tipe="error"
            )
            renderer = Renderer()
            return renderer.render(error)

        # All loaded — render children
        renderer = Renderer()
        rendered = []
        for child in self._children_raw:
            if isinstance(child, LazyComponent):
                child._load()
                if child._last_result is not None:
                    # Use cached result from previous call
                    result = child._last_result
                    if isinstance(result, str):
                        rendered.append(result)
                    elif isinstance(result, Component):
                        rendered.append(result.render())
                elif child._component:
                    rendered.append(f"<!-- lazy: {child.component_name} (no result) -->")
            elif isinstance(child, str):
                rendered.append(child)
            elif isinstance(child, Component):
                rendered.append(child.render())
            else:
                rendered.append(str(child))

        return "\n".join(rendered)


def suspense(
    loading: Optional[Component] = None,
    error: Optional[Component] = None,
    children: Optional[List[Any]] = None,
    **kwargs,
) -> SuspenseComponent:
    """
    Create a Suspense wrapper.

    Usage:
        page = suspense(
            loading=loader(),
            children=[lazy_chart(data=[...])],
        )
    """
    return SuspenseComponent(
        loading=loading,
        error=error,
        children=children or [],
        **kwargs,
    )


# ==================== Dynamic Import ====================

def dynamic_import(module_path: str, attribute: Optional[str] = None,
                   fallback: Any = None) -> Any:
    """
    Dynamic import — import module at runtime.

    Usage:
        # Import entire module
        charts = dynamic_import("pyvibe.components.charts")
        html = charts.chart_bar(data=[...])

        # Import specific attribute
        chart_bar = dynamic_import("pyvibe.components.charts", "chart_bar")
        html = chart_bar(data=[...])

        # With fallback
        modal = dynamic_import(
            "pyvibe.components.advanced",
            "modal",
            fallback=lambda *a, **k: Component("div"),
        )
    """
    try:
        if module_path in sys.modules:
            module = sys.modules[module_path]
        else:
            module = importlib.import_module(module_path)

        if attribute:
            return getattr(module, attribute)
        return module

    except Exception as e:
        if fallback is not None:
            return fallback
        raise ImportError(f"Gagal import '{module_path}': {e}")


def dynamic_import_all(module_paths: Dict[str, str]) -> Dict[str, Any]:
    """
    Dynamic import multiple modules.

    Usage:
        modules = dynamic_import_all({
            "charts": "pyvibe.components.charts",
            "forms": "pyvibe.forms",
            "advanced": "pyvibe.components.advanced_ui",
        })
        charts = modules["charts"]
    """
    result = {}
    for name, path in module_paths.items():
        try:
            result[name] = dynamic_import(path)
        except ImportError:
            result[name] = None
    return result


# ==================== Code Splitting ====================

@dataclass
class Chunk:
    """A code chunk for lazy loading."""
    name: str
    modules: List[str]
    components: List[str] = field(default_factory=list)
    loaded: bool = False
    load_time: float = 0.0
    size_estimate: int = 0  # Estimated size in bytes


class ChunkManager:
    """
    Manages code splitting and chunk loading.

    Usage:
        chunks = ChunkManager()

        # Define chunks
        chunks.define("charts", [
            "pyvibe.components.charts",
        ], components=["chart_bar", "chart_line", "chart_pie"])

        chunks.define("forms", [
            "pyvibe.forms",
        ], components=["Form", "FormBuilder", "Validators"])

        chunks.define("advanced_ui", [
            "pyvibe.components.advanced_ui",
        ], components=["calendar_component", "kanban", "video_player"])

        # Load specific chunks
        chunks.load("charts")
        chunks.load("forms")

        # Check what's loaded
        print(chunks.loaded_chunks)  # ["charts", "forms"]
        print(chunks.pending_chunks)  # ["advanced_ui"]
    """

    def __init__(self):
        self._chunks: Dict[str, Chunk] = {}
        self._loaded_modules: Set[str] = set()
        self._load_callbacks: Dict[str, List[Callable]] = {}

    def define(self, name: str, modules: List[str],
               components: Optional[List[str]] = None,
               size_estimate: int = 0) -> ChunkManager:
        """
        Define a code chunk.

        Usage:
            chunks.define("charts", [
                "pyvibe.components.charts",
            ], components=["chart_bar", "chart_line"])
        """
        chunk = Chunk(
            name=name,
            modules=modules,
            components=components or [],
            size_estimate=size_estimate,
        )
        self._chunks[name] = chunk
        return self

    def load(self, name: str) -> bool:
        """
        Load a specific chunk.

        Returns True if loaded successfully.
        """
        chunk = self._chunks.get(name)
        if not chunk:
            raise ValueError(f"Chunk '{name}' not defined")

        if chunk.loaded:
            return True

        start = time.time()
        try:
            for module_path in chunk.modules:
                if module_path not in self._loaded_modules:
                    importlib.import_module(module_path)
                    self._loaded_modules.add(module_path)

            chunk.loaded = True
            chunk.load_time = time.time() - start

            # Run callbacks
            for callback in self._load_callbacks.get(name, []):
                try:
                    callback(chunk)
                except Exception:
                    pass

            return True

        except Exception as e:
            print(f"  ⚠️ Gagal load chunk '{name}': {e}")
            return False

    def load_all(self) -> Dict[str, bool]:
        """Load all chunks."""
        results = {}
        for name in self._chunks:
            results[name] = self.load(name)
        return results

    def load_parallel(self, names: Optional[List[str]] = None) -> Dict[str, bool]:
        """
        Load multiple chunks in parallel (threaded).

        Usage:
            chunks.load_parallel(["charts", "forms", "advanced_ui"])
        """
        targets = names or list(self._chunks.keys())
        results = {}
        threads = []

        def _load_chunk(chunk_name):
            results[chunk_name] = self.load(chunk_name)

        for name in targets:
            if name in self._chunks and not self._chunks[name].loaded:
                t = threading.Thread(target=_load_chunk, args=(name,), daemon=True)
                threads.append(t)
                t.start()

        for t in threads:
            t.join(timeout=10)

        return results

    def on_load(self, chunk_name: str, callback: Callable):
        """Register callback when chunk is loaded."""
        if chunk_name not in self._load_callbacks:
            self._load_callbacks[chunk_name] = []
        self._load_callbacks[chunk_name].append(callback)

    @property
    def loaded_chunks(self) -> List[str]:
        """Get list of loaded chunk names."""
        return [name for name, chunk in self._chunks.items() if chunk.loaded]

    @property
    def pending_chunks(self) -> List[str]:
        """Get list of pending (not loaded) chunk names."""
        return [name for name, chunk in self._chunks.items() if not chunk.loaded]

    @property
    def total_chunks(self) -> int:
        """Total number of chunks."""
        return len(self._chunks)

    def get_stats(self) -> Dict[str, Any]:
        """Get loading statistics."""
        loaded = [c for c in self._chunks.values() if c.loaded]
        total_time = sum(c.load_time for c in loaded)
        return {
            "total_chunks": len(self._chunks),
            "loaded": len(loaded),
            "pending": len(self._chunks) - len(loaded),
            "total_load_time": round(total_time, 4),
            "loaded_modules": len(self._loaded_modules),
            "chunks": {
                name: {
                    "loaded": chunk.loaded,
                    "load_time": round(chunk.load_time, 4),
                    "modules": len(chunk.modules),
                    "components": len(chunk.components),
                }
                for name, chunk in self._chunks.items()
            },
        }

    def __repr__(self):
        loaded = len(self.loaded_chunks)
        total = self.total_chunks
        return f"<ChunkManager loaded={loaded}/{total}>"


# ==================== Utility ====================

# Global chunk manager instance
_default_chunks = ChunkManager()


def get_chunks() -> ChunkManager:
    """Get the default chunk manager."""
    return _default_chunks


def define_chunk(name: str, modules: List[str],
                 components: Optional[List[str]] = None) -> ChunkManager:
    """Shorthand to define a chunk."""
    return _default_chunks.define(name, modules, components)


def load_chunk(name: str) -> bool:
    """Shorthand to load a chunk."""
    return _default_chunks.load(name)


def lazy_component(module_path: str, component_name: str) -> LazyComponent:
    """Shorthand to create a lazy component."""
    return LazyComponent(module_path, component_name)
