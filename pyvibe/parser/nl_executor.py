"""
NL Executor — eksekusi natural language syntax langsung di Python.

Ini memungkinkan lo nulis kode seperti ini:

    from pyvibe.nl import *

    app = App("My Website")

    @app.route("/")
    def beranda():
        return tampil(
            "tampilin judul 'Selamat Datang' di tengah",
            "tampilin paragraf 'Halo, ini website gue.'",
            "tampilin tombol 'Klik Saya' warna ungu",
        )

    app.jalan()

Atau langsung execute NL code:

    from pyvibe.nl import run_nl

    run_nl('''
    tampilin judul "Halo Dunia" di tengah
    tampilin paragraf "Ini website pertama gue."
    tampilin tombol "Klik Saya" warna ungu
    ''')
"""

from __future__ import annotations
import re
from typing import Any, Dict, List, Optional, Union

from pyvibe.core.component import Component
from pyvibe.parser.natural import NaturalLanguageParser


# ==================== NL String Handler ====================

class NLString:
    """
    Wrapper untuk NL syntax string yang bisa di-render langsung.

    Usage:
        # Di dalam tampil()
        tampil(
            NLString('tampilin judul "Halo" di tengah'),
            NLString('tampilin paragraf "Dunia"'),
        )
    """

    def __init__(self, nl_code: str):
        self.nl_code = nl_code
        self.parser = NaturalLanguageParser()
        self._parsed = self.parser.parse(nl_code)
        self._component = None

    def render(self, indent: int = 0) -> str:
        """Render NL string ke HTML."""
        component = self._to_component()
        if component:
            return component.render(indent)
        return f"<!-- NL: {self.nl_code} -->"

    def _to_component(self) -> Optional[Component]:
        """Convert NL string ke Component object."""
        if self._component:
            return self._component

        if not self._parsed:
            return None

        from pyvibe.components.basic import judul, subjudul, paragraf, teks, gambar, tautan, ikon, badge, chip
        from pyvibe.components.input import tombol, tombol_icon, input_teks, input_angka, input_email, input_sandi, centang, pilihan, textarea
        from pyvibe.components.layout import kartu, kolom, baris, bagian, spacer, grid, kontainer
        from pyvibe.components.navigation import navbar, sidebar, footer, tabs, breadcrumb
        from pyvibe.components.feedback import notifikasi, alert, loader, badge_status, skeleton
        from pyvibe.components.data import tabel, grafik_sederhana, daftar
        from pyvibe.components.advanced import carousel, accordion, modal

        p = self._parsed
        comp_name = p["component"]
        content = p["content"]
        styles = p["styles"]
        props = p["props"]

        # Map component names to functions
        comp_map = {
            "judul": lambda: judul(content),
            "subjudul": lambda: subjudul(content),
            "paragraf": lambda: paragraf(content),
            "teks": lambda: teks(content),
            "gambar": lambda: gambar(content),
            "tautan": lambda: tautan(content, url=props.get("url", props.get("href", "#"))),
            "ikon": lambda: ikon(content),
            "badge": lambda: badge(content),
            "chip": lambda: chip(content),
            "tombol": lambda: tombol(content, warna=props.get("warna", "ungu")),
            "tombol_icon": lambda: tombol_icon(content),
            "input_teks": lambda: input_teks(label=content),
            "input_angka": lambda: input_angka(label=content),
            "input_email": lambda: input_email(label=content),
            "input_sandi": lambda: input_sandi(label=content),
            "textarea": lambda: textarea(label=content),
            "centang": lambda: centang(content),
            "pilihan": lambda: pilihan(label=content),
            "kartu": lambda: kartu(judul=content) if content else kartu(),
            "kolom": lambda: kolom(int(props.get("width", "6"))),
            "baris": lambda: baris(),
            "bagian": lambda: bagian(),
            "grid": lambda: grid(),
            "kontainer": lambda: kontainer(),
            "spacer": lambda: spacer(props.get("height", "24px")),
            "navbar": lambda: navbar(logo=content or "PyVibe"),
            "sidebar": lambda: sidebar(),
            "footer": lambda: footer(copyright=content),
            "tabs": lambda: tabs(),
            "breadcrumb": lambda: breadcrumb(),
            "notifikasi": lambda: notifikasi(content, tipe=props.get("tipe", "info")),
            "alert": lambda: alert(content, tipe=props.get("tipe", "info")),
            "loader": lambda: loader(),
            "badge_status": lambda: badge_status(content, status=props.get("status", "default")),
            "skeleton": lambda: skeleton(),
            "tabel": lambda: tabel(data=[]),
            "grafik_sederhana": lambda: grafik_sederhana(data=[]),
            "daftar": lambda: daftar(),
            "carousel": lambda: carousel(),
            "accordion": lambda: accordion(),
            "modal": lambda: modal(content),
        }

        if comp_name not in comp_map:
            return None

        comp = comp_map[comp_name]()

        # Apply styles
        style_map = {
            "tengah": lambda c: c.tengah(),
            "kiri": lambda c: c.kiri(),
            "kanan": lambda c: c.kanan(),
            "besar": lambda c: c.besar(),
            "kecil": lambda c: c.kecil(),
            "tebal": lambda c: c.tebal(),
            "tipis": lambda c: c.tipis(),
            "bulat": lambda c: c.bulat(),
        }

        for style in styles:
            if style in style_map:
                comp = style_map[style](comp)
            elif style.startswith("warna_"):
                color = style.replace("warna_", "")
                comp = comp.warna(color)
            elif style == "bayangan":
                comp = comp.bayangan("md")
            elif style == "gradient":
                comp = comp.bg("gradient-ungu")

        self._component = comp
        return comp

    def to_dict(self) -> Dict[str, Any]:
        """Serialize ke dictionary."""
        return {
            "type": "NLString",
            "nl_code": self.nl_code,
            "parsed": self._parsed,
        }


