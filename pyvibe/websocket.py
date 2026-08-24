"""
🐍 PyVibe WebSocket Client — Real-time connection support.

"Connect, send, receive — sesimpel ngobrol."

Features:
- WebSocketClient — Full WebSocket client with auto-reconnect
- WebSocketManager — Manage multiple connections
- Event-based message handling
- Auto-reconnect with exponential backoff
- Binary and text message support
- Connection state management
- Heartbeat/ping support

Usage:
    from pyvibe.websocket import WebSocketClient, WebSocketManager

    # Single connection
    ws = WebSocketClient("ws://localhost:8080")
    ws.on("message", lambda data: print(f"Received: {data}"))
    ws.on("open", lambda: print("Connected!"))
    ws.on("close", lambda code, reason: print(f"Closed: {reason}"))
    ws.connect()

    # Send messages
    ws.send({"type": "chat", "message": "Hello!"})
    ws.send_text("Plain text")

    # Auto-reconnect
    ws.connect(auto_reconnect=True)

    # Manager for multiple connections
    manager = WebSocketManager()
    manager.add("chat", "ws://localhost:8080/chat")
    manager.add("notifications", "ws://localhost:8080/notify")
    manager.connect_all()
"""

from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, Union, Set
from dataclasses import dataclass, field
from enum import Enum
import json
import time
import threading
import socket
import struct
import hashlib
import base64
import os


# ==================== Connection State ====================

class WSState(Enum):
    """WebSocket connection state."""
    CONNECTING = "connecting"
    OPEN = "open"
    CLOSING = "closing"
    CLOSED = "closed"
    RECONNECTING = "reconnecting"
    ERROR = "error"


# ==================== WebSocket Client ====================

