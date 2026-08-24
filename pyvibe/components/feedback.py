"""
Feedback Components — notifikasi, alert, loader v2.
"""

from __future__ import annotations
from typing import Optional
from pyvibe.core.component import Component


def notifikasi(teks: str, tipe: str = "info", icon: str = "", dismissible: bool = True, **kwargs) -> Component:
    """Toast notification component."""
    type_map = {
        "sukses": ("pv-alert-success", "✅"),
        "berhasil": ("pv-alert-success", "✅"),
        "error": ("pv-alert-danger", "❌"),
        "gagal": ("pv-alert-danger", "❌"),
        "peringatan": ("pv-alert-warning", "⚠️"),
        "warning": ("pv-alert-warning", "⚠️"),
        "info": ("pv-alert-info", "ℹ️"),
    }
    css_class, default_icon = type_map.get(tipe, type_map["info"])
    display_icon = icon or default_icon

    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-alert", css_class])

    icon_span = Component(tag="span", content=display_icon)
    text = Component(tag="span", content=teks)

    if dismissible:
        close = Component(tag="span", content="✕")
        close.class_names.extend(["pv-cursor-pointer", "pv-ml-auto"])
        close.style.color = "#9CA3AF"
        close.attrs["onclick"] = "this.parentElement.style.display='none'"
        comp.children = [icon_span, text, close]
    else:
        comp.children = [icon_span, text]

    return comp


def alert(teks: str, tipe: str = "info", judul: str = "", **kwargs) -> Component:
    """Alert banner component."""
    type_map = {
        "info": ("pv-alert-info", "ℹ️"),
        "sukses": ("pv-alert-success", "✅"),
        "success": ("pv-alert-success", "✅"),
        "peringatan": ("pv-alert-warning", "⚠️"),
        "warning": ("pv-alert-warning", "⚠️"),
        "danger": ("pv-alert-danger", "🚨"),
        "error": ("pv-alert-danger", "🚨"),
    }
    css_class, icon = type_map.get(tipe, type_map["info"])

    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-alert", css_class])

    header = Component(tag="div")
    header.class_names.extend(["pv-flex", "pv-items-center", "pv-gap-8"])

    icon_span = Component(tag="span", content=icon)

    if judul:
        title = Component(tag="strong", content=judul)
        header.children = [icon_span, title]
    else:
        header.children = [icon_span]

    text = Component(tag="p", content=teks)
    text.class_names.extend(["pv-mt-8", "pv-mb-0"])

    comp.children = [header, text]
    return comp


def loader(ukuran: str = "sedang", teks: str = "", **kwargs) -> Component:
    """Loading spinner component."""
    size_map = {"kecil": "pv-spinner-sm", "sedang": "", "besar": "pv-spinner-lg"}
    size_class = size_map.get(ukuran, "")

    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-flex", "pv-flex-col", "pv-items-center", "pv-gap-12", "pv-p-24"])

    spinner = Component(tag="div")
    spinner.class_names.append("pv-spinner")
    if size_class:
        spinner.class_names.append(size_class)

    comp.children.append(spinner)

    if teks:
        text = Component(tag="div", content=teks)
        text.class_names.append("pv-text-gray")
        comp.children.append(text)

    return comp


def badge_status(teks: str, status: str = "default", **kwargs) -> Component:
    """Status badge component."""
    status_map = {
        "sukses": "pv-badge-success", "success": "pv-badge-success",
        "active": "pv-badge-success", "peringatan": "pv-badge-warning",
        "warning": "pv-badge-warning", "pending": "pv-badge-warning",
        "error": "pv-badge-danger", "danger": "pv-badge-danger",
        "info": "pv-badge-info", "default": "pv-badge-gray",
    }
    comp = Component(tag="span", content=teks, **kwargs)
    comp.class_names.append(status_map.get(status, "pv-badge-gray"))
    return comp


def skeleton(lebar: str = "100%", tinggi: str = "20px", **kwargs) -> Component:
    """Skeleton loading component."""
    comp = Component(tag="div", **kwargs)
    comp.class_names.append("pv-skeleton")
    comp.style.width = lebar
    comp.style.height = tinggi
    return comp
