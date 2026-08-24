"""
🐍 Example 2: Landing Page — website profesional!

Landing page lengkap dengan navbar, hero, fitur, pricing, dan footer.

Usage:
    python examples/02_landing_page.py
"""

from pyvibe import *

app = App("PyVibe Landing", title="PyVibe — Bikin Website Gak Pake Ribet")

@app.route("/")
def beranda():
    return tampil(
        # ===== Navbar =====
        navbar(
            logo="🐍 PyVibe",
            menu=["Fitur", "Harga", "Dokumentasi", "Contoh"],
            tombol_login="Login",
            tombol_daftar="Mulai Gratis",
        ),

        # ===== Hero Section =====
        bagian(
            judul("Bikin Website\nGak Pake Ribet").besar().tengah(),
            paragraf(
                "PyVibe bikin coding website jadi semudah ngobrol. "
                "Gak perlu jago CSS, gak perlu hafal syntax ribet. "
                "Tulis seperti lo ngobrol, langsung jadi website!"
            ).tengah(),
            baris(
                tombol("Coba Gratis 🚀", warna="ungu", ukuran="besar"),
                tombol("Lihat Dokumentasi", warna="outline", ukuran="besar"),
                justify="center",
                gap="16px",
            ),
            padding="96px 32px",
            text_align="center",
            bg="gradient-ungu",
        ),

        # ===== Social Proof =====
        bagian(
            baris(
                count_down(1234, label="Developers"),
                count_down(5678, label="Websites Built"),
                count_down(99, label="Components"),
                count_down(100, label="Open Source"),
                justify="center",
                gap="64px",
            ),
            padding="48px 32px",
            bg="terang",
        ),

        # ===== Fitur Utama =====
        bagian(
            judul("Fitur yang Bikin PyVibe Gacor").tengah(),
            paragraf(
                "Semua yang lo butuhkan untuk bikin website profesional, "
                "udah built-in. Gak perlu install 1000 package."
            ).tengah(),
            grid(
                kartu(
                    judul_kartu("🗣️ Bahasa Natural"),
                    paragraf("Tulis kode seperti lo ngobrol. 'tampilin judul Halo' langsung jadi heading."),
                ),
                kartu(
                    judul_kartu("📱 Auto Responsive"),
                    paragraf("Semua komponen otomatis responsive. Gak perlu mikir CSS media query."),
                ),
                kartu(
                    judul_kartu("🔥 Hot Reload"),
                    paragraf("Simpen file, langsung ke-update di browser. Real-time banget!"),
                ),
                kartu(
                    judul_kartu("🧩 50+ Components"),
                    paragraf("Heading, button, card, table, chart — semua udah ada dari awal."),
                ),
                kartu(
                    judul_kartu("🎨 Theme System"),
                    paragraf("10+ tema built-in. Dark mode, gradient, animations — tinggal pake."),
                ),
                kartu(
                    judul_kartu("🇮🇩 Made in Indonesia"),
                    paragraf("Dokumentasi, error message, komunitas — semua Bahasa Indonesia."),
                ),
                kolom=3,
                gap="24px",
            ),
            padding="64px 32px",
        ),

        # ===== Code Example =====
        bagian(
            judul("Coding Sesimpel Ini").tengah(),
            paragraf("Dari install sampai website online, cukup 3 command.").tengah(),
            # Code block
            Component(
                tag="pre",
                content='from pyvibe import *\n\napp = App("My Website")\n\n@app.route("/")\ndef beranda():\n    return tampil(\n        judul("Halo Dunia!"),\n        paragraf("Ini website pertama gue."),\n        tombol("Klik Saya", warna="ungu"),\n    )\n\napp.jalan()'
            ),
            padding="64px 32px",
            bg="gelap",
            text_align="center",
        ),

        # ===== Pricing =====
        bagian(
            judul("Harga? Gratis!").tengah(),
            paragraf("PyVibe 100% gratis dan open source. Gak ada hidden fee.").tengah(),
            baris(
                kartu(
                    judul_kartu("Free"),
                    Component(tag="div", content="Rp 0").style.__dict__,
                    paragraf("✓ Semua fitur"),
                    paragraf("✓ Unlimited projects"),
                    paragraf("✓ Community support"),
                    paragraf("✓ Open source"),
                    tombol("Mulai Gratis", warna="ungu", ukuran="besar"),
                ),
                justify="center",
                gap="24px",
            ),
            padding="64px 32px",
            bg="terang",
        ),

        # ===== CTA =====
        bagian(
            judul("Siap Bikin Website?").besar().tengah(),
            paragraf("Mulai coding sekarang, gak perlu nunggu nanti.").tengah(),
            tombol("Mulai Sekarang! 🚀", warna="ungu", ukuran="besar"),
            padding="96px 32px",
            text_align="center",
            bg="gradient-ungu",
        ),

        # ===== Footer =====
        footer(
            links=["GitHub", "Discord", "Twitter", "YouTube", "Blog"],
            copyright="© 2026 PyVibe. Made with ❤️ in Indonesia.",
        ),
    )

app.jalan()