class WebSocketClient:
    """
    WebSocket client with auto-reconnect and event system.

    Usage:
        ws = WebSocketClient("ws://localhost:8080")

        @ws.on_event("message")
        def handle_message(data):
            print(f"Received: {data}")

        @ws.on_event("open")
        def handle_open():
            print("Connected!")

        ws.connect()
        ws.send({"type": "chat", "text": "Hello!"})
    """

    def __init__(self, url: str, **kwargs):
        self._url = url
        self._state = WSState.CLOSED
        self._socket: Optional[socket.socket] = None
        self._thread: Optional[threading.Thread] = None
        self._receive_thread: Optional[threading.Thread] = None

        # Event handlers
        self._handlers: Dict[str, List[Callable]] = {
            "open": [],
            "close": [],
            "message": [],
            "error": [],
            "reconnect": [],
            "ping": [],
            "pong": [],
        }

        # Config
        self._auto_reconnect = kwargs.get("auto_reconnect", False)
        self._reconnect_delay = kwargs.get("reconnect_delay", 1.0)
        self._max_reconnect_delay = kwargs.get("max_reconnect_delay", 30.0)
        self._reconnect_attempts = 0
        self._max_reconnect_attempts = kwargs.get("max_reconnect_attempts", 10)
        self._heartbeat_interval = kwargs.get("heartbeat_interval", 30)
        self._timeout = kwargs.get("timeout", 5.0)

        # Message queue
        self._send_queue: List[bytes] = []
        self._queue_lock = threading.Lock()

        # Parse URL
        self._parse_url(url)

    def _parse_url(self, url: str):
        """Parse WebSocket URL."""
        self._secure = url.startswith("wss://")
        url_clean = url.replace("wss://", "").replace("ws://", "")
        parts = url_clean.split("/", 1)
        host_port = parts[0].split(":")

        self._host = host_port[0]
        self._port = int(host_port[1]) if len(host_port) > 1 else (443 if self._secure else 80)
        self._path = "/" + parts[1] if len(parts) > 1 else "/"

    # ==================== Event System ====================

    def on(self, event: str, handler: Callable) -> WebSocketClient:
        """
        Register event handler.

        Usage:
            ws.on("message", lambda data: print(data))
            ws.on("open", lambda: print("Connected"))
            ws.on("close", lambda code, reason: print("Closed"))
            ws.on("error", lambda err: print(f"Error: {err}"))
        """
        if event in self._handlers:
            self._handlers[event].append(handler)
        return self

    def on_event(self, event: str) -> Callable:
        """
        Decorator for event handlers.

        Usage:
            @ws.on_event("message")
            def handle(data):
                print(data)
        """
        def decorator(func: Callable):
            self.on(event, func)
            return func
        return decorator

    def off(self, event: str, handler: Optional[Callable] = None):
        """Remove event handler."""
        if handler:
            self._handlers[event] = [h for h in self._handlers[event] if h != handler]
        else:
            self._handlers[event] = []

    def _emit(self, event: str, *args):
        """Emit event to handlers."""
        for handler in self._handlers.get(event, []):
            try:
                handler(*args)
            except Exception as e:
                self._emit("error", e)

    # ==================== Connection ====================

    def connect(self, auto_reconnect: Optional[bool] = None):
        """
        Connect to WebSocket server.

        Usage:
            ws.connect()
            ws.connect(auto_reconnect=True)
        """
        if auto_reconnect is not None:
            self._auto_reconnect = auto_reconnect

        self._state = WSState.CONNECTING
        self._reconnect_attempts = 0

        try:
            self._do_connect()
        except Exception as e:
            self._state = WSState.ERROR
            self._emit("error", e)
            if self._auto_reconnect:
                self._schedule_reconnect()

    def _do_connect(self):
        """Perform the actual connection."""
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(self._timeout)

        try:
            self._socket.connect((self._host, self._port))
        except Exception as e:
            self._socket.close()
            self._socket = None
            raise ConnectionError(f"Gagal koneksi ke {self._url}: {e}")

        # WebSocket handshake
        self._perform_handshake()

        self._state = WSState.OPEN
        self._reconnect_attempts = 0
        self._emit("open")

        # Start receive thread
        self._receive_thread = threading.Thread(
            target=self._receive_loop, daemon=True
        )
        self._receive_thread.start()

        # Start heartbeat if configured
        if self._heartbeat_interval > 0:
            self._heartbeat_thread = threading.Thread(
                target=self._heartbeat_loop, daemon=True
            )
            self._heartbeat_thread.start()

    def _perform_handshake(self):
        """Perform WebSocket handshake."""
        # Generate random key
        key = base64.b64encode(os.urandom(16)).decode()

        # Send upgrade request
        request = (
            f"GET {self._path} HTTP/1.1\r\n"
            f"Host: {self._host}:{self._port}\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n"
            f"\r\n"
        )
        self._socket.sendall(request.encode())

        # Read response
        response = b""
        while b"\r\n\r\n" not in response:
            chunk = self._socket.recv(4096)
            if not chunk:
                raise ConnectionError("Handshake gagal: koneksi terputus")
            response += chunk

        # Verify 101 status
        status_line = response.split(b"\r\n")[0].decode()
        if "101" not in status_line:
            raise ConnectionError(f"Handshake gagal: {status_line}")

    def _receive_loop(self):
        """Receive messages in background thread."""
        while self._state == WSState.OPEN:
            try:
                data = self._receive_frame()
                if data is None:
                    # Connection closed
                    self._handle_close(1000, "Connection closed")
                    break
                self._emit("message", data)
            except socket.timeout:
                continue
            except ConnectionError:
                self._handle_close(1000, "Connection lost")
                break
            except Exception as e:
                self._emit("error", e)
                if self._state == WSState.OPEN:
                    continue
                break

    def _heartbeat_loop(self):
        """Send periodic pings."""
        while self._state == WSState.OPEN:
            try:
                time.sleep(self._heartbeat_interval)
                if self._state == WSState.OPEN:
                    self._send_frame(b"\x09", b"")  # Ping frame
            except Exception:
                break

    def _receive_frame(self) -> Optional[bytes]:
        """Receive and parse a WebSocket frame."""
        # Read first byte (FIN + opcode)
        first_byte = self._recv_exact(1)
        if not first_byte:
            return None

        opcode = first_byte[0] & 0x0F
        is_final = first_byte[0] & 0x80

        # Read second byte (mask + length)
        second_byte = self._recv_exact(1)
        if not second_byte:
            return None

        masked = second_byte[0] & 0x80
        length = second_byte[0] & 0x7F

        # Extended length
        if length == 126:
            raw = self._recv_exact(2)
            if not raw:
                return None
            length = struct.unpack("!H", raw)[0]
        elif length == 127:
            raw = self._recv_exact(8)
            if not raw:
                return None
            length = struct.unpack("!Q", raw)[0]

        # Masking key
        mask_key = None
        if masked:
            mask_key = self._recv_exact(4)

        # Payload
        payload = self._recv_exact(length) if length > 0 else b""

        # Unmask if needed
        if masked and mask_key:
            payload = bytes(
                b ^ mask_key[i % 4]
                for i, b in enumerate(payload)
            )

        # Handle control frames
        if opcode == 0x08:  # Close
            return None
        elif opcode == 0x09:  # Ping
            self._send_frame(b"\x0A", payload)  # Pong
            self._emit("ping", payload)
            return self._receive_frame() if is_final else None
        elif opcode == 0x0A:  # Pong
            self._emit("pong", payload)
            return self._receive_frame() if is_final else None

        # Text or binary
        if opcode == 0x01:  # Text
            try:
                return payload.decode("utf-8")
            except UnicodeDecodeError:
                return payload
        elif opcode == 0x02:  # Binary
            return payload

        return payload if payload else None

    def _recv_exact(self, n: int) -> Optional[bytes]:
        """Receive exactly n bytes."""
        data = b""
        while len(data) < n:
            try:
                chunk = self._socket.recv(n - len(data))
                if not chunk:
                    return None
                data += chunk
            except socket.timeout:
                if self._state != WSState.OPEN:
                    return None
                continue
            except Exception:
                return None
        return data

    def _send_frame(self, opcode: int, payload: bytes):
        """Send a WebSocket frame."""
        if not self._socket or self._state != WSState.OPEN:
            return

        frame = bytearray()
        frame.append(0x80 | opcode)  # FIN + opcode

        length = len(payload)
        if length < 126:
            frame.append(length)
        elif length < 65536:
            frame.append(126)
            frame.extend(struct.pack("!H", length))
        else:
            frame.append(127)
            frame.extend(struct.pack("!Q", length))

        frame.extend(payload)

        try:
            self._socket.sendall(bytes(frame))
        except Exception:
            self._handle_close(1001, "Send gagal")

    # ==================== Send Methods ====================

    def send(self, data: Union[str, dict, list, bytes]):
        """
        Send message.

        Usage:
            ws.send("Hello!")
            ws.send({"type": "chat", "text": "Hello!"})
            ws.send(b"binary data")
        """
        if isinstance(data, (dict, list)):
            payload = json.dumps(data).encode("utf-8")
            self._send_frame(0x01, payload)
        elif isinstance(data, str):
            self._send_frame(0x01, data.encode("utf-8"))
        elif isinstance(data, bytes):
            self._send_frame(0x02, data)
        else:
            self._send_frame(0x01, str(data).encode("utf-8"))

    def send_text(self, text: str):
        """Send text message."""
        self._send_frame(0x01, text.encode("utf-8"))

    def send_json(self, data: Union[dict, list]):
        """Send JSON message."""
        self._send_frame(0x01, json.dumps(data).encode("utf-8"))

    def send_binary(self, data: bytes):
        """Send binary message."""
        self._send_frame(0x02, data)

    # ==================== Disconnect ====================

    def disconnect(self, code: int = 1000, reason: str = "Client disconnect"):
        """Disconnect from server."""
        if self._state == WSState.CLOSED:
            return

        self._state = WSState.CLOSING

        try:
            # Send close frame
            close_payload = struct.pack("!H", code) + reason.encode("utf-8")
            self._send_frame(0x08, close_payload)
        except Exception:
            pass

        self._state = WSState.CLOSED
        self._emit("close", code, reason)

        if self._socket:
            try:
                self._socket.close()
            except Exception:
                pass
            self._socket = None

    # ==================== Reconnect ====================

    def _handle_close(self, code: int, reason: str):
        """Handle connection close."""
        self._state = WSState.CLOSED
        if self._socket:
            try:
                self._socket.close()
            except Exception:
                pass
            self._socket = None

        self._emit("close", code, reason)

        if self._auto_reconnect:
            self._schedule_reconnect()

    def _schedule_reconnect(self):
        """Schedule reconnection with exponential backoff."""
        if self._reconnect_attempts >= self._max_reconnect_attempts:
            self._emit("error", Exception(
                f"Max reconnect attempts ({self._max_reconnect_attempts}) tercapai"
            ))
            return

        self._state = WSState.RECONNECTING
        delay = min(
            self._reconnect_delay * (2 ** self._reconnect_attempts),
            self._max_reconnect_delay
        )
        self._reconnect_attempts += 1

        self._emit("reconnect", {
            "attempt": self._reconnect_attempts,
            "delay": delay,
            "max_attempts": self._max_reconnect_attempts,
        })

        def _reconnect_after_delay():
            time.sleep(delay)
            if self._state == WSState.RECONNECTING:
                try:
                    self._do_connect()
                except Exception as e:
                    self._emit("error", e)
                    self._schedule_reconnect()

        thread = threading.Thread(target=_reconnect_after_delay, daemon=True)
        thread.start()

    # ==================== State ====================

    @property
    def state(self) -> WSState:
        """Get connection state."""
        return self._state

    @property
    def is_connected(self) -> bool:
        """Check if connected."""
        return self._state == WSState.OPEN

    @property
    def url(self) -> str:
        """Get server URL."""
        return self._url

    def __repr__(self):
        return f"<WebSocketClient url='{self._url}' state={self._state.value}>"


