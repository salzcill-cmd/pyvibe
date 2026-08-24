"""
🐍 PyVibe Error Boundary — Tangkap error, tampilkan fallback UI.

"Error gak bikin crash, tetap cantik."

Features:
- ErrorBoundary — Catch render errors, show fallback
- FallbackRenderer — Custom fallback UI
- ErrorLogger — Log errors to console/file
- RecoveryBoundary — Auto-retry on error

Usage:
    from pyvibe.error_boundary import ErrorBoundary, FallbackRenderer

    # Wrap components with error boundary
    boundary = ErrorBoundary(
        fallback=paragraf("Terjadi kesalahan!"),
        on_error=lambda e: print(f"Error: {e}"),
    )
    boundary.add(judul("Hello"))
    boundary.add(broken_component)
    html = boundary.render()

    # Auto recovery
    recovery = RecoveryBoundary(max_retries=3)
"""

from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, Union
from dataclasses import dataclass, field
import traceback
import time
import json


@dataclass
class ErrorInfo:
    """Information about a caught error."""
    message: str
    component: str = ""
    timestamp: float = 0.0
    stack: str = ""
    retry_count: int = 0

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = time.time()

    def to_dict(self) -> Dict:
        return {
            "message": self.message,
            "component": self.component,
            "timestamp": self.timestamp,
            "stack": self.stack,
            "retry_count": self.retry_count,
        }


class ErrorBoundary:
    """
    Catch errors during component rendering and show fallback UI.

    Usage:
        boundary = ErrorBoundary(
            fallback=paragraf("Something went wrong!"),
            on_error=lambda e: print(f"Caught: {e.message}"),
        )
        boundary.add(judul("Hello"))
        boundary.add(broken_component)  # If this fails, shows fallback
        html = boundary.render()
    """

    def __init__(self, fallback: Any = None,
                 on_error: Optional[Callable] = None,
                 show_details: bool = False,
                 log_errors: bool = True):
        self._children: List[Any] = []
        self._fallback = fallback
        self._on_error = on_error
        self._show_details = show_details
        self._log_errors = log_errors
        self._errors: List[ErrorInfo] = []
        self._has_error = False
        self._error_component = None

    def add(self, *children) -> ErrorBoundary:
        """Add child components to boundary."""
        for child in children:
            self._children.append(child)
        return self

    def render(self) -> str:
        """Render children, catching any errors."""
        from pyvibe.core.renderer import Renderer
        renderer = Renderer()
        rendered = []

        for child in self._children:
            try:
                if hasattr(child, "render"):
                    html = child.render()
                elif callable(child):
                    result = child()
                    html = result if isinstance(result, str) else str(result)
                else:
                    html = str(child)
                rendered.append(html)
            except Exception as e:
                self._has_error = True
                error_info = ErrorInfo(
                    message=str(e),
                    component=getattr(child, "__class__", type(child)).__name__,
                    stack=traceback.format_exc(),
                )
                self._errors.append(error_info)

                if self._log_errors:
                    print(f"  ⚠️ ErrorBoundary caught: {e}")

                if self._on_error:
                    try:
                        self._on_error(error_info)
                    except Exception:
                        pass

                # Render fallback for this component
                if self._fallback:
                    if hasattr(self._fallback, "render"):
                        rendered.append(self._fallback.render())
                    elif callable(self._fallback):
                        result = self._fallback(error_info)
                        rendered.append(result if isinstance(result, str) else str(result))
                    else:
                        rendered.append(str(self._fallback))
                elif self._show_details:
                    rendered.append(self._error_detail(error_info))
                else:
                    rendered.append(
                        '<div style="padding:16px;color:#EF4444;'
                        'border:1px solid #FCA5A5;border-radius:8px;'
                        'background:#FEF2F2;">⚠️ Component error</div>'
                    )

        return "\n".join(rendered)

    def _error_detail(self, error: ErrorInfo) -> str:
        """Render detailed error UI."""
        return (
            f'<div style="padding:16px;border:1px solid #FCA5A5;'
            f'border-radius:8px;background:#FEF2F2;font-family:monospace;">'
            f'<strong style="color:#EF4444;">⚠️ Error in {error.component}</strong>'
            f'<pre style="margin-top:8px;font-size:12px;color:#7F1D1D;'
            f'white-space:pre-wrap;overflow:auto;">{error.message}</pre>'
            f'</div>'
        )

    @property
    def has_error(self) -> bool:
        return self._has_error

    @property
    def errors(self) -> List[ErrorInfo]:
        return self._errors

    def clear_errors(self):
        self._errors.clear()
        self._has_error = False


