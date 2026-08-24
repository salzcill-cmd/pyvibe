"""
NL File Format — support untuk file .nl

File .nl adalah format natural language untuk mendeskripsikan halaman web.
Setiap baris adalah instruksi dalam bahasa Indonesia.

Contoh file .nl:

    # navbar
    tampilin navbar dengan logo "MyBrand" dan menu "Home", "About", "Contact"

    # hero section
    tampilin judul "Selamat Datang" di tengah
    tampilin paragraf "Ini website pertama gue."
    tampilin tombol "Mulai" warna ungu

    # features
    tampilin judul "Fitur Kami" di tengah
    tampilin paragraf "Semua fitur yang lo butuhkan."
"""

from __future__ import annotations
import os
from typing import Any, Dict, List, Optional

from pyvibe.parser.natural import NaturalLanguageParser


def load_nl_file(filepath: str) -> str:
    """
    Load file .nl dan return content.

    Usage:
        content = load_nl_file("website.nl")
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def parse_nl_file(filepath: str) -> List[Dict[str, Any]]:
    """
    Parse file .nl jadi list component definitions.

    Usage:
        components = parse_nl_file("website.nl")
        for comp in components:
            print(comp)
    """
    content = load_nl_file(filepath)
    parser = NaturalLanguageParser()
    return parser.parse_block(content)


def nl_file_to_python(filepath: str) -> str:
    """
    Convert file .nl ke Python PyVibe code.

    Usage:
        python_code = nl_file_to_python("website.nl")
        print(python_code)
    """
    content = load_nl_file(filepath)
    parser = NaturalLanguageParser()
    return parser.to_python(content)


def nl_file_to_html(filepath: str) -> str:
    """
    Convert file .nl ke HTML.

    Usage:
        html = nl_file_to_html("website.nl")
    """
    from pyvibe.parser.nl_executor import NLString

    content = load_nl_file(filepath)
    lines = content.split("\n")
    html_parts = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        nl_str = NLString(line)
        html = nl_str.render()
        if html:
            html_parts.append(html)

    return "\n".join(html_parts)


def nl_file_to_app(filepath: str, app_name: str = "NL App") -> Any:
    """
    Convert file .nl ke PyVibe App.

    Usage:
        app = nl_file_to_app("website.nl", "My Website")
        app.jalan()
    """
    from pyvibe.core.app import App
    from pyvibe.core.renderer import tampil
    from pyvibe.parser.nl_executor import NLString

    content = load_nl_file(filepath)
    lines = content.split("\n")

    # Parse components
    components = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        nl_str = NLString(line)
        comp = nl_str._to_component()
        if comp:
            components.append(comp)

    # Create app
    app = App(app_name)

    @app.route("/")
    def beranda():
        return tampil(*components)

    return app


# ==================== Example NL File Format ====================

EXAMPLE_NL_CONTENT = """# 🐍 PyVibe NL File Example
# File ini mendeskripsikan halaman web dalam bahasa Indonesia

# Navbar
tampilin navbar dengan logo "MyBrand" dan menu "Home", "About", "Contact"

# Hero Section
tampilin judul "Selamat Datang di MyBrand" di tengah
tampilin paragraf "Kami menyediakan solusi terbaik untuk bisnis Anda." di tengah
tampilin tombol "Mulai Sekarang" warna ungu besar

# Spacer
tampilin spasi

# Features Section
tampilin judul "Fitur Unggulan" di tengah
tampilin paragraf "Semua yang Anda butuhkan dalam satu platform." di tengah

# Feature Cards
tampilin kartu dengan judul "Cepat"
tampilin kartu dengan judul "Mudah"
tampilin kartu dengan judul "Aman"

# CTA Section
tampilin judul "Siap Memulai?" di tengah
tampilin tombol "Hubungi Kami" warna hijau

# Footer
tampilin footer dengan copyright "© 2026 MyBrand"
"""


def create_example_nl_file(filepath: str = "example.nl"):
    """Create example .nl file."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(EXAMPLE_NL_CONTENT)
    print(f"✅ Example NL file created: {filepath}")
    return filepath


if __name__ == "__main__":
    # Create example and show conversion
    print("🐍 NL File Format Demo")
    print("=" * 50)
    print()

    # Create example file
    filepath = create_example_nl_file("example.nl")

    # Show Python conversion
    print("📄 NL File Content:")
    print("-" * 50)
    print(EXAMPLE_NL_CONTENT)

    print("🐍 Python Conversion:")
    print("-" * 50)
    python_code = nl_file_to_python(filepath)
    print(python_code)

    print("📱 HTML Output:")
    print("-" * 50)
    html = nl_file_to_html(filepath)
    print(html[:500] + "..." if len(html) > 500 else html)
