"""
🐍 PyVibe Documentation Website
Built with PyVibe itself
"""
from pyvibe import *

app = App("PyVibe Docs", theme="gelap")


# ==================== COMPONENTS ====================

def get_navbar():
    """Main navigation bar"""
    return navbar(
        judul("🐍 PyVibe"),
        baris(
            tautan("Home", url="/"),
            tautan("Getting Started", url="/getting-started"),
            tautan("Components", url="/components"),
            tautan("Syntax", url="/syntax"),
            tautan("Styling", url="/styling"),
            tautan("API", url="/api"),
            gap="24px",
        ),
        baris(
            tombol("⭐ GitHub", warna="outline"),
            tombol("📦 Install", warna="hijau"),
            gap="8px",
        ),
        gap="32px",
    )


def get_footer():
    """Page footer"""
    return footer(
        kontainer(
            baris(
                kolom(4,
                    judul("🐍 PyVibe", size="md"),
                    spasi(8),
                    paragraf("Build websites in Python as easy as chatting.", warna="abu-400", size="sm"),
                ),
                kolom(2,
                    judul("Resources", size="sm"),
                    tautan("Docs", url="/"),
                    tautan("Components", url="/components"),
                ),
                kolom(2,
                    judul("Community", size="sm"),
                    tautan("GitHub", url="https://github.com/salzcill-cmd/pyvibe"),
                ),
                gap="32px",
            ),
            spasi(24),
            pemisah(),
            spasi(16),
            baris(
                paragraf("© 2026 PyVibe", size="xs", warna="abu-500"),
                paragraf("Made with ❤️ in Indonesia 🇮🇩", size="xs", warna="abu-500"),
                justify="between",
            ),
        ),
        max_width="1200px",
    )


# ==================== PAGES ====================

@app.route("/")
def beranda():
    """Homepage"""
    return tampil(
        get_navbar(),
        
        # Hero
        bagian(
            kontainer(
                baris(
                    kolom(7,
                        badge("✨ v0.1.0 Now Available!", warna="hijau"),
                        spasi(16),
                        judul("Build Websites with Python 🐍", size="xl").tebal(),
                        spasi(12),
                        paragraf(
                            "PyVibe adalah framework Python untuk membuat website frontend yang super bagus "
                            "pakai Bahasa Indonesia.",
                            warna="abu-300",
                            size="lg",
                        ),
                        spasi(32),
                        baris(
                            tombol("Get Started →", warna="biru", size="lg"),
                            tombol("pip install pyvibe-id", warna="outline", size="lg"),
                            gap="16px",
                        ),
                        spasi(32),
                        baris(
                            stat_card("🐍", "58+", "Components"),
                            stat_card("⚡", "16", "NL Keywords"),
                            stat_card("🛡️", "Built-in", "Security"),
                            gap="16px",
                        ),
                    ),
                    kolom(5,
                        kartu(
                            code_block('''from pyvibe import *

app = App("My Website")

@app.route("/")
def beranda():
    return tampil(
        judul("Halo Dunia! 🌍")
            .besar().tengah(),
        paragraf("Website keren!")
            .tengah(),
        tombol("Mulai", warna="biru"),
    )

app.jalan()''', bahasa="python"),
                            judul_kartu("Quick Start ⚡"),
                            border="2px solid #3B82F6",
                        ),
                    ),
                    gap="32px",
                ),
                max_width="1200px",
            ),
            padding="96px 0",
            bg="gradient-biru",
        ),
        
        # Features
        bagian(
            kontainer(
                judul("Why PyVibe? 🤔", size="lg").tengah(),
                spasi(48),
                grid(
                    kartu(teks("🗣️", size="2xl"), judul("Natural Language", size="md"), spasi(4), paragraf("Tulis kode kayak ngobrol.", warna="abu-400", size="sm"), padding="24px", border="1px solid #374151"),
                    kartu(teks("🧩", size="2xl"), judul("58+ Components", size="md"), spasi(4), paragraf("Komponen UI lengkap.", warna="abu-400", size="sm"), padding="24px", border="1px solid #374151"),
                    kartu(teks("🎨", size="2xl"), judul("Auto Responsive", size="md"), spasi(4), paragraf("Otomatis responsive.", warna="abu-400", size="sm"), padding="24px", border="1px solid #374151"),
                    kartu(teks("🛡️", size="2xl"), judul("Security Built-in", size="md"), spasi(4), paragraf("CSRF, XSS, Rate Limiting.", warna="abu-400", size="sm"), padding="24px", border="1px solid #374151"),
                    kartu(teks("🇮🇩", size="2xl"), judul("Bahasa Indonesia", size="md"), spasi(4), paragraf("Syntax & error message ID.", warna="abu-400", size="sm"), padding="24px", border="1px solid #374151"),
                    kartu(teks("⚡", size="2xl"), judul("Zero Config", size="md"), spasi(4), paragraf("Install, tulis, jalan.", warna="abu-400", size="sm"), padding="24px", border="1px solid #374151"),
                    kolom=3,
                    gap=24,
                ),
                max_width="1200px",
            ),
            padding="96px 0",
            bg="bg-gray-900",
        ),
        
        # Code Example
        bagian(
            kontainer(
                judul("See It In Action 🎬", size="lg").tengah(),
                spasi(48),
                baris(
                    kolom(6,
                        kartu(
                            judul_kartu("🗣️ Natural Language"),
                            code_block('''# Tulis kayak ngobrol
tampilin judul "Halo!" di tengah
tampilin tombol "Klik" warna biru
tampilin badge "NEW" warna hijau''', bahasa="python"),
                            padding="24px",
                            border="1px solid #374151",
                        ),
                    ),
                    kolom(6,
                        kartu(
                            judul_kartu("🧩 Components"),
                            code_block('''return tampil(
    navbar(judul("My App")),
    bagian(
        judul("Features").tengah(),
        grid(kartu1, kartu2, kolom=2),
    ),
    footer(paragraf("© MyApp").tengah()),
)''', bahasa="python"),
                            padding="24px",
                            border="1px solid #374151",
                        ),
                    ),
                    gap="24px",
                ),
                max_width="1200px",
            ),
            padding="96px 0",
        ),
        
        # CTA
        bagian(
            kontainer(
                judul("Ready to Build? 🚀", size="lg").tengah(),
                spasi(24),
                baris(
                    tombol("pip install pyvibe-id", warna="hijau", size="lg"),
                    tombol("Documentation →", warna="outline", size="lg"),
                    gap="16px",
                ).tengah(),
            ),
            padding="96px 0",
            bg="gradient-ungu",
        ),
        
        get_footer(),
    )


