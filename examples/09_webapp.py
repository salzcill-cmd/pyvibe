"""
PyVibe Example 09: Web Application (SPA)
Aplikasi web lengkap dengan routing, state, dan komponen interaktif.
"""
from pyvibe import *

app = App("PyVibe Web App")
app.theme("gelap")
state = State({"halaman": "beranda", "user": None, "notifications": 3})


# ==================== COMPONENTS ====================

def komponen_navbar():
    """Navbar utama"""
    return navbar(
        judul("🐍 PyVibe", size="md"),
        baris(
            tautan("Beranda", href="#beranda"),
            tautan("Produk", href="#produk"),
            tautan("Blog", href="#blog"),
            tautan("Kontak", href="#kontak"),
        ).gap(4),
        baris(
            tombol("Masuk", warna="outline"),
            tombol("Daftar", warna="biru"),
        ).gap(2),
    )


def komponen_hero():
    """Hero section"""
    return bagian(
        kontainer(
            baris(
                kolom(7,
                    badge("🚀 V2.0 Sudah Rilis!", warna="hijau"),
                    spasi(16),
                    judul("Bangun Website Keren dengan Python", size="xl"),
                    spasi(8),
                    paragraf(
                        "PyVibe bikin frontend development jadi gampang. "
                        "Tulis kode Python, langsung jadi website cantik.",
                        warna="abu-400",
                    ),
                    spasi(24),
                    baris(
                        tombol("Mulai Sekarang", warna="biru", icon="rocket"),
                        tombol("Lihat Demo", warna="outline"),
                    ).gap(4),
                    spasi(32),
                    baris(
                        stat_card("⭐ 2.5k", "GitHub Stars"),
                        stat_card("📦 50+", "Components"),
                        stat_card("📥 10k+", "Downloads"),
                    ).gap(6),
                ),
                kolom(5,
                    kartu(
                        code_block('''
from pyvibe import *

app = App("My Site")
app.tampil(
    judul("Halo!"),
    tombol("Klik Saya"),
)
app.jalan()''', bahasa="python"),
                        judul_kartu("Quick Start"),
                    ),
                ),
            ).gap(8).items("center"),
            max_width="1200px",
        ),
        padding="96px 0",
        bg="gradient-biru",
    )


def komponen_fitur():
    """Features section"""
    fitur = [
        ("🗣️", "Natural Language", "Tulis kode kayak ngobrol. PyVibe convert otomatis."),
        ("🎨", "50+ Components", "Komponen UI lengkap, responsive by default."),
        ("⚡", "Hot Reload", "Perubahan langsung keliatan tanpa refresh."),
        ("🌙", "Dark Mode", "Tema gelap built-in, satu baris kode."),
        ("🛡️", "Security Built-in", "CSRF, XSS, rate limiting sudah include."),
        ("📦", "Zero Config", "Install, tulis kode, langsung jalan."),
    ]

    cards = []
    for icon, judul_t, desc in fitur:
        cards.append(
            kartu(
                teks(icon, size="3xl"),
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
            judul("Kenapa PyVibe? 🤔", size="lg").tengah(),
            spasi(8),
            paragraf("Fitur yang bikin development jadi fun & cepat.", warna="abu-400").tengah(),
            spasi(48),
            grid(*cards, kolom=3, gap=24),
            max_width="1200px",
        ),
        padding="96px 0",
        bg="bg-gray-900",
    )


def komponen_pricing():
    """Pricing section"""
    paket = [
        ("Gratis", "Rp 0", [
            "58+ Components",
            "Natural Language",
            "Responsive Design",
            "Dark Mode",
            "Community Support",
        ], False),
        ("Pro", "Rp 99K/bulan", [
            "Semua fitur Gratis",
            "Priority Support",
            "Custom Themes",
            "Advanced Components",
            "API Access",
        ], True),
        ("Enterprise", "Hubungi Kami", [
            "Semua fitur Pro",
            "Dedicated Support",
            "Custom Development",
            "SLA Guarantee",
            "Training Sessions",
        ], False),
    ]

    cards = []
    for nama, harga, fiturs, highlight in paket:
        bg = "bg-biru-600" if highlight else "bg-gray-800"
        border = "2px solid #3B82F6" if highlight else "1px solid #374151"

        items = []
        for f in fiturs:
            items.append(baris(
                teks("✅", size="sm"),
                paragraf(f, size="sm"),
            ).gap(2).items("center"))

        cards.append(
            kartu(
                badge("POPULER" if highlight else "", warna="biru") if highlight else spacer(height=24),
                judul(nama, size="md"),
                spasi(8),
                judul(harga, size="lg"),
                spasi(16),
                *items,
                spasi(24),
                tombol("Pilih Paket" if highlight else "Mulai", warna="biru" if highlight else "outline", lebar="full"),
                padding="32px",
                border=border,
                radius="16px",
                bg=bg,
            )
        )

    return bagian(
        kontainer(
            judul("Harga 💰", size="lg").tengah(),
            spasi(8),
            paragraf("Pilih paket yang cocok buat lo.", warna="abu-400").tengah(),
            spasi(48),
            grid(*cards, kolom=3, gap=24),
            max_width="1000px",
        ),
        padding="96px 0",
    )


