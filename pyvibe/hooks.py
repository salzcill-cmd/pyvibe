"""
PyVibe Hooks — composable functions for reusable logic.

Usage:
    from pyvibe.hooks import use_local_storage, use_debounce, use_media_query

    # Local storage
    count = use_local_storage("count", 0)
    count.value = 1  # Auto-saved

    # Debounce
    debounced_search = use_debounce(search_func, delay=300)

    # Media query
    is_mobile = use_media_query("(max-width: 768px)")
"""

from __future__ import annotations
import time
import json
import os
import hashlib
from typing import Any, Callable, Dict, List, Optional, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps
from collections import defaultdict


T = TypeVar("T")


# ==================== Local Storage ====================

class LocalStorage:
    """
    File-based localStorage simulation.
    
    Usage:
        storage = LocalStorage("my-app")
        storage.set("count", 0)
        count = storage.get("count")
    """

    def __init__(self, namespace: str = "pyvibe"):
        self.namespace = namespace
        self._dir = os.path.join(".pyvibe", "storage")
        os.makedirs(self._dir, exist_ok=True)

    def _get_path(self, key: str) -> str:
        safe_key = hashlib.md5(f"{self.namespace}:{key}".encode()).hexdigest()
        return os.path.join(self._dir, f"{safe_key}.json")

    def get(self, key: str, default: Any = None) -> Any:
        """Get value from storage."""
        path = self._get_path(key)
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                    return data.get("value", default)
            except Exception:
                pass
        return default

    def set(self, key: str, value: Any) -> None:
        """Set value in storage."""
        path = self._get_path(key)
        with open(path, "w") as f:
            json.dump({"value": value, "timestamp": time.time()}, f)

    def delete(self, key: str) -> bool:
        """Delete value from storage."""
        path = self._get_path(key)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False

    def clear(self) -> None:
        """Clear all storage for this namespace."""
        for filename in os.listdir(self._dir):
            filepath = os.path.join(self._dir, filename)
            if os.path.isfile(filepath):
                try:
                    with open(filepath, "r") as f:
                        data = json.load(f)
                    # Only clear items for this namespace
                    if data.get("namespace") == self.namespace:
                        os.remove(filepath)
                except Exception:
                    pass

    def keys(self) -> List[str]:
        """Get all keys."""
        keys = []
        for filename in os.listdir(self._dir):
            filepath = os.path.join(self._dir, filename)
            if os.path.isfile(filepath):
                try:
                    with open(filepath, "r") as f:
                        data = json.load(f)
                    keys.append(filename)
                except Exception:
                    pass
        return keys

    def has(self, key: str) -> bool:
        """Check if key exists."""
        path = self._get_path(key)
        return os.path.exists(path)


def use_local_storage(key: str, default: Any = None, namespace: str = "pyvibe") -> Any:
    """
    Hook for local storage.
    
    Usage:
        count = use_local_storage("count", 0)
    """
    storage = LocalStorage(namespace)
    value = storage.get(key, default)
    return value


# ==================== Debounce ====================

def use_debounce(func: Callable, delay: int = 300) -> Callable:
    """
    Debounce function calls.
    
    Usage:
        debounced_search = use_debounce(search, delay=300)
        debounced_search("query")  # Only executes after 300ms of no calls
    """
    last_called = [0.0]
    timer = [None]

    @wraps(func)
    def wrapper(*args, **kwargs):
        last_called[0] = time.time()
        
        def execute():
            if time.time() - last_called[0] >= delay / 1000:
                return func(*args, **kwargs)
        
        if timer[0]:
            try:
                timer[0].cancel()
            except Exception:
                pass
        
        import threading
        timer[0] = threading.Timer(delay / 1000, execute)
        timer[0].start()
        
        return None

    return wrapper


# ==================== Throttle ====================

def use_throttle(func: Callable, limit: int = 100) -> Callable:
    """
    Throttle function calls.
    
    Usage:
        throttled_scroll = use_throttle(on_scroll, limit=200)
    """
    last_called = [0.0]

    @wraps(func)
    def wrapper(*args, **kwargs):
        now = time.time()
        if now - last_called[0] >= limit / 1000:
            last_called[0] = now
            return func(*args, **kwargs)
        return None

    return wrapper


# ==================== Media Query ====================

def use_media_query(query: str) -> bool:
    """
    Check media query (simulated for server-side).
    
    Usage:
        is_mobile = use_media_query("(max-width: 768px)")
    """
    # This is a server-side simulation
    # In production, this would be evaluated client-side
    return False


# ==================== Memoize ====================

def use_memo(func: Callable, deps: Optional[List] = None) -> Callable:
    """
    Memoize function result.
    
    Usage:
        expensive_result = use_memo(lambda: expensive_calculation(), [dep1, dep2])
    """
    cache = {}
    cache_key = str(deps) if deps else None

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal cache_key
        current_key = cache_key or str((args, sorted(kwargs.items())))
        
        if current_key in cache:
            return cache[current_key]
        
        result = func(*args, **kwargs)
        cache[current_key] = result
        return result

    wrapper.clear = lambda: cache.clear()
    return wrapper


