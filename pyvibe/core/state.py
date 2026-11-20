"""
State management untuk PyVibe — reactive data yang otomatis update UI.

Usage:
    state = State(nama="Andi", umur=20)
    state.nama = "Budi"  # UI otomatis update
    state.compute("full_name", lambda: f"{state.first} {state.last}")
    state.watch("nama", lambda baru, lama: print(f"Nama berubah: {lama} → {baru}"))
"""

from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
import json


@dataclass
class StateChange:
    """Representasi perubahan state."""
    key: str
    old_value: Any
    new_value: Any
    timestamp: float = 0.0


class State:
    """
    Reactive state management with advanced computed properties.

    State mendukung:
    - Nested objects
    - List/array
    - Change listeners (on_change)
    - Derived/computed states (auto-update when dependencies change)
    - Watchers untuk monitoring perubahan
    - Serialization
    - History tracking
    - Cloning state
    """

    def __init__(self, **initial):
        self._data: Dict[str, Any] = dict(initial)
        self._watchers: Dict[str, List[Callable]] = {}
        self._global_watchers: List[Callable] = []
        self._history: List[StateChange] = []
        # Computed (derived) states
        self._computed_functions: Dict[str, Callable] = {}
        self._computed_deps: Dict[str, set] = {}
        self._computed_values: Dict[str, Any] = {}
        self._dirty: Dict[str, bool] = {}
        # Flag to track if this is the first access
        self._first_access: Dict[str, bool] = {}
        # Track computed dependencies for auto-recomputation
        self._computed_dependents: Dict[str, set] = {}
        # Map of data keys to dependent computed states
        self._data_to_computed: Dict[str, set] = {}

    # --- Basic attribute access ---

    def __getattr__(self, name: str) -> Any:
        """Called when normal attribute lookup fails."""
        # If name is a computed state, handle it
        if name in self._computed_functions:
            # Always recompute on first access, then check dirty
            if self._first_access.get(name, True) or self._dirty.get(name, False):
                try:
                    value = self._computed_functions[name]()
                    self._computed_values[name] = value
                    self._first_access[name] = False
                    self._dirty[name] = False
                except Exception:
                    pass
            return self._computed_values.get(name)
        # Normal data access
        return self._data.get(name)

    def __setattr__(self, name: str, value: Any):
        """Set attribute, tracking computed dependencies."""
        # Initialize internal attrs without triggering our custom logic
        internal_attrs = (
            "_data", "_watchers", "_global_watchers", "_history",
            "_computed_functions", "_computed_deps", "_computed_values", "_dirty",
            "_first_access", "_computed_dependents", "_data_to_computed"
        )
        if name in internal_attrs:
            super().__setattr__(name, value)
            return

        # Normal data set
        old_value = self._data.get(name)
        self._data[name] = value
        self._notify(name, old_value, value)

        # Check if any computed state depends on this key and mark dirty
        for comp_name, deps in self._computed_deps.items():
            if name in deps:
                self._dirty[comp_name] = True

        # Register this key as depending on computed states
        for comp_name, dep_set in self._data_to_computed.items():
            if name in dep_set:
                self._dirty[comp_name] = True

    def __delattr__(self, name: str):
        """Handle deletion."""
        if name in self._data:
            old_value = self._data[name]
            del self._data[name]
            self._notify(name, old_value, None)
        else:
            super().__delattr__(name)

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

    def __setitem__(self, key: str, value: Any):
        old_value = self._data.get(key)
        self._data[key] = value
        self._notify(key, old_value, value)

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __repr__(self) -> str:
        return f"State({self._data})"

    # --- Notifications ---

    def _notify(self, key: str, old_value: Any, new_value: Any):
        """Notify semua listeners tentang perubahan."""
        import time
        change = StateChange(key, old_value, new_value, time.time())
        self._history.append(change)

        # Notify specific watchers
        if key in self._watchers:
            for callback in self._watchers[key]:
                try:
                    callback(new_value, old_value)
                except Exception:
                    pass

        # Notify global watchers
        for watcher in self._global_watchers:
            try:
                watcher(change)
            except Exception:
                pass

        # Recompute dependent computed states
        if key in self._data_to_computed:
            for computed_name in self._data_to_computed[key]:
                self._dirty[computed_name] = True

    # --- Change listeners ---

    def on_change(self, key: str, callback: Callable):
        """Register listener untuk perubahan state tertentu.

        Usage:
            state.on_change("nama", lambda baru, lama: print(f"Nama berubah: {lama} → {baru}"))
        """
        if key not in self._watchers:
            self._watchers[key] = []
        self._watchers[key].append(callback)

    def on_any_change(self, callback: Callable):
        """Register listener untuk semua perubahan state."""
        self._global_watchers.append(callback)

    # --- State setting ---

    def set(self, key: str, value: Any):
        """Set state value (alternative syntax)."""
        self._data[key] = value
        self._notify(key, None, value)

    def get(self, key: str, default: Any = None) -> Any:
        """Get state value with default."""
        return self._data.get(key, default)

    def update(self, **kwargs):
        """Update multiple values at once.

        Usage:
            state.update(nama="Budi", umur=21)
        """
        for key, value in kwargs.items():
            self.set(key, value)

    # --- Reset ---

    def reset(self):
        """Reset state ke initial values."""
        self._data.clear()
        self._watchers.clear()
        self._global_watchers.clear()
        self._history.clear()
        self._computed_functions.clear()
        self._computed_deps.clear()
        self._computed_values.clear()
        self._dirty.clear()
        self._first_access.clear()
        self._computed_dependents.clear()
        self._data_to_computed.clear()

    # --- Serialization ---

    def to_dict(self) -> Dict[str, Any]:
        """Serialize state ke dictionary."""
        return dict(self._data)

    def to_json(self) -> str:
        """Serialize state ke JSON string."""
        return json.dumps(self._data, indent=2, ensure_ascii=False)

    def from_dict(self, data: Dict[str, Any]):
        """Load state dari dictionary."""
        self._data.clear()
        for key, value in data.items():
            self._data[key] = value

    def from_json(self, json_str: str):
        """Load state dari JSON string."""
        data = json.loads(json_str)
        self.from_dict(data)

    # --- History ---

    def get_history(self) -> List[StateChange]:
        """Get semua perubahan state."""
        return list(self._history)

    def has_changed(self, key: str) -> bool:
        """Cek apakah state pernah berubah."""
        return any(change.key == key for change in self._history)

    # --- Clone ---

    def clone(self) -> State:
        """Clone state."""
        return State(**self._data)

    # --- Computed/Derived States ---

    def compute(self, name: str, fn: Callable[[], Any], *dep_keys: str) -> None:
        """
        Create a computed/derived state that auto-updates when dependencies change.

        Usage:
            state.compute("full_name", lambda: f"{state.data['first']} {state.data['last']}", "first", "last")

        Parameters:
            name: Name of the computed state
            fn: Function that takes NO arguments and returns the computed value
            *dep_keys: Data keys that this computed state depends on
        """
        self._computed_functions[name] = fn
        # Store dependencies as a set of data keys
        self._computed_deps[name] = set(dep_keys) if dep_keys else set()
        # Map data keys to dependent computed states
        for dep in (dep_keys if dep_keys else []):
            if dep not in self._data_to_computed:
                self._data_to_computed[dep] = set()
            self._data_to_computed[dep].add(name)
        # Register dependents for each dependency
        for dep in (dep_keys if dep_keys else []):
            if dep not in self._computed_dependents:
                self._computed_dependents[dep] = set()
            self._computed_dependents[dep].add(name)
        self._computed_values[name] = None
        self._dirty[name] = True  # Mark as needing initial computation
        self._first_access[name] = True  # First access flag

    def depend_on(self, computed_name: str, *dep_keys: str) -> None:
        """
        Mark that a computed state depends on specific data keys.

        Usage:
            state.depend_on("full_name", "first", "last")
        """
        if computed_name in self._computed_deps:
            self._computed_deps[computed_name].update(dep_keys)
            # Also register dependents
            for dep in dep_keys:
                if dep not in self._computed_dependents:
                    self._computed_dependents[dep] = set()
                self._computed_dependents[dep].add(computed_name)
                # Also update data_to_computed
                if dep in self._data_to_computed:
                    self._data_to_computed[dep].add(computed_name)

    def mark_dirty(self, name: str) -> None:
        """Mark a computed state as dirty, will be recomputed on next access."""
        self._dirty[name] = True

    def _recompute(self, name: str) -> Any:
        """Recompute a derived state."""
        if name not in self._computed_functions:
            return self._data.get(name)
        try:
            value = self._computed_functions[name]()
            self._computed_values[name] = value
            self._dirty[name] = False
            # Notify watchers
            if name in self._watchers:
                for cb in self._watchers[name]:
                    try:
                        cb(value, self._computed_values.get(name))
                    except Exception:
                        pass
            # Notify global watchers
            for w in self._global_watchers:
                try:
                    w(StateChange(name, self._computed_values.get(name), value, __import__('time').time()))
                except Exception:
                    pass
            return value
        except Exception:
            return self._computed_values.get(name)

    # --- Access computed states via __getattr__ ---

    def __getattr__(self, name: str) -> Any:
        """Access computed states automatically."""
        if name in self._computed_functions:
            # Always recompute on first access, then check dirty
            if self._first_access.get(name, True) or self._dirty.get(name, False):
                self._recompute(name)
            return self._computed_values.get(name)
        # Fallback - shouldn't normally reach here for normal data
        return self._data.get(name)

    def __setattr__(self, name: str, value: Any):
        """Set attributes, tracking computed dependencies."""
        internal_attrs = (
            "_data", "_watchers", "_global_watchers", "_history",
            "_computed_functions", "_computed_deps", "_computed_values", "_dirty",
            "_first_access", "_computed_dependents", "_data_to_computed"
        )
        if name in internal_attrs:
            super().__setattr__(name, value)
            return

        # Normal data set
        old_value = self._data.get(name)
        self._data[name] = value
        self._notify(name, old_value, value)

        # Check if any computed state depends on this key and mark dirty
        for comp_name, deps in self._computed_deps.items():
            if name in deps:
                self.mark_dirty(comp_name)

    def __delattr__(self, name: str):
        """Handle deletion."""
        if name in self._data:
            old_value = self._data[name]
            del self._data[name]
            self._notify(name, old_value, None)
        else:
            super().__delattr__(name)

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

    def __setitem__(self, key: str, value: Any):
        old_value = self._data.get(key)
        self._data[key] = value
        self._notify(key, old_value, value)

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __repr__(self) -> str:
        return f"State({self._data})"


import inspect