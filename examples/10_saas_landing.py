"""
PyVibe Example 10: SaaS Landing Page
Landing page lengkap untuk produk SaaS.
"""
from pyvibe import *

app = App("SaaS Landing Page")
app.theme("gelap")


# ==================== COMPONENTS ====================

def navbar():
    return _navbar(
        judul("🚀 LaunchPad", size="md"),
        baris(
            tautan("Fitur", href="#fitur"),
            tautan("Harga", href="#harga"),
            tautan("Blog", href="#blog"),
            tautan("Dokumentasi", href="#docs"),
        ).gap(6),
        baris(
            tombol("Masuk", warna="outline"),
            tombol("Mulai Gratis", warna="biru"),
        ).gap(3),
    )


def hero():
    return bagian(
        kontainer(
            baris(
                kolom(6,
                    badge("✨ Versi 2.0 Sudah Rilis!", warna="hijau"),
                    spasi(16),
                    judul("Deploy Website dalam Hitungan Menit", size="xl"),
                    spasi(12),
                    paragraf(
                        "Platform all-in-one untuk build, deploy, dan scale "
                        "website tanpa ribet. Fokus coding, biar kita handle sisanya.",
                        warna="abu-400",
                        size="lg",
                    ),
                    spasi(32),
                    baris(
                        tombol("Mulai Gratis →", warna="biru", size="lg"),
                        tombol("Watch Demo ▶", warna="outline", size="lg"),
                    ).gap(4),
                    spasi(32),
                    baris(
                        stat_card("10K+", "Developers"),
                        stat_card("99.9%", "Uptime"),
                        stat_card("50ms", "Avg Response"),
                    ).gap(6),
                ),
                kolom(6,
                    kartu(
                        code_block('''
# Deploy dalam 3 langkah
pip install launchpad

# 1. Buat project
launchpad init my-app

# 2. Develop
launchpad dev

# 3. Deploy
launchpad deploy''', bahasa="bash"),
                        judul_kartu("Quick Deploy ⚡"),
                        border="1px solid #3B82F6",
                    ),
                ),
            ).gap(8).items("center"),
            max_width="1200px",
        ),
        padding="96px 0",
        bg="gradient-biru",
    )


def logos():
    return bagian(
        kontainer(
            paragraf("Dipercaya oleh 10,000+ developer dari:", warna="abu-500").tengah(),
            spasi(32),
            baris(
                teks("Google", size="xl", warna="abu-600"),
                teks("Microsoft", size="xl", warna="abu-600"),
                teks("Stripe", size="xl", warna="abu-600"),
                teks("Vercel", size="xl", warna="abu-600"),
                teks("Netlify", size="xl", warna="abu-600"),
            ).gap(12).tengah().items("center"),
            max_width="800px",
        ),
        padding="48px 0",
    )


def fitur():
    items = [
        ("⚡", "Lightning Fast", "Build time < 1 detik. Hot reload instant. Gak ada lag."),
        ("🔒", "Secure by Default", "SSL, CSRF, XSS protection sudah include. Gak perlu setup."),
        ("📈", "Auto Scaling", "Traffic naik? Tenang, server auto scale sesuai load."),
        ("🎨", "Beautiful UI", "50+ komponen responsive. Dark mode built-in."),
        ("🌍", "Global CDN", "Website lo di-deploy ke 50+ data center全球."),
        ("🔌", "Plugin System", "Install plugin dari community. Extend sesuai kebutuhan."),
    ]

    cards = []
    for icon, judul_t, desc in items:
        cards.append(
            kartu(
                teks(icon, size="2xl"),
                spasi(12),
                judul(judul_t, size="md"),
                spasi(4),
                paragraf(desc, warna="abu-400", size="sm"),
                padding="24px",
                border="1px solid #374151",
                radius="12px",
            )
        )

    return bagian(
        kontainer(
            judul("Fitur Unggulan 🛠️", size="lg").tengah(),
            spasi(8),
            paragraf("Semua yang lo butuhkan untuk build website production-ready.", warna="abu-400").tengah(),
            spasi(48),
            grid(*cards, kolom=3, gap=24),
            max_width="1200px",
        ),
        padding="96px 0",
    )


