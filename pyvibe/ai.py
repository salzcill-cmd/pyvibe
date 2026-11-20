"""
🐍 PyVibe AI — Integrasi AI/LLM untuk component generation.

"AI bantu bikin UI, kamu tinggal duduk manis."

Features:
- AIUIBuilder — Generate UI from natural language
- SmartSuggestions — Get component suggestions
- CodeGenerator — Generate PyVibe code
- PromptTemplates — Common AI prompts

Usage:
    from pyvibe.ai import AIUIBuilder, PromptTemplates, CodeGenerator, AISuggestion

    ai = AIUIBuilder()
    components = ai.generate("Bikin landing page untuk kopi shop")
    html = ai.render("Bikin form login yang cantik")
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
import json


@dataclass
class AISuggestion:
    """AI component suggestion."""

    component: str
    description: str
    code: str
    confidence: float = 0.8
    category: str = "general"

    def to_dict(self) -> Dict:
        return {
            "component": self.component,
            "description": self.description,
            "code": self.code,
            "confidence": self.confidence,
            "category": self.category,
        }


class PromptTemplates:
    """Pre-built prompts for common UI generation tasks."""

    LANDING_PAGE = """Buat landing page dengan:
- Judul utama: {title}
- Subjudul: {subtitle}
- {feature_count} fitur utama
- Call-to-action button
- Footer

Komponen: navbar, hero section, features grid, CTA, footer"""

    DASHBOARD = """Buat dashboard admin dengan:
- Sidebar navigation
- Stat cards: {stats}
- Data table
- Chart (opsional)

Komponen: sidebar, kartu_stat, tabel, chart_bar"""

    FORM = """Buat form {form_type} dengan field:
- {fields}
- Validasi: {validation}
- Submit button"""

    PORTFOLIO = """Buat halaman portofolio untuk {name}:
- Hero section dengan nama dan title
- Skills/tech stack
- Project cards
- Contact section"""

    ECOMMERCE = """Buat halaman toko online:
