"""
Extra Components — stepper, timeline, rating, countdown, typing effect, dll.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from pyvibe.core.component import Component


# ==================== Stepper / Wizard ====================

def stepper(
    steps: List[str],
    aktif: int = 0,
    **kwargs,
) -> Component:
    """
    Stepper / wizard component.

    Usage:
        stepper(["Info Dasar", "Upload Foto", "Konfirmasi"], aktif=1)
    """
    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-flex", "pv-items-center", "pv-justify-between", "pv-mb-32"])

    for i, step in enumerate(steps):
        # Step circle
        circle = Component(tag="div")
        is_done = i < aktif
        is_current = i == aktif

        if is_done:
            circle.class_names.extend(["pv-rounded-full", "pv-bg-success", "pv-text-white", "pv-flex", "pv-items-center", "pv-justify-center"])
            circle.style.width = "32px"
            circle.style.height = "32px"
            circle.content = "✓"
        elif is_current:
            circle.class_names.extend(["pv-rounded-full", "pv-bg-primary", "pv-text-white", "pv-flex", "pv-items-center", "pv-justify-center"])
            circle.style.width = "32px"
            circle.style.height = "32px"
            circle.content = str(i + 1)
        else:
            circle.class_names.extend(["pv-rounded-full", "pv-bg-gray", "pv-text-gray", "pv-flex", "pv-items-center", "pv-justify-center"])
            circle.style.width = "32px"
            circle.style.height = "32px"
            circle.content = str(i + 1)

        # Step label
        label = Component(tag="div", content=step)
        label.class_names.extend(["pv-text-sm", "pv-text-center"])
        if is_current:
            label.class_names.append("pv-text-bold")
            label.style.color = "#7C3AED"
        elif is_done:
            label.class_names.append("pv-text-success")
        else:
            label.class_names.append("pv-text-gray")

        step_container = Component(tag="div")
        step_container.class_names.extend(["pv-flex", "pv-flex-col", "pv-items-center", "pv-gap-8"])
        step_container.children = [circle, label]

        comp.children.append(step_container)

        # Connector line (except last)
        if i < len(steps) - 1:
            connector = Component(tag="div")
            connector.style.flex = "1"
            connector.style.height = "2px"
            connector.style.background = "#E5E7EB" if i < aktif else "#D1D5DB"
            connector.style.margin = "0 8px"
            connector.style.margin_bottom = "24px"
            comp.children.append(connector)

    return comp


# ==================== Timeline ====================

def timeline(
    *items: Dict[str, str],
    **kwargs,
) -> Component:
    """
    Timeline component.

    Usage:
        timeline(
            {"tanggal": "24 Agustus", "judul": "Project Started", "isi": "Memulai development."},
            {"tanggal": "25 Agustus", "judul": "Alpha Release", "isi": "Release versi alpha."},
        )
    """
    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-relative", "pv-pl-32"])

    for i, item in enumerate(items):
        entry = Component(tag="div")
        entry.class_names.extend(["pv-relative", "pv-mb-24"])

        # Dot
        dot = Component(tag="div")
        dot.class_names.extend(["pv-absolute", "pv-rounded-full", "pv-bg-primary"])
        dot.style.width = "12px"
        dot.style.height = "12px"
        dot.style.left = "-26px"
        dot.style.top = "4px"

        # Line
        if i < len(items) - 1:
            line = Component(tag="div")
            line.class_names.extend(["pv-absolute", "pv-bg-gray"])
            line.style.width = "2px"
            line.style.height = "100%"
            line.style.left = "-21px"
            line.style.top = "16px"
            entry.children.append(line)

        # Date
        if "tanggal" in item:
            date = Component(tag="div", content=item["tanggal"])
            date.class_names.extend(["pv-text-sm", "pv-text-gray", "pv-mb-4"])
            entry.children.append(date)

        # Title
        if "judul" in item:
            title = Component(tag="h4", content=item["judul"])
            title.class_names.extend(["pv-mb-4", "pv-text-bold"])
            entry.children.append(title)

        # Content
        if "isi" in item:
            content = Component(tag="p", content=item["isi"])
            content.class_names.append("pv-text-gray")
            entry.children.append(content)

        entry.children.insert(0, dot)
        comp.children.append(entry)

    return comp


# ==================== Rating ====================

def rating(
    bintang: int = 5,
    max_bintang: int = 5,
    ukuran: str = "24px",
    warna: str = "#EAB308",
    readonly: bool = True,
    **kwargs,
) -> Component:
    """
    Star rating component.

    Usage:
        rating(bintang=4, max_bintang=5)
        rating(bintang=5, warna="#F97316")
    """
    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-flex", "pv-items-center", "pv-gap-4"])

    for i in range(max_bintang):
        star = Component(tag="span")
        if i < bintang:
            star.content = "★"
            star.style.color = warna
        else:
            star.content = "☆"
            star.style.color = "#D1D5DB"
        star.style.font_size = ukuran
        if not readonly:
            star.class_names.append("pv-cursor-pointer")
        comp.children.append(star)

    return comp


# ==================== Countdown ====================

def countdown(
    detik: int = 60,
    label: str = "Tersisa",
    id: str = "countdown",
    **kwargs,
) -> Component:
    """
    Countdown timer component.

    Usage:
        countdown(detik=300, label="Waktu habis dalam")
    """
    menit = detik // 60
    sisa_detik = detik % 60

    comp = Component(tag="div", id=id, **kwargs)
    comp.class_names.extend(["pv-flex", "pv-items-center", "pv-gap-8", "pv-text-center"])

    label_el = Component(tag="span", content=label)
    label_el.class_names.extend(["pv-text-sm", "pv-text-gray"])

    timer = Component(tag="span")
    timer.class_names.extend(["pv-text-2xl", "pv-text-bold", "pv-text-primary"])
    timer.attrs["data-countdown"] = str(detik)
    timer.content = f"{menit:02d}:{sisa_detik:02d}"

    comp.children = [label_el, timer]
    return comp


# ==================== Typing Effect ====================

def typing_effect(
    texts: List[str],
    speed: int = 100,
    delete_speed: int = 50,
    pause: int = 2000,
    id: str = "typing",
    **kwargs,
) -> Component:
    """
    Typing effect component.

    Usage:
        typing_effect(["Halo!", "Selamat Datang", "di PyVibe"])
    """
    comp = Component(tag="span", id=id, **kwargs)
    comp.class_names.append("pv-text-primary")
    comp.style.border_right = "2px solid #7C3AED"
    comp.style.animation = "pvPulse 1s infinite"
    comp.attrs["data-typing"] = ",".join(texts)
    comp.attrs["data-speed"] = str(speed)
    comp.attrs["data-delete-speed"] = str(delete_speed)
    comp.attrs["data-pause"] = str(pause)
    comp.content = texts[0] if texts else ""
    return comp


# ==================== Scroll to Top ====================

def scroll_to_top(
    warna: str = "#7C3AED",
    **kwargs,
) -> Component:
    """
    Scroll to top button.

    Usage:
        scroll_to_top()
    """
    comp = Component(tag="button", content="↑", **kwargs)
    comp.class_names.extend(["pv-btn", "pv-btn-primary", "pv-rounded-full", "pv-fixed"])
    comp.style.bottom = "24px"
    comp.style.right = "24px"
    comp.style.width = "48px"
    comp.style.height = "48px"
    comp.style.display = "flex"
    comp.style.align_items = "center"
    comp.style.justify_content = "center"
    comp.style.z_index = "50"
    comp.style.box_shadow = "var(--pv-shadow-lg)"
    comp.attrs["onclick"] = "window.scrollTo({top: 0, behavior: 'smooth'})"
    return comp


# ==================== Image Gallery ====================

def galeri(
    gambar: List[str],
    kolom: int = 3,
    gap: str = "16px",
    **kwargs,
) -> Component:
    """
    Image gallery component.

    Usage:
        galeri(["img1.jpg", "img2.jpg", "img3.jpg"], kolom=3)
    """
    comp = Component(tag="div", **kwargs)
    comp.class_names.append("pv-grid")

    grid_map = {2: "pv-grid-2", 3: "pv-grid-3", 4: "pv-grid-4"}
    comp.class_names.append(grid_map.get(kolom, "pv-grid-3"))
    comp.style.gap = gap

    for img_src in gambar:
        img_container = Component(tag="div")
        img_container.class_names.extend(["pv-overflow-hidden", "pv-rounded-lg", "pv-cursor-pointer"])

        img = Component(tag="img", src=img_src)
        img.class_names.extend(["pv-w-full", "pv-animate-scale"])
        img.style.height = "200px"
        img.style.object_fit = "cover"
        img.style.transition = "transform 0.3s"
        img.attrs["onmouseenter"] = "this.style.transform='scale(1.05)'"
        img.attrs["onmouseleave"] = "this.style.transform='scale(1)'"

        img_container.children.append(img)
        comp.children.append(img_container)

    return comp


# ==================== Code Block ====================

def code_block(
    kode: str,
    bahasa: str = "python",
    show_line_numbers: bool = True,
    **kwargs,
) -> Component:
    """
    Code block with syntax highlighting.

    Usage:
        code_block('print("Hello World")', bahasa="python")
    """
    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-rounded-lg", "pv-overflow-hidden", "pv-shadow-sm"])

    # Header
    header = Component(tag="div")
    header.class_names.extend(["pv-flex", "pv-items-center", "pv-justify-between", "pv-p-12", "pv-px-16"])
    header.style.background = "#1E293B"

    lang_badge = Component(tag="span", content=bahasa.upper())
    lang_badge.class_names.extend(["pv-badge", "pv-badge-primary"])

    copy_btn = Component(tag="button", content="📋 Copy")
    copy_btn.class_names.extend(["pv-btn", "pv-btn-ghost", "pv-btn-sm"])
    copy_btn.style.color = "#94A3B8"
    copy_btn.attrs["onclick"] = f"navigator.clipboard.writeText(this.closest('.pv-code-block').querySelector('code').textContent)"

    header.children = [lang_badge, copy_btn]

    # Code
    pre = Component(tag="pre")
    pre.style.background = "#0F172A"
    pre.style.padding = "16px"
    pre.style.overflow = "auto"
    pre.style.margin = "0"

    code = Component(tag="code", content=kode)
    code.style.font_family = "'JetBrains Mono', monospace"
    code.style.font_size = "14px"
    code.style.line_height = "1.6"
    code.style.color = "#E2E8F0"

    pre.children.append(code)
    comp.children = [header, pre]

    return comp


# ==================== Markdown Renderer ====================

def markdown(content: str, **kwargs) -> Component:
    """
    Simple markdown renderer.

    Usage:
        markdown("# Hello\\n\\nThis is **bold** and *italic*.")
    """
    import re

    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-prose", "pv-max-w-2xl"])

    lines = content.split("\n")
    elements = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Headers
        if line.startswith("### "):
            h = Component(tag="h3", content=line[4:])
            h.class_names.extend(["pv-mt-24", "pv-mb-12"])
            elements.append(h)
        elif line.startswith("## "):
            h = Component(tag="h2", content=line[3:])
            h.class_names.extend(["pv-mt-32", "pv-mb-16"])
            elements.append(h)
        elif line.startswith("# "):
            h = Component(tag="h1", content=line[2:])
            h.class_names.extend(["pv-mt-32", "pv-mb-16"])
            elements.append(h)
        # Lists
        elif line.startswith("- "):
            li = Component(tag="li", content=line[2:])
            li.class_names.extend(["pv-py-4", "pv-ml-16"])
            elements.append(li)
        # Bold
        elif line.startswith("**") and line.endswith("**"):
            p = Component(tag="p", content=line[2:-2])
            p.class_names.append("pv-text-bold")
            elements.append(p)
        # Regular paragraph
        else:
            p = Component(tag="p", content=line)
            p.class_names.append("pv-text-gray")
            elements.append(p)

    comp.children = elements
    return comp


# ==================== Empty State ====================

def empty_state(
    judul: str = "Tidak ada data",
    deskripsi: str = "",
    icon: str = "📭",
    tombol_text: str = "",
    tombol_url: str = "#",
    **kwargs,
) -> Component:
    """
    Empty state component.

    Usage:
        empty_state("Belum ada pesanan", "Buat pesanan pertama kamu!")
    """
    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-text-center", "pv-p-48", "pv-py-64"])

    icon_el = Component(tag="div", content=icon)
    icon_el.style.font_size = "4rem"
    icon_el.style.margin_bottom = "16px"

    title = Component(tag="h3", content=judul)
    title.class_names.extend(["pv-mb-8", "pv-text-gray"])

    comp.children.extend([icon_el, title])

    if deskripsi:
        desc = Component(tag="p", content=deskripsi)
        desc.class_names.extend(["pv-text-gray", "pv-mb-24"])
        comp.children.append(desc)

    if tombol_text:
        btn = tombol(tombol_text, warna="ungu")
        btn.attrs["href"] = tombol_url
        comp.children.append(btn)

    return comp


# ==================== Stat Card Alternative ====================

def stat_card(
    icon: str = "📊",
    nilai: str = "0",
    label: str = "",
    perubahan: str = "",
    arah: str = "up",
    warna: str = "ungu",
    **kwargs,
) -> Component:
    """
    Stat card with icon.

    Usage:
        stat_card(icon="👥", nilai="1,234", label="Users", perubahan="+12%", arah="up")
    """
    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-card", "pv-card-hover"])

    # Icon
    icon_el = Component(tag="div", content=icon)
    icon_el.style.font_size = "2rem"
    icon_el.style.margin_bottom = "12px"

    # Value
    value = Component(tag="div", content=nilai)
    value.class_names.extend(["pv-text-2xl", "pv-text-bold", "pv-mb-4"])

    # Label
    label_el = Component(tag="div", content=label)
    label_el.class_names.extend(["pv-text-sm", "pv-text-gray", "pv-mb-8"])

    comp.children.extend([icon_el, value, label_el])

    # Change indicator
    if perubahan:
        change_color = "pv-text-success" if arah == "up" else "pv-text-danger"
        change_icon = "↑" if arah == "up" else "↓"
        change = Component(tag="div", content=f"{change_icon} {perubahan}")
        change.class_names.extend([change_color, "pv-text-sm", "pv-text-bold"])
        comp.children.append(change)

    return comp
