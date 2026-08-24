"""
PyVibe Example 14: Modern Blog
Blog website dengan featured posts, categories, dan newsletter.
"""
from pyvibe import *

app = App("Tech Blog", theme="gelap")


@app.route("/")
def beranda():
    return tampil(
        navbar(
            judul("📝 TechBlog"),
            baris(
                tautan("Home", url="/"),
                tautan("Articles", url="#articles"),
                tautan("Categories", url="#categories"),
                tautan("About", url="#about"),
                gap="24px",
            ),
            baris(
                input_teks("Search...", placeholder="Search articles"),
                tombol("Subscribe", warna="biru"),
                gap="8px",
            ),
            gap="32px",
        ),
        
        # Hero
        bagian(
            kontainer(
                judul("Tech Blog 📚", size="xl").tengah(),
                spasi(8),
                paragraf("Insights, tutorials, and news about web development.", warna="abu-400").tengah(),
                spasi(48),
                
                # Featured Post
                kartu(
                    badge("Featured", warna="ungu"),
                    judul("Building Modern Web Apps with PyVibe", size="lg"),
                    spasi(12),
                    paragraf(
                        "Learn how to build beautiful, responsive websites using Python and PyVibe framework. "
                        "From zero to production in minutes.",
                        warna="abu-400",
                    ),
                    spasi(24),
                    baris(
                        avatar("John Doe"),
                        kolom(
                            paragraf("John Doe", size="sm"),
                            paragraf("Aug 24, 2026 · 8 min read", size="xs", warna="abu-500"),
                        ),
                        tombol("Read More →", warna="biru"),
                        justify="between",
                    ),
                    padding="32px",
                    border="2px solid #7C3AED",
                    radius="16px",
                ),
                max_width="900px",
            ),
            padding="96px 0",
            bg="gradient-biru",
        ),
        
        # Categories
        bagian(
            kontainer(
                judul("Browse Categories 📂", size="lg").tengah(),
                spasi(32),
                baris(
                    kartu(teks("🐍", size="2xl"), judul("Python", size="md"), paragraf("42 articles", warna="abu-400", size="sm"), padding="24px", border="1px solid #374151"),
                    kartu(teks("⚛️", size="2xl"), judul("React", size="md"), paragraf("38 articles", warna="abu-400", size="sm"), padding="24px", border="1px solid #374151"),
                    kartu(teks("🎨", size="2xl"), judul("CSS", size="md"), paragraf("28 articles", warna="abu-400", size="sm"), padding="24px", border="1px solid #374151"),
                    kartu(teks("☁️", size="2xl"), judul("DevOps", size="md"), paragraf("19 articles", warna="abu-400", size="sm"), padding="24px", border="1px solid #374151"),
                    gap="16px",
                ),
                max_width="1000px",
            ),
            padding="64px 0",
        ),
        
        # Latest Articles
        bagian(
            kontainer(
                judul("Latest Articles ✍️", size="lg").tengah(),
                spasi(48),
                grid(
                    kartu(
                        badge("Python", warna="biru"),
                        judul("10 Tips Python untuk Pemula", size="md"),
                        spasi(8),
                        paragraf("Tips dan trik Python yang wajib diketahui developer pemula.", warna="abu-400", size="sm"),
                        spasi(16),
                        baris(
                            paragraf("Aug 20, 2026", size="xs", warna="abu-500"),
                            paragraf("5 min read", size="xs", warna="abu-500"),
                            justify="between",
                        ),
                        padding="24px",
                        border="1px solid #374151",
                    ),
                    kartu(
                        badge("React", warna="cyan"),
                        judul("React vs PyVibe: Which to Choose?", size="md"),
                        spasi(8),
                        paragraf("A comprehensive comparison of modern frontend frameworks.", warna="abu-400", size="sm"),
                        spasi(16),
                        baris(
                            paragraf("Aug 18, 2026", size="xs", warna="abu-500"),
                            paragraf("7 min read", size="xs", warna="abu-500"),
                            justify="between",
                        ),
                        padding="24px",
                        border="1px solid #374151",
                    ),
                    kartu(
                        badge("CSS", warna="orange"),
                        judul("Modern CSS Layout Techniques", size="md"),
                        spasi(8),
                        paragraf("Master Flexbox and Grid with practical examples.", warna="abu-400", size="sm"),
                        spasi(16),
                        baris(
                            paragraf("Aug 15, 2026", size="xs", warna="abu-500"),
                            paragraf("6 min read", size="xs", warna="abu-500"),
                            justify="between",
                        ),
                        padding="24px",
                        border="1px solid #374151",
                    ),
                    kolom=3,
                    gap=24,
                ),
                max_width="1200px",
            ),
            padding="96px 0",
            bg="bg-gray-900",
        ),
        
        # Newsletter
        bagian(
            kontainer(
                judul("Subscribe to Newsletter 📧", size="lg").tengah(),
                spasi(8),
                paragraf("Get the latest articles delivered to your inbox.", warna="abu-400").tengah(),
                spasi(24),
                baris(
                    input_email("Email", placeholder="your@email.com"),
                    tombol("Subscribe", warna="biru"),
                    gap="8px",
                ).tengah(),
                max_width="500px",
            ),
            padding="96px 0",
            bg="gradient-ungu",
        ),
        
        footer(
            kontainer(
                baris(
                    judul("📝 TechBlog", size="md"),
                    paragraf("© 2026 TechBlog. Built with 🐍 PyVibe", size="sm", warna="abu-400"),
                    justify="between",
                ),
            ),
            padding="48px 0",
        ),
    )


if __name__ == "__main__":
    app.jalan(port=8014)