- Product grid
- Shopping cart (basic)
- Product cards dengan harga
- Filter/sort section"""

    @classmethod
    def landing_page(cls, title: str, subtitle: str = "",
                     features: Optional[List[str]] = None) -> str:
        feature_count = len(features) if features else 3
        return cls.LANDING_PAGE.format(
            title=title, subtitle=subtitle or "Solusi terbaik untuk kebutuhan Anda",
            feature_count=feature_count,
        )

    @classmethod
    def dashboard(cls, stats: Optional[List[str]] = None) -> str:
        stats_str = ", ".join(stats) if stats else "Users, Revenue, Orders"
        return cls.DASHBOARD.format(stats=stats_str)

    @classmethod
    def form(cls, form_type: str = "kontak",
             fields: Optional[List[str]] = None,
             validation: Optional[List[str]] = None) -> str:
        fields_str = ", ".join(fields) if fields else "Nama, Email, Pesan"
        validation_str = ", ".join(validation) if validation else "required, email"
        return cls.FORM.format(
            form_type=form_type, fields=fields_str, validation=validation_str,
        )

    @classmethod
    def portfolio(cls, name: str = "Developer", skills: Optional[List[str]] = None) -> str:
        skills_str = ", ".join(skills) if skills else "Python, PyVibe, React"
        return cls.PORTFOLIO.format(name=name, skills=skills_str)

    @classmethod
    def ecommerce(cls, title: str = "Toko Online") -> str:
        return cls.ECOMMERCE


class SmartSuggestions:
    """Get smart component suggestions based on context."""

    SUGGESTIONS = {
        "landing": [
            AISuggestion("navbar", "Navigation bar", "navbar(logo, menu)", 0.9, "navigation"),
            AISuggestion("hero", "Hero section", "bagian(judul().besar().tengah())", 0.95, "layout"),
            AISuggestion("features", "Feature grid", "grid(kartu(), kolom=3)", 0.9, "layout"),
            AISuggestion("cta", "Call to action", "tombol('Mulai Sekarang')", 0.85, "input"),
            AISuggestion("footer", "Footer", "footer(copyright='2026')", 0.9, "navigation"),
            AISuggestion("counter", "Counter/statistics", "statistik([{'label': 'Users', 'value': '1234'}] )", 0.8, "data"),
        ],
        "dashboard": [
            AISuggestion("sidebar", "Sidebar navigation", "sidebar('Dashboard', 'Users')", 0.9, "navigation"),
            AISuggestion("stats", "Stat cards", "kartu_stat('Users', '1,234')", 0.95, "layout"),
            AISuggestion("table", "Data table", "tabel(data)", 0.9, "data"),
            AISuggestion("chart", "Chart", "chart_bar(data)", 0.85, "charts"),
            AISuggestion("filter", "Filter section", "pilihan('Filter', ['Semua', 'Hari ini', 'Minggu'])", 0.85, "input"),
        ],
        "form": [
            AISuggestion("input", "Text input", "input_teks(label='Nama')", 0.95, "input"),
            AISuggestion("email", "Email input", "input_email(label='Email')", 0.95, "input"),
            AISuggestion("password", "Password input", "input_sandi(label='Password')", 0.9, "input"),
            AISuggestion("textarea", "Textarea", "textarea(label='Pesan')", 0.9, "input"),
            AISuggestion("submit", "Submit button", "tombol('Kirim')", 0.9, "input"),
            AISuggestion("validasi", "Form validation", "FormBuilder().email('email', required=True).build()", 0.9, "form"),
        ],
        "ecommerce": [
            AISuggestion("product-card", "Product card", "kartu(gambar(), judul(), harga())", 0.95, "layout"),
            AISuggestion("price", "Price display", "teks('Rp 100.000').warna('ungu')", 0.9, "basic"),
            AISuggestion("cart-btn", "Add to cart", "tombol('+ Keranjang', warna='biru')", 0.9, "input"),
            AISuggestion("filter", "Product filter", "pilihan('Kategori', ['Fashion', 'Elektronik', 'Makanan'])", 0.85, "input"),
        ],
        "portfolio": [
            AISuggestion("hero", "Hero section", "bagian(judul('Portofolio Andi').besar().tengah())", 0.95, "layout"),
            AISuggestion("skills", "Skills section", "statistik([{'label': 'Python', 'value': 'Expert'}, {'label': 'React', 'value': 'Senior'}])", 0.9, "data"),
            AISuggestion("project", "Project cards", "grid(kartu(judul('Project 1'), paragraf('Deskripsi')), kolom=2)", 0.9, "layout"),
            AISuggestion("contact", "Contact section", "footer(copyright='2026')", 0.9, "navigation"),
        ],
    }

    @classmethod
    def get(cls, context: str) -> List[AISuggestion]:
        """Get suggestions for a context."""
        context_lower = context.lower()
        for key, suggestions in cls.SUGGESTIONS.items():
            if key in context_lower:
                return suggestions
        # Default: return landing suggestions
        return cls.SUGGESTIONS["landing"]

    @classmethod
    def get_by_category(cls, category: str) -> List[AISuggestion]:
        """Get suggestions by category."""
        results = []
        for suggestions in cls.SUGGESTIONS.values():
            for s in suggestions:
                if s.category == category:
                    results.append(s)
        return results

    @classmethod
    def get_random(cls, category: str, count: int = 3) -> List[AISuggestion]:
        """Get random suggestions from a category."""
        import random
        suggestions = cls.get_by_category(category)
        return random.sample(suggestions, min(count, len(suggestions)))


class AIUIBuilder:
    """
    AI-powered UI builder.

    Usage:
        ai = AIUIBuilder()

        # Generate components from description
        suggestions = ai.generate("Bikin form login")
        for s in suggestions:
            print(f"{s.component}: {s.code}")

        # Render from description
        html = ai.render("Bikin hero section judul 'Selamat Datang'")
    """

    def __init__(self):
        self.suggestions = SmartSuggestions()

    def generate(self, description: str) -> List[AISuggestion]:
        """Generate component suggestions from description."""
        return SmartSuggestions.get(description)

    def render(self, description: str) -> str:
        """Render components from description."""
        suggestions = self.generate(description)
        parts = []
        for s in suggestions:
            parts.append(f"<!-- {s.description} -->")
            parts.append(s.code)
        return "\n".join(parts)

    def suggest_code(self, description: str) -> str:
        """Suggest PyVibe code for a description."""
        suggestions = self.generate(description)
        lines = ["from pyvibe import *", ""]
        for s in suggestions:
            lines.append(f"# {s.description}")
            lines.append(s.code)
            lines.append("")
        return "\n".join(lines)

    def explain(self, component: str) -> str:
        """Explain how to use a component."""
        explanations = {
            "navbar": "Navbar adalah navigasi di bagian atas website.\n"
                     "Usage: navbar(logo='MyBrand', menu=['Beranda', 'Produk'])",
            "kartu": "Kartu (Card) untuk menampilkan konten dalam box.\n"
                    "Usage: kartu(judul('Title'), paragraf('Content'))",
            "tombol": "Tombol (Button) untuk aksi user.\n"
                     "Usage: tombol('Klik', warna='ungu')",
            "form": "Form untuk input data user.\n"
                   "Usage: FormBuilder().text('nama').email('email').build()",
            "hero": "Hero section untuk landing page.\n"
                   "Usage: bagian(judul('Judul Utama').besar().tengah())",
            "footer": "Footer section untuk akhir halaman.\n"
                     "Usage: footer(copyright='2026')",
        }
        return explanations.get(component, f"Component '{component}' belum ada dokumentasi.")

    def get_template(self, template_name: str) -> str:
        """Get a prompt template by name."""
        templates = {
            "landing": PromptTemplates.landing_page,
            "dashboard": PromptTemplates.dashboard,
            "form": PromptTemplates.form,
            "portfolio": PromptTemplates.portfolio,
            "ecommerce": PromptTemplates.ecommerce,
        }
        template_func = templates.get(template_name)
        if template_func:
            return template_func()
        return ""


class CodeGenerator:
    """Generate complete PyVibe code from specs."""

    @staticmethod
    def landing_page(title: str, subtitle: str = "",
                     features: Optional[List[str]] = None,
                     color: str = "#7C3AED") -> str:
        """Generate landing page code."""
        features = features or ["Cepat", "Mudah", "Aman"]
        feature_code = "\n".join(
            f'                kartu(teks("⚡").besar().tengah(), judul("{f}").tengah())'
            for f in features
        )

        # Add theme color CSS variables
        theme_css = f"""
