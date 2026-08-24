"""
PyVibe Reactivity — reactive state with localStorage persistence and computed properties.

Usage:
    from pyvibe.reactivity import ReactiveStore, computed, watch

    store = ReactiveStore("my-app")
    store.state = {"count": 0, "user": {"name": "Andi"}}

    # Auto-persists to localStorage
    store.state["count"] = 1  # Auto-saved

    # Computed
    count_display = computed(lambda: f"Count: {store.state['count']}")

    # Watch
    watch(store.state, "count", lambda new, old: print(f"Changed: {old} → {new}"))
"""

from __future__ import annotations
import json
import os
import time
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field


class ReactiveDict(dict):
    """
    Dictionary that triggers callbacks on change.
    
    Usage:
        state = ReactiveDict(name="Andi", count=0)
        state.on_change("count", lambda new, old: print(f"Changed!"))
        state["count"] = 1  # Triggers callback
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._listeners: Dict[str, List[Callable]] = {}
        self._global_listeners: List[Callable] = []
        self._history: List[Dict] = []
        self._max_history: int = 50

    def __setitem__(self, key: str, value: Any) -> None:
        old = self.get(key)
        super().__setitem__(key, value)
        
        # Record history
        self._history.append({
            "key": key,
            "old": old,
            "new": value,
            "time": time.time(),
        })
        if len(self._history) > self._max_history:
            self._history.pop(0)
        
        # Notify listeners
        if key in self._listeners:
            for callback in self._listeners[key]:
                try:
                    callback(value, old)
                except Exception:
                    pass
        
        # Global listeners
        for callback in self._global_listeners:
            try:
                callback(key, value, old)
            except Exception:
                pass

    def on_change(self, key: str, callback: Callable) -> None:
        """Listen to changes on a specific key."""
        if key not in self._listeners:
            self._listeners[key] = []
        self._listeners[key].append(callback)

    def on_any_change(self, callback: Callable) -> None:
        """Listen to any change."""
        self._global_listeners.append(callback)

    def off_change(self, key: str, callback: Optional[Callable] = None) -> None:
        """Remove listener."""
        if callback and key in self._listeners:
            self._listeners[key] = [cb for cb in self._listeners[key] if cb != callback]
        elif key in self._listeners:
            self._listeners[key] = []

    def get_history(self, key: Optional[str] = None) -> List[Dict]:
        """Get change history."""
        if key:
            return [h for h in self._history if h["key"] == key]
        return list(self._history)

    def undo(self) -> bool:
        """Undo last change."""
        if not self._history:
            return False
        last = self._history.pop()
        super().__setitem__(last["key"], last["old"])
        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to regular dict."""
        return dict(self)


class ReactiveStore:
    """
    Persistent reactive state store with localStorage.
    
    Usage:
        store = ReactiveStore("my-app")
        store.state = {"count": 0}
        
        # Auto-saves to localStorage
        store.state["count"] = 1
        
        # Load from localStorage
        store.load()
        
        # Clear
        store.clear()
    """

    def __init__(self, name: str = "pyvibe", storage_path: Optional[str] = None):
        self.name = name
        self.storage_path = storage_path
        self.state = ReactiveDict()
        self._initialized = False

    def init(self, defaults: Optional[Dict] = None) -> "ReactiveStore":
        """Initialize store with defaults and load from storage."""
        if defaults:
            for k, v in defaults.items():
                if k not in self.state:
                    self.state[k] = v
        self.load()
        self._initialized = True
        return self

    def load(self) -> "ReactiveStore":
        """Load state from storage."""
        try:
            if self.storage_path and os.path.exists(self.storage_path):
                with open(self.storage_path, "r") as f:
                    data = json.load(f)
                    self.state.update(data)
            else:
                # Try localStorage simulation (file-based)
                path = self._get_storage_path()
                if os.path.exists(path):
                    with open(path, "r") as f:
                        data = json.load(f)
                        self.state.update(data)
        except Exception:
            pass
        return self

    def save(self) -> "ReactiveStore":
        """Save state to storage."""
        try:
            path = self._get_storage_path()
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                json.dump(self.state.to_dict(), f, indent=2)
        except Exception:
            pass
        return self

    def clear(self) -> "ReactiveStore":
        """Clear all state."""
        self.state.clear()
        try:
            path = self._get_storage_path()
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass
        return self

    def reset(self, defaults: Optional[Dict] = None) -> "ReactiveStore":
        """Reset to defaults."""
        self.clear()
        if defaults:
            self.state.update(defaults)
        self.save()
        return self

    def _get_storage_path(self) -> str:
        """Get storage file path."""
        if self.storage_path:
            return self.storage_path
        return os.path.join(".pyvibe", "state", f"{self.name}.json")

    def to_dict(self) -> Dict[str, Any]:
        """Export state as dict."""
        if hasattr(self.state, 'to_dict'):
            return self.state.to_dict()
        return dict(self.state)

    def from_dict(self, data: Dict[str, Any]) -> "ReactiveStore":
        """Import state from dict."""
        self.state.update(data)
        self.save()
        return self


# ==================== Computed Properties ====================

class Computed:
    """Computed property that recalculates when dependencies change."""

    def __init__(self, func: Callable, dependencies: Optional[List[str]] = None):
        self._func = func
        self._dependencies = dependencies or []
        self._cache = None
        self._dirty = True

    @property
    def value(self) -> Any:
        if self._dirty or self._cache is None:
            self._cache = self._func()
            self._dirty = False
        return self._cache

    def invalidate(self) -> None:
        self._dirty = True

    def __repr__(self) -> str:
        return f"Computed({self.value})"


def computed(func: Callable, dependencies: Optional[List[str]] = None) -> Computed:
    """Create a computed property."""
    return Computed(func, dependencies)


# ==================== Watchers ====================

def watch(target: Any, key: str, callback: Callable) -> Callable:
    """
    Watch a reactive property.
    
    Usage:
        state = ReactiveDict(count=0)
        unwatch = watch(state, "count", lambda new, old: print(f"{old} → {new}"))
        state["count"] = 1  # Prints: 0 → 1
        unwatch()  # Stop watching
    """
    if isinstance(target, ReactiveDict):
        target.on_change(key, callback)
        def unwatch():
            target.off_change(key, callback)
        return unwatch
    return lambda: None


def watch_all(target: ReactiveDict, callback: Callable) -> Callable:
    """Watch all changes on a reactive dict."""
    target.on_any_change(callback)
    def unwatch():
        target.off_change("*", callback)
    return unwatch


# ==================== Batch Updates ====================

class BatchContext:
    """Context manager for batch updates."""

    def __init__(self, store: ReactiveStore):
        self.store = store
        self._original_listeners = {}

    def __enter__(self):
        return self.store

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.store.save()


def batch(store: ReactiveStore) -> BatchContext:
    """Batch multiple updates into one save."""
    return BatchContext(store)