# ==================== Helper Functions ====================

def nl(*nl_codes: str) -> List[Union[NLString, str]]:
    """
    Create multiple NL strings.

    Usage:
        return tampil(
            *nl(
                'tampilin judul "Halo" di tengah',
                'tampilin paragraf "Dunia"',
                'tampilin tombol "Klik" warna ungu',
            )
        )
    """
    return [NLString(code) for code in nl_codes]


def nl_file(filepath: str) -> str:
    """
    Load and convert NL file ke Python code.

    Usage:
        python_code = nl_file("website.nl")
        print(python_code)
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    parser = NaturalLanguageParser()
    return parser.to_python(content)


def run_nl(nl_code: str, output_dir: str = "output"):
    """
    Execute NL code langsung dan generate HTML.

    Usage:
        run_nl('''
        tampilin judul "Halo Dunia" di tengah
        tampilin paragraf "Ini website pertama gue."
        tampilin tombol "Klik Saya" warna ungu
        ''')
    """
    from pyvibe.core.app import App
    from pyvibe.core.renderer import tampil

    app = App("NL Website")

    # Parse NL code
    parser = NaturalLanguageParser()
    parsed_lines = parser.parse_block(nl_code)

    # Convert to components
    components = []
    for p in parsed_lines:
        nl_str = NLString(p["raw"])
        comp = nl_str._to_component()
        if comp:
            components.append(comp)

    # Create route
    @app.route("/")
    def beranda():
        return tampil(*components)

    # Export
    app.export(output_dir)
    print(f"✅ Website exported ke {output_dir}/")


# ==================== NL Context Manager ====================

class NLContext:
    """
    Context manager untuk NL syntax.

    Usage:
        with NLContext() as nl:
            nl.tampilin_judul("Halo", tengah=True)
            nl.tampilin_paragraf("Dunia")
            nl.tampilin_tombol("Klik", warna="ungu")

        # Get rendered HTML
        html = nl.render()
    """

    def __init__(self):
        self.components: List[Component] = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def tampilin_judul(self, teks: str, **kwargs):
        from pyvibe.components.basic import judul
        comp = judul(teks)
        for k, v in kwargs.items():
            if hasattr(comp, k):
                getattr(comp, k)() if v is True else getattr(comp, k)(v)
        self.components.append(comp)

    def tampilin_paragraf(self, teks: str, **kwargs):
        from pyvibe.components.basic import paragraf
        comp = paragraf(teks)
        for k, v in kwargs.items():
            if hasattr(comp, k):
                getattr(comp, k)() if v is True else getattr(comp, k)(v)
        self.components.append(comp)

    def tampilin_tombol(self, teks: str, warna: str = "ungu", **kwargs):
        from pyvibe.components.input import tombol
        comp = tombol(teks, warna=warna, **kwargs)
        self.components.append(comp)

    def tampilin_gambar(self, src: str, **kwargs):
        from pyvibe.components.basic import gambar
        comp = gambar(src, **kwargs)
        self.components.append(comp)

    def render(self) -> str:
        from pyvibe.core.renderer import Renderer
        renderer = Renderer()
        return renderer.render(*self.components)
