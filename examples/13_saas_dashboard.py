"""
PyVibe Example 13: SaaS Dashboard
Dashboard admin untuk aplikasi SaaS dengan sidebar, stats, dan charts.
"""
from pyvibe import *

app = App("SaaS Dashboard", theme="gelap")
state = State(sidebar_open=True, active_page="dashboard")


@app.route("/")
def dashboard():
    return tampil(
        baris(
            # Sidebar
            sidebar(
                "📊 Dashboard",
                "👥 Users",
                "📦 Products",
                "💰 Revenue",
                "📈 Analytics",
                "⚙️ Settings",
                judul="SaaS App",
            ),
            
            # Main Content
            kolom(10,
                navbar(
                    judul("Dashboard"),
                    baris(
                        notifikasi("3 new", warna="merah"),
                        avatar("Admin"),
                        gap="16px",
                    ),
                    gap="32px",
                ),
                
                kontainer(
                    judul("Welcome back, Admin! 👋", size="lg"),
                    spasi(8),
                    paragraf("Here's what's happening with your business today.", warna="abu-400"),
                    spasi(24),
                    
                    # Stats Cards
                    baris(
                        kartu_stat("Total Users", "12,345", "+12.5%"),
                        kartu_stat("Revenue", "Rp 45.2M", "+8.2%"),
                        kartu_stat("Orders", "1,234", "+23.1%"),
                        kartu_stat("Conversion", "3.24%", "+1.2%"),
                        gap="16px",
                    ),
                    
                    spasi(32),
                    
                    # Charts Row
                    baris(
                        kolom(8,
                            kartu(
                                judul_kartu("Revenue Overview"),
                                grafik_sederhana([
                                    {"label": "Jan", "value": 45},
                                    {"label": "Feb", "value": 52},
                                    {"label": "Mar", "value": 48},
                                    {"label": "Apr", "value": 61},
                                    {"label": "May", "value": 55},
                                    {"label": "Jun", "value": 67},
                                ]),
                                padding="24px",
                                border="1px solid #374151",
                            ),
                        ),
                        kolom(4,
                            kartu(
                                judul_kartu("Top Products"),
                                tabel(
                                    [
                                        {"Produk": "Pro Plan", "Sales": "1,234"},
                                        {"Produk": "Enterprise", "Sales": "567"},
                                        {"Produk": "Starter", "Sales": "890"},
                                    ],
                                    kolom=["Produk", "Sales"],
                                ),
                                padding="24px",
                                border="1px solid #374151",
                            ),
                        ),
                        gap="16px",
                    ),
                    
                    spasi(32),
                    
                    # Recent Orders
                    kartu(
                        judul_kartu("Recent Orders"),
                        tabel(
                            [
                                {"Order": "#1234", "Customer": "Budi Santoso", "Amount": "Rp 1.2M", "Status": "Completed"},
                                {"Order": "#1235", "Customer": "Sari Dewi", "Amount": "Rp 850K", "Status": "Pending"},
                                {"Order": "#1236", "Customer": "Andi Pratama", "Amount": "Rp 2.1M", "Status": "Processing"},
                                {"Order": "#1237", "Customer": "Maya Putri", "Amount": "Rp 450K", "Status": "Completed"},
                            ],
                            kolom=["Order", "Customer", "Amount", "Status"],
                        ),
                        padding="24px",
                        border="1px solid #374151",
                    ),
                ),
            ),
        ),
    )


if __name__ == "__main__":
    app.jalan(port=8013)
