"""
PyVibe CLI Templates — project templates for quick start.
"""

TEMPLATES = {
    "landing-page": '''"""
🐍 {name} — Landing Page
"""
from pyvibe import *

app = App("{name}")


@app.route("/")
def beranda():
    return tampil(
        navbar(
            judul("🐍 {name}"),
            tombol("Mulai", warna="biru"),
        ),
        
        bagian(
            kontainer(
                judul("Selamat Datang di {name}!", size="xl").tengah(),
                spasi(8),
                paragraf("Website keren yang dibangun pakai PyVibe.", warna="abu-400").tengah(),
                spasi(24),
                baris(
                    tombol("Mulai Sekarang", warna="biru"),
                    tombol("Pelajari Lebih", warna="outline"),
                    gap="16px",
                ).tengah(),
                max_width="800px",
            ),
            padding="96px 0",
            bg="gradient-biru",
        ),
        
        bagian(
            kontainer(
                judul("Fitur", size="lg").tengah(),
                spasi(48),
                grid(
                    kartu(teks("⚡", size="2xl"), judul("Cepat", size="md"), paragraf("Lightning fast.", warna="abu-400")),
                    kartu(teks("🎨", size="2xl"), judul("Indah", size="md"), paragraf("Desain modern.", warna="abu-400")),
                    kartu(teks("🔒", size="2xl"), judul("Aman", size="md"), paragraf("Security built-in.", warna="abu-400")),
                    kolom=3,
                    gap=24,
                ),
                max_width="1000px",
            ),
            padding="96px 0",
        ),
        
        footer(kontainer(paragraf("© 2026 {name}. Built with 🐍 PyVibe").tengah(), padding="24px 0")),
    )


app.jalan()
''',

    "dashboard": '''"""
🐍 {name} — Dashboard Admin
"""
from pyvibe import *

app = App("{name}")


@app.route("/")
def dashboard():
    return tampil(
        baris(
            sidebar("📊 Dashboard", "👥 Users", "📦 Products", "⚙️ Settings", judul="{name}"),
            kolom(10,
                navbar(judul("Dashboard"), gap="32px"),
                kontainer(
                    judul("Welcome back! 👋", size="lg"),
                    spasi(24),
                    baris(
                        kartu_stat("Users", "1,234", "+12%"),
                        kartu_stat("Revenue", "Rp 45M", "+8%"),
                        kartu_stat("Orders", "567", "+23%"),
                        gap="16px",
                    ),
                    spasi(32),
                    kartu(
                        judul_kartu("Recent Activity"),
                        tabel(
                            [{"Action": "User Signup", "Time": "2 min ago"}, {"Action": "Order #123", "Time": "5 min ago"}],
                            kolom=["Action", "Time"],
                        ),
                        padding="24px",
                        border="1px solid #374151",
                    ),
                ),
            ),
        ),
    )


app.jalan()
''',

    "portfolio": '''"""
🐍 {name} — Developer Portfolio
"""
from pyvibe import *

app = App("{name}")


@app.route("/")
def beranda():
    return tampil(
        navbar(
            judul("👨‍💻 {name}"),
            baris(tautan("About"), tautan("Projects"), tautan("Contact"), gap="24px"),
            gap="32px",
        ),
        
        bagian(
            kontainer(
                baris(
                    kolom(7,
                        judul("Hi, I'm {name} 👋", size="xl").tebal(),
                        spasi(12),
                        paragraf("Full-stack Developer | UI/UX Enthusiast", warna="abu-300", size="lg"),
                        spasi(24),
                        baris(
                            tombol("View Projects", warna="biru"),
                            tombol("Contact Me", warna="outline"),
                            gap="16px",
                        ),
                    ),
                    kolom(5, avatar("{name}", size="lg")),
                    gap="48px",
                ),
                max_width="1000px",
            ),
            padding="96px 0",
        ),
        
        bagian(
            kontainer(
                judul("Projects 🚀", size="lg").tengah(),
                spasi(48),
                grid(
                    kartu(badge("Featured", warna="ungu"), judul("Project 1"), paragraf("Description", warna="abu-400"), padding="24px", border="1px solid #374151"),
                    kartu(badge("Open Source", warna="hijau"), judul("Project 2"), paragraf("Description", warna="abu-400"), padding="24px", border="1px solid #374151"),
                    kolom=2,
                    gap=24,
                ),
                max_width="800px",
            ),
            padding="96px 0",
            bg="bg-gray-900",
        ),
        
        bagian(
            kontainer(
                judul("Contact 📬", size="lg").tengah(),
                spasi(24),
                input_teks("Name"),
                spasi(8),
                input_email("Email"),
                spasi(8),
                textarea("Message"),
                spasi(16),
                tombol("Send Message", warna="biru", lebar="full"),
                max_width="500px",
            ),
            padding="96px 0",
        ),
        
        footer(kontainer(paragraf("© 2026 {name}. Built with 🐍 PyVibe").tengah(), padding="24px 0")),
    )


app.jalan()
''',

    "blog": '''"""
🐍 {name} — Tech Blog
"""
from pyvibe import *

app = App("{name}")


@app.route("/")
def beranda():
    return tampil(
        navbar(
            judul("📝 {name}"),
            baris(tautan("Home"), tautan("Articles"), tautan("About"), gap="24px"),
            tombol("Subscribe", warna="biru"),
            gap="32px",
        ),
        
        bagian(
            kontainer(
                judul("Latest Articles ✍️", size="lg").tengah(),
                spasi(48),
                grid(
                    kartu(
                        badge("Python", warna="biru"),
                        judul("Getting Started with PyVibe", size="md"),
                        spasi(8),
                        paragraf("Learn how to build websites with Python.", warna="abu-400", size="sm"),
                        spasi(16),
                        paragraf("Aug 24, 2026 · 5 min read", size="xs", warna="abu-500"),
                        padding="24px",
                        border="1px solid #374151",
                    ),
                    kartu(
                        badge("Tutorial", warna="hijau"),
                        judul("10 PyVibe Tips & Tricks", size="md"),
                        spasi(8),
                        paragraf("Master PyVibe with these pro tips.", warna="abu-400", size="sm"),
                        spasi(16),
                        paragraf("Aug 22, 2026 · 8 min read", size="xs", warna="abu-500"),
                        padding="24px",
                        border="1px solid #374151",
                    ),
                    kolom=2,
                    gap=24,
                ),
                max_width="900px",
            ),
            padding="96px 0",
        ),
        
        footer(kontainer(paragraf("© 2026 {name}. Built with 🐍 PyVibe").tengah(), padding="24px 0")),
    )


app.jalan()
''',

    "ecommerce": '''"""
🐍 {name} — E-commerce Store
"""
from pyvibe import *

app = App("{name}")


@app.route("/")
def beranda():
    return tampil(
        navbar(
            judul("🛒 {name}"),
            baris(input_teks("Search..."), gap="8px"),
            tombol("Cart (0)", warna="kuning"),
            gap="32px",
        ),
        
        bagian(
            kontainer(
                judul("Featured Products 🛍️", size="lg").tengah(),
                spasi(48),
                grid(
                    kartu(
                        badge("New!", warna="hijau"),
                        judul("Product 1", size="md"),
                        paragraf("Rp 150.000", warna="biru", size="lg"),
                        paragraf("Description here.", warna="abu-400", size="sm"),
                        tombol("+ Cart", warna="biru", lebar="full"),
                        padding="24px",
                        border="1px solid #374151",
                    ),
                    kartu(
                        badge("Sale", warna="merah"),
                        judul("Product 2", size="md"),
                        paragraf("Rp 99.000", warna="biru", size="lg"),
                        paragraf("Description here.", warna="abu-400", size="sm"),
                        tombol("+ Cart", warna="biru", lebar="full"),
                        padding="24px",
                        border="1px solid #374151",
                    ),
                    kartu(
                        judul("Product 3", size="md"),
                        paragraf("Rp 199.000", warna="biru", size="lg"),
                        paragraf("Description here.", warna="abu-400", size="sm"),
                        tombol("+ Cart", warna="biru", lebar="full"),
                        padding="24px",
                        border="1px solid #374151",
                    ),
                    kolom=3,
                    gap=24,
                ),
                max_width="1000px",
            ),
            padding="96px 0",
        ),
        
        footer(kontainer(paragraf("© 2026 {name}. Built with 🐍 PyVibe").tengah(), padding="24px 0")),
    )


app.jalan()
''',

    "minimal": '''"""
🐍 {name} — Minimal Website
"""
from pyvibe import *

app = App("{name}")


@app.route("/")
def beranda():
    return tampil(
        judul("Hello, {name}! 👋").tengah(),
        paragraf("Welcome to your new PyVibe website.").tengah(),
        tombol("Get Started", warna="biru"),
    )


app.jalan()
''',
}


def get_template(name: str) -> str:
    """Get template by name."""
    return TEMPLATES.get(name, TEMPLATES["minimal"])


def list_templates() -> list:
    """List all available templates."""
    return list(TEMPLATES.keys())