@app.route("/getting-started")
def getting_started():
    """Getting Started page"""
    return tampil(
        get_navbar(),
        
        bagian(
            kontainer(
                judul("Getting Started 🚀", size="lg"),
                spasi(24),
                
                judul("1. Install PyVibe", size="md"),
                spasi(8),
                code_block("pip install pyvibe-id", bahasa="bash"),
                spasi(24),
                
                judul("2. Write Code", size="md"),
                spasi(8),
                code_block('''from pyvibe import *

app = App("My Website")

@app.route("/")
def beranda():
    return tampil(
        judul("Halo Dunia! 🌍").besar().tengah(),
        paragraf("Ini website pertama gue.").tengah(),
        tombol("Mulai Sekarang", warna="biru"),
    )

app.jalan()''', bahasa="python"),
                spasi(24),
                
                judul("3. Run", size="md"),
                spasi(8),
                code_block("python app.py", bahasa="bash"),
                spasi(8),
                paragraf("Buka browser: http://localhost:3000"),
            ),
            padding="48px 0",
            max_width="800px",
        ),
        
        get_footer(),
    )


@app.route("/components")
def components():
    """Components Reference"""
    return tampil(
        get_navbar(),
        
        bagian(
            kontainer(
                judul("Components 🧩", size="lg"),
                spasi(24),
                
                kartu(
                    judul_kartu("judul(teks)"),
                    code_block('judul("Hello").besar().tengah()', bahasa="python"),
                    judul("Preview:", size="sm"),
                    judul("Hello").besar().tengah(),
                    padding="24px",
                    border="1px solid #374151",
                ),
                spasi(16),
                
                kartu(
                    judul_kartu("tombol(teks, warna)"),
                    code_block('tombol("Click", warna="biru")', bahasa="python"),
                    judul("Preview:", size="sm"),
                    baris(
                        tombol("Primary", warna="biru"),
                        tombol("Success", warna="hijau"),
                        tombol("Danger", warna="merah"),
                        gap="8px",
                    ),
                    padding="24px",
                    border="1px solid #374151",
                ),
                spasi(16),
                
                kartu(
                    judul_kartu("badge(teks, warna)"),
                    code_block('badge("NEW", warna="hijau")', bahasa="python"),
                    judul("Preview:", size="sm"),
                    baris(
                        badge("NEW"),
                        badge("Sale", warna="merah"),
                        badge("Pro", warna="ungu"),
                        gap="8px",
                    ),
                    padding="24px",
                    border="1px solid #374151",
                ),
                spasi(16),
                
                kartu(
                    judul_kartu("grid(*children, kolom)"),
                    code_block('''grid(
    kartu(paragraf("1")),
    kartu(paragraf("2")),
    kartu(paragraf("3")),
    kolom=3,
)''', bahasa="python"),
                    judul("Preview:", size="sm"),
                    grid(
                        kartu(paragraf("Card 1").tengah(), padding="16px", border="1px solid #374151"),
                        kartu(paragraf("Card 2").tengah(), padding="16px", border="1px solid #374151"),
                        kartu(paragraf("Card 3").tengah(), padding="16px", border="1px solid #374151"),
                        kolom=3,
                        gap=16,
                    ),
                    padding="24px",
                    border="1px solid #374151",
                ),
            ),
            padding="48px 0",
            max_width="800px",
        ),
        
        get_footer(),
    )