# ==================== WebSocket Manager ====================

class WebSocketManager:
    """
    Manage multiple WebSocket connections.

    Usage:
        manager = WebSocketManager()

        manager.add("chat", "ws://localhost:8080/chat")
        manager.add("notifications", "ws://localhost:8080/notify")

        manager.on("chat", "message", lambda data: print(f"Chat: {data}"))
        manager.on("notifications", "message", lambda data: print(f"Notify: {data}"))

        manager.connect_all()
        manager.send("chat", {"type": "message", "text": "Hello!"})
    """

    def __init__(self):
        self._clients: Dict[str, WebSocketClient] = {}
        self._shared_handlers: Dict[str, List[Callable]] = {
            "message": [],
            "open": [],
            "close": [],
            "error": [],
        }

    def add(self, name: str, url: str, **kwargs) -> WebSocketManager:
        """Add a new WebSocket connection."""
        client = WebSocketClient(url, **kwargs)

        # Add shared handlers
        for event, handlers in self._shared_handlers.items():
            for handler in handlers:
                client.on(event, lambda data, n=name: handler(n, data))

        self._clients[name] = client
        return self

    def remove(self, name: str):
        """Remove a connection."""
        if name in self._clients:
            self._clients[name].disconnect()
            del self._clients[name]

    def get(self, name: str) -> Optional[WebSocketClient]:
        """Get a client by name."""
        return self._clients.get(name)

    def on(self, name: str, event: str, handler: Callable):
        """Register handler for specific connection."""
        if name in self._clients:
            self._clients[name].on(event, handler)

    def on_all(self, event: str, handler: Callable):
        """Register handler for all connections."""
        self._shared_handlers[event].append(handler)

    def connect(self, name: str, **kwargs):
        """Connect a specific client."""
        if name in self._clients:
            self._clients[name].connect(**kwargs)

    def connect_all(self, **kwargs):
        """Connect all clients."""
        for name, client in self._clients.items():
            try:
                client.connect(**kwargs)
            except Exception as e:
                print(f"  ⚠️ Gagal koneksi '{name}': {e}")

    def disconnect(self, name: str):
        """Disconnect a specific client."""
        if name in self._clients:
            self._clients[name].disconnect()

    def disconnect_all(self):
        """Disconnect all clients."""
        for client in self._clients.values():
            client.disconnect()

    def send(self, name: str, data: Any):
        """Send message to specific connection."""
        if name in self._clients:
            self._clients[name].send(data)

    def send_all(self, data: Any):
        """Send message to all connections."""
        for client in self._clients.values():
            if client.is_connected:
                client.send(data)

    def broadcast(self, data: Any, exclude: Optional[str] = None):
        """Broadcast message to all except one."""
        for name, client in self._clients.items():
            if name != exclude and client.is_connected:
                client.send(data)

    @property
    def connected_clients(self) -> List[str]:
        """Get list of connected client names."""
        return [name for name, c in self._clients.items() if c.is_connected]

    @property
    def disconnected_clients(self) -> List[str]:
        """Get list of disconnected client names."""
        return [name for name, c in self._clients.items() if not c.is_connected]

    @property
    def total(self) -> int:
        """Total number of clients."""
        return len(self._clients)

    def get_stats(self) -> Dict[str, Any]:
        """Get connection statistics."""
        return {
            "total": self.total,
            "connected": len(self.connected_clients),
            "disconnected": len(self.disconnected_clients),
            "clients": {
                name: {
                    "url": client.url,
                    "state": client.state.value,
                    "reconnect_attempts": client._reconnect_attempts,
                }
                for name, client in self._clients.items()
            },
        }

    def __repr__(self):
        return (
            f"<WebSocketManager total={self.total} "
            f"connected={len(self.connected_clients)}>"
        )