:root {{
    --pv-primary: {color};
    --pv-primary-light: {color}22;
    --pv-primary-hover: {color}dd;
}}
"""

        return f'''{theme_css}from pyvibe import *

app = App("{title}")

@app.route("/")
def beranda():
    return tampil(
        navbar(judul("{title}"), tombol("Mulai", warna="ungu")),
        bagian(
            judul("{title}").besar().tengah(),
            paragraf("{subtitle or 'Solusi terbaik untuk Anda'}).tengah().warna("abu-400"),
            tombol("Mulai Sekarang", warna="ungu"),
            padding="96px 0",
            bg="gradient-ungu",
        ),
        bagian(
            grid(
{feature_code},
                kolom=3,
            ),
            padding="96px 0",
        ),
        footer(kontainer(paragraf("© 2026 {title}").tengah())),
    )

app.jalan()'''

    @staticmethod
    def dashboard(title: str = "Admin Panel",
                  stats: Optional[List[Dict]] = None) -> str:
        """Generate dashboard code."""
        stats = stats or [
            {"label": "Users", "value": "1,234", "icon": "👥"},
            {"label": "Revenue", "value": "Rp 45M", "icon": "💰"},
        ]

        stat_code = "\n".join(
            f'            kartu_stat("{s["label"]}", "{s["value"]}", ""),'
            for s in stats
        )

        return f'''from pyvibe import *

app = App("{title}")

@app.route("/")
def dashboard():
    return tampil(
        baris(
            sidebar("📊 Dashboard", "👥 Users", "⚙️ Settings"),
            kolom(10,
                judul("{title}").besar(),
                baris(
{stat_code},
                    gap="16px",
                ),
            ),
        ),
    )

app.jalan()'''

    @staticmethod
    def form_page(fields: Optional[List[str]] = None) -> str:
        """Generate form page code."""
        fields = fields or ["Nama", "Email", "Pesan"]
        field_code = "\n".join(
            f'    .text("{f.lower()}", label="{f}", required=True)'
            for f in fields
        )

        return f'''from pyvibe import *

app = App("Contact Form")

@app.route("/")
def form_page():
    form = (FormBuilder("contact")
{field_code}
        .submit("Kirim")
        .build()
    )

    return tampil(
        bagian(
            judul("Hubungi Kami").besar().tengah(),
            form.render(),
            padding="96px 0",
        ),
    )

app.jalan()'''

    @staticmethod
    def ecommerce_page(title: str = "Toko Online", products: Optional[List[Dict]] = None) -> str:
        """Generate e-commerce page code."""
        products = products or [
            {"nama": "Nike Air", "harga": "Rp 1.2M", "gambar": "nike.jpg", "kategori": "Fashion"},
            {"nama": "Adidas Run", "harga": "Rp 900K", "gambar": "adidas.jpg", "kategori": "Fashion"},
        ]

        product_cards = "\n".join(
            f'            kartu(gambar("{p["gambar"]}"), judul("{p["nama"]}"), teks("{p["harga"]}"))'
            for p in products
        )

        return f'''from pyvibe import *

app = App("{title}")

@app.route("/")
def beranda():
    produk = {str(products)}
    
    return tampil(
        navbar(judul("{title}"), menu=["Beranda", "Produk", "Kontak"]),
        bagian(
            judul("Toko Gacor 🛍️").besar().tengah(),
            paragraf("Belanja gampang, harga gacor!").tengah(),
            grid(
{product_cards},
                kolom=4,
                gap="24px",
                padding="32px",
            ),
        ),
        footer(kontainer(paragraf("© 2026 {title}").tengah())),
    )

app.jalan()'''

    @staticmethod
    def form_page_advanced(fields: Optional[List[Dict]] = None) -> str:
        """Generate advanced form code with validation."""
        fields = fields or [
            {"name": "nama", "label": "Nama", "type": "text", "required": True},
            {"name": "email", "label": "Email", "type": "email", "required": True, "validators": ["email"]},
            {"name": "pesan", "label": "Pesan", "type": "textarea"},
        ]

        field_code = "\n".join(
            f'    .{f["type"]}("{f["name"]}", label="{f["label"]}", required={str(f.get("required", False)).lower()})'
            f'{(f"Validators.{f["validators"][0]}" if f.get("validators") else "")}'
            for f in fields
        )

        return f'''from pyvibe import *

app = App("Formulir Canggih")

@app.route("/")
def form_page():
    form = (FormBuilder("canggih")
{field_code}
        .submit("Kirim")
        .build()
    )

    return tampil(
        bagian(
            judul("Formulir Canggih").besar().tengah(),
            form.render(),
            padding="96px 0",
        ),
    )

app.jalan()'''

    @staticmethod
    def about_page(title: str = "Tentang Kami", team: Optional[List[Dict]] = None) -> str:
        """Generate about page code."""
        team = team or [
            {"name": "Andi Pratama", "role": "Founder", "bio": "Senior Python Developer"},
            {"name": "Budi Santoso", "role": "CTO", "bio": "Full Stack Architect"},
        ]

        team_cards = "\n".join(
            f'            kartu(judul("{t["name"]}"), paragraf("{t["bio"]}"))'
            for t in team
        )

        return f'''from pyvibe import *

app = App("{title}")

@app.route("/")
def tentang():
    return tampil(
        navbar(judul("{title}"), menu=["Beranda", "Tim", "Kontak"]),
        bagian(
            judul("Tentang Kami").besar().tengah(),
            paragraf("Tim kami terdiri dari pengembang yang berpengalaman di berbagai industri.").tengah(),
            grid(
{team_cards},
                kolom=3,
                gap="24px",
            ),
            padding="64px 0",
        ),
        footer(kontainer(paragraf("© 2026 {title}").tengah())),
    )

app.jalan()'''

    @staticmethod
    def pricing_page(title: str = "Paket Langganan", plans: Optional[List[Dict]] = None) -> str:
        """Generate pricing page code."""
        plans = plans or [
            {"name": "Basic", "harga": "Rp 50.000/bulan", "fitur": ["1 project", "5 halaman"], "populer": False},
            {"name": "Pro", "harga": "Rp 150.000/bulan", "fitur": [" projects", "halaman tidak terbatas", "Support prioritas"], "populer": True},
            {"name": "Enterprise", "harga": "Rp 500.000/bulan", "fitur": [" projects tidak terbatas", "Support 24/7", "Manager khusus"], "populer": False},
        ]

        plan_cards = "\n".join(
            f'            kartu(judul("{p["name"]}"), teks("{p["harga"]}"), paragraf(", ".join(p["fitur"])))'
            f'{"'" if p.get("populer") else ""} .populer()" if p.get("populer") else ""'
            for p in plans
        )

        return f'''from pyvibe import *

app = App("{title}")

@app.route("/")
def pricing():
    return tampil(
        navbar(judul("{title}"), menu=["Beranda", "Fitur", "Kontak"]),
        bagian(
            judul("Pilih Paket yang Tepat").besar().tengah(),
            grid(
{plan_cards},
                kolom=3,
                gap="24px",
                padding="48px",
            ),
            padding="64px 0",
        ),
        footer(kontainer(paragraf("© 2026 {title}").tengah())),
    )

app.jalan()'''

    @staticmethod
    def contact_page(title: str = "Hubungi Kami", fields: Optional[List[str]] = None) -> str:
        """Generate contact page code."""
        fields = fields or ["Nama", "Email", "Pesan", "Topik"]

        field_code = "\n".join(
            f'    .text("{f.lower()}", label="{f}", required=True)'
            for f in fields
        )

        return f'''from pyvibe import *

app = App("{title}")

@app.route("/")
def kontak():
    form = (FormBuilder("kontak")
{field_code}
        .submit("Kirim")
        .build()
    )

    return tampil(
        bagian(
            judul("{title}").besar().tengah(),
            form.render(),
            padding="96px 0",
        ),
        footer(kontainer(paragraf("© 2026 {title}").tengah())),
    )

app.jalan()'''

    @staticmethod
    def portfolio_page(title: str = "Portofolio", projects: Optional[List[Dict]] = None) -> str:
        """Generate portfolio page code."""
        projects = projects or [
            {"name": "Project Alpha", "description": "Aplikasi pengelola inventory", "technologies": ["Python", "PyVibe", "SQL"]},
            {"name": "Project Beta", "description": "Website toko online", "technologies": ["HTML", "CSS", "JavaScript"]},
        ]

        project_cards = "\n".join(
            f'            kartu(judul("{p["name"]}"), paragraf("{p["description"]}"), teks(", ".join(p["technologies"])))'
            for p in projects
        )

        return f'''from pyvibe import *

app = App("{title}")

@app.route("/")
def portofolio():
    return tampil(
        navbar(judul("{title}"), menu=["Beranda", "Project", "Kontak"]),
        bagian(
            judul("Portofolio Saya").besar().tengah(),
            paragraf("Proyek-proyek terbaik saya.").tengah(),
            grid(
{project_cards},
                kolom=3,
                gap="24px",
            ),
            padding="64px 0",
        ),
        footer(kontainer(paragraf("© 2026 {title}").tengah())),
    )

app.jalan()'''