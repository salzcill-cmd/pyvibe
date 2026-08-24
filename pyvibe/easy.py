"""
🐍 PyVibe Easy — Bikin website sesimpel ngobrol.

"Gak perlu ribet, tinggal bilang maunya apa."

Usage:
    from pyvibe.easy import *

    # Satu baris udah jadi website!
    halaman("Halo Dunia!")

    # Atau bikin lebih lengkap
    halaman(
        judul("Selamat Datang"),
        teks("Ini website gue."),
        tombol("Klik Disini"),
    )

    # Landing page dalam 5 baris
    landing(
        judul="Toko Gacor",
        subjudul="Belanja gampang, harga mantap!",
        fitur=["Cepat", "Murah", "Aman"],
    )
"""

from pyvibe.core.component import Component
from pyvibe.core.renderer import tampil


# ==================== Super Simple Functions ====================

def halaman(*children, judul: str = "", **kwargs) -> str:
    """
    Bikin halaman HTML dari komponen.

    Usage:
        halaman(judul("Halo"), paragraf("Dunia"))
        halaman("Teks langsung jadi halaman")
    """
    from pyvibe.components.basic import judul as j, paragraf as p, teks as t
    from pyvibe.core.renderer import Renderer

    components = []
    for child in children:
        if isinstance(child, str):
            # Auto-detect: kalau cuma string, jadiin paragraf
            components.append(p(child))
        elif isinstance(child, Component):
            components.append(child)

    renderer = Renderer()
    return renderer.render(*components)


def ringkas(*teks_items, **kwargs) -> str:
    """
    Render komponen jadi HTML string.

    Usage:
        html = ringkas(judul("Halo"), paragraf("Dunia"))
    """
    from pyvibe.core.renderer import Renderer
    renderer = Renderer()
    return renderer.render(*teks_items)


# ==================== One-Liner Templates ====================

def halaman_sederhana(judul_teks: str, teks_teks: str = "") -> str:
    """
    Halaman sederhana satu judul.

    Usage:
        halaman_sederhana("Selamat Datang!")
        halaman_sederhana("Halo", "Ini website gue.")
    """
    from pyvibe.components.basic import judul, paragraf
    from pyvibe.core.renderer import Renderer
    components = [judul(judul_teks)]
    if teks_teks:
        components.append(paragraf(teks_teks))
    renderer = Renderer()
    return renderer.render(*components)


def landing(
    judul: str = "Selamat Datang",
    subjudul: str = "",
    tombol_teks: str = "Mulai",
    fitur: list = None,
    copyright: str = "",
    **kwargs,
) -> str:
    """
    Bikin landing page lengkap dalam satu fungsi.

    Usage:
        landing(
            judul="Toko Gacor",
            subjudul="Belanja gampang!",
            tombol_teks="Beli Sekarang",
            fitur=["Cepat", "Murah", "Aman"],
        )
    """
    from pyvibe.components.basic import judul as j, paragraf as p, teks as t, spasi, gradien_teks
    from pyvibe.components.input import tombol as tb
    from pyvibe.components.layout import bagian, kontainer, grid, kartu, baris
    from pyvibe.components.navigation import navbar, footer
    from pyvibe.core.renderer import Renderer

    components = []

    # Navbar
    components.append(navbar(j(judul, level=3)))

    # Hero Section
    hero_content = [j(judul).besar().tengah()]
    if subjudul:
        hero_content.append(spasi("16px"))
        hero_content.append(p(subjudul).tengah().warna("abu-400").besar())
    hero_content.append(spasi("32px"))
    hero_content.append(tb(tombol_teks, warna="ungu"))
    components.append(bagian(kontainer(*hero_content).tengah(), padding="96px 0", bg="gradient-ungu"))

    # Fitur Section
    if fitur:
        fitur_items = []
        icons = ["⚡", "🎨", "🔒", "🚀", "💰", "✨", "🎯", "🔥"]
        for i, f in enumerate(fitur):
            icon = icons[i % len(icons)]
            fitur_items.append(kartu(
                t(icon).besar().tengah(),
                j(f, level=3).tengah(),
                padding="24px",
            ))
        components.append(bagian(
            kontainer(grid(*fitur_items, kolom=min(len(fitur), 3), gap="24px")).tengah(),
            padding="96px 0",
        ))

    # Footer
    if copyright:
        components.append(footer(kontainer(p(copyright).tengah(), padding="24px 0")))
    else:
        components.append(footer(kontainer(p(f"© 2026 {judul}. Built with 🐍 PyVibe").tengah(), padding="24px 0")))

    renderer = Renderer()
    return renderer.render(*components)


