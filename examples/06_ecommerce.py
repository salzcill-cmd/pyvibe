"""
🐍 Example 6: E-commerce Website — toko online lengkap!

Usage:
    python examples/06_ecommerce.py
"""

from pyvibe import *

app = App("Toko Gacor", title="Toko Gacor — Belanja Gampang Harga Gacor")

# Sample data
produk_list = [
    {"nama": "Nike Air Max", "harga": "Rp 1.299.000", "gambar": "👟", "kategori": "Sepatu"},
    {"nama": "MacBook Air", "harga": "Rp 15.999.000", "gambar": "💻", "kategori": "Elektronik"},
    {"nama": "iPhone 15", "harga": "Rp 18.999.000", "gambar": "📱", "kategori": "Handphone"},
    {"nama": "Samsung TV 55\"", "harga": "Rp 7.499.000", "gambar": "📺", "kategori": "Elektronik"},
    {"nama": "PlayStation 5", "harga": "Rp 6.299.000", "gambar": "🎮", "kategori": "Gaming"},
    {"nama": "AirPods Pro", "harga": "Rp 3.499.000", "gambar": "🎧", "kategori": "Audio"},
]


@app.route("/")
def beranda():
    return tampil(
        # Navbar
        navbar(
            logo="🛍️ Toko Gacor",
            menu=["Beranda", "Produk", "Kategori", "Tentang"],
            tombol_login="Login",
            tombol_daftar="Daftar",
        ),

        # Hero
        bagian(
            judul("Belanja Gampang,\nHarga Gacor!").besar().tengah(),
            paragraf("Temukan produk terbaik dengan harga terjangkau.").tengah(),
            baris(
                tombol("Mulai Belanja 🛒", warna="ungu", ukuran="besar"),
                tombol("Lihat Produk", warna="outline", ukuran="besar"),
                justify="center", gap="16px",
            ),
            padding="96px 32px",
            bg="gradient-pink",
        ),

        # Stats
        bagian(
            baris(
                count_down(10000, label="Produk"),
                count_down(50000, label="Pelanggan"),
                count_down(100, label="Kota"),
                count_down(99, label="Puas"),
                justify="center", gap="64px",
            ),
            padding="48px 32px",
            bg="terang",
        ),

        # Kategori
        bagian(
            judul("Kategori Populer").tengah(),
            baris(
                kartu(
                    judul_kartu("👟 Sepatu"),
                    paragraf("500+ produk"),
                ),
                kartu(
                    judul_kartu("💻 Elektronik"),
                    paragraf("300+ produk"),
                ),
                kartu(
                    judul_kartu("📱 Handphone"),
                    paragraf("200+ produk"),
                ),
                kartu(
                    judul_kartu("🎮 Gaming"),
                    paragraf("150+ produk"),
                ),
                justify="center", gap="24px",
            ),
            padding="64px 32px",
        ),

        # Produk Terlaris
        bagian(
            judul("Produk Terlaris").tengah(),
            paragraf("Produk paling diminati pelanggan kami.").tengah(),
            grid(
                *[
                    kartu(
                        Component(tag="div", content=produk["gambar"], style={"font_size": "3rem", "text_align": "center"}),
                        judul_kartu(produk["nama"]),
                        Component(tag="div", content=produk["harga"], style={"font_size": "1.25rem", "font_weight": "700", "color": "#7C3AED"}),
                        badge(produk["kategori"]),
                        spacer("12px"),
                        tombol("Tambah ke Keranjang 🛒", warna="ungu"),
                    )
                    for produk in produk_list
                ],
                kolom=3,
                gap="24px",
            ),
            padding="64px 32px",
        ),

        # Promo
        bagian(
            judul("🔥 Promo Spesial!").besar().tengah(),
            paragraf("Diskon hingga 50% untuk produk terpilih!").tengah(),
            tombol("Lihat Promo", warna="ungu", ukuran="besar"),
            padding="64px 32px",
            bg="gradient-ungu",
        ),

        # Testimoni
        bagian(
            judul("Apa Kata Pelanggan?").tengah(),
            grid(
                kartu(
                    paragraf("""Produknya bagus-bagus, harga juga terjangkau. Pengiriman cepat!"""),
                    baris(
                        avatar("https://i.pravatar.cc/40?img=1", ukuran="40px"),
                        teks("Andi, Jakarta"),
                    ),
                ),
                kartu(
                    paragraf("""Pelayanannya ramah, barang sesuai pesanan. Recommended!"""),
                    baris(
                        avatar("https://i.pravatar.cc/40?img=2", ukuran="40px"),
                        teks("Budi, Bandung"),
                    ),
                ),
                kartu(
                    paragraf("""Belanja di sini gampang banget, tinggal pilih langsung dikirim."""),
                    baris(
                        avatar("https://i.pravatar.cc/40?img=3", ukuran="40px"),
                        teks("Citra, Surabaya"),
                    ),
                ),
                kolom=3, gap="24px",
            ),
            padding="64px 32px",
            bg="terang",
        ),

        # Footer
        footer(
            links=["Produk", "Kategori", "Promo", "Kontak", "FAQ"],
            copyright="© 2026 Toko Gacor. Made with 🐍 PyVibe",
        ),
    )


@app.route("/produk/<id>")
def detail_produk(id):
    return tampil(
        navbar(logo="🛍️ Toko Gacor"),
        bagian(
            judul(f"Produk #{id}").besar(),
            paragraf("Detail produk akan ditampilkan di sini."),
            padding="64px 32px",
        ),
        footer(copyright="© 2026 Toko Gacor"),
    )


if __name__ == "__main__":
    print("🛍️ Toko Gacor — E-commerce Demo")
    print("=" * 50)
    app.export("output/06_ecommerce")
    print("✅ Exported to output/06_ecommerce/")
    print()
    app.jalan()