class FallbackRenderer:
    """
    Pre-built fallback UI renderers.

    Usage:
        html = FallbackRenderer.error_card("Something broke!")
        html = FallbackRenderer.loading_skeleton()
        html = FallbackRenderer.not_found("Page not found")
    """

    @staticmethod
    def error_card(message: str = "Terjadi kesalahan",
                   details: str = "", icon: str = "⚠️") -> str:
        """Render error card."""
        details_html = ""
        if details:
            details_html = (
                f'<pre style="margin-top:8px;font-size:12px;color:#6B7280;'
                f'white-space:pre-wrap;">{details}</pre>'
            )
        return (
            f'<div style="padding:24px;border:1px solid #FCA5A5;'
            f'border-radius:12px;background:#FEF2F2;text-align:center;'
            f'font-family:-apple-system,sans-serif;">'
            f'<div style="font-size:48px;margin-bottom:12px;">{icon}</div>'
            f'<h3 style="color:#991B1B;margin-bottom:8px;">{message}</h3>'
            f'{details_html}'
            f'</div>'
        )

    @staticmethod
    def not_found(message: str = "Halaman tidak ditemukan",
                  code: str = "404") -> str:
        """Render not-found UI."""
        return (
            f'<div style="padding:64px 24px;text-align:center;'
            f'font-family:-apple-system,sans-serif;">'
            f'<div style="font-size:72px;color:#D1D5DB;">{code}</div>'
            f'<h2 style="color:#374151;margin:16px 0 8px;">{message}</h2>'
            f'<p style="color:#6B7280;">Halaman yang kamu cari tidak tersedia.</p>'
            f'</div>'
        )

    @staticmethod
    def loading_skeleton(lines: int = 3) -> str:
        """Render loading skeleton."""
        bars = ""
        for i in range(lines):
            width = f"{70 + (i % 3) * 10}%"
            bars += (
                f'<div style="height:16px;background:#E5E7EB;border-radius:4px;'
                f'margin-bottom:12px;width:{width};'
                f'animation:pulse 2s infinite;"></div>'
            )
        return (
            f'<div style="padding:16px;">'
            f'<style>@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.5}}}}</style>'
            f'{bars}</div>'
        )


class RecoveryBoundary(ErrorBoundary):
    """
    Error boundary with automatic retry.

    Usage:
        recovery = RecoveryBoundary(max_retries=3, retry_delay=1.0)
        recovery.add(unstable_component)
        html = recovery.render()
    """

    def __init__(self, max_retries: int = 3, retry_delay: float = 1.0,
                 **kwargs):
        super().__init__(**kwargs)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._retry_counts: Dict[int, int] = {}

    def render(self) -> str:
        """Render with retry logic."""
        from pyvibe.core.renderer import Renderer
        renderer = Renderer()
        rendered = []

        for idx, child in enumerate(self._children):
            retries = self._retry_counts.get(idx, 0)

            while retries <= self.max_retries:
                try:
                    if hasattr(child, "render"):
                        html = child.render()
                    elif callable(child):
                        result = child()
                        html = result if isinstance(result, str) else str(result)
                    else:
                        html = str(child)
                    rendered.append(html)
                    break
                except Exception as e:
                    retries += 1
                    self._retry_counts[idx] = retries

                    if retries > self.max_retries:
                        error_info = ErrorInfo(
                            message=str(e),
                            component=getattr(child, "__class__", type(child)).__name__,
                            stack=traceback.format_exc(),
                            retry_count=retries,
                        )
                        self._errors.append(error_info)
                        self._has_error = True

                        if self._fallback:
                            if hasattr(self._fallback, "render"):
                                rendered.append(self._fallback.render())
                            else:
                                rendered.append(str(self._fallback))
                        else:
                            rendered.append(
                                f'<div style="padding:16px;color:#EF4444;'
                                f'border:1px solid #FCA5A5;border-radius:8px;'
                                f'background:#FEF2F2;">'
                                f'⚠️ Gagal setelah {retries}x percobaan</div>'
                            )
                    else:
                        time.sleep(self.retry_delay)

        return "\n".join(rendered)


class ErrorCollector:
    """
    Collect errors from multiple boundaries.

    Usage:
        collector = ErrorCollector()
        boundary1 = ErrorBoundary(on_error=collector.collect)
        boundary2 = ErrorBoundary(on_error=collector.collect)

        # Later...
        report = collector.get_report()
    """

    def __init__(self):
        self._errors: List[ErrorInfo] = []

    def collect(self, error: ErrorInfo):
        """Collect an error."""
        self._errors.append(error)

    def get_report(self) -> Dict:
        """Get error report."""
        return {
            "total": len(self._errors),
            "unique_messages": list(set(e.message for e in self._errors)),
            "components": list(set(e.component for e in self._errors)),
            "errors": [e.to_dict() for e in self._errors],
        }

    def to_json(self) -> str:
        """Get report as JSON."""
        return json.dumps(self.get_report(), indent=2, ensure_ascii=False)

    def clear(self):
        """Clear collected errors."""
        self._errors.clear()

    @property
    def count(self) -> int:
        return len(self._errors)
