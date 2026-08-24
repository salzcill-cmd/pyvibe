"""
pyvibe.nl — Natural Language syntax untuk PyVibe.

Import module ini untuk pakai NL syntax langsung:

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
"""

# Import pyvibe first (this brings in the single-arg nl converter)
from pyvibe import *
from pyvibe.parser.nl_executor import NLString, nl as nl_components, nl_file, run_nl, NLContext
from pyvibe.parser.natural import nl as nl_to_python, nl_parse, NaturalLanguageParser

# Override nl with multi-arg version (creates components)
nl = nl_components
# Keep the converter accessible as nl_convert
nl_convert = nl_to_python

__all__ = [
    # NL specific
    "NLString", "nl", "nl_file", "run_nl", "NLContext",
    "nl_convert", "nl_parse", "NaturalLanguageParser",
    # All from pyvibe
    "App", "State", "Component", "Router", "tampil",
    "judul", "subjudul", "paragraf", "teks",
    "gambar", "tautan", "ikon",
    "tombol", "tombol_icon", "input_teks", "input_angka",
    "kartu", "kolom", "baris", "bagian", "grid", "kontainer",
    "navbar", "sidebar", "footer",
    "notifikasi", "alert", "loader",
    "tabel", "grafik_sederhana", "daftar",
    "badge_status", "carousel", "accordion", "modal",
]
