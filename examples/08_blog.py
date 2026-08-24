"""
🐍 Example 8: Blog Website — blog sederhana!

Usage:
    python examples/08_blog.py
"""

from pyvibe import *

app = App("PyVibe Blog", title="PyVibe Blog — Tips & Tricks")

# Sample blog posts
posts = [
    {
        "judul": "Cara Memulai dengan PyVibe",
        "slug": "cara-memulai-pyvibe",
        "excerpt": "Tutorial lengkap cara bikin website pertama pakai PyVibe.",
        "date": "24 Agustus 2026",
        "kategori": "Tutorial",
        "read_time": "5 min",
    },
    {
        "judul": "10 Fitur PyVibe yang Wajib Diketahui",
        "slug": "10-fitur-pyvibe",
        "excerpt": "Fitur-fitur keren PyVibe yang bikin coding jadi gampang.",
        "date": "22 Agustus 2026",
        "kategori": "Tips",
        "read_time": "7 min",
    },
    {
        "judul": "Membangun Dashboard dengan PyVibe",
        "slug": "membangun-dashboard",
        "excerpt": "Step-by-step bikin dashboard admin profesional.",
        "date": "20 Agustus 2026",
        "kategori": "Tutorial",
        "read_time": "10 min",
    },
    {
        "judul": "PyVibe vs React: Perbandingan Lengkap",
        "slug": "pyvibe-vs-react",
        "excerpt": "PerbandinganPyVibe dengan React dari berbagai aspek.",
        "date": "18 Agustus 2026",
        "kategori": "Review",
        "read_time": "8 min",
    },
    {
        "judul": "Natural Language Syntax: coding Kayak Ngobrol",
        "slug": "natural-language-syntax",
        "excerpt": "Cara pakai natural language syntax di PyVibe.",
        "date": "16 Agustus 2026",
        "kategori": "Fitur",
        "read_time": "6 min",
    },
    {
        "judul": "Tips Responsive Design dengan PyVibe",
        "slug": "tips-responsive-design",
        "excerpt": "Tips bikin website responsive tanpa mikir CSS.",
        "date": "14 Agustus 2026",
        "kategori": "Tips",
        "read_time": "5 min",
    },
]


@app.route("/")
def beranda():
    return tampil(
        # Navbar
        navbar(
            logo="📝 PyVibe Blog",
            menu=["Beranda", "Tutorial", "Tips", "Tentang"],
            tombol_daftar="Subscribe",
        ),

        # Hero
        bagian(
            judul("PyVibe Blog").besar().tengah(),
            paragraf("Tips, tutorial, dan berita seputar PyVibe.").tengah(),
            padding="64px 32px",
            bg="gradient-ungu",
        ),

        # Featured Post
        bagian(
            judul("Artikel Terbaru").tengah(),
            grid(
                kartu(
                    badge(posts[0]["kategori"], warna="ungu"),
                    judul_kartu(posts[0]["judul"]),
                    paragraf(posts[0]["excerpt"]),
                    baris(
                        teks(posts[0]["date"]),
                        teks(f"• {posts[0]['read_time']} read"),
                    ),
                    spacer("12px"),
                    tautan("Baca Selengkapnya →", url=f'/blog/{posts[0]["slug"]}'),
                ),
                kartu(
                    badge(posts[1]["kategori"], warna="biru"),
                    judul_kartu(posts[1]["judul"]),
                    paragraf(posts[1]["excerpt"]),
                    baris(
                        teks(posts[1]["date"]),
                        teks(f"• {posts[1]['read_time']} read"),
                    ),
                    spacer("12px"),
                    tautan("Baca Selengkapnya →", url=f'/blog/{posts[1]["slug"]}'),
                ),
                kolom=2, gap="24px",
            ),
            padding="64px 32px",
        ),

        # All Posts
        bagian(
            judul("Semua Artikel").tengah(),
            grid(
                *[
                    kartu(
                        badge(post["kategori"], warna="ungu" if post["kategori"] == "Tutorial" else "biru"),
                        judul_kartu(post["judul"]),
                        paragraf(post["excerpt"]),
                        baris(
                            teks(post["date"]),
                            teks(f"• {post['read_time']} read"),
                        ),
                        spacer("12px"),
                        tautan("Baca →", url=f'/blog/{post["slug"]}'),
                    )
                    for post in posts[2:]
                ],
                kolom=3, gap="24px",
            ),
            padding="64px 32px",
            bg="terang",
        ),

        # Newsletter
        bagian(
            judul("Subscribe Newsletter").tengah(),
            paragraf("Dapatkan artikel terbaru langsung di inbox lo.").tengah(),
            kartu(
                baris(
                    input_email(label="", placeholder="Email address..."),
                    tombol("Subscribe", warna="ungu"),
                    gap="12px",
                ),
            ),
            padding="64px 32px",
        ),

        # Footer
        footer(
            links=["Beranda", "Tutorial", "Tips", "Kontak"],
            copyright="© 2026 PyVibe Blog. Built with 🐍 PyVibe",
        ),
    )


@app.route("/blog/<slug>")
def blog_post(slug):
    # Find post by slug
    post = next((p for p in posts if p["slug"] == slug), None)

    if not post:
        return tampil(
            judul("404 - Artikel Tidak Ditemukan"),
            paragraf("Artikel yang lo cari gak ada."),
            tautan("Kembali ke Beranda", url="/"),
        )

    return tampil(
        navbar(logo="📝 PyVibe Blog"),
        bagian(
            badge(post["kategori"], warna="ungu"),
            judul(post["judul"]).besar(),
            baris(
                teks(post["date"]),
                teks(f"• {post['read_time']} read"),
            ),
            spacer("24px"),
            paragraf(post["excerpt"]),
            paragraf("Ini adalah contoh konten blog. Di production, konten ini akan dimuat dari database atau CMS."),
            paragraf("PyVibe memudahkan developer untuk bikin website tanpa harus mikir CSS yang ribet."),
            paragraf("Dengan syntax yang natural dan components yang lengkap, lo bisa fokus ke konten."),
            padding="64px 32px",
        ),
        footer(copyright="© 2026 PyVibe Blog"),
    )


if __name__ == "__main__":
    print("📝 PyVibe Blog")
    print("=" * 50)
    app.export("output/08_blog")
    print("✅ Exported to output/08_blog/")
    print()
    app.jalan()
