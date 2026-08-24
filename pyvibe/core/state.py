"""
State management untuk PyVibe — reactive data yang otomatis update UI.

Usage:
    state = State(nama="Andi", umur=20)
    state.nama = "Budi"  # UI otomatis update
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
    Reactive state management.

    State mendukung:
    - Nested objects
    - List/array
    - Change listeners
    - Serialization
    """

    def __init__(self, **initial):
        self._data: Dict[str, Any] = dict(initial)
        self._listeners: Dict[str, List[Callable]] = {}
        self._global_listeners: List[Callable] = []
        self._history: List[StateChange] = []

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            return super().__getattribute__(name)
        return self._data.get(name)

    def __setattr__(self, name: str, value: Any):
        if name.startswith("_"):
            super().__setattr__(name, value)
            return
        old_value = self._data.get(name)
        self._data[name] = value
        self._notify(name, old_value, value)

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

    def _notify(self, key: str, old_value: Any, new_value: Any):
        """Notify semua listeners tentang perubahan."""
        import time
        change = StateChange(key, old_value, new_value, time.time())
        self._history.append(change)

        # Notify specific listeners
        if key in self._listeners:
            for listener in self._listeners[key]:
                listener(new_value, old_value)

        # Notify global listeners
        for listener in self._global_listeners:
            listener(change)

    def on_change(self, key: str, callback: Callable):
        """Register listener untuk perubahan state tertentu.

        Usage:
            state.on_change("nama", lambda baru, lama: print(f"Nama berubah: {lama} → {baru}"))
        """
        if key not in self._listeners:
            self._listeners[key] = []
        self._listeners[key].append(callback)

    def on_any_change(self, callback: Callable):
        """Register listener untuk semua perubahan state."""
        self._global_listeners.append(callback)

    def set(self, key: str, value: Any):
        """Set state value (alternative syntax)."""
        setattr(self, key, value)

    def get(self, key: str, default: Any = None) -> Any:
        """Get state value with default."""
        return self._data.get(key, default)

    def update(self, **kwargs):
        """Update multiple values at once.

        Usage:
            state.update(nama="Budi", umur=21)
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def reset(self):
        """Reset state ke initial values."""
        self._data.clear()
        self._listeners.clear()
        self._global_listeners.clear()

    def to_dict(self) -> Dict[str, Any]:
        """Serialize state ke dictionary."""
        return dict(self._data)

    def to_json(self) -> str:
        """Serialize state ke JSON string."""
        return json.dumps(self._data, indent=2, ensure_ascii=False)

    def from_dict(self, data: Dict[str, Any]):
        """Load state dari dictionary."""
        for key, value in data.items():
            setattr(self, key, value)

    def from_json(self, json_str: str):
        """Load state dari JSON string."""
        data = json.loads(json_str)
        self.from_dict(data)

    def get_history(self) -> List[StateChange]:
        """Get semua perubahan state."""
        return list(self._history)

    def has_changed(self, key: str) -> bool:
        """Cek apakah state pernah berubah."""
        return any(change.key == key for change in self._history)

    def clone(self) -> State:
        """Clone state."""
        return State(**self._data)
