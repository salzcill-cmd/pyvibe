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
                judul("Selamat Datang di {name}!").besar().tengah(),
                spasi(8),
                paragraf("Website keren yang dibangun pakai PyVibe.").tengah(),
                spasi(24),
                baris(
                    tombol("Mulai Sekarang", warna="biru"),
                    tombol("Pelajari Lebih", warna="outline"),
                    gap="16px",
                ).tengah(),
                max_lebar="800px",
            ),
            padding="96px 0",
            bg="gradient-biru",
        ),
        
        bagian(
            kontainer(
                judul("Fitur").tengah(),
                spasi(48),
                grid(
                    kartu(teks("⚡").besar(), judul("Cepat").tengah(), paragraf("Lightning fast.").tengah().warna("abu-400")),
                    kartu(teks("🎨").besar(), judul("Indah").tengah(), paragraf("Desain modern.").tengah().warna("abu-400")),
                    kartu(teks("🔒").besar(), judul("Aman").tengah(), paragraf("Security built-in.").tengah().warna("abu-400")),
                    kolom=3,
                    gap="24px",
                ),
                max_lebar="1000px",
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
                navbar(judul("Dashboard")),
                kontainer(
                    judul("Welcome back! 👋").besar(),
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
        ),
        
        bagian(
            kontainer(
                baris(
                    kolom(7,
                        judul("Hi, I'm {name} 👋").besar().tebal(),
                        spasi(12),
                        paragraf("Full-stack Developer | UI/UX Enthusiast").warna("abu-300").besar(),
                        spasi(24),
                        baris(
                            tombol("View Projects", warna="biru"),
                            tombol("Contact Me", warna="outline"),
                            gap="16px",
                        ),
                    ),
                    kolom(5, avatar("photo.jpg", ukuran="200px")),
                    gap="48px",
                ),
                max_lebar="1000px",
            ),
            padding="96px 0",
        ),
        
        bagian(
            kontainer(
                judul("Projects 🚀").tengah(),
                spasi(48),
                grid(
                    kartu(badge("Featured", warna="ungu"), judul("Project 1"), paragraf("Description").warna("abu-400")),
                    kartu(badge("Open Source", warna="hijau"), judul("Project 2"), paragraf("Description").warna("abu-400")),
                    kolom=2,
                    gap="24px",
                ),
                max_lebar="800px",
            ),
            padding="96px 0",
            bg="gelap",
        ),
        
        bagian(
            kontainer(
                judul("Contact 📬").tengah(),
                spasi(24),
                input_teks(label="Name"),
                input_email(label="Email"),
                textarea(label="Message"),
                spasi(16),
                tombol("Send Message", warna="biru"),
                max_lebar="500px",
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
        ),
        
        bagian(
            kontainer(
                judul("Latest Articles ✍️").tengah(),
                spasi(48),
                grid(
                    kartu(
                        badge("Python", warna="biru"),
                        judul("Getting Started with PyVibe"),
                        spasi(8),
                        paragraf("Learn how to build websites with Python.").warna("abu-400"),
                        spasi(16),
                        paragraf("Aug 24, 2026 · 5 min read").warna("abu-500"),
                    ),
                    kartu(
                        badge("Tutorial", warna="hijau"),
                        judul("10 PyVibe Tips & Tricks"),
                        spasi(8),
                        paragraf("Master PyVibe with these pro tips.").warna("abu-400"),
                        spasi(16),
                        paragraf("Aug 22, 2026 · 8 min read").warna("abu-500"),
                    ),
                    kolom=2,
                    gap="24px",
                ),
                max_lebar="900px",
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
            tombol("Cart (0)", warna="kuning"),
        ),
        
        bagian(
            kontainer(
                judul("Featured Products 🛍️").tengah(),
                spasi(48),
                grid(
                    kartu(
                        badge("New!", warna="hijau"),
                        judul("Product 1"),
                        paragraf("Rp 150.000").besar().warna("biru"),
                        paragraf("Description here.").warna("abu-400"),
                        tombol("+ Cart", warna="biru"),
                    ),
                    kartu(
                        badge("Sale", warna="merah"),
                        judul("Product 2"),
                        paragraf("Rp 99.000").besar().warna("biru"),
                        paragraf("Description here.").warna("abu-400"),
                        tombol("+ Cart", warna="biru"),
                    ),
                    kartu(
                        judul("Product 3"),
                        paragraf("Rp 199.000").besar().warna("biru"),
                        paragraf("Description here.").warna("abu-400"),
                        tombol("+ Cart", warna="biru"),
                    ),
                    kolom=3,
                    gap="24px",
                ),
                max_lebar="1000px",
            ),
            padding="96px 0",
        ),
        
        footer(kontainer(paragraf("© 2026 {name}. Built with 🐍 PyVibe").tengah(), padding="24px 0")),
    )


app.jalan()
''',

    "admin": '''"""
🐍 {name} — Admin Panel
"""
from pyvibe import *

app = App("{name}", theme="dark")


@app.route("/")
def admin_dashboard():
    return tampil(
        baris(
            sidebar(
                "📊 Dashboard", "👥 Users", "📦 Products", 
                "🛒 Orders", "💬 Messages", "⚙️ Settings",
                judul="{name} Admin"
            ),
            kolom(10,
                navbar(judul("Admin Panel")),
                kontainer(
                    judul("Dashboard Admin 📊").besar(),
                    spasi(24),
                    baris(
                        kartu_stat("Users", "1,234", "+12%"),
                        kartu_stat("Revenue", "Rp 45M", "+8%"),
                        kartu_stat("Orders", "567", "+23%"),
                        kartu_stat("Rating", "4.8 ⭐", "+0.2"),
                        gap="16px",
                    ),
                    spasi(32),
                    kartu(
                        judul_kartu("Recent Users"),
                        tabel(
                            [
                                {"name": "Andi", "email": "andi@test.com", "role": "Admin"},
                                {"name": "Budi", "email": "budi@test.com", "role": "User"},
                                {"name": "Citra", "email": "citra@test.com", "role": "Editor"},
                            ],
                            kolom=["name", "email", "role"],
                        ),
                    ),
                ),
            ),
        ),
    )


app.jalan()
''',

    "saas": '''"""
🐍 {name} — SaaS Landing Page
"""
from pyvibe import *

app = App("{name}")


@app.route("/")
def beranda():
    return tampil(
        navbar(
            judul("🚀 {name}"),
            baris(
                tautan("Features"), tautan("Pricing"), tautan("Docs"),
                gap="24px",
            ),
            tombol("Get Started", warna="biru"),
        ),
        
        # Hero
        bagian(
            kontainer(
                badge("✨ New: AI Features Now Available", warna="ungu"),
                spasi(24),
                judul("Build Amazing Products\nFaster Than Ever").besar().tengah(),
                spasi(16),
                paragraf("The all-in-one platform that helps teams ship products 10x faster.").tengah().warna("abu-400").besar(),
                spasi(32),
                baris(
                    tombol("Start Free Trial", warna="biru", ukuran="besar"),
                    tombol("Watch Demo", warna="outline", ukuran="besar"),
                    gap="16px",
                ).tengah(),
                spasi(16),
                paragraf("Free 14-day trial · No credit card required").tengah().warna("abu-500"),
                max_lebar="800px",
            ),
            padding="120px 0",
            bg="gradient-ungu",
        ),
        
        # Pricing
        bagian(
            kontainer(
                judul("Simple, Transparent Pricing 💰").tengah(),
                spasi(48),
                grid(
                    kartu(
                        judul("Starter").tengah(),
                        paragraf("Rp 99K/mo").besar().tengah().tebal(),
                        paragraf("Perfect for individuals").warna("abu-400").tengah(),
                        spasi(16),
                        daftar("1 User", "10 Projects", "1GB Storage"),
                        spasi(16),
                        tombol("Get Started", warna="outline"),
                    ),
                    kartu(
                        badge("Popular", warna="ungu"),
                        judul("Pro").tengah(),
                        paragraf("Rp 299K/mo").besar().tengah().tebal(),
                        paragraf("Best for small teams").warna("abu-400").tengah(),
                        spasi(16),
                        daftar("5 Users", "Unlimited Projects", "10GB Storage"),
                        spasi(16),
                        tombol("Get Started", warna="biru"),
                    ),
                    kartu(
                        judul("Enterprise").tengah(),
                        paragraf("Custom").besar().tengah().tebal(),
                        paragraf("For large organizations").warna("abu-400").tengah(),
                        spasi(16),
                        daftar("Unlimited Users", "Unlimited Everything", "Priority Support"),
                        spasi(16),
                        tombol("Contact Sales", warna="outline"),
                    ),
                    kolom=3,
                    gap="24px",
                ),
                max_lebar="1000px",
            ),
            padding="96px 0",
        ),
        
        footer(kontainer(paragraf("© 2026 {name}. Built with 🐍 PyVibe").tengah(), padding="24px 0")),
    )


app.jalan()
''',

    "restaurant": '''"""
🐍 {name} — Restaurant Website
"""
from pyvibe import *

app = App("{name}")


@app.route("/")
def beranda():
    return tampil(
        navbar(
            judul("🍽️ {name}"),
            baris(tautan("Menu"), tautan("About"), tautan("Contact"), gap="24px"),
            tombol("Order Now", warna="merah"),
        ),
        
        bagian(
            kontainer(
                judul("Selamat Datang di {name}!").besar().tengah(),
                spasi(8),
                paragraf("Masakan autentik Indonesia dengan sentuhan modern.").tengah().besar(),
                spasi(24),
                tombol("Lihat Menu", warna="merah", ukuran="besar"),
                max_lebar="800px",
            ),
            padding="120px 0",
            bg="gradient-orange",
        ),
        
        bagian(
            kontainer(
                judul("Menu Favorit 🍜").tengah(),
                spasi(48),
                grid(
                    kartu(
                        gambar("nasi-goreng.jpg"),
                        judul("Nasi Goreng Spesial"),
                        paragraf("Rp 35.000").besar().warna("merah"),
                        paragraf("Nasi goreng dengan ayam, udang, dan telur.").warna("abu-400"),
                    ),
                    kartu(
                        gambar("rendang.jpg"),
                        judul("Rendang Padang"),
                        paragraf("Rp 55.000").besar().warna("merah"),
                        paragraf("Rendang sapi authentic resep turun temurun.").warna("abu-400"),
                    ),
                    kartu(
                        gambar("sate.jpg"),
                        judul("Sate Ayam Madura"),
                        paragraf("Rp 25.000").besar().warna("merah"),
                        paragraf("Sate ayam dengan bumbu kacang khas Madura.").warna("abu-400"),
                    ),
                    kolom=3,
                    gap="24px",
                ),
                max_lebar="1000px",
            ),
            padding="96px 0",
        ),
        
        footer(kontainer(paragraf("© 2026 {name}. Built with 🐍 PyVibe").tengah(), padding="24px 0")),
    )


app.jalan()
''',

    "saas-dashboard": '''"""
🐍 {name} — SaaS Dashboard
"""
from pyvibe import *

app = App("{name}", theme="dark")


@app.route("/")
def dashboard():
    return tampil(
        baris(
            sidebar(
                "📊 Overview", "👥 Customers", "💳 Billing",
                "📧 Emails", "📈 Analytics", "⚙️ Settings",
                judul="{name}"
            ),
            kolom(10,
                navbar(
                    judul("Dashboard"),
                    tombol("+ New", warna="biru"),
                ),
                kontainer(
                    judul("Overview 📊").besar(),
                    spasi(24),
                    baris(
                        kartu_stat("Revenue", "Rp 12.5M", "+23%"),
                        kartu_stat("Customers", "1,234", "+12%"),
                        kartu_stat("Conversion", "3.2%", "+0.5%"),
                        gap="16px",
                    ),
                    spasi(32),
                    baris(
                        kartu(
                            judul_kartu("Recent Transactions"),
                            tabel(
                                [{"customer": "Andi", "amount": "Rp 500K", "status": "Success"}],
                                kolom=["customer", "amount", "status"],
                            ),
                            kolom=7,
                        ),
                        kartu(
                            judul_kartu("Quick Stats"),
                            statistik([
                                {"label": "Active", "value": "89%", "icon": "✅"},
                                {"label": "Pending", "value": "11%", "icon": "⏳"},
                            ]),
                            kolom=5,
                        ),
                        gap="16px",
                    ),
                ),
            ),
        ),
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
