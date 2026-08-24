"""
🐍 PyVibe — Build frontend websites in Python as easy as chatting.

"Gak perlu ribet, yang penting gacor."

v0.3.0 — Complete Framework with Advanced Features

Usage:
    from pyvibe import *

    app = App("My Website")
    app.tampil(
        judul("Halo Dunia!"),
        paragraf("Ini website pertama gue."),
    )
    app.jalan()
"""

__version__ = "0.3.0"
__author__ = "PyVibe Team"

# Core
from pyvibe.core.app import App
from pyvibe.core.state import State
from pyvibe.core.component import Component, Teks
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

# Components - Modern
from pyvibe.components.modern import (
    pagination, toast, switch, avatar_group,
    date_picker, color_picker, range_slider,
    empty_state_modern, command_palette, stat_grid,
)

# Components - Charts
from pyvibe.components.charts import (
    chart_bar, chart_line, chart_pie, chart_doughnut,
    chart_sparkline, chart_progress_ring,
)

# Components - Advanced UI
from pyvibe.components.advanced_ui import (
    calendar_component, kanban, video_player,
    timeline_enhanced, infinite_scroll, notification_center,
    theme_toggle, search_command,
)

# Layout helpers
from pyvibe.style.helpers import (
    tengah, kiri, kanan, rata_kiri, rata_kanan, rata_tengah,
    gelap, terang, gradient,
    bulat, bayangan, border,
    responsif, flex,
)

# Style system
from pyvibe.style import (
    Theme, Animation, Responsive,
    get_theme, list_themes, list_animations,
)

# Forms system
from pyvibe.forms import (
    Form, Field, FormBuilder, Validators,
    form_kontak, form_login, form_register, form_search,
)

# Build function shorthand
from pyvibe.core.renderer import tampil

# Natural Language Parser
from pyvibe.parser.natural import nl, nl_parse, NaturalLanguageParser

# Security
from pyvibe.security import Security, csrf_protect, rate_limit, sanitize, escape_html

# Middleware
from pyvibe.middleware import (
    Middleware, MiddlewareManager, CorsMiddleware, LoggerMiddleware,
    AuthMiddleware, CacheMiddleware, TimingMiddleware, SecurityHeadersMiddleware,
)

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

# Database
from pyvibe.database import Database, Model, QuerySet

# Auth
from pyvibe.auth import Auth, User

# i18n
from pyvibe.i18n import t as i18n_t, set_locale, get_locale

# Deploy
from pyvibe.deploy import Vercel, Netlify, GitHubPages, Docker

# Plugins
from pyvibe.plugins import Plugin, PluginManager

# Testing
from pyvibe.testing import Client, TestCase

# Reactivity
from pyvibe.reactivity import ReactiveStore, ReactiveDict, computed, watch, watch_all, batch

# Navigation & SEO
from pyvibe.navigation import (
    Router as EnhancedRouter, SEO, SitemapGenerator, RobotsGenerator,
    use_params, use_query, build_url, redirect,
)

# Hooks
from pyvibe.hooks import (
    use_local_storage, use_debounce, use_throttle, use_memo,
    use_effect, use_interval, use_timeout, use_previous,
    use_counter, use_toggle, use_list,
    LocalStorage,
)

# Logging
from pyvibe.logging import (
    Logger, get_logger, setup_logging, LogLevel,
)

# Performance
from pyvibe.performance import (
    monitor, timer, profile, benchmark, get_timer,
    Timer, get_memory_usage, CacheStats,
)

__all__ = [
    # Core
    "App", "State", "Component", "Teks", "Router", "tampil",
    
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
    
    # Modern
    "pagination", "toast", "switch", "avatar_group",
    "date_picker", "color_picker", "range_slider",
    "empty_state_modern", "command_palette", "stat_grid",
    
    # Charts
    "chart_bar", "chart_line", "chart_pie", "chart_doughnut",
    "chart_sparkline", "chart_progress_ring",
    
    # Advanced UI
    "calendar_component", "kanban", "video_player",
    "timeline_enhanced", "infinite_scroll", "notification_center",
    "theme_toggle", "search_command",
    
    # Style helpers
    "tengah", "kiri", "kanan", "rata_kiri", "rata_kanan", "rata_tengah",
    "gelap", "terang", "gradient",
    "bulat", "bayangan", "border",
    "responsif", "flex",
    
    # Style system
    "Theme", "Animation", "Responsive",
    "get_theme", "list_themes", "list_animations",
    
    # Forms
    "Form", "Field", "FormBuilder", "Validators",
    "form_kontak", "form_login", "form_register", "form_search",
    
    # Natural Language
    "nl", "nl_parse", "NaturalLanguageParser",
    
    # Security
    "Security", "csrf_protect", "rate_limit", "sanitize", "escape_html",
    
    # Middleware
    "Middleware", "MiddlewareManager", "CorsMiddleware", "LoggerMiddleware",
    "AuthMiddleware", "CacheMiddleware", "TimingMiddleware", "SecurityHeadersMiddleware",
    
    # Events
    "EventEmitter", "Event", "emit", "on", "once",
    
    # Cache
    "Cache", "FileCache",
    
    # Errors
    "PyVibeError", "NotFoundError", "ValidationError",
    "AuthenticationError", "AuthorizationError", "ConflictError",
    "RateLimitError", "ServerError", "DatabaseError", "FileError", "NetworkError",
    "ErrorHandler",
    
    # Database
    "Database", "Model", "QuerySet",
    
    # Auth
    "Auth", "User",
    
    # i18n
    "i18n_t", "set_locale", "get_locale",
    
    # Deploy
    "Vercel", "Netlify", "GitHubPages", "Docker",
    
    # Plugins
    "Plugin", "PluginManager",
    
    # Testing
    "Client", "TestCase",
    
    # Reactivity
    "ReactiveStore", "ReactiveDict", "computed", "watch", "watch_all", "batch",
    
    # Navigation & SEO
    "SEO", "SitemapGenerator", "RobotsGenerator",
    "use_params", "use_query", "build_url", "redirect",
    
    # Hooks
    "use_local_storage", "use_debounce", "use_throttle", "use_memo",
    "use_effect", "use_interval", "use_timeout", "use_previous",
    "use_counter", "use_toggle", "use_list", "LocalStorage",
    
    # Logging
    "Logger", "get_logger", "setup_logging", "LogLevel",
    
    # Performance
    "monitor", "timer", "profile", "benchmark", "get_timer",
    "Timer", "get_memory_usage", "CacheStats",
]
