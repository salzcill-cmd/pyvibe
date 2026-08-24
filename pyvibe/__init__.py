"""
🐍 PyVibe — Build frontend websites in Python as easy as chatting.

"Gak perlu ribet, yang penting gacor."

Usage:
    from pyvibe import *

    app = App("My Website")
    app.tampil(
        judul("Halo Dunia!"),
        paragraf("Ini website pertama gue."),
    )
    app.jalan()
"""

__version__ = "0.1.0"
__author__ = "PyVibe Team"

from pyvibe.core.app import App
from pyvibe.core.state import State
from pyvibe.core.component import Component
from pyvibe.core.router import Router

# Components - Basic
from pyvibe.components.basic import (
    judul, subjudul, paragraf, teks, teks_teal, teks_tipis, teks_balik,
    gambar, gambar_rounded, video, iframe, tautan, ikon,
    spasi, pemisah, gradien_teks, badge, avatar, progress_bar, chip, count_down,
)

# Components - Input
from pyvibe.components.input import (
    input_teks, input_angka, input_email, input_sandi,
    centang, pilihan, unggah_file, textarea, tombol_kirim,
    tombol, tombol_icon,
)

# Components - Layout
from pyvibe.components.layout import (
    kartu, kolom, baris, bagian, kartu_stat,
    judul_kartu, spacer, grid, kontainer, overlay,
)

# Components - Navigation
from pyvibe.components.navigation import (
    navbar, sidebar, footer, tabs, breadcrumb,
)

# Components - Feedback
from pyvibe.components.feedback import (
    notifikasi, loader, badge_status, alert, skeleton,
)

# Components - Data
from pyvibe.components.data import (
    tabel, grafik_sederhana, daftar, statistik,
)

# Components - Advanced
from pyvibe.components.advanced import (
    carousel, accordion, modal, tooltip, dropdown,
)

# Components - Extras
from pyvibe.components.extras import (
    stepper, timeline, rating, countdown, typing_effect,
    scroll_to_top, galeri, code_block, markdown,
    empty_state, stat_card,
)

# Layout helpers
from pyvibe.style.helpers import (
    tengah, kiri, kanan, rata_kiri, rata_kanan, rata_tengah,
    gelap, terang, gradient,
    bulat, bayangan, border,
    responsif, flex,
)

# Build function shorthand
from pyvibe.core.renderer import tampil

# Natural Language Parser
from pyvibe.parser.natural import nl, nl_parse, NaturalLanguageParser

# Security
from pyvibe.security import Security, csrf_protect, rate_limit, sanitize, escape_html

# Middleware
from pyvibe.middleware import Middleware, MiddlewareManager, CorsMiddleware, LoggerMiddleware, AuthMiddleware, CacheMiddleware

# Events
from pyvibe.events import EventEmitter, Event, emit, on, once

# Cache
from pyvibe.cache import Cache, FileCache

# Errors
from pyvibe.errors import (
    PyVibeError, NotFoundError, ValidationError,
    AuthenticationError, AuthorizationError, ConflictError,
    RateLimitError, ServerError, DatabaseError, FileError, NetworkError,
    ErrorHandler,
)

__all__ = [
    # Core
    "App", "State", "Component", "Router", "tampil",
    # Basic
    "judul", "subjudul", "paragraf", "teks", "teks_teal", "teks_tipis", "teks_balik",
    "gambar", "gambar_rounded", "video", "iframe", "tautan", "ikon",
    "spasi", "pemisah", "gradien_teks", "badge", "avatar", "progress_bar", "chip", "count_down",
    # Input
    "input_teks", "input_angka", "input_email", "input_sandi",
    "centang", "pilihan", "unggah_file", "textarea", "tombol_kirim",
    "tombol", "tombol_icon",
    # Layout
    "kartu", "kolom", "baris", "bagian", "kartu_stat",
    "judul_kartu", "spacer", "grid", "kontainer", "overlay",
    # Navigation
    "navbar", "sidebar", "footer", "tabs", "breadcrumb",
    # Feedback
    "notifikasi", "loader", "badge_status", "alert", "skeleton",
    # Data
    "tabel", "grafik_sederhana", "daftar", "statistik",
    # Advanced
    "carousel", "accordion", "modal", "tooltip", "dropdown",
    # Extras
    "stepper", "timeline", "rating", "countdown", "typing_effect",
    "scroll_to_top", "galeri", "code_block", "markdown",
    "empty_state", "stat_card",
    # Style helpers
    "tengah", "kiri", "kanan", "rata_kiri", "rata_kanan", "rata_tengah",
    "gelap", "terang", "gradient",
    "bulat", "bayangan", "border",
    "responsif", "flex",
    # Natural Language
    "nl", "nl_parse", "NaturalLanguageParser",
    # Security
    "Security", "csrf_protect", "rate_limit", "sanitize", "escape_html",
    # Middleware
    "Middleware", "MiddlewareManager", "CorsMiddleware", "LoggerMiddleware", "AuthMiddleware", "CacheMiddleware",
    # Events
    "EventEmitter", "Event", "emit", "on", "once",
    # Cache
    "Cache", "FileCache",
    # Errors
    "PyVibeError", "NotFoundError", "ValidationError",
    "AuthenticationError", "AuthorizationError", "ConflictError",
    "RateLimitError", "ServerError", "DatabaseError", "FileError", "NetworkError",
    "ErrorHandler",
]
