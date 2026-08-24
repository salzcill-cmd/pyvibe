"""
🐍 Example 5: Full Website — website lengkap dengan semua fitur!

Contoh website lengkap dengan:
- Navbar responsive
- Hero section
- Features section
- Pricing section
- Contact form
- Footer

Usage:
    python examples/05_full_website.py
"""

from pyvibe import *

app = App(
    "PyVibe Official",
    title="PyVibe — Build Frontend Websites in Python",
    description="PyVibe adalah framework Python untuk bikin website frontend yang gacor.",
    primary_color="#7C3AED",
)

# ===== State Management =====
state = State(
    current_page="beranda",
    is_menu_open=False,
    form_nama="",
    form_email="",
    form_pesan="",
    notification=None,
)

# ===== Routes =====

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
            Component(
                tag="div",
                children=[
                    judul("Build Frontend Websites\nin Python as Easy as Chatting").besar().tengah(),
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
                ],
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
            judul("Kenapa PyVibe?").tengah(),
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
            Component(
                tag="pre",
                content='from pyvibe import *\n\napp = App("My Website")\n\n@app.route("/")\ndef beranda():\n    return tampil(\n        judul("Halo Dunia!"),\n        paragraf("Ini website pertama gue."),\n        tombol("Klik Saya", warna="ungu"),\n    )\n\napp.jalan()',
            ),
            padding="64px 32px",
            bg="gelap",
            text_align="center",
        ),

        # ===== Pricing =====
        bagian(
            judul("Harga? Gratis!").tengah(),
            paragraf("PyVibe 100% gratis dan open source. Gak ada hidden fee.").tengah(),
            kartu(
                judul_kartu("Free Forever"),
                Component(tag="div", content="Rp 0"),
                paragraf("✓ Semua fitur"),
                paragraf("✓ Unlimited projects"),
                paragraf("✓ Community support"),
                paragraf("✓ Open source MIT License"),
                tombol("Mulai Gratis", warna="ungu", ukuran="besar"),
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


@app.route("/fitur")
def fitur():
    return tampil(
        navbar(
            logo="🐍 PyVibe",
            menu=["Fitur", "Harga", "Dokumentasi", "Contoh"],
            tombol_daftar="Mulai Gratis",
        ),
        bagian(
            judul("Fitur PyVibe").besar().tengah(),
            paragraf("Semua fitur yang lo butuhkan untuk bikin website profesional.").tengah(),
            padding="64px 32px",
        ),
        bagian(
            grid(
                kartu(
                    judul_kartu("🗣️ Natural Language"),
                    paragraf("Tulis kode seperti lo ngobrol. 'tampilin judul Halo' langsung jadi heading."),
                    paragraf("Support 3 syntax styles: Natural, OOP, Hybrid."),
                ),
                kartu(
                    judul_kartu("📱 Auto Responsive"),
                    paragraf("Semua komponen otomatis responsive. Gak perlu mikir CSS media query."),
                    paragraf("Mobile-first approach, works on all devices."),
                ),
                kartu(
                    judul_kartu("🔥 Hot Reload"),
                    paragraf("Simpen file, langsung ke-update di browser. Real-time banget!"),
                    paragraf("WebSocket-based, super fast feedback loop."),
                ),
                kartu(
                    judul_kartu("🧩 50+ Components"),
                    paragraf("Heading, button, card, table, chart — semua udah ada dari awal."),
                    paragraf("Build with builder pattern, chainable styling."),
                ),
                kartu(
                    judul_kartu("🎨 Theme System"),
                    paragraf("10+ tema built-in. Dark mode, gradient, animations — tinggal pake."),
                    paragraf("CSS custom properties for easy customization."),
                ),
                kartu(
                    judul_kartu("🇮🇩 Made in Indonesia"),
                    paragraf("Dokumentasi, error message, komunitas — semua Bahasa Indonesia."),
                    paragraf("First Indonesian-born web framework."),
                ),
                kolom=3,
                gap="24px",
            ),
            padding="64px 32px",
        ),
        footer(
            copyright="© 2026 PyVibe. Made with ❤️ in Indonesia.",
        ),
    )


@app.route("/kontak")
def kontak():
    return tampil(
        navbar(
            logo="🐍 PyVibe",
            menu=["Fitur", "Harga", "Dokumentasi", "Contoh"],
            tombol_daftar="Mulai Gratis",
        ),
        bagian(
            judul("Hubungi Kami").besar().tengah(),
            paragraf("Punya pertanyaan atau saran? Kirim pesan ke kami.").tengah(),
            padding="64px 32px",
        ),
        bagian(
            kartu(
                judul_kartu("Kirim Pesan"),
                input_teks(label="Nama Lengkap", placeholder="Masukkan nama..."),
                input_email(label="Email", placeholder="email@domain.com"),
                textarea(label="Pesan", placeholder="Tulis pesan lo di sini..."),
                tombol("Kirim Pesan", warna="ungu"),
            ),
            padding="64px 32px",
        ),
        footer(
            copyright="© 2026 PyVibe. Made with ❤️ in Indonesia.",
        ),
    )


# ===== Export & Run =====
if __name__ == "__main__":
    print("🐍 PyVibe Official Website")
    print("=" * 50)
    print()
    print("Exporting website...")
    app.export("output/website")
    print()
    print("✅ Website exported ke output/website/")
    print()
    print("To run development server:")
    print("  python examples/05_full_website.py")
    print()
    app.jalan()
