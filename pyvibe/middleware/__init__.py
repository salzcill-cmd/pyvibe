"""
PyVibe Middleware — request/response processing pipeline.

Usage:
    from pyvibe.middleware import Middleware, CorsMiddleware, LoggerMiddleware

    # Add middleware to app
    app = App("My Website")
    app.add_middleware(CorsMiddleware())
    app.add_middleware(LoggerMiddleware())

    # Custom middleware
    class MyMiddleware(Middleware):
        def process_request(self, request):
            # Do something before request
            request["start_time"] = time.time()

        def process_response(self, request, response):
            # Do something after request
            duration = time.time() - request["start_time"]
            print(f"Request took {duration:.2f}s")
"""

from __future__ import annotations
import time
import json
from typing import Any, Callable, Dict, List, Optional
from functools import wraps


class Middleware:
    """Base middleware class."""

    def process_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process request before handler. Return modified request or None."""
        return request

    def process_response(self, request: Dict[str, Any], response: Any) -> Any:
        """Process response after handler. Return modified response."""
        return response

    def process_error(self, request: Dict[str, Any], error: Exception) -> Any:
        """Process error. Return error response."""
        return {"error": str(error)}


class CorsMiddleware(Middleware):
    """CORS middleware."""

    def __init__(self, origins: Optional[List[str]] = None, methods: Optional[List[str]] = None):
        self.origins = origins or ["*"]
        self.methods = methods or ["GET", "POST", "PUT", "DELETE", "OPTIONS"]

    def process_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        request["cors_origins"] = self.origins
        request["cors_methods"] = self.methods
        return request

    def process_response(self, request: Dict[str, Any], response: Any) -> Any:
        headers = {
            "Access-Control-Allow-Origin": ", ".join(self.origins),
            "Access-Control-Allow-Methods": ", ".join(self.methods),
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        }
        if isinstance(response, dict):
            response["_headers"] = headers
        return response


class LoggerMiddleware(Middleware):
    """Request logger middleware."""

    def __init__(self, log_file: Optional[str] = None):
        self.log_file = log_file

    def process_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        request["start_time"] = time.time()
        return request

    def process_response(self, request: Dict[str, Any], response: Any) -> Any:
        duration = time.time() - request.get("start_time", time.time())
        method = request.get("method", "GET")
        path = request.get("path", "/")
        status = request.get("status", 200)

        log_msg = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {method} {path} - {status} ({duration:.3f}s)"

        if self.log_file:
            with open(self.log_file, "a") as f:
                f.write(log_msg + "\n")
        else:
            print(log_msg)

        return response


class TimingMiddleware(Middleware):
    """Request timing middleware."""

    def process_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        request["start_time"] = time.time()
        return request

    def process_response(self, request: Dict[str, Any], response: Any) -> Any:
        duration = time.time() - request.get("start_time", time.time())
        if isinstance(response, dict):
            response["_timing"] = f"{duration:.3f}s"
        return response


class SecurityHeadersMiddleware(Middleware):
    """Security headers middleware."""

    def __init__(self, headers: Optional[Dict[str, str]] = None):
        self.headers = headers or {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
        }

    def process_response(self, request: Dict[str, Any], response: Any) -> Any:
        if isinstance(response, dict):
            response["_headers"] = self.headers
        return response


class JsonBodyMiddleware(Middleware):
    """Parse JSON body middleware."""

    def process_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        body = request.get("body", "")
        if isinstance(body, str) and body:
            try:
                request["json"] = json.loads(body)
            except json.JSONDecodeError:
                request["json"] = None
        return request


class AuthMiddleware(Middleware):
    """Authentication middleware."""

    def __init__(self, auth_func: Optional[Callable] = None):
        self.auth_func = auth_func

    def process_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        token = request.get("headers", {}).get("Authorization", "")
        if token.startswith("Bearer "):
            token = token[7:]

        if self.auth_func and token:
            user = self.auth_func(token)
            request["user"] = user

        return request


class CacheMiddleware(Middleware):
    """Simple cache middleware."""

    def __init__(self, ttl: int = 300):
        self.ttl = ttl
        self.cache: Dict[str, Dict[str, Any]] = {}

    def process_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if request.get("method") == "GET":
            cache_key = request.get("path", "/")
            if cache_key in self.cache:
                cached = self.cache[cache_key]
                if time.time() - cached["time"] < self.ttl:
                    request["_cached"] = cached["response"]
                    return request
        return request

    def process_response(self, request: Dict[str, Any], response: Any) -> Any:
        if request.get("method") == "GET" and not request.get("_cached"):
            cache_key = request.get("path", "/")
            self.cache[cache_key] = {
                "response": response,
                "time": time.time(),
            }
        return response


# ==================== Middleware Manager ====================

class MiddlewareManager:
    """Manage middleware stack."""

    def __init__(self):
        self.middleware: List[Middleware] = []

    def add(self, middleware: Middleware):
        """Add middleware to stack."""
        self.middleware.append(middleware)

    def remove(self, middleware: Middleware):
        """Remove middleware from stack."""
        self.middleware.remove(middleware)

    def process_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process request through all middleware."""
        for mw in self.middleware:
            request = mw.process_request(request)
            if request is None:
                return None
        return request

    def process_response(self, request: Dict[str, Any], response: Any) -> Any:
        """Process response through all middleware."""
        for mw in reversed(self.middleware):
            response = mw.process_response(request, response)
        return response

    def process_error(self, request: Dict[str, Any], error: Exception) -> Any:
        """Process error through all middleware."""
        for mw in reversed(self.middleware):
            response = mw.process_error(request, error)
            if response:
                return response
        return {"error": str(error)}
