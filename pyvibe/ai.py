"""
🐍 PyVibe AI — Integrasi AI/LLM untuk component generation.

"AI bantu bikin UI, kamu tinggal duduk manis."

Features:
- AIUIBuilder — Generate UI from natural language
- SmartSuggestions — Get component suggestions
- CodeGenerator — Generate PyVibe code
- PromptTemplates — Common AI prompts

Usage:
    from pyvibe.ai import AIUIBuilder, PromptTemplates

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


class SmartSuggestions:
    """Get smart component suggestions based on context."""

    SUGGESTIONS = {
        "landing": [
            AISuggestion("navbar", "Navigation bar", "navbar(logo, menu)", 0.9, "navigation"),
            AISuggestion("hero", "Hero section", "bagian(judul().besar().tengah())", 0.95, "layout"),
            AISuggestion("features", "Feature grid", "grid(kartu(), kolom=3)", 0.9, "layout"),
            AISuggestion("cta", "Call to action", "tombol('Mulai Sekarang')", 0.85, "input"),
            AISuggestion("footer", "Footer", "footer(copyright='2026')", 0.9, "navigation"),
        ],
        "dashboard": [
            AISuggestion("sidebar", "Sidebar navigation", "sidebar('Dashboard', 'Users')", 0.9, "navigation"),
            AISuggestion("stats", "Stat cards", "kartu_stat('Users', '1,234')", 0.95, "layout"),
            AISuggestion("table", "Data table", "tabel(data)", 0.9, "data"),
            AISuggestion("chart", "Chart", "chart_bar(data)", 0.85, "charts"),
        ],
        "form": [
            AISuggestion("input", "Text input", "input_teks(label='Nama')", 0.95, "input"),
            AISuggestion("email", "Email input", "input_email(label='Email')", 0.95, "input"),
            AISuggestion("password", "Password input", "input_sandi(label='Password')", 0.9, "input"),
            AISuggestion("textarea", "Textarea", "textarea(label='Pesan')", 0.9, "input"),
            AISuggestion("submit", "Submit button", "tombol('Kirim')", 0.9, "input"),
        ],
        "ecommerce": [
            AISuggestion("product-card", "Product card", "kartu(gambar(), judul(), harga())", 0.95, "layout"),
            AISuggestion("price", "Price display", "teks('Rp 100.000').warna('ungu')", 0.9, "basic"),
            AISuggestion("cart-btn", "Add to cart", "tombol('+ Keranjang', warna='biru')", 0.9, "input"),
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
        }
        return explanations.get(component, f"Component '{component}' belum ada dokumentasi.")


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

        return f'''from pyvibe import *

app = App("{title}")

@app.route("/")
def beranda():
    return tampil(
        navbar(judul("{title}"), tombol("Mulai", warna="ungu")),
        bagian(
            judul("{title}").besar().tengah(),
            paragraf("{subtitle or 'Solusi terbaik untuk Anda'}").tengah().warna("abu-400"),
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
