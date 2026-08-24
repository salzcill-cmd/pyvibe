"""
Layout Components — struktur layout untuk PyVibe v2.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from pyvibe.core.component import Component


def kartu(
    *children: Union[Component, str],
    judul: str = "",
    padding: str = "24px",
    shadow: str = "md",
    border: bool = True,
    hover: bool = True,
    **kwargs,
) -> Component:
    """Card component."""
    comp = Component(tag="div", **kwargs)
    comp.class_names.append("pv-card")
    if hover:
        comp.class_names.append("pv-card-hover")

    if judul:
        title = Component(tag="h3", content=judul)
        title.class_names.append("pv-card-title")
        comp.children.append(title)

    for child in children:
        if isinstance(child, str):
            comp.children.append(Component(tag="p", content=child))
        else:
            comp.children.append(child)

    return comp


def kartu_stat(
    judul: str = "",
    nilai: str = "0",
    perubahan: str = "",
    arah: str = "up",
    icon: str = "📊",
    **kwargs,
) -> Component:
    """Stat card component."""
    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-card", "pv-card-hover"])

    header = Component(tag="div")
    header.class_names.extend(["pv-flex", "pv-items-center", "pv-justify-between", "pv-mb-8"])

    icon_span = Component(tag="span", content=icon)
    icon_span.style.font_size = "1.5rem"

    title = Component(tag="div", content=judul)
    title.class_names.extend(["pv-text-sm", "pv-text-gray"])

    header.children = [icon_span, title]

    value = Component(tag="div", content=nilai)
    value.style.font_size = "1.75rem"
    value.style.font_weight = "700"
    value.style.color = "#111827"
    value.style.margin_bottom = "4px"

    change_color = "pv-text-success" if arah == "up" else "pv-text-danger"
    change_icon = "↑" if arah == "up" else "↓"
    change = Component(tag="div", content=f"{change_icon} {perubahan}")
    change.class_names.append(change_color)
    change.style.font_size = "0.8125rem"
    change.style.font_weight = "500"

    comp.children = [header, value, change]
    return comp


def judul_kartu(teks: str = "", **kwargs) -> Component:
    """Card title."""
    comp = Component(tag="h3", content=teks, **kwargs)
    comp.class_names.append("pv-card-title")
    return comp


def kolom(
    width: Union[int, str] = 12,
    *children: Union[Component, str],
    **kwargs,
) -> Component:
    """Column component."""
    comp = Component(tag="div", **kwargs)

    if isinstance(width, int):
        comp.style.width = f"{(width / 12) * 100}%"
    else:
        comp.style.width = width

    comp.style.display = "inline-block"
    comp.style.vertical_align = "top"
    comp.style.padding = "0 12px"
    comp.style.box_sizing = "border-box"

    for child in children:
        if isinstance(child, str):
            comp.children.append(Component(tag="div", content=child))
        else:
            comp.children.append(child)

    return comp


def baris(
    *children: Union[Component, str],
    gap: str = "16px",
    justify: str = "flex-start",
    align: str = "stretch",
    wrap: bool = True,
    **kwargs,
) -> Component:
    """Row / Flexbox component."""
    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-flex", "pv-flex-wrap"])

    justify_map = {
        "center": "pv-justify-center",
        "between": "pv-justify-between",
        "end": "pv-justify-end",
        "start": "",
    }
    align_map = {
        "center": "pv-items-center",
        "start": "pv-items-start",
        "end": "pv-items-end",
        "stretch": "",
    }

    if justify in justify_map and justify_map[justify]:
        comp.class_names.append(justify_map[justify])
    if align in align_map and align_map[align]:
        comp.class_names.append(align_map[align])

    if gap != "0":
        gap_map = {"4px": "pv-gap-4", "8px": "pv-gap-8", "12px": "pv-gap-12",
                    "16px": "pv-gap-16", "24px": "pv-gap-24", "32px": "pv-gap-32"}
        if gap in gap_map:
            comp.class_names.append(gap_map[gap])
        else:
            comp.style.gap = gap

    for child in children:
        if isinstance(child, str):
            comp.children.append(Component(tag="div", content=child))
        else:
            comp.children.append(child)

    return comp


def bagian(
    *children: Union[Component, str],
    judul: str = "",
    subjudul: str = "",
    padding: str = "64px 32px",
    bg: str = "",
    text_align: str = "",
    **kwargs,
) -> Component:
    """Section component."""
    comp = Component(tag="section", **kwargs)
    comp.style.padding = padding

    if bg:
        bg_map = {
            "gelap": "pv-bg-dark", "terang": "pv-bg-gray", "white": "pv-bg-white",
            "ungu": "pv-gradient-purple", "biru": "pv-gradient-blue",
            "cyan": "pv-gradient-blue", "pink": "pv-gradient-pink",
            "gradient-ungu": "pv-gradient-purple", "gradient-biru": "pv-gradient-blue",
            "gradient-pink": "pv-gradient-pink",
        }
        if bg in bg_map:
            comp.class_names.append(bg_map[bg])
        else:
            comp.style.bg = bg

    if text_align:
        text_map = {"center": "pv-text-center", "left": "pv-text-left", "right": "pv-text-right"}
        comp.class_names.append(text_map.get(text_align, "pv-text-center"))

    if judul:
        title = Component(tag="h2", content=judul)
        title.class_names.extend(["pv-text-center", "pv-mb-16"])
        title.style.font_size = "2rem"
        title.style.font_weight = "700"
        comp.children.append(title)

    if subjudul:
        subtitle = Component(tag="p", content=subjudul)
        subtitle.class_names.extend(["pv-text-center", "pv-mb-32", "pv-mx-auto"])
        subtitle.style.font_size = "1.125rem"
        subtitle.style.max_width = "600px"
        comp.children.append(subtitle)

    for child in children:
        if isinstance(child, str):
            comp.children.append(Component(tag="div", content=child))
        else:
            comp.children.append(child)

    return comp


def spacer(tinggi: str = "24px") -> Component:
    """Spacer component."""
    comp = Component(tag="div", content="")
    comp.style.height = tinggi
    return comp


def kontainer(
    *children: Union[Component, str],
    max_lebar: str = "1200px",
    padding: str = "0 32px",
    **kwargs,
) -> Component:
    """Container component."""
    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-mx-auto", "pv-w-full"])
    comp.style.max_width = max_lebar
    comp.style.padding = padding

    for child in children:
        if isinstance(child, str):
            comp.children.append(Component(tag="div", content=child))
        else:
            comp.children.append(child)

    return comp


def grid(
    *children: Union[Component, str],
    kolom: int = 3,
    gap: str = "24px",
    min_lebar_item: str = "280px",
    **kwargs,
) -> Component:
    """CSS Grid component."""
    comp = Component(tag="div", **kwargs)
    comp.class_names.append("pv-grid")

    grid_map = {2: "pv-grid-2", 3: "pv-grid-3", 4: "pv-grid-4"}
    if kolom in grid_map:
        comp.class_names.append(grid_map[kolom])
    else:
        comp.style.grid_template_columns = f"repeat(auto-fill, minmax({min_lebar_item}, 1fr))"

    if gap:
        gap_map = {"16px": "pv-gap-16", "24px": "pv-gap-24", "32px": "pv-gap-32"}
        if gap in gap_map:
            comp.class_names.append(gap_map[gap])
        else:
            comp.style.gap = gap

    for child in children:
        if isinstance(child, str):
            comp.children.append(Component(tag="div", content=child))
        else:
            comp.children.append(child)

    return comp


def overlay(
    *children: Union[Component, str],
    id: str = "",
    visible: bool = False,
    **kwargs,
) -> Component:
    """Overlay / modal backdrop."""
    comp = Component(tag="div", id=id, **kwargs)
    comp.class_names.extend(["pv-modal", "pv-fixed", "pv-inset-0", "pv-z-1000"])
    if visible:
        comp.class_names.append("active")

    for child in children:
        if isinstance(child, str):
            comp.children.append(Component(tag="div", content=child))
        else:
            comp.children.append(child)

    return comp
