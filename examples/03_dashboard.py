"""
🐍 Example 3: Dashboard Admin — panel administrasi lengkap!

Dashboard dengan sidebar, stats cards, charts, dan data table.

Usage:
    python examples/03_dashboard.py
"""

from pyvibe import *

app = App("Dashboard Admin", title="Admin Dashboard — PyVibe")

@app.route("/")
def dashboard():
    return tampil(
        # ===== Sidebar =====
        sidebar(
            "📊 Beranda",
            "📦 Produk",
            "🛒 Pesanan",
            "👥 Pelanggan",
            "📈 Laporan",
            "⚙️ Pengaturan",
            judul="Admin Panel",
            aktif="📊 Beranda",
        ),

        # ===== Main Content =====
        Component(
            tag="div",
            # Offset for sidebar
        ),

        # ===== Header =====
        baris(
            judul("Dashboard"),
            spacer(),
            badge("Admin", warna="ungu"),
            justify="space-between",
            align="center",
        ),

        # ===== Stats Cards =====
        grid(
            kartu_stat("Total Penjualan", "Rp 328 Juta", "+12% bulan lalu", "up", "💰"),
            kartu_stat("Pesanan Hari Ini", "142", "+8% dari kemarin", "up", "📦"),
            kartu_stat("Pelanggan Aktif", "1,234", "+3% bulan ini", "up", "👥"),
            kartu_stat("Rating Toko", "4.8 ⭐", "+0.2 dari bulan lalu", "up", "⭐"),
            kolom=4,
            gap="16px",
        ),

        spacer("24px"),

        # ===== Charts Row =====
        baris(
            # Bar Chart
            kartu(
                judul_kartu("Tren Penjualan 6 Bulan"),
                grafik_sederhana(
                    data=[
                        {"label": "Januari", "value": 45},
                        {"label": "Februari", "value": 52},
                        {"label": "Maret", "value": 48},
                        {"label": "April", "value": 61},
                        {"label": "Mei", "value": 55},
                        {"label": "Juni", "value": 67},
                    ],
                    warna="#7C3AED",
                ),
            ),

            # Summary Card
            kartu(
                judul_kartu("Ringkasan"),
                statistik([
                    {"nilai": "142", "label": "Pesanan", "icon": "📦"},
                    {"nilai": "98%", "label": "Terkirim", "icon": "✅"},
                    {"nilai": "4.8", "label": "Rating", "icon": "⭐"},
                ]),
            ),
        ),

        spacer("24px"),

        # ===== Recent Orders Table =====
        kartu(
            baris(
                judul_kartu("Pesanan Terbaru"),
                spacer(),
                tombol("+ Tambah Pesanan", warna="ungu"),
            ),
            tabel(
                data=[
                    {"id": "#001", "pelanggan": "Andi", "produk": "Nike Air Max", "total": "Rp 1.299.000", "status": "Dikirim"},
                    {"id": "#002", "pelanggan": "Budi", "produk": "MacBook Air", "total": "Rp 15.999.000", "status": "Diproses"},
                    {"id": "#003", "pelanggan": "Citra", "produk": "iPhone 15", "total": "Rp 18.999.000", "status": "Selesai"},
                    {"id": "#004", "pelanggan": "Dian", "produk": "Samsung TV 55\"", "total": "Rp 7.499.000", "status": "Dikirim"},
                    {"id": "#005", "pelanggan": "Eka", "produk": "PlayStation 5", "total": "Rp 6.299.000", "status": "Diproses"},
                ],
                kolom=["id", "pelanggan", "produk", "total", "status"],
            ),
        ),

        spacer("24px"),

        # ===== Bottom Row =====
        baris(
            # Quick Actions
            kartu(
                judul_kartu("Aksi Cepat"),
                baris(
                    tombol("📦 Tambah Produk", warna="ungu"),
                    tombol("📊 Lihat Laporan", warna="biru"),
                    gap="12px",
                ),
                spacer("16px"),
                baris(
                    tombol("👤 Tambah Pelanggan", warna="hijau"),
                    tombol("⚙️ Pengaturan", warna="abu"),
                    gap="12px",
                ),
            ),

            # Activity
            kartu(
                judul_kartu("Aktivitas Terbaru"),
                paragraf("📦 Pesanan #001 berhasil dikirim"),
                paragraf("💰 Pembayaran diterima dari Budi"),
                paragraf("👤 Pelanggan baru: Fajar mendaftar"),
                paragraf("⭐ Rating 5 bintang dari Citra"),
            ),
        ),

        # ===== Footer =====
        footer(
            copyright="© 2026 Admin Dashboard. Built with 🐍 PyVibe",
        ),
    )

app.jalan()