def dashboard(
    judul: str = "Dashboard",
    stats: list = None,
    data: list = None,
    menu: list = None,
    **kwargs,
) -> str:
    """
    Bikin dashboard admin dalam satu fungsi.

    Usage:
        dashboard(
            judul="Admin Panel",
            stats=[
                {"judul": "Users", "nilai": "1,234", "perubahan": "+12%"},
                {"judul": "Revenue", "nilai": "Rp 45M", "perubahan": "+8%"},
            ],
            data=[
                {"Action": "User Signup", "Time": "2 min ago"},
            ],
        )
    """
    from pyvibe.components.basic import judul as j, paragraf as p
    from pyvibe.components.layout import kartu_stat, kartu, judul_kartu, baris, kontainer
    from pyvibe.components.data import tabel
    from pyvibe.components.navigation import sidebar, navbar
    from pyvibe.core.renderer import Renderer

    components = []

    # Sidebar + Main
    sidebar_items = menu or ["📊 Dashboard", "👥 Users", "⚙️ Settings"]
    sidebar_items.insert(0, j(judul, level=3))

    main_content = []

    # Navbar
    main_content.append(navbar(j(judul)))

    # Stats
    if stats:
        stat_cards = []
        for s in stats:
            stat_cards.append(kartu_stat(
                s.get("judul", ""),
                s.get("nilai", "0"),
                s.get("perubahan", ""),
            ))
        main_content.append(baris(*stat_cards, gap="16px"))
        main_content.append(spasi("24px"))

    # Data Table
    if data:
        main_content.append(kartu(
            judul_kartu("Data"),
            tabel(data),
        ))

    components.append(baris(
        sidebar(*sidebar_items),
        kontainer(*main_content, padding="24px"),
    ))

    renderer = Renderer()
    return renderer.render(*components)


# ==================== Smart Components ====================

def judul_teks(teks: str, level: int = 1) -> Component:
    """Judul otomatis."""
    from pyvibe.components.basic import judul
    return judul(teks, level=level)


def par(teks: str) -> Component:
    """Paragraf pendek."""
    from pyvibe.components.basic import paragraf
    return paragraf(teks)


def btn(teks: str = "Klik", warna: str = "ungu") -> Component:
    """Tombol pendek."""
    from pyvibe.components.input import tombol
    return tombol(teks, warna=warna)


def img(src: str, alt: str = "") -> Component:
    """Gambar pendek."""
    from pyvibe.components.basic import gambar
    return gambar(src, alt=alt)


def link(teks: str, url: str = "#") -> Component:
    """Tautan pendek."""
    from pyvibe.components.basic import tautan
    return tautan(teks, url=url)


def kartu_sederhana(judul: str = "", *isi, **kwargs) -> Component:
    """Kartu sederhana."""
    from pyvibe.components.layout import kartu, judul_kartu
    children = []
    if judul:
        children.append(judul_kartu(judul))
    children.extend(isi)
    return kartu(*children, **kwargs)


def form_sederhana(*fields: str, submit_text: str = "Kirim") -> str:
    """
    Form sederhana dari list nama field.

    Usage:
        form_sederhana("Nama", "Email", "Pesan", submit_text="Kirim")
    """
    from pyvibe.forms import FormBuilder, Validators
    from pyvibe.core.renderer import Renderer

    builder = FormBuilder()
    for field_name in fields:
        name = field_name.lower().replace(" ", "_")
        if "email" in name:
            builder.email(name, label=field_name, required=True)
        elif "sandi" in name or "password" in name or "kata" in name:
            builder.password(name, label=field_name, required=True)
        elif "pesan" in name or "deskripsi" in name or "message" in name:
            builder.textarea(name, label=field_name)
        else:
            builder.text(name, label=field_name, required=True)
    builder.submit(submit_text)
    form_component = builder.build().render()
    renderer = Renderer()
    return renderer.render(form_component)


def tabel_sederhana(data: list, **kwargs) -> str:
    """Tabel sederhana dari list of dict."""
    from pyvibe.components.data import tabel
    from pyvibe.core.renderer import Renderer
    renderer = Renderer()
    return renderer.render(tabel(data, **kwargs))


# ==================== Indonesian Aliases ====================

# Biar lebih natural, tambahin alias bahasa Indonesia