def cara_kerja():
    langkah = [
        ("1", "Install", "pip install launchpad", "Cuma satu command untuk install."),
        ("2", "Develop", "launchpad dev", "Hot reload, auto browser, error overlay."),
        ("3", "Deploy", "launchpad deploy", "One-click deploy ke production."),
    ]

    steps = []
    for nomor, judul_t, code, desc in langkah:
        steps.append(
            baris(
                teks(nomor, size="2xl", warna="biru"),
                kolom(
                    judul(judul_t, size="md"),
                    code_block(code, bahasa="bash"),
                    paragraf(desc, warna="abu-400", size="sm"),
                ),
            ).gap(4).items("start")
        )

    return bagian(
        kontainer(
            judul("3 Langkah Saja 🎯", size="lg").tengah(),
            spasi(48),
            kolom(*[s for i, s in enumerate(steps) for _ in [spasi(32)] if i > 0], gap=0),
            max_width="600px",
        ),
        padding="96px 0",
        bg="bg-gray-900",
    )


def pricing():
    paket = [
        ("Starter", "Gratis", [
            "1 Project",
            "1GB Storage",
            "Basic Analytics",
            "Community Support",
            "Custom Domain",
        ], False),
        ("Pro", "Rp 199K/bulan", [
            "Unlimited Projects",
            "100GB Storage",
            "Advanced Analytics",
            "Priority Support",
            "Custom Domains",
            "SSL Certificate",
            "API Access",
        ], True),
        ("Enterprise", "Rp 999K/bulan", [
            "Semua fitur Pro",
            "Unlimited Storage",
            "Dedicated Server",
            "24/7 Support",
            "SLA 99.99%",
            "Custom Integrations",
            "Training Sessions",
            "Dedicated Account Manager",
        ], False),
    ]

    cards = []
    for nama, harga, fiturs, highlight in paket:
        bg = "bg-biru-900" if highlight else "bg-gray-800"
        border = "2px solid #3B82F6" if highlight else "1px solid #374151"

        items = []
        for f in fiturs:
            items.append(baris(
                teks("✅", size="sm"),
                paragraf(f, size="sm"),
            ).gap(2).items("center"))

        cards.append(
            kartu(
                badge("PALING POPULER ⭐", warna="biru") if highlight else spacer(height=28),
                judul(nama, size="md"),
                spasi(8),
                judul(harga, size="lg"),
                spasi(4),
                paragraf("per bulan" if harga != "Gratis" else "", size="xs", warna="abu-500"),
                spasi(24),
                *items,
                spasi(24),
                tombol("Mulai Sekarang" if highlight else "Pilih Paket", warna="biru" if highlight else "outline", lebar="full"),
                padding="32px",
                border=border,
                radius="16px",
            )
        )

    return bagian(
        kontainer(
            judul("Harga Transparan 💰", size="lg").tengah(),
            spasi(8),
            paragraf("Gak ada biaya tersembunyi. Bayar yang lo pakai.", warna="abu-400").tengah(),
            spasi(48),
            grid(*cards, kolom=3, gap=24),
            max_width="1000px",
        ),
        padding="96px 0",
    )


def testimoni():
    items = [
        ("Rizky Pratama", "CTO, TechStart", "LaunchPad bikin deployment jadi gampang banget. Dari 2 jam jadi 2 menit."),
        ("Maya Sari", "Full-stack Dev", "Platform terbaik yang pernah gue pake. Performance-nya gila!"),
        ("Dimas Putra", "Indie Hacker", "Startup gue scale dari 0 ke 100K users tanpa pindah platform. Mantap!"),
    ]

    cards = []
    for nama, role, quote in items:
        cards.append(
            kartu(
                paragraf(f'"{quote}"', italic=True),
                spasi(16),
                baris(
                    avatar(nama, size="sm"),
                    kolom(
                        judul(nama, size="sm"),
                        paragraf(role, size="xs", warna="abu-400"),
                    ),
                ).gap(3).items("center"),
                padding="24px",
                border="1px solid #374151",
                radius="12px",
            )
        )

    return bagian(
        kontainer(
            judul("Testimoni 💬", size="lg").tengah(),
            spasi(48),
            grid(*cards, kolom=3, gap=24),
            max_width="1200px",
        ),
        padding="96px 0",
        bg="bg-gray-900",
    )


