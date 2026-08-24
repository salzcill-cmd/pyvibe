"""
Basic Components — elemen UI dasar untuk PyVibe v2.

Semua components sekarang pakai CSS classes untuk performance lebih baik.
"""

from __future__ import annotations
from typing import Optional, Union
from pyvibe.core.component import Component


# ==================== Typography ====================

def judul(teks: str, level: int = 1, **kwargs) -> Component:
    """Heading component. Level 1-6."""
    tag = f"h{min(max(level, 1), 6)}"
    comp = Component(tag=tag, content=teks, **kwargs)
    comp.class_names.append(f"pv-heading-{level}")
    return comp


def subjudul(teks: str, **kwargs) -> Component:
    """Shorthand untuk judul level 2."""
    return judul(teks, level=2, **kwargs)


def paragraf(teks: str, **kwargs) -> Component:
    """Paragraph component."""
    comp = Component(tag="p", content=teks, **kwargs)
    comp.class_names.append("pv-text")
    return comp


def teks(teks: str, **kwargs) -> Component:
    """Inline text component (span)."""
    return Component(tag="span", content=teks, **kwargs)


def teks_teal(teks: str, **kwargs) -> Component:
    """Teks dengan warna teal/cyan."""
    comp = Component(tag="span", content=teks, **kwargs)
    comp.class_names.append("pv-text-primary")
    return comp


def teks_tipis(teks: str, **kwargs) -> Component:
    """Teks dengan weight tipis."""
    comp = Component(tag="span", content=teks, **kwargs)
    comp.class_names.append("pv-text-light")
    return comp


def teks_balik(teks: str, **kwargs) -> Component:
    """Teks yang di-highlight dengan background."""
    comp = Component(tag="span", content=teks, **kwargs)
    comp.class_names.extend(["pv-bg-primary", "pv-text-white", "pv-rounded", "pv-p-4", "pv-py-2"])
    return comp


# ==================== Media ====================

def gambar(src: str, alt: str = "", **kwargs) -> Component:
    """Image component."""
    return Component(tag="img", src=src, alt=alt, **kwargs)


def gambar_rounded(src: str, alt: str = "", ukuran: str = "48px", **kwargs) -> Component:
    """Circular image (avatar)."""
    comp = Component(tag="img", src=src, alt=alt, **kwargs)
    comp.class_names.append("pv-avatar")
    comp.style.width = ukuran
    comp.style.height = ukuran
    return comp


def video(src: str, **kwargs) -> Component:
    """Video component."""
    return Component(tag="video", src=src, controls=True, **kwargs)


def iframe(src: str, **kwargs) -> Component:
    """Iframe component."""
    return Component(tag="iframe", src=src, **kwargs)


# ==================== Links ====================

def tautan(teks: str, url: str = "#", **kwargs) -> Component:
    """Link component."""
    comp = Component(tag="a", content=teks, href=url, **kwargs)
    return comp


# ==================== Icons ====================

def ikon(nama: str, ukuran: str = "16px", **kwargs) -> Component:
    """Icon component (emoji atau Unicode)."""
    return Component(tag="span", content=nama, **kwargs)


# ==================== Spacing ====================

def spasi(tinggi: str = "24px") -> Component:
    """Spacing component."""
    comp = Component(tag="div", content="")
    comp.style.height = tinggi
    return comp


def pemisah(**kwargs) -> Component:
    """Divider / horizontal rule."""
    comp = Component(tag="hr", **kwargs)
    comp.class_names.append("pv-border-t")
    comp.style.border = "none"
    comp.style.margin = "24px 0"
    return comp


# ==================== Decorative ====================

def gradien_teks(teks: str, warna1: str = "#7C3AED", warna2: str = "#06B6D4", **kwargs) -> Component:
    """Teks dengan gradient color."""
    comp = Component(tag="span", content=teks, **kwargs)
    comp.attrs["style"] = f"background: linear-gradient(135deg, {warna1}, {warna2}); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: bold;"
    return comp


def badge(teks: str, warna: str = "ungu", **kwargs) -> Component:
    """Badge / label component."""
    color_map = {
        "ungu": "pv-badge-primary", "biru": "pv-badge-info",
        "hijau": "pv-badge-success", "merah": "pv-badge-danger",
        "kuning": "pv-badge-warning", "abu": "pv-badge-gray",
    }
    comp = Component(tag="span", content=teks, **kwargs)
    comp.class_names.append(color_map.get(warna, "pv-badge-primary"))
    return comp


def avatar(src: str, ukuran: str = "40px", **kwargs) -> Component:
    """Avatar component."""
    comp = Component(tag="img", src=src, **kwargs)
    comp.class_names.append("pv-avatar")
    comp.style.width = ukuran
    comp.style.height = ukuran
    return comp


def progress_bar(persen: int = 0, warna: str = "#7C3AED", **kwargs) -> Component:
    """Progress bar component."""
    outer = Component(tag="div", **kwargs)
    outer.class_names.append("pv-progress")

    inner = Component(tag="div", content="")
    inner.class_names.append("pv-progress-bar")
    inner.style.width = f"{min(max(persen, 0), 100)}%"
    inner.style.bg = warna

    outer.children = [inner]
    return outer


def chip(teks: str, warna: str = "#E5E7EB", **kwargs) -> Component:
    """Chip / tag component."""
    comp = Component(tag="span", content=teks, **kwargs)
    comp.class_names.extend(["pv-badge", "pv-badge-gray"])
    comp.style.bg = warna
    return comp


def count_down(angka: int, label: str = "", **kwargs) -> Component:
    """Counter / stat number component."""
    wrapper = Component(tag="div", **kwargs)
    wrapper.class_names.append("pv-text-center")

    num = Component(tag="div", content=str(angka))
    num.style.font_size = "2rem"
    num.style.font_weight = "700"
    num.style.color = "#7C3AED"

    if label:
        lbl = Component(tag="div", content=label)
        lbl.class_names.extend(["pv-text-sm", "pv-text-gray"])
        wrapper.children = [num, lbl]
    else:
        wrapper.children = [num]

    return wrapper
