"""
🐍 Example 7: Developer Portfolio — portofolio developer!

Usage:
    python examples/07_portfolio.py
"""

from pyvibe import *

app = App("Andi's Portfolio", title="Andi — Full Stack Developer")


@app.route("/")
def beranda():
    return tampil(
        # Navbar
        navbar(
            logo="👨‍💻 Andi",
            menu=["Beranda", "Proyek", "Skills", "Kontak"],
            tombol_daftar="Hire Me",
        ),

        # Hero
        bagian(
            Component(
                tag="div",
                children=[
                    badge("Open to Work", warna="hijau"),
                    spasi("16px"),
                    judul("Halo, Gue Andi 👋").besar().tengah(),
                    paragraf("Full Stack Developer yang passionate bikin website keren.").tengah(),
                    paragraf("Jakarta, Indonesia 🇮🇩").tengah(),
                    baris(
                        tombol("Lihat Proyek", warna="ungu"),
                        tombol("Download CV", warna="outline"),
                        justify="center", gap="16px",
                    ),
                ],
            ),
            padding="96px 32px",
            bg="gradient-ungu",
        ),

        # About
        bagian(
            judul("Tentang Gue").tengah(),
            paragraf(
                "Gue adalah Full Stack Developer dengan 3+ tahun pengalaman. "
                "Fokus di web development, UI/UX, dan mobile apps. "
                "Suka banget eksplor teknologi baru dan contribute ke open source."
            ).tengah(),
            padding="64px 32px",
        ),

        # Skills
        bagian(
            judul("Skills").tengah(),
            grid(
                kartu(
                    judul_kartu("Frontend"),
                    chip("HTML"), chip("CSS"), chip("JavaScript"),
                    chip("React"), chip("Vue"), chip("PyVibe"),
                ),
                kartu(
                    judul_kartu("Backend"),
                    chip("Python"), chip("Node.js"), chip("Django"),
                    chip("FastAPI"), chip("PostgreSQL"),
                ),
                kartu(
                    judul_kartu("Tools"),
                    chip("Git"), chip("Docker"), chip("AWS"),
                    chip("Figma"), chip("VS Code"),
                ),
                kolom=3, gap="24px",
            ),
            padding="64px 32px",
            bg="terang",
        ),

        # Projects
        bagian(
            judul("Proyek Terbaru").tengah(),
            grid(
                kartu(
                    Component(tag="div", content="🛍️", style={"font_size": "3rem", "text_align": "center"}),
                    judul_kartu("Toko Gacor"),
                    paragraf("E-commerce platform dengan PyVibe. Full responsive, real-time inventory."),
                    baris(
                        chip("PyVibe"), chip("Python"), chip("SQLite"),
                    ),
                    spacer("12px"),
                    tautan("Lihat Proyek →", url="#"),
                ),
                kartu(
                    Component(tag="div", content="📊", style={"font_size": "3rem", "text_align": "center"}),
                    judul_kartu("Dashboard Analytics"),
                    paragraf("Dashboard admin untuk analytics. Charts, tables, real-time data."),
                    baris(
                        chip("PyVibe"), chip("Chart.js"), chip("WebSocket"),
                    ),
                    spacer("12px"),
                    tautan("Lihat Proyek →", url="#"),
                ),
                kartu(
                    Component(tag="div", content="📝", style={"font_size": "3rem", "text_align": "center"}),
                    judul_kartu("Blog Platform"),
                    paragraf("Platform blog sederhana dengan markdown support dan comments."),
                    baris(
                        chip("PyVibe"), chip("Markdown"), chip("Comments"),
                    ),
                    spacer("12px"),
                    tautan("Lihat Proyek →", url="#"),
                ),
                kolom=3, gap="24px",
            ),
            padding="64px 32px",
        ),

        # Experience
        bagian(
            judul("Pengalaman").tengah(),
            kartu(
                judul_kartu("Full Stack Developer"),
                teks("PT Teknologi Maju • 2023 - Sekarang"),
                paragraf("Develop dan maintain web applications untuk enterprise clients."),
                spacer("16px"),
                judul_kartu("Frontend Developer"),
                teks("Startup Keren • 2022 - 2023"),
                paragraf("Build responsive web interfaces dengan React dan Vue."),
                spacer("16px"),
                judul_kartu("Freelance Developer"),
                teks("Self-employed • 2021 - 2022"),
                paragraf("Bikin website untuk UMKM dan startup lokal."),
            ),
            padding="64px 32px",
            bg="terang",
        ),

        # Contact
        bagian(
            judul("Kontak Gue").tengah(),
            paragraf("Ada project? Yuk ngobrol!").tengah(),
            kartu(
                judul_kartu("Kirim Pesan"),
                input_teks(label="Nama"),
                input_email(label="Email"),
                textarea(label="Pesan"),
                tombol("Kirim Pesan", warna="ungu"),
            ),
            padding="64px 32px",
        ),

        # Footer
        footer(
            links=["GitHub", "LinkedIn", "Twitter", "Instagram"],
            copyright="© 2026 Andi. Built with 🐍 PyVibe",
        ),
    )


if __name__ == "__main__":
    print("👨‍💻 Andi's Portfolio")
    print("=" * 50)
    app.export("output/07_portfolio")
    print("✅ Exported to output/07_portfolio/")
    print()
    app.jalan()
