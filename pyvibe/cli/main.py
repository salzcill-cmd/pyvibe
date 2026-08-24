"""
PyVibe CLI — command-line interface untuk PyVibe.

Usage:
    pyvibe create my-website
    pyvibe dev
    pyvibe build
    pyvibe version
    pyvibe components
    pyvibe new landing-page
"""

import os
import sys
import argparse
from pathlib import Path


TEMPLATES = {
    "landing-page": '''"""
🐍 {name} — Landing Page
"""
from pyvibe import *

app = App("{name}")
app.theme("gelap")


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
                ).tengah().gap(4),
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
                    kartu(
                        teks("⚡", size="2xl"),
                        judul("Cepat", size="md"),
                        paragraf("Lightning fast performance.", warna="abu-400"),
                    ),
                    kartu(
                        teks("🎨", size="2xl"),
                        judul("Indah", size="md"),
                        paragraf("Desain modern & responsive.", warna="abu-400"),
                    ),
                    kartu(
                        teks("🔒", size="2xl"),
                        judul("Aman", size="md"),
                        paragraf("Security built-in.", warna="abu-400"),
                    ),
                    kolom=3,
                    gap=24,
                ),
                max_width="1000px",
            ),
            padding="96px 0",
        ),
        
        footer(
            kontainer(
                paragraf("© 2026 {name}. Built with 🐍 PyVibe").tengah(),
                padding="24px 0",
            ),
        ),
    )


app.jalan()
''',
    "dashboard": '''"""
🐍 {name} — Dashboard Admin
"""
from pyvibe import *

app = App("{name}")
app.theme("gelap")
state = State({"sidebar_open": True, "page": "dashboard"})


@app.route("/")
def dashboard():
    return tampil(
        baris(
            sidebar(
                judul("🐍 {name}"),
                tautan("📊 Dashboard"),
                tautan("👥 Users"),
                tautan("📦 Products"),
                tautan("⚙️ Settings"),
            ),
            kolom(10,
                navbar(
                    judul("Dashboard"),
                    baris(
                        notifikasi("3 new", warna="merah"),
                        avatar("Admin"),
                    ).gap(4),
                ),
                kontainer(
                    judul("Dashboard", size="lg"),
                    spasi(24),
                    baris(
                        kartu_stat("Total Users", "1,234", "+12%"),
                        kartu_stat("Revenue", "Rp 45M", "+8%"),
                        kartu_stat("Orders", "567", "+23%"),
                    ).gap(6),
                    spasi(24),
                    tabel(
                        ["Nama", "Email", "Status", "Aksi"],
                        [
                            ["Budi", "budi@mail.com", "Active", "Edit"],
                            ["Sari", "sari@mail.com", "Pending", "Edit"],
                            ["Andi", "andi@mail.com", "Active", "Edit"],
                        ],
                    ),
                ),
            ),
        ),
    )


app.jalan()
''',
    "ecommerce": '''"""
🐍 {name} — E-commerce
"""
from pyvibe import *

app = App("{name}")
app.theme("gelap")


@app.route("/")
def beranda():
    return tampil(
        navbar(
            judul("🛒 {name}"),
            baris(
                input_teks("Search..."),
                tombol("🔍"),
            ).gap(2),
            tombol("Keranjang (0)", warna="kuning"),
        ),
        
        bagian(
            kontainer(
                judul("Produk Terbaru 🔥", size="lg").tengah(),
                spasi(48),
                grid(
                    kartu(
                        badge("Baru!", warna="hijau"),
                        judul("Laptop Pro", size="md"),
                        paragraf("Rp 15.000.000", warna="biru", size="lg"),
                        paragraf("Laptop高性能 untuk profesional.", warna="abu-400", size="sm"),
                        tombol("+ Keranjang", warna="biru", lebar="full"),
                        padding="24px",
                        border="1px solid #374151",
                    ),
                    kartu(
                        judul("Headphone X", size="md"),
                        paragraf("Rp 2.500.000", warna="biru", size="lg"),
                        paragraf("Sound quality premium.", warna="abu-400", size="sm"),
                        tombol("+ Keranjang", warna="biru", lebar="full"),
                        padding="24px",
                        border="1px solid #374151",
                    ),
                    kartu(
                        badge("Sale", warna="merah"),
                        judul("Keyboard Mech", size="md"),
                        paragraf("Rp 850.000", warna="biru", size="lg"),
                        paragraf("RGB mechanical keyboard.", warna="abu-400", size="sm"),
                        tombol("+ Keranjang", warna="biru", lebar="full"),
                        padding="24px",
                        border="1px solid #374151",
                    ),
                    kolom=3,
                    gap=24,
                ),
                max_width="1200px",
            ),
            padding="96px 0",
        ),
        
        footer(
            kontainer(
                paragraf("© 2026 {name}. Built with 🐍 PyVibe").tengah(),
                padding="24px 0",
            ),
        ),
    )


app.jalan()
''',
    "portfolio": '''"""
🐍 {name} — Portfolio Website
"""
from pyvibe import *

app = App("{name}")
app.theme("gelap")


@app.route("/")
def beranda():
    return tampil(
        navbar(
            judul("👨‍💻 {name}"),
            baris(
                tautan("About"),
                tautan("Projects"),
                tautan("Contact"),
            ).gap(6),
        ),
        
        bagian(
            kontainer(
                baris(
                    kolom(6,
                        judul("Hi, I'm Developer! 👋", size="xl"),
                        spasi(8),
                        paragraf("Full-stack developer yang passionate dalam membangun produk digital.", warna="abu-400", size="lg"),
                        spasi(24),
                        baris(
                            tombol("View Projects", warna="biru"),
                            tombol("Contact Me", warna="outline"),
                        ).gap(4),
                    ),
                    kolom(6,
                        avatar("Developer", size="lg"),
                    ),
                ).gap(8).items("center"),
                max_width="1000px",
            ),
            padding="96px 0",
        ),
        
        bagian(
            kontainer(
                judul("Projects 🚀", size="lg").tengah(),
                spasi(48),
                grid(
                    kartu(
                        judul("Project 1", size="md"),
                        paragraf("Web app keren dengan PyVibe.", warna="abu-400"),
                        baris(
                            badge("Python", warna="biru"),
                            badge("PyVibe", warna="hijau"),
                        ).gap(2),
                        tombol("View →", warna="outline"),
                        padding="24px",
                        border="1px solid #374151",
                    ),
                    kartu(
                        judul("Project 2", size="md"),
                        paragraf("Mobile app dengan Flutter.", warna="abu-400"),
                        baris(
                            badge("Dart", warna="biru"),
                            badge("Flutter", warna="cyan"),
                        ).gap(2),
                        tombol("View →", warna="outline"),
                        padding="24px",
                        border="1px solid #374151",
                    ),
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
                input_teks("Nama"),
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
        
        footer(
            kontainer(
                paragraf("© 2026 {name}. Built with 🐍 PyVibe").tengah(),
                padding="24px 0",
            ),
        ),
    )


app.jalan()
''',
    "blog": '''"""
🐍 {name} — Blog
"""
from pyvibe import *

app = App("{name}")
app.theme("gelap")


@app.route("/")
def beranda():
    return tampil(
        navbar(
            judul("📝 {name}"),
            baris(
                tautan("Home"),
                tautan("Articles"),
                tautan("About"),
            ).gap(6),
            tombol("Subscribe", warna="biru"),
        ),
        
        bagian(
            kontainer(
                judul("Latest Articles ✍️", size="lg").tengah(),
                spasi(48),
                kartu(
                    badge("Featured", warna="ungu"),
                    judul("Membuat Website dengan PyVibe", size="md"),
                    spasi(8),
                    paragraf("Tutorial lengkap membuat website modern menggunakan Python dan PyVibe framework.", warna="abu-400"),
                    spasi(16),
                    baris(
                        avatar("Author"),
                        kolom(
                            paragraf("Budi Developer", size="sm"),
                            paragraf("15 Januari 2026", size="xs", warna="abu-500"),
                        ),
                    ).gap(3).items("center"),
                    tombol("Baca Selengkapnya →", warna="outline"),
                    padding="24px",
                    border="1px solid #374151",
                ),
                spasi(16),
                grid(
                    kartu(
                        judul("10 Tips Python untuk Pemula", size="md"),
                        paragraf("Tips dan trik Python yang wajib diketahui.", warna="abu-400", size="sm"),
                        paragraf("10 Januari 2026", size="xs", warna="abu-500"),
                        padding="16px",
                        border="1px solid #374151",
                    ),
                    kartu(
                        judul("React vs PyVibe", size="md"),
                        paragraf("Perbandingan frontend framework terbaru.", warna="abu-400", size="sm"),
                        paragraf("5 Januari 2026", size="xs", warna="abu-500"),
                        padding="16px",
                        border="1px solid #374151",
                    ),
                    kolom=2,
                    gap=16,
                ),
                max_width="800px",
            ),
            padding="96px 0",
        ),
        
        footer(
            kontainer(
                paragraf("© 2026 {name}. Built with 🐍 PyVibe").tengah(),
                padding="24px 0",
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


def cmd_create(args):
    """Create new PyVibe project."""
    project_name = args.name
    template = args.template or "landing-page"
    print(f"\n🐍 Creating new PyVibe project: {project_name}\n")

    # Create project directory
    project_dir = Path(project_name)
    if project_dir.exists():
        print(f"  ❌ Directory '{project_name}' already exists!")
        return

    project_dir.mkdir(parents=True)

    # Get template
    if template not in TEMPLATES:
        print(f"  ❌ Template '{template}' not found!")
        print(f"  📋 Available templates: {', '.join(TEMPLATES.keys())}")
        return

    # Create app.py from template
    app_content = TEMPLATES[template].format(name=project_name)
    (project_dir / "app.py").write_text(app_content, encoding="utf-8")

    # Create requirements.txt
    (project_dir / "requirements.txt").write_text("pyvibe>=0.1.0\n", encoding="utf-8")

    # Create README.md
    readme_content = f"""# 🐍 {project_name}

Built with [PyVibe](https://github.com/pyvibe/pyvibe) — Build frontend websites in Python as easy as chatting.

## 🚀 Quick Start

```bash
# Install PyVibe
pip install pyvibe

# Run development server
python app.py

# Open browser
open http://localhost:3000
```

## 📝 Template

This project was created using the **{template}** template.

## 📚 Documentation

- [Getting Started](https://pyvibe.dev/docs)
- [Components](https://pyvibe.dev/components)
- [Examples](https://pyvibe.dev/examples)

## 📄 License

MIT License
"""
    (project_dir / "README.md").write_text(readme_content, encoding="utf-8")

    # Create .gitignore
    gitignore_content = """# PyVibe
.pyvibe/
__pycache__/
*.pyc
*.pyo
.env
dist/
build/
*.egg-info/
"""
    (project_dir / ".gitignore").write_text(gitignore_content, encoding="utf-8")

    print(f"  ✅ Project created!")
    print(f"\n  📁 Files created:")
    print(f"     {project_name}/app.py")
    print(f"     {project_name}/requirements.txt")
    print(f"     {project_name}/README.md")
    print(f"     {project_name}/.gitignore")
    print(f"\n  🚀 To get started:")
    print(f"     cd {project_name}")
    print(f"     pip install pyvibe")
    print(f"     python app.py")
    print(f"\n  🌐 Open browser: http://localhost:3000\n")


def cmd_new(args):
    """Create new project from template (alias for create)."""
    cmd_create(args)


def cmd_templates(args):
    """List available templates."""
    print("\n📋 Available Templates:\n")
    for name, content in TEMPLATES.items():
        lines = content.strip().split("\n")
        desc = next((l for l in lines if l.startswith('#')), "# No description")
        print(f"  🐍 {name}")
        print(f"     {desc.strip('# ')}")
        print()
    print("  Usage: pyvibe create <project-name> --template <template-name>\n")


def cmd_dev(args):
    """Start development server."""
    print("\n🔥 Starting PyVibe development server...\n")

    # Find app.py
    app_file = Path("app.py")
    if not app_file.exists():
        print("  ❌ app.py not found!")
        print("  💡 Run 'pyvibe create <name>' first, or create app.py manually.")
        return

    # Import and run app
    try:
        sys.path.insert(0, os.getcwd())
        import importlib.util
        spec = importlib.util.spec_from_file_location("app", "app.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"  ❌ Error loading app.py: {e}")


def cmd_build(args):
    """Build static files."""
    print("\n📦 Building PyVibe project...\n")

    app_file = Path("app.py")
    if not app_file.exists():
        print("  ❌ app.py not found!")
        return

    try:
        sys.path.insert(0, os.getcwd())
        import importlib.util
        spec = importlib.util.spec_from_file_location("app", "app.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "app"):
            module.app.export(args.output or "dist")
        else:
            print("  ❌ No 'app' variable found in app.py!")
    except Exception as e:
        print(f"  ❌ Error building: {e}")


def cmd_components(args):
    """List all available components."""
    print("\n🧩 PyVibe Components (58 total):\n")

    categories = {
        "Basic": ["judul", "subjudul", "paragraf", "teks", "teks_teal", "teks_tipis", "teks_balik",
                  "gambar", "tautan", "ikon", "spasi", "pemisah", "gradien_teks", "badge", "avatar",
                  "progress_bar", "chip", "count_down"],
        "Input": ["tombol", "tombol_icon", "input_teks", "input_angka", "input_email", "input_sandi",
                  "textarea", "centang", "pilihan", "unggah_file"],
        "Layout": ["kartu", "kolom", "baris", "bagian", "kartu_stat", "judul_kartu", "spacer",
                   "grid", "kontainer", "overlay"],
        "Navigation": ["navbar", "sidebar", "footer", "tabs", "breadcrumb"],
        "Feedback": ["notifikasi", "loader", "badge_status", "alert", "skeleton"],
        "Data": ["tabel", "grafik_sederhana", "daftar", "statistik"],
        "Advanced": ["carousel", "accordion", "modal", "tooltip", "dropdown"],
        "Extras": ["stepper", "timeline", "rating", "countdown", "typing_effect",
                   "scroll_to_top", "galeri", "code_block", "markdown", "empty_state", "stat_card"],
    }

    for category, components in categories.items():
        print(f"  📦 {category} ({len(components)}):")
        print(f"     {', '.join(components)}")
        print()


def cmd_version(args):
    """Show PyVibe version."""
    from pyvibe import __version__
    print(f"\n🐍 PyVibe v{__version__}\n")
    print("  📦 Build frontend websites in Python as easy as chatting")
    print("  🌐 https://pyvibe.dev")
    print("  📝 GitHub: https://github.com/pyvibe/pyvibe\n")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="pyvibe",
        description="🐍 PyVibe — Build frontend websites in Python as easy as chatting",
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # create
    create_parser = subparsers.add_parser("create", help="Create new PyVibe project")
    create_parser.add_argument("name", help="Project name")
    create_parser.add_argument("-t", "--template", default="landing-page",
                               choices=list(TEMPLATES.keys()),
                               help="Project template")
    create_parser.set_defaults(func=cmd_create)

    # new (alias)
    new_parser = subparsers.add_parser("new", help="Create new project (alias for create)")
    new_parser.add_argument("name", help="Project name")
    new_parser.add_argument("-t", "--template", default="landing-page",
                            choices=list(TEMPLATES.keys()),
                            help="Project template")
    new_parser.set_defaults(func=cmd_new)

    # templates
    templates_parser = subparsers.add_parser("templates", help="List available templates")
    templates_parser.set_defaults(func=cmd_templates)

    # dev
    dev_parser = subparsers.add_parser("dev", help="Start development server")
    dev_parser.set_defaults(func=cmd_dev)

    # build
    build_parser = subparsers.add_parser("build", help="Build static files")
    build_parser.add_argument("-o", "--output", default="dist", help="Output directory")
    build_parser.set_defaults(func=cmd_build)

    # components
    components_parser = subparsers.add_parser("components", help="List all components")
    components_parser.set_defaults(func=cmd_components)

    # version
    version_parser = subparsers.add_parser("version", help="Show PyVibe version")
    version_parser.set_defaults(func=cmd_version)

    args = parser.parse_args()

    if args.command:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