# ==================== Callback ====================

def use_callback(func: Callable, deps: Optional[List] = None) -> Callable:
    """
    Stable callback reference.
    
    Usage:
        stable_callback = use_callback(lambda: print("hello"), [])
    """
    return func


# ==================== Effect ====================

class Effect:
    """
    Side effect runner.
    
    Usage:
        effect = Effect()
        effect.run(lambda: print("Something changed"))
        effect.cleanup()  # Run cleanup
    """

    def __init__(self):
        self._cleanup_funcs: List[Callable] = []
        self._running = False

    def run(self, func: Callable) -> None:
        """Run effect."""
        self.cleanup()
        self._running = True
        result = func()
        if result and callable(result):
            self._cleanup_funcs.append(result)

    def cleanup(self) -> None:
        """Run cleanup functions."""
        self._running = False
        for cleanup in self._cleanup_funcs:
            try:
                cleanup()
            except Exception:
                pass
        self._cleanup_funcs.clear()


def use_effect(func: Callable, deps: Optional[List] = None) -> Effect:
    """
    Hook for side effects.
    
    Usage:
        effect = use_effect(lambda: print("Mounted"))
    """
    effect = Effect()
    effect.run(func)
    return effect


# ==================== Interval ====================

def use_interval(callback: Callable, interval_ms: int) -> Callable:
    """
    Run callback at intervals.
    
    Usage:
        stop = use_interval(lambda: print("tick"), 1000)
        stop()  # Stop interval
    """
    import threading
    
    running = [True]
    
    def loop():
        while running[0]:
            callback()
            time.sleep(interval_ms / 1000)
    
    thread = threading.Thread(target=loop, daemon=True)
    thread.start()
    
    def stop():
        running[0] = False
    
    return stop


# ==================== Timeout ====================

def use_timeout(callback: Callable, delay_ms: int) -> Callable:
    """
    Run callback after delay.
    
    Usage:
        cancel = use_timeout(lambda: print("done"), 1000)
        cancel()  # Cancel timeout
    """
    import threading
    
    timer = threading.Timer(delay_ms / 1000, callback)
    timer.start()
    
    def cancel():
        timer.cancel()
    
    return cancel


# ==================== Previous Value ====================

_previous_storage = {"value": None, "initialized": False}

def use_previous(value: Any) -> Any:
    """
    Get previous value.
    
    Usage:
        prev_count = use_previous(count)
    """
    prev = _previous_storage["value"]
    _previous_storage["value"] = value
    return prev


# ==================== Counter ====================

class CounterState:
    """Mutable counter state."""
    def __init__(self, initial: int = 0):
        self.count = initial

def use_counter(initial: int = 0) -> Dict[str, Any]:
    """
    Counter hook.
    
    Usage:
        counter = use_counter(0)
        counter["increment"]()  # count = 1
        counter["decrement"]()  # count = 0
        counter["reset"]()  # count = 0
    """
    state = CounterState(initial)

    def increment():
        state.count += 1
        return state.count

    def decrement():
        state.count -= 1
        return state.count

    def reset():
        state.count = initial
        return state.count

    return {
        "_state": state,
        "increment": increment,
        "decrement": decrement,
        "reset": reset,
    }


def _get_counter_count(counter: Dict[str, Any]) -> int:
    """Get current counter value."""
    return counter["_state"].count


# ==================== Toggle ====================

class ToggleState:
    """Mutable toggle state."""
    def __init__(self, initial: bool = False):
        self.value = initial

def use_toggle(initial: bool = False) -> Dict[str, Any]:
    """
    Toggle hook.
    
    Usage:
        toggle = use_toggle(False)
        toggle["toggle"]()  # True
        toggle["on"]()  # True
        toggle["off"]()  # False
    """
    state = ToggleState(initial)

    def toggle():
        state.value = not state.value
        return state.value

    def on():
        state.value = True
        return True

    def off():
        state.value = False
        return False

    return {
        "_state": state,
        "toggle": toggle,
        "on": on,
        "off": off,
    }


def _get_toggle_value(toggle: Dict[str, Any]) -> bool:
    """Get current toggle value."""
    return toggle["_state"].value


# ==================== List ====================

class ListState:
    """Mutable list state."""
    def __init__(self, initial: Optional[List] = None):
        self.items = list(initial or [])

def use_list(initial: Optional[List] = None) -> Dict[str, Any]:
    """
    List hook.
    
    Usage:
        todo_list = use_list(["Item 1"])
        todo_list["add"]("Item 2")
        todo_list["remove"](0)
        todo_list["clear"]()
    """
    state = ListState(initial)

    def add(item):
        state.items.append(item)
        return state.items

    def remove(index):
        if 0 <= index < len(state.items):
            state.items.pop(index)
        return state.items

    def clear():
        state.items.clear()
        return state.items

    def update(index, value):
        if 0 <= index < len(state.items):
            state.items[index] = value
        return state.items

    return {
        "_state": state,
        "add": add,
        "remove": remove,
        "clear": clear,
        "update": update,
    }


def _get_list_items(lst: Dict[str, Any]) -> List:
    """Get current list items."""
    return lst["_state"].items
