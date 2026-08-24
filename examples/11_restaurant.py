"""
PyVibe Example 11: Restaurant Website
Website restoran dengan menu, pemesanan, dan galeri.
"""
from pyvibe import *

app = App("Warung Nusantara")
app.theme("gelap")


# ==================== COMPONENTS ====================

def navbar():
    return _navbar(
        judul("🍜 Warung Nusantara", size="md"),
        baris(
            tautan("Menu", href="#menu"),
            tautan("Tentang", href="#tentang"),
            tautan("Galeri", href="#galeri"),
            tautan("Kontak", href="#kontak"),
        ).gap(6),
        tombol("Pesan Sekarang 🛒", warna="kuning"),
    )


def hero():
    return bagian(
        kontainer(
            baris(
                kolom(6,
                    badge("🔥 Promo Bulan Ini!", warna="merah"),
                    spasi(16),
                    judul("Rasa Nusantara Autentik 🇮🇩", size="xl"),
                    spasi(12),
                    paragraf(
                        "Masakan Indonesia asli dengan bumbu tradisional. "
                        "Dibuat dengan cinta, disajikan denganhangat.",
                        warna="abu-400",
                        size="lg",
                    ),
                    spasi(32),
                    baris(
                        tombol("Lihat Menu 📋", warna="kuning", size="lg"),
                        tombol("Pesan Online 🛵", warna="outline", size="lg"),
                    ).gap(4),
                    spasi(32),
                    baris(
                        stat_card("4.9 ⭐", "Rating"),
                        stat_card("1000+", "Order/Bulan"),
                        stat_card("15 Menit", "Delivery"),
                    ).gap(6),
                ),
                kolom(6,
                    kartu(
                        teks("🍜", size="4xl"),
                        judul("Mie Ayam Spesial", size="md"),
                        paragraf("Mie ayam dengan bumbu rahasia turun temurun.", warna="abu-400"),
                        baris(
                            teks("Rp 25.000", size="lg", warna="kuning"),
                            tombol("+ Keranjang", warna="kuning"),
                        ).justify("between").items("center"),
                        padding="24px",
                        border="1px solid #374151",
                    ),
                ),
            ).gap(8).items("center"),
            max_width="1200px",
        ),
        padding="96px 0",
        bg="gradient-kuning",
    )


def menu():
    kategori = [
        ("🍜 Mie & Bakso", [
            ("Mie Ayam Spesial", "Rp 25.000", "Mie ayam dengan bumbu rahasia.", "🔥 Best Seller"),
            ("Bakso Urat", "Rp 28.000", "Bakso urat sapi super kenyal.", ""),
            ("Mie Goreng Seafood", "Rp 32.000", "Mie goreng dengan udang & cumi.", ""),
        ]),
        ("🍚 Nasi & Rice Bowl", [
            ("Nasi Goreng Kampung", "Rp 22.000", "Nasi goreng dengan petai & teri.", ""),
            ("Chicken Katsu Don", "Rp 35.000", "Chicken katsu dengan nasi Jepang.", "⭐ Chef's Pick"),
            ("Nasi Rendang", "Rp 38.000", "Rendang Padang autentik.", ""),
        ]),
        ("🥤 Minuman", [
            ("Es Teh Manis", "Rp 8.000", "Teh manis es segar.", ""),
            ("Es Jeruk Segar", "Rp 12.000", "Jeruk peras segar.", ""),
            ("Kopi Tubruk", "Rp 15.000", "Kopi robusta Jawa.", "☕ Popular"),
        ]),
    ]

    sections = []
    for kategori_nama, items in kategori:
        cards = []
        for nama, harga, desc, badge_t in items:
            cards.append(
                kartu(
                    baris(
                        kolom(8,
                            badge(badge_t, warna="merah") if badge_t else spacer(height=0),
                            judul(nama, size="md"),
                            spasi(4),
                            paragraf(desc, warna="abu-400", size="sm"),
                        ),
                        kolom(4,
                            judul(harga, size="md").tengah(),
                            spasi(8),
                            tombol("+ Keranjang", warna="kuning", lebar="full"),
                        ),
                    ).gap(4).items("center").justify("between"),
                    padding="16px",
                    border="1px solid #374151",
                )
            )

        sections.append(
            bagian(
                judul(kategori_nama, size="md"),
                spasi(16),
                kolom(*cards, gap=12),
            )
        )

    return bagian(
        kontainer(
            judul("Menu Kami 📋", size="lg").tengah(),
            spasi(48),
            *sections,
            spasi(32),
            max_width="800px",
        ),
        padding="96px 0",
        id="menu",
    )


