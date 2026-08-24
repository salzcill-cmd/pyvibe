"""
PyVibe Events — event-driven architecture.

Usage:
    from pyvibe.events import Event, EventEmitter

    # Create emitter
    emitter = EventEmitter()

    # Listen to events
    @emitter.on("user.created")
    def on_user_created(user):
        print(f"User {user['nama']} created!")

    # Emit events
    emitter.emit("user.created", {"nama": "Andi", "email": "andi@test.com"})

    # Once listener
    @emitter.once("app.ready")
    def on_ready():
        print("App is ready!")

    emitter.emit("app.ready")  # Triggers listener
    emitter.emit("app.ready")  # Does NOT trigger (once)
"""

from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from collections import defaultdict
import time


class Event:
    """Represents an event."""

    def __init__(self, name: str, data: Any = None):
        self.name = name
        self.data = data
        self.time = time.time()
        self.propagation_stopped = False

    def stop_propagation(self):
        """Stop event propagation."""
        self.propagation_stopped = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "data": self.data,
            "time": self.time,
        }


class EventEmitter:
    """
    Event emitter for decoupled communication.

    Usage:
        emitter = EventEmitter()

        @emitter.on("message")
        def handle_message(data):
            print(data)

        emitter.emit("message", "Hello!")
    """

    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = defaultdict(list)
        self._once_listeners: Dict[str, List[Callable]] = defaultdict(list)
        self._event_history: List[Event] = []

    def on(self, event: str, callback: Callable) -> Callable:
        """Register event listener."""
        self._listeners[event].append(callback)
        return callback

    def once(self, event: str, callback: Callable) -> Callable:
        """Register one-time event listener."""
        self._once_listeners[event].append(callback)
        return callback

    def off(self, event: str, callback: Optional[Callable] = None):
        """Remove event listener."""
        if callback:
            if event in self._listeners:
                self._listeners[event] = [
                    cb for cb in self._listeners[event] if cb != callback
                ]
            if event in self._once_listeners:
                self._once_listeners[event] = [
                    cb for cb in self._once_listeners[event] if cb != callback
                ]
        else:
            self._listeners[event] = []
            self._once_listeners[event] = []

    def emit(self, event: str, data: Any = None) -> bool:
        """Emit an event."""
        evt = Event(event, data)
        self._event_history.append(evt)

        # Regular listeners
        for callback in self._listeners.get(event, []):
            if evt.propagation_stopped:
                break
            callback(data, evt)

        # Once listeners
        for callback in self._once_listeners.get(event, []):
            if evt.propagation_stopped:
                break
            callback(data, evt)
        self._once_listeners[event] = []

        # Wildcard listeners
        for callback in self._listeners.get("*", []):
            callback(data, evt)

        return not evt.propagation_stopped

    def has_listeners(self, event: str) -> bool:
        """Check if event has listeners."""
        return bool(self._listeners.get(event) or self._once_listeners.get(event))

    def listener_count(self, event: str) -> int:
        """Get listener count for event."""
        return len(self._listeners.get(event, [])) + len(self._once_listeners.get(event, []))

    def get_history(self, event: Optional[str] = None) -> List[Event]:
        """Get event history."""
        if event:
            return [e for e in self._event_history if e.name == event]
        return list(self._event_history)

    def clear_history(self):
        """Clear event history."""
        self._event_history.clear()


# ==================== Built-in Events ====================

class AppEvents:
    """Built-in application events."""

    STARTING = "app.starting"
    STARTED = "app.started"
    STOPPING = "app.stopping"
    STOPPED = "app.stopped"
    ERROR = "app.error"
    REQUEST = "app.request"
    RESPONSE = "app.response"
    ROUTE_NOT_FOUND = "app.route_not_found"


class UserEvents:
    """Built-in user events."""

    CREATED = "user.created"
    UPDATED = "user.updated"
    DELETED = "user.deleted"
    LOGGED_IN = "user.logged_in"
    LOGGED_OUT = "user.logged_out"
    PASSWORD_CHANGED = "user.password_changed"


class DatabaseEvents:
    """Built-in database events."""

    QUERY = "db.query"
    INSERT = "db.insert"
    UPDATE = "db.update"
    DELETE = "db.delete"
    ERROR = "db.error"


# ==================== Global EventEmitter ====================

_events = EventEmitter()


def get_events() -> EventEmitter:
    """Get global event emitter."""
    return _events


def on(event: str, callback: Callable) -> Callable:
    """Register global event listener."""
    return _events.on(event, callback)


def once(event: str, callback: Callable) -> Callable:
    """Register global one-time event listener."""
    return _events.once(event, callback)


def emit(event: str, data: Any = None) -> bool:
    """Emit global event."""
    return _events.emit(event, data)