# ==================== Utility Functions ====================

def create_ws_client(url: str, on_message: Optional[Callable] = None,
                     auto_reconnect: bool = True) -> WebSocketClient:
    """
    Quick create a WebSocket client.

    Usage:
        ws = create_ws_client(
            "ws://localhost:8080",
            on_message=lambda data: print(data),
        )
    """
    client = WebSocketClient(url, auto_reconnect=auto_reconnect)
    if on_message:
        client.on("message", on_message)
    return client


def ws_url(host: str = "localhost", port: int = 8080,
           path: str = "/", secure: bool = False) -> str:
    """Build WebSocket URL."""
    protocol = "wss" if secure else "ws"
    path = path if path.startswith("/") else f"/{path}"
    return f"{protocol}://{host}:{port}{path}"


# ==================== Channel System ====================

class Channel:
    """
    Named communication channel over WebSocket.

    Usage:
        ws = WebSocketClient("ws://localhost:8080")
        channel = Channel("chat", ws)

        channel.on("message", lambda data: print(data))
        channel.send({"text": "Hello!"})

        # Join/leave rooms
        channel.join("room-1")
        channel.leave("room-1")
    """

    def __init__(self, name: str, client: WebSocketClient):
        self.name = name
        self.client = client
        self._handlers: Dict[str, List[Callable]] = {
            "message": [],
            "join": [],
            "leave": [],
        }
        self._rooms: Set[str] = set()

        # Listen for channel messages
        self.client.on("message", self._handle_message)

    def _handle_message(self, data):
        """Handle incoming message and filter by channel."""
        if isinstance(data, dict):
            channel = data.get("channel", "")
            if channel == self.name:
                event = data.get("event", "message")
                payload = data.get("payload", data)
                for handler in self._handlers.get(event, []):
                    try:
                        handler(payload)
                    except Exception:
                        pass

    def on(self, event: str, handler: Callable):
        """Register event handler."""
        self._handlers[event].append(handler)

    def send(self, data: Any, event: str = "message"):
        """Send message on this channel."""
        self.client.send({
            "channel": self.name,
            "event": event,
            "payload": data,
        })

    def join(self, room: str):
        """Join a room."""
        self._rooms.add(room)
        self.send({"room": room}, event="join")

    def leave(self, room: str):
        """Leave a room."""
        self._rooms.discard(room)
        self.send({"room": room}, event="leave")

    @property
    def rooms(self) -> Set[str]:
        """Get joined rooms."""
        return self._rooms.copy()

    def __repr__(self):
        return f"<Channel name='{self.name}' rooms={len(self._rooms)}>"
