"""
Data Components — tabel, grafik, daftar v2.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from pyvibe.core.component import Component


def tabel(
    data: List[Dict[str, Any]],
    kolom: Optional[List[str]] = None,
    header: Optional[Dict[str, str]] = None,
    striped: bool = True,
    hover: bool = True,
    compact: bool = False,
    **kwargs,
) -> Component:
    """Data table component."""
    if not data:
        empty = Component(tag="div", content="Tidak ada data")
        empty.class_names.extend(["pv-text-center", "pv-p-32", "pv-text-gray"])
        return empty

    if not kolom:
        kolom = list(data[0].keys())
    if not header:
        header = {k: k.replace("_", " ").title() for k in kolom}

    comp = Component(tag="div", **kwargs)
    comp.class_names.append("pv-overflow-auto")

    table = Component(tag="table")
    table.class_names.append("pv-table")
    if striped:
        table.class_names.append("pv-table-striped")

    thead = Component(tag="thead")
    header_row = Component(tag="tr")
    for col in kolom:
        th = Component(tag="th", content=header.get(col, col))
        header_row.children.append(th)
    thead.children.append(header_row)

    tbody = Component(tag="tbody")
    for row in data:
        tr = Component(tag="tr")
        for col in kolom:
            td = Component(tag="td", content=str(row.get(col, "")))
            tr.children.append(td)
        tbody.children.append(tr)

    table.children = [thead, tbody]
    comp.children.append(table)
    return comp


def grafik_sederhana(
    data: List[Dict[str, Any]],
    tipe: str = "bar",
    label_key: str = "label",
    value_key: str = "value",
    warna: str = "#7C3AED",
    **kwargs,
) -> Component:
    """Simple bar chart component."""
    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-flex", "pv-flex-col", "pv-gap-12"])

    max_val = max((item.get(value_key, 1) for item in data), default=1)

    for item in data:
        label = item.get(label_key, "")
        value = item.get(value_key, 0)
        percentage = (value / max_val * 100) if max_val > 0 else 0

        row = Component(tag="div")
        row.class_names.extend(["pv-flex", "pv-items-center", "pv-gap-12"])

        lbl = Component(tag="div", content=label)
        lbl.class_names.extend(["pv-text-sm", "pv-text-gray", "pv-text-right"])
        lbl.style.width = "120px"
        lbl.style.flex_shrink = "0"

        bar_container = Component(tag="div")
        bar_container.class_names.append("pv-progress")
        bar_container.style.flex = "1"

        bar_fill = Component(tag="div")
        bar_fill.class_names.append("pv-progress-bar")
        bar_fill.style.width = f"{percentage}%"
        bar_fill.style.bg = warna

        bar_container.children.append(bar_fill)

        val = Component(tag="div", content=str(value))
        val.class_names.extend(["pv-text-sm", "pv-text-bold"])
        val.style.width = "50px"

        row.children = [lbl, bar_container, val]
        comp.children.append(row)

    return comp


def daftar(
    *items: Union[str, Dict[str, str]],
    tipe: str = "bullet",
    **kwargs,
) -> Component:
    """List component."""
    tag = "ul" if tipe != "numbered" else "ol"
    comp = Component(tag=tag, **kwargs)
    comp.style.padding_left = "20px"

    for item in items:
        li = Component(tag="li")
        if isinstance(item, str):
            li.content = item
        elif isinstance(item, dict):
            li.content = item.get("text", "")
        li.class_names.extend(["pv-py-6", "pv-text-sm"])
        comp.children.append(li)

    return comp


def statistik(
    items: List[Dict[str, Any]],
    **kwargs,
) -> Component:
    """Statistics grid component."""
    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-grid", "pv-gap-24"])

    grid_cols = len(items)
    if grid_cols == 2:
        comp.class_names.append("pv-grid-2")
    elif grid_cols == 3:
        comp.class_names.append("pv-grid-3")
    elif grid_cols >= 4:
        comp.class_names.append("pv-grid-4")

    for item in items:
        stat = Component(tag="div")
        stat.class_names.extend(["pv-text-center", "pv-p-24", "pv-bg-gray", "pv-rounded-lg"])

        if "icon" in item:
            icon = Component(tag="div", content=item["icon"])
            icon.style.font_size = "2rem"
            icon.style.margin_bottom = "8px"
            stat.children.append(icon)

        nilai = Component(tag="div", content=item.get("nilai", "0"))
        nilai.class_names.extend(["pv-text-2xl", "pv-text-bold"])
        nilai.style.color = "#111827"
        stat.children.append(nilai)

        label = Component(tag="div", content=item.get("label", ""))
        label.class_names.extend(["pv-text-sm", "pv-text-gray", "pv-mt-4"])
        stat.children.append(label)

        comp.children.append(stat)

    return comp
