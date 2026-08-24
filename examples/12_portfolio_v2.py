"""
PyVibe Example 12: Developer Portfolio v2
Portfolio website profesional dengan dark mode dan animations.
"""
from pyvibe import *

app = App("Developer Portfolio", theme="gelap")


@app.route("/")
def beranda():
    return tampil(
        navbar(
            judul("👨‍💻 John Doe"),
            baris(
                tautan("About", url="#about"),
                tautan("Projects", url="#projects"),
                tautan("Skills", url="#skills"),
                tautan("Contact", url="#contact"),
                gap="24px",
            ),
            tombol("Hire Me", warna="biru"),
            gap="32px",
        ),
        
        # Hero
        bagian(
            kontainer(
                baris(
                    kolom(7,
                        badge("Available for hire", warna="hijau"),
                        spasi(16),
                        judul("Hi, I'm John Doe 👋", size="xl").tebal(),
                        spasi(12),
                        paragraf("Full-stack Developer | UI/UX Enthusiast | Open Source Contributor", warna="abu-300", size="lg"),
                        spasi(24),
                        paragraf(
                            "I build beautiful, performant web applications with modern technologies. "
                            "Passionate about clean code and great user experiences.",
                            warna="abu-400",
                        ),
                        spasi(32),
                        baris(
                            tombol("View Projects", warna="biru"),
                            tombol("Download CV", warna="outline"),
                            gap="16px",
                        ),
                        spasi(32),
                        baris(
                            stat_card("💼", "5+", "Years Exp"),
                            stat_card("🚀", "50+", "Projects"),
                            stat_card("⭐", "1K+", "GitHub Stars"),
                            gap="16px",
                        ),
                    ),
                    kolom(5,
                        avatar("John Doe", size="lg"),
                    ),
                    gap="48px",
                ),
                max_width="1200px",
            ),
            padding="96px 0",
        ),
        
        # Skills
        bagian(
            kontainer(
                judul("Skills & Technologies 🛠️", size="lg").tengah(),
                spasi(48),
                grid(
                    kartu(
                        teks("🐍", size="2xl"),
                        judul("Python", size="md"),
                        paragraf("Django, Flask, FastAPI", warna="abu-400", size="sm"),
                        progress_bar(90),
                        padding="24px",
                        border="1px solid #374151",
                    ),
                    kartu(
                        teks("⚛️", size="2xl"),
                        judul("React", size="md"),
                        paragraf("Next.js, Redux, TypeScript", warna="abu-400", size="sm"),
                        progress_bar(85),
                        padding="24px",
                        border="1px solid #374151",
                    ),
                    kartu(
                        teks("🎨", size="2xl"),
                        judul("CSS/Design", size="md"),
                        paragraf("Tailwind, Figma, UI/UX", warna="abu-400", size="sm"),
                        progress_bar(80),
                        padding="24px",
                        border="1px solid #374151",
                    ),
                    kartu(
                        teks("🗄️", size="2xl"),
                        judul("Database", size="md"),
                        paragraf("PostgreSQL, MongoDB, Redis", warna="abu-400", size="sm"),
                        progress_bar(75),
                        padding="24px",
                        border="1px solid #374151",
                    ),
                    kartu(
                        teks("☁️", size="2xl"),
                        judul("DevOps", size="md"),
                        paragraf("Docker, AWS, CI/CD", warna="abu-400", size="sm"),
                        progress_bar(70),
                        padding="24px",
                        border="1px solid #374151",
                    ),
                    kartu(
                        teks("📱", size="2xl"),
                        judul("Mobile", size="md"),
                        paragraf("React Native, Flutter", warna="abu-400", size="sm"),
                        progress_bar(65),
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
        
        # Projects
        bagian(
            kontainer(
                judul("Featured Projects 🚀", size="lg").tengah(),
                spasi(48),
                grid(
                    kartu(
                        badge("Featured", warna="ungu"),
                        judul("E-Commerce Platform", size="md"),
                        spasi(8),
                        paragraf("Full-stack e-commerce with payment integration, real-time inventory, and analytics dashboard.", warna="abu-400", size="sm"),
                        spasi(16),
                        baris(
                            badge("Python", warna="biru"),
                            badge("React", warna="cyan"),
                            badge("PostgreSQL", warna="hijau"),
                            gap="4px",
                        ),
                        spasi(16),
                        baris(
                            tautan("Live Demo →"),
                            tautan("GitHub →"),
                            gap="16px",
                        ),
                        padding="24px",
                        border="1px solid #374151",
                        radius="12px",
                    ),
                    kartu(
                        badge("Open Source", warna="hijau"),
                        judul("PyVibe Framework", size="md"),
                        spasi(8),
                        paragraf("Python frontend framework with Natural Language syntax and 58+ components.", warna="abu-400", size="sm"),
                        spasi(16),
                        baris(
                            badge("Python", warna="biru"),
                            badge("HTML/CSS", warna="orange"),
                            gap="4px",
                        ),
                        spasi(16),
                        baris(
                            tautan("Live Demo →"),
                            tautan("GitHub →"),
                            gap="16px",
                        ),
                        padding="24px",
                        border="1px solid #374151",
                        radius="12px",
                    ),
                    kolom=2,
                    gap=24,
                ),
                max_width="1000px",
            ),
            padding="96px 0",
        ),
        
        # Contact
        bagian(
            kontainer(
                judul("Get In Touch 📬", size="lg").tengah(),
                spasi(8),
                paragraf("Let's work together on your next project!", warna="abu-400").tengah(),
                spasi(48),
                baris(
                    kolom(6,
                        input_teks("Name", placeholder="Your name"),
                        spasi(12),
                        input_email("Email", placeholder="your@email.com"),
                        spasi(12),
                        textarea("Message", placeholder="Tell me about your project...", rows=4),
                        spasi(16),
                        tombol("Send Message", warna="biru", lebar="full"),
                    ),
                    kolom(6,
                        kartu(
                            judul_kartu("Contact Info"),
                            baris(tombol_icon("📧"), paragraf("john@example.com")), gap="8px",
                            spasi(12),
                            baris(tombol_icon("📍"), paragraf("Jakarta, Indonesia")), gap="8px",
                            spasi(12),
                            baris(tombol_icon("💼"), paragraf("linkedin.com/in/johndoe")), gap="8px",
                            spasi(12),
                            baris(tombol_icon("🐙"), paragraf("github.com/johndoe")), gap="8px",
                            padding="24px",
                            border="1px solid #374151",
                            radius="12px",
                        ),
                    ),
                    gap="48px",
                ),
                max_width="1000px",
            ),
            padding="96px 0",
            bg="bg-gray-900",
        ),
        
        footer(
            kontainer(
                paragraf("© 2026 John Doe. Built with 🐍 PyVibe").tengah(),
                spasi(16),
                baris(
                    tautan("GitHub"),
                    tautan("LinkedIn"),
                    tautan("Twitter"),
                    gap="16px",
                ).tengah(),
            ),
            padding="48px 0",
        ),
        
        scroll_to_top(),
    )


if __name__ == "__main__":
    app.jalan(port=8012)
