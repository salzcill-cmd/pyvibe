"""
🐍 Example 1: Hello World — PyVibe paling simpel!

Cara paling gampang bikin website pakai PyVibe.
Cukup 5 baris kode, website udah jadi!

Usage:
    python examples/01_hello_world.py
"""

from pyvibe import *

# Buat aplikasi
app = App("Hello World")

# Route utama
@app.route("/")
def beranda():
    return tampil(
        # Navbar
        navbar(
            logo="🐍 PyVibe",
            menu=["Beranda", "Tentang"],
        ),

        # Hero Section
        bagian(
            judul("Halo, Dunia! 🌍").besar().tengah(),
            paragraf("Ini website pertama gue pakai PyVibe. Gak perlu ribet!").tengah(),
            tombol("Mulai Coding", warna="ungu"),
            padding="96px 32px",
            text_align="center",
            bg="gradient-ungu",
        ),

        # Features
        bagian(
            judul("Kenapa PyVibe?").tengah(),
            grid(
                kartu(
                    judul_kartu("⚡ Super Cepat"),
                    paragraf("Hot reload real-time, zero config."),
                ),
                kartu(
                    judul_kartu("🎨 Responsive"),
                    paragraf("Semua komponen otomatis responsive."),
                ),
                kartu(
                    judul_kartu("🇮🇩 Bahasa Indonesia"),
                    paragraf("Syntax & error message Bahasa Indonesia."),
                ),
                kolom=3,
                gap="24px",
            ),
            padding="64px 32px",
        ),

        # Footer
        footer(
            copyright="© 2026 PyVibe",
            links=["GitHub", "Twitter", "Discord"],
        ),
    )

# Jalankan server
app.jalan()
