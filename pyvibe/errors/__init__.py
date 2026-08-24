"""
PyVibe Errors — error handling dengan pesan Bahasa Indonesia.

Usage:
    from pyvibe.errors import PyVibeError, NotFoundError, ValidationError

    raise NotFoundError("Halaman tidak ditemukan")
    raise ValidationError("Email sudah terdaftar")
"""

from __future__ import annotations
from typing import Any, Dict, Optional


class PyVibeError(Exception):
    """Base exception untuk PyVibe."""

    def __init__(self, message: str = "Terjadi kesalahan", code: str = "error", status: int = 500):
        self.message = message
        self.code = code
        self.status = status
        super().__init__(message)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": self.message,
            "code": self.code,
            "status": self.status,
        }


class NotFoundError(PyVibeError):
    """404 Not Found."""

    def __init__(self, resource: str = "Resource"):
        super().__init__(
            message=f"{resource} tidak ditemukan.",
            code="not_found",
            status=404,
        )


class ValidationError(PyVibeError):
    """400 Validation Error."""

    def __init__(self, message: str = "Data tidak valid", field: Optional[str] = None):
        super().__init__(
            message=message,
            code="validation_error",
            status=400,
        )
        self.field = field

    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        if self.field:
            result["field"] = self.field
        return result


class AuthenticationError(PyVibeError):
    """401 Unauthorized."""

    def __init__(self, message: str = "Anda belum masuk. Silakan login terlebih dahulu."):
        super().__init__(
            message=message,
            code="unauthorized",
            status=401,
        )


class AuthorizationError(PyVibeError):
    """403 Forbidden."""

    def __init__(self, message: str = "Anda tidak memiliki akses ke resource ini."):
        super().__init__(
            message=message,
            code="forbidden",
            status=403,
        )


class ConflictError(PyVibeError):
    """409 Conflict."""

    def __init__(self, message: str = "Data sudah ada."):
        super().__init__(
            message=message,
            code="conflict",
            status=409,
        )


class RateLimitError(PyVibeError):
    """429 Too Many Requests."""

    def __init__(self, message: str = "Terlalu banyak permintaan. Silakan coba lagi nanti."):
        super().__init__(
            message=message,
            code="rate_limit",
            status=429,
        )


class ServerError(PyVibeError):
    """500 Internal Server Error."""

    def __init__(self, message: str = "Terjadi kesalahan pada server."):
        super().__init__(
            message=message,
            code="server_error",
            status=500,
        )


class DatabaseError(PyVibeError):
    """Database error."""

    def __init__(self, message: str = "Terjadi kesalahan pada database."):
        super().__init__(
            message=message,
            code="database_error",
            status=500,
        )


class FileError(PyVibeError):
    """File operation error."""

    def __init__(self, message: str = "Terjadi kesalahan saat memproses file."):
        super().__init__(
            message=message,
            code="file_error",
            status=500,
        )


class NetworkError(PyVibeError):
    """Network error."""

    def __init__(self, message: str = "Terjadi kesalahan jaringan."):
        super().__init__(
            message=message,
            code="network_error",
            status=502,
        )


# ==================== Error Handler ====================

class ErrorHandler:
    """Handle errors dan generate error response."""

    def __init__(self, debug: bool = False):
        self.debug = debug
        self.handlers = {}

    def register(self, error_class: type, handler: callable):
        """Register custom error handler."""
        self.handlers[error_class] = handler

    def handle(self, error: Exception) -> Dict[str, Any]:
        """Handle error and return response."""
        # Check custom handlers
        for error_class, handler in self.handlers.items():
            if isinstance(error, error_class):
                return handler(error)

        # Default handling
        if isinstance(error, PyVibeError):
            response = error.to_dict()
        else:
            response = {
                "error": str(error) if self.debug else "Terjadi kesalahan.",
                "code": "error",
                "status": 500,
            }

        return response

    def render_error_page(self, error: Exception) -> str:
        """Render error page HTML."""
        if isinstance(error, PyVibeError):
            status = error.status
            message = error.message
        else:
            status = 500
            message = "Terjadi kesalahan" if not self.debug else str(error)

        return f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error {status}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #F9FAFB; }}
        .error-container {{ text-align: center; padding: 48px; }}
        .error-code {{ font-size: 6rem; font-weight: 700; color: #7C3AED; line-height: 1; }}
        .error-message {{ font-size: 1.25rem; color: #6B7280; margin: 16px 0 32px; }}
        .error-btn {{ display: inline-block; padding: 12px 24px; background: #7C3AED; color: white; text-decoration: none; border-radius: 8px; font-weight: 500; }}
        .error-btn:hover {{ opacity: 0.9; }}
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-code">{status}</div>
        <div class="error-message">{message}</div>
        <a href="/" class="error-btn">Kembali ke Beranda</a>
    </div>
</body>
</html>"""