def about():
    return bagian(
        kontainer(
            baris(
                kolom(6,
                    judul("Tentang Kami 🏠", size="lg"),
                    spasi(16),
                    paragraf(
                        "Warung Nusantara sudah melayani masyarakat sejak tahun 2010. "
                        "Kami berkomitmen menghadirkan masakan Indonesia autentik dengan "
                        "bahan-bahan segar dan bumbu tradisional.",
                        warna="abu-400",
                    ),
                    spasi(16),
                    paragraf(
                        "Setiap masakan dibuat dengan penuh cinta oleh koki berpengalaman "
                        "kami. Dari Mie Ayam legendaris hingga Rendang Padang autentik.",
                        warna="abu-400",
                    ),
                    spasi(24),
                    baris(
                        stat_card("15+", "Tahun Pengalaman"),
                        stat_card("50+", "Menu Variasi"),
                        stat_card("10K+", "Pelanggan Setia"),
                    ).gap(4),
                ),
                kolom(6,
                    kartu(
                        teks("👨‍🍳", size="4xl"),
                        judul("Chef Budi", size="md"),
                        paragraf("Head Chef dengan pengalaman 20 tahun.", warna="abu-400"),
                        paragraf('"Masakan yang baik adalah masakan yang dibuat dengan cinta."', italic=True, warna="abu-300"),
                        padding="24px",
                        border="1px solid #374151",
                    ),
                ),
            ).gap(8).items("center"),
            max_width="1000px",
        ),
        padding="96px 0",
        bg="bg-gray-900",
    )


def gallery():
    items = ["🍜", "🍚", "🍛", "🥘", "🍲", "🥤"]
    cards = []
    for icon in items:
        cards.append(
            kartu(
                teks(icon, size="4xl"),
                padding="48px",
                border="1px solid #374151",
                radius="12px",
                bg="bg-gray-800",
            )
        )

    return bagian(
        kontainer(
            judul("Galeri Kami 📸", size="lg").tengah(),
            spasi(48),
            grid(*cards, kolom=3, gap=16),
            max_width="800px",
        ),
        padding="96px 0",
    )


def contact():
    return bagian(
        kontainer(
            judul("Kontak Kami 📞", size="lg").tengah(),
            spasi(48),
            baris(
                kolom(6,
                    judul("Kirim Pesan", size="md"),
                    spasi(16),
                    input_teks("Nama Lengkap", placeholder="Masukkan nama lo"),
                    spasi(8),
                    input_email("Email", placeholder="email@contoh.com"),
                    spasi(8),
                    input_teks("Telepon", placeholder="08xxx"),
                    spasi(8),
                    textarea("Pesan", placeholder="Tulis pesan lo di sini...", rows=4),
                    spasi(16),
                    tombol("Kirim Pesan 📨", warna="kuning", lebar="full"),
                ),
                kolom(6,
                    judul("Informasi", size="md"),
                    spasi(16),
                    kartu(
                        judul("📍 Alamat", size="sm"),
                        paragraf("Jl. Sudirman No. 123, Jakarta Selatan", warna="abu-400", size="sm"),
                        padding="16px",
                        border="1px solid #374151",
                    ),
                    spasi(8),
                    kartu(
                        judul("⏰ Jam Buka", size="sm"),
                        paragraf("Senin - Minggu: 10:00 - 22:00", warna="abu-400", size="sm"),
                        padding="16px",
                        border="1px solid #374151",
                    ),
                    spasi(8),
                    kartu(
                        judul("📱 Telepon", size="sm"),
                        paragraf("0812-3456-7890", warna="abu-400", size="sm"),
                        padding="16px",
                        border="1px solid #374151",
                    ),
                ),
            ).gap(8),
            max_width="1000px",
        ),
        padding="96px 0",
        bg="bg-gray-900",
    )


def _footer():
    return footer(
        kontainer(
            baris(
                kolom(4,
                    judul("🍜 Warung Nusantara", size="md"),
                    spasi(8),
                    paragraf("Masakan Indonesia autentik dengan cita rasa yang tak terlupakan.", size="sm", warna="abu-400"),
                ),
                kolom(2,
                    judul("Menu", size="sm"),
                    tautan("Mie & Bakso", href="#menu"),
                    tautan("Nasi & Rice Bowl", href="#menu"),
                    tautan("Minuman", href="#menu"),
                ),
                kolom(2,
                    judul("Info", size="sm"),
                    tautan("Tentang Kami", href="#tentang"),
                    tautan("Galeri", href="#galeri"),
                    tautan("Kontak", href="#kontak"),
                ),
                kolom(2,
                    judul("Lainnya", size="sm"),
                    tautan("Karir", href="#karir"),
                    tautan("Blog", href="#blog"),
                    tautan("FAQ", href="#faq"),
                ),
            ).gap(8),
            spasi(32),
            pemisah(),
            spasi(16),
            baris(
                paragraf("© 2026 Warung Nusantara. All rights reserved.", size="xs", warna="abu-500"),
                paragraf("Made with ❤️ in Jakarta", size="xs", warna="abu-500"),
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
        menu(),
        about(),
        gallery(),
        contact(),
        _footer(),
        scroll_to_top(),
    )


if __name__ == "__main__":
    app.jalan(port=8011)
