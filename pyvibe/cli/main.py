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
from pyvibe.cli.templates import TEMPLATES, get_template, list_templates


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
    template_content = get_template(template).format(name=project_name)
    
    # Create app.py from template
    (project_dir / "app.py").write_text(template_content, encoding="utf-8")

    # Create requirements.txt
    (project_dir / "requirements.txt").write_text("pyvibe-id>=0.1.0\n", encoding="utf-8")

    # Create README.md
    readme_content = f"""# 🐍 {project_name}

Built with [PyVibe](https://github.com/salzcill-cmd/pyvibe) — Build frontend websites in Python as easy as chatting.

## 🚀 Quick Start

```bash
# Install PyVibe
pip install pyvibe-id

# Run development server
python app.py

# Open browser
open http://localhost:3000
```

## 📚 Documentation

- [Getting Started](https://github.com/salzcill-cmd/pyvibe/blob/main/docs/getting-started.md)
- [Components](https://github.com/salzcill-cmd/pyvibe/blob/main/docs/components.md)
- [Natural Language](https://github.com/salzcill-cmd/pyvibe/blob/main/docs/syntax.md)

## 📄 License

MIT License
"""
    (project_dir / "README.md").write_text(readme_content, encoding="utf-8")

    # Create .gitignore
    gitignore_content = """# PyVibe
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
    print(f"     pip install pyvibe-id")
    print(f"     python app.py")
    print(f"\n  🌐 Open browser: http://localhost:3000\n")


def cmd_new(args):
    """Create new project (alias for create)."""
    cmd_create(args)


def cmd_templates(args):
    """List available templates."""
    print("\n📋 Available Templates:\n")
    templates = list_templates()
    for name in templates:
        print(f"  🐍 {name}")
    print(f"\n  Usage: pyvibe create <project-name> --template <template-name>\n")


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
        "Basic (17)": ["judul", "subjudul", "paragraf", "teks", "teks_teal", "teks_tipis", "teks_balik",
                       "gambar", "tautan", "ikon", "spasi", "pemisah", "gradien_teks", "badge", "avatar",
                       "progress_bar", "chip", "count_down"],
        "Input (10)": ["tombol", "tombol_icon", "input_teks", "input_angka", "input_email", "input_sandi",
                       "textarea", "centang", "pilihan", "unggah_file"],
        "Layout (10)": ["kartu", "kolom", "baris", "bagian", "kartu_stat", "judul_kartu", "spacer",
                        "grid", "kontainer", "overlay"],
        "Navigation (5)": ["navbar", "sidebar", "footer", "tabs", "breadcrumb"],
        "Feedback (5)": ["notifikasi", "loader", "badge_status", "alert", "skeleton"],
        "Data (4)": ["tabel", "grafik_sederhana", "daftar", "statistik"],
        "Advanced (5)": ["carousel", "accordion", "modal", "tooltip", "dropdown"],
        "Extras (11)": ["stepper", "timeline", "rating", "countdown", "typing_effect",
                        "scroll_to_top", "galeri", "code_block", "markdown", "empty_state", "stat_card"],
    }

    for category, components in categories.items():
        print(f"  📦 {category}:")
        print(f"     {', '.join(components)}")
        print()


def cmd_version(args):
    """Show PyVibe version."""
    from pyvibe import __version__
    print(f"\n🐍 PyVibe v{__version__}\n")
    print("  📦 Build frontend websites in Python as easy as chatting")
    print("  🌐 https://github.com/salzcill-cmd/pyvibe")
    print("  📝 Install: pip install pyvibe-id\n")


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
                               help="Project template")
    create_parser.set_defaults(func=cmd_create)

    # new (alias)
    new_parser = subparsers.add_parser("new", help="Create new project (alias)")
    new_parser.add_argument("name", help="Project name")
    new_parser.add_argument("-t", "--template", default="landing-page",
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