def faq():
    pertanyaan = [
        ("Apa itu LaunchPad?", "LaunchPad adalah platform all-in-one untuk build, deploy, dan scale website. Semua tools yang lo butuhkan ada di satu tempat."),
        ("Gratis gak sih?", "Ya! Paket Starter gratis selamanya. Lo bisa upgrade ke Pro atau Enterprise kalau butuh fitur lebih."),
        ("Support bahasa apa aja?", "Python (PyVibe), JavaScript, TypeScript, Go, Rust, dan banyak lagi. Kita support 20+ bahasa pemrograman."),
        ("Bagaimana dengan keamanan?", "Security adalah prioritas kami. SSL, CSRF, XSS protection, dan DDoS mitigation sudah include di semua paket."),
    ]

    cards = []
    for q, a in pertanyaan:
        cards.append(
            accordion(q, a)
        )

    return bagian(
        kontainer(
            judul("FAQ ❓", size="lg").tengah(),
            spasi(48),
            kolom(*cards, gap=12),
            max_width="800px",
        ),
        padding="96px 0",
    )


def cta():
    return bagian(
        kontainer(
            judul("Siap Launch Website? 🚀", size="lg").tengah(),
            spasi(8),
            paragraf("Mulai gratis. Gak perlu kartu kredit.", warna="abu-300").tengah(),
            spasi(24),
            baris(
                tombol("Mulai Gratis Sekarang →", warna="biru", size="lg"),
                tombol("Hubungi Sales", warna="outline", size="lg"),
            ).gap(4).tengah(),
            max_width="600px",
        ),
        padding="96px 0",
        bg="gradient-biru",
        tengah=True,
    )


def _footer():
    return footer(
        kontainer(
            baris(
                kolom(4,
                    judul("🚀 LaunchPad", size="md"),
                    spasi(8),
                    paragraf("Platform all-in-one untuk build, deploy, dan scale website.", size="sm", warna="abu-400"),
                    spasi(16),
                    baris(
                        tautan("Twitter", href="#twitter"),
                        tautan("GitHub", href="#github"),
                        tautan("Discord", href="#discord"),
                    ).gap(4),
                ),
                kolom(2,
                    judul("Product", size="sm"),
                    tautan("Features", href="#fitur"),
                    tautan("Pricing", href="#harga"),
                    tautan("Docs", href="#docs"),
                    tautan("Blog", href="#blog"),
                    tautan("Changelog", href="#changelog"),
                ),
                kolom(2,
                    judul("Company", size="sm"),
                    tautan("About", href="#about"),
                    tautan("Careers", href="#careers"),
                    tautan("Contact", href="#contact"),
                    tautan("Press Kit", href="#press"),
                ),
                kolom(2,
                    judul("Resources", size="sm"),
                    tautan("Community", href="#community"),
                    tautan("Templates", href="#templates"),
                    tautan("Plugins", href="#plugins"),
                    tautan("Status", href="#status"),
                ),
                kolom(2,
                    judul("Legal", size="sm"),
                    tautan("Privacy", href="#privacy"),
                    tautan("Terms", href="#terms"),
                    tautan("Security", href="#security"),
                    tautan("GDPR", href="#gdpr"),
                ),
            ).gap(8),
            spasi(32),
            pemisah(),
            spasi(16),
            baris(
                paragraf("© 2026 LaunchPad. All rights reserved.", size="xs", warna="abu-500"),
                paragraf("Made with ❤️ by PyVibe Team", size="xs", warna="abu-500"),
            ).justify("between"),
        ),
        max_width="1200px",
        padding="48px 24px",
    )


# ==================== PAGES ====================

@app.route("/")
def beranda():
    return tampil(
        navbar(),
        hero(),
        logos(),
        fitur(),
        cara_kerja(),
        pricing(),
        testimoni(),
        faq(),
        cta(),
        _footer(),
        scroll_to_top(),
    )


if __name__ == "__main__":
    app.jalan(port=8010)