def halo(dunia: str = "Dunia!") -> str:
    """Halo Dunia! - Hello World versi PyVibe."""
    return halaman_sederhana(f"Halo, {dunia}!")


def selamat_datang(nama: str = "Developer") -> str:
    """Selamat datang page."""
    return landing(
        judul=f"Selamat Datang, {nama}!",
        subjudul="Selamat datang di website PyVibe kamu.",
        tombol_teks="Mulai",
    )


def portofolio(nama: str, skill: list = None) -> str:
    """Bikin halaman portofolio."""
    from pyvibe.components.basic import judul as j, paragraf as p, spasi, badge
    from pyvibe.components.layout import bagian, kontainer, grid, kartu, baris
    from pyvibe.core.renderer import Renderer

    skills = skill or ["Python", "PyVibe", "Web Dev"]
    components = [
        bagian(
            kontainer(
                j(f"Hi, I'm {nama} 👋").besar().tengah(),
                spasi("16px"),
                p("Full-stack Developer").tengah().warna("abu-400"),
                spasi("24px"),
                baris(*[badge(s) for s in skills], gap="8px").tengah(),
            ),
            padding="96px 0",
            bg="gradient-ungu",
        )
    ]
    renderer = Renderer()
    return renderer.render(*components)


def toko(nama: str, produk: list = None) -> str:
    """Bikin halaman toko sederhana."""
    from pyvibe.components.basic import judul as j, paragraf as p, teks as t, spasi
    from pyvibe.components.input import tombol as tb
    from pyvibe.components.layout import bagian, kontainer, grid, kartu
    from pyvibe.core.renderer import Renderer

    items = produk or [
        {"nama": "Produk 1", "harga": "Rp 100.000"},
        {"nama": "Produk 2", "harga": "Rp 200.000"},
        {"nama": "Produk 3", "harga": "Rp 150.000"},
    ]

    produk_cards = []
    for item in items:
        produk_cards.append(kartu(
            j(item.get("nama", "")).tengah(),
            p(item.get("harga", "")).besar().tengah().warna("ungu"),
            tb("+ Keranjang", warna="biru"),
            padding="24px",
        ))

    components = [
        bagian(
            kontainer(
                j(f"🛍️ {nama}").besar().tengah(),
                spasi("48px"),
                grid(*produk_cards, kolom=min(len(items), 3), gap="24px"),
            ),
            padding="96px 0",
        )
    ]
    renderer = Renderer()
    return renderer.render(*components)


# ==================== Re-export Common Things ====================

def spasi(tinggi: str = "24px") -> Component:
    """Spasi."""
    from pyvibe.components.basic import spasi as s
    return s(tinggi)


def baris(*items, gap: str = "16px", justify: str = "flex-start") -> Component:
    """Baris flex."""
    from pyvibe.components.layout import baris as b
    return b(*items, gap=gap, justify=justify)


def kolom(lebar: int, *items) -> Component:
    """Kolom."""
    from pyvibe.components.layout import kolom as k
    return k(lebar, *items)


def grid(*items, kolom: int = 3, gap: str = "24px") -> Component:
    """Grid."""
    from pyvibe.components.layout import grid as g
    return g(*items, kolom=kolom, gap=gap)


def kartu(*items, **kwargs) -> Component:
    """Kartu."""
    from pyvibe.components.layout import kartu as k
    return k(*items, **kwargs)


def kontainer(*items, **kwargs) -> Component:
    """Kontainer."""
    from pyvibe.components.layout import kontainer as k
    return k(*items, **kwargs)


def bagian(*items, **kwargs) -> Component:
    """Bagian/section."""
    from pyvibe.components.layout import bagian as b
    return b(*items, **kwargs)


def judul(teks: str, level: int = 1) -> Component:
    """Judul."""
    from pyvibe.components.basic import judul as j
    return j(teks, level=level)


def paragraf(teks: str) -> Component:
    """Paragraf."""
    from pyvibe.components.basic import paragraf as p
    return p(teks)


def teks(teks: str) -> Component:
    """Teks inline."""
    from pyvibe.components.basic import teks as t
    return t(teks)


def tombol(teks: str = "Klik", warna: str = "ungu") -> Component:
    """Tombol."""
    from pyvibe.components.input import tombol as tb
    return tb(teks, warna=warna)


def gambar(src: str, alt: str = "") -> Component:
    """Gambar."""
    from pyvibe.components.basic import gambar as g
    return g(src, alt=alt)