def komponen_testimoni():
    """Testimonials section"""
    testimonials = [
        ("Budi", "Full-stack Developer", "PyVibe bikin frontend jadi fun! Gak perlu lagi pusing sama CSS.", "⭐⭐⭐⭐⭐"),
        ("Sari", "UI/UX Designer", "Natural language syntax-nya gila sih, inovatif banget.", "⭐⭐⭐⭐⭐"),
        ("Andi", "Startup Founder", "Prototype website cuma 10 menit. Mantap!", "⭐⭐⭐⭐⭐"),
    ]

    cards = []
    for nama, role, quote, bintang in testimonials:
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
                    kolom(
                        teks(bintang, size="sm"),
                    ),
                ).gap(3).items("center").justify("between"),
                padding="24px",
                border="1px solid #374151",
                radius="12px",
            )
        )

    return bagian(
        kontainer(
            judul("Apa Kata Mereka? 💬", size="lg").tengah(),
            spasi(48),
            grid(*cards, kolom=3, gap=24),
            max_width="1200px",
        ),
        padding="96px 0",
        bg="bg-gray-900",
    )


def komponen_cta():
    """Call to Action"""
    return bagian(
        kontainer(
            judul("Siap Mulai? 🚀", size="lg").tengah(),
            spasi(8),
            paragraf("Install PyVibe sekarang dan mulai bikin website impian lo.", warna="abu-300").tengah(),
            spasi(24),
            baris(
                tombol("pip install pyvibe", warna="hijau", icon="terminal"),
                tombol("Lihat Dokumentasi", warna="outline"),
            ).gap(4).tengah(),
            max_width="600px",
        ),
        padding="96px 0",
        bg="gradient-ungu",
        tengah=True,
    )


def komponen_footer():
    """Footer"""
    return footer(
        kontainer(
            baris(
                kolom(4,
                    judul("🐍 PyVibe", size="md"),
                    spasi(8),
                    paragraf("Build frontend websites in Python as easy as chatting.", size="sm", warna="abu-400"),
                ),
                kolom(2,
                    judul("Product", size="sm"),
                    tautan("Features", href="#fitur"),
                    tautan("Pricing", href="#harga"),
                    tautan("Docs", href="#docs"),
                    tautan("Blog", href="#blog"),
                ),
                kolom(2,
                    judul("Community", size="sm"),
                    tautan("GitHub", href="#github"),
                    tautan("Discord", href="#discord"),
                    tautan("Twitter", href="#twitter"),
                    tautan("Telegram", href="#telegram"),
                ),
                kolom(2,
                    judul("Company", size="sm"),
                    tautan("About", href="#about"),
                    tautan("Contact", href="#contact"),
                    tautan("Careers", href="#careers"),
                ),
            ).gap(8),
            spasi(32),
            pemisah(),
            spasi(16),
            baris(
                paragraf("© 2026 PyVibe. All rights reserved.", size="xs", warna="abu-500"),
                paragraf("Made with ❤️ in Indonesia", size="xs", warna="abu-500"),
            ).justify("between"),
        ),
        max_width="1200px",
        padding="48px 24px",
    )


# ==================== PAGES ====================

@app.route("/")
def beranda():
    return tampil(
        komponen_navbar(),
        komponen_hero(),
        komponen_fitur(),
        komponen_pricing(),
        komponen_testimoni(),
        komponen_cta(),
        komponen_footer(),
        scroll_to_top(),
    )


@app.route("/produk")
def produk():
    return tampil(
        komponen_navbar(),
        bagian(
            kontainer(
                judul("Produk Kami 📦", size="lg").tengah(),
                spasi(48),
                grid(
                    kartu(
                        badge("Baru!", warna="hijau"),
                        judul("PyVibe Core", size="md"),
                        paragraf("Framework utama untuk build website.", warna="abu-400"),
                        tombol("Pelajari →", warna="biru"),
                        padding="24px",
                        border="1px solid #374151",
                    ),
                    kartu(
                        badge("Pro", warna="ungu"),
                        judul("PyVibe UI Kit", size="md"),
                        paragraf("100+ komponen premium siap pakai.", warna="abu-400"),
                        tombol("Pelajari →", warna="biru"),
                        padding="24px",
                        border="1px solid #374151",
                    ),
                    kartu(
                        judul("PyVibe CLI", size="md"),
                        paragraf("Command line tool untuk manage project.", warna="abu-400"),
                        tombol("Pelajari →", warna="biru"),
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
        komponen_footer(),
    )


if __name__ == "__main__":
    app.jalan(port=8009)