@app.route("/syntax")
def syntax():
    """Natural Language Syntax"""
    return tampil(
        get_navbar(),
        
        bagian(
            kontainer(
                judul("Natural Language 🗣️", size="lg"),
                spasi(24),
                
                judul("Tulis kode kayak ngobrol!", size="md"),
                spasi(16),
                baris(
                    kolom(6,
                        kartu(
                            judul_kartu("Input (NL)"),
                            code_block('''tampilin judul "Halo!" di tengah
tampilin tombol "Mulai" warna biru
tampilin badge "NEW" warna hijau''', bahasa="python"),
                            padding="24px",
                            border="1px solid #374151",
                        ),
                    ),
                    kolom(6,
                        kartu(
                            judul_kartu("Output (Python)"),
                            code_block('''judul("Halo!").tengah()
tombol("Mulai", warna="biru")
badge("NEW", warna="hijau")''', bahasa="python"),
                            padding="24px",
                            border="1px solid #374151",
                        ),
                    ),
                    gap="24px",
                ),
            ),
            padding="48px 0",
            max_width="800px",
        ),
        
        get_footer(),
    )


@app.route("/styling")
def styling():
    """Styling Guide"""
    return tampil(
        get_navbar(),
        
        bagian(
            kontainer(
                judul("Styling 🎨", size="lg"),
                spasi(24),
                
                judul("Builder Pattern", size="md"),
                spasi(16),
                code_block('''judul("Hello").besar().tengah().warna("biru")
tombol("Click").warna("merah")
baris(c1, c2).gap("16px").justify("between")''', bahasa="python"),
                spasi(24),
                
                judul("Colors", size="md"),
                spasi(16),
                baris(
                    tombol("Biru", warna="biru"),
                    tombol("Merah", warna="merah"),
                    tombol("Hijau", warna="hijau"),
                    tombol("Kuning", warna="kuning"),
                    tombol("Ungu", warna="ungu"),
                    gap="8px",
                ),
            ),
            padding="48px 0",
            max_width="800px",
        ),
        
        get_footer(),
    )


@app.route("/api")
def api():
    """API Reference"""
    return tampil(
        get_navbar(),
        
        bagian(
            kontainer(
                judul("API Reference 📚", size="lg"),
                spasi(24),
                
                judul("App Class", size="md"),
                spasi(16),
                code_block('''class App(name: str, **config):
    """Main application container."""''', bahasa="python"),
                spasi(16),
                code_block('''@app.route("/")
def home():
    return tampil(judul("Home"))

app.jalan(port=3000)''', bahasa="python"),
            ),
            padding="48px 0",
            max_width="800px",
        ),
        
        get_footer(),
    )


if __name__ == "__main__":
    print("🐍 PyVibe Documentation")
    print("📍 http://localhost:8000")
    app.jalan(port=8000)
