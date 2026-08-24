"""
Input Components — form elements untuk PyVibe v2.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from pyvibe.core.component import Component


# ==================== Text Inputs ====================

def input_teks(
    label: str = "",
    placeholder: str = "",
    name: str = "",
    value: str = "",
    required: bool = False,
    disabled: bool = False,
    **kwargs,
) -> Component:
    """Text input component."""
    wrapper = Component(tag="div", **kwargs)
    wrapper.class_names.append("pv-form-group")

    if label:
        lbl = Component(tag="label", content=label)
        lbl.class_names.append("pv-label")
        wrapper.children.append(lbl)

    inp = Component(tag="input", type="text", placeholder=placeholder)
    inp.class_names.append("pv-input")
    if name:
        inp.attrs["name"] = name
    if value:
        inp.attrs["value"] = value
    if required:
        inp.attrs["required"] = "required"
    if disabled:
        inp.attrs["disabled"] = "disabled"

    wrapper.children.append(inp)
    return wrapper


def input_angka(
    label: str = "",
    placeholder: str = "",
    name: str = "",
    value: str = "",
    min_val: Optional[int] = None,
    max_val: Optional[int] = None,
    required: bool = False,
    **kwargs,
) -> Component:
    """Number input component."""
    wrapper = Component(tag="div", **kwargs)
    wrapper.class_names.append("pv-form-group")

    if label:
        lbl = Component(tag="label", content=label)
        lbl.class_names.append("pv-label")
        wrapper.children.append(lbl)

    inp = Component(tag="input", type="number", placeholder=placeholder)
    inp.class_names.append("pv-input")
    if name:
        inp.attrs["name"] = name
    if value:
        inp.attrs["value"] = value
    if min_val is not None:
        inp.attrs["min"] = str(min_val)
    if max_val is not None:
        inp.attrs["max"] = str(max_val)
    if required:
        inp.attrs["required"] = "required"

    wrapper.children.append(inp)
    return wrapper


def input_email(
    label: str = "",
    placeholder: str = "email@domain.com",
    name: str = "",
    required: bool = False,
    **kwargs,
) -> Component:
    """Email input component."""
    wrapper = Component(tag="div", **kwargs)
    wrapper.class_names.append("pv-form-group")

    if label:
        lbl = Component(tag="label", content=label)
        lbl.class_names.append("pv-label")
        wrapper.children.append(lbl)

    inp = Component(tag="input", type="email", placeholder=placeholder)
    inp.class_names.append("pv-input")
    if name:
        inp.attrs["name"] = name
    if required:
        inp.attrs["required"] = "required"

    wrapper.children.append(inp)
    return wrapper


def input_sandi(
    label: str = "",
    placeholder: str = "••••••••",
    name: str = "",
    required: bool = False,
    **kwargs,
) -> Component:
    """Password input component."""
    wrapper = Component(tag="div", **kwargs)
    wrapper.class_names.append("pv-form-group")

    if label:
        lbl = Component(tag="label", content=label)
        lbl.class_names.append("pv-label")
        wrapper.children.append(lbl)

    inp = Component(tag="input", type="password", placeholder=placeholder)
    inp.class_names.append("pv-input")
    if name:
        inp.attrs["name"] = name
    if required:
        inp.attrs["required"] = "required"

    wrapper.children.append(inp)
    return wrapper


def textarea(
    label: str = "",
    placeholder: str = "",
    name: str = "",
    rows: int = 4,
    required: bool = False,
    **kwargs,
) -> Component:
    """Textarea component."""
    wrapper = Component(tag="div", **kwargs)
    wrapper.class_names.append("pv-form-group")

    if label:
        lbl = Component(tag="label", content=label)
        lbl.class_names.append("pv-label")
        wrapper.children.append(lbl)

    ta = Component(tag="textarea", placeholder=placeholder)
    ta.class_names.append("pv-textarea")
    if name:
        ta.attrs["name"] = name
    ta.attrs["rows"] = str(rows)
    if required:
        ta.attrs["required"] = "required"

    wrapper.children.append(ta)
    return wrapper


# ==================== Selection Inputs ====================

def centang(
    label: str = "",
    name: str = "",
    checked: bool = False,
    **kwargs,
) -> Component:
    """Checkbox component."""
    wrapper = Component(tag="label", **kwargs)
    wrapper.class_names.extend(["pv-flex", "pv-items-center", "pv-gap-8", "pv-cursor-pointer"])

    cb = Component(tag="input", type="checkbox")
    cb.class_names.append("pv-checkbox")
    if name:
        cb.attrs["name"] = name
    if checked:
        cb.attrs["checked"] = "checked"

    text = Component(tag="span", content=label)

    wrapper.children = [cb, text]
    return wrapper


def pilihan(
    label: str = "",
    options: Optional[List[str]] = None,
    name: str = "",
    placeholder: str = "Pilih salah satu...",
    **kwargs,
) -> Component:
    """Select dropdown component."""
    wrapper = Component(tag="div", **kwargs)
    wrapper.class_names.append("pv-form-group")

    if label:
        lbl = Component(tag="label", content=label)
        lbl.class_names.append("pv-label")
        wrapper.children.append(lbl)

    select = Component(tag="select")
    select.class_names.append("pv-select")
    if name:
        select.attrs["name"] = name

    placeholder_opt = Component(tag="option", content=placeholder)
    placeholder_opt.attrs["value"] = ""
    select.children.append(placeholder_opt)

    for opt in (options or []):
        option = Component(tag="option", content=opt)
        option.attrs["value"] = opt.lower().replace(" ", "_")
        select.children.append(option)

    wrapper.children.append(select)
    return wrapper


def unggah_file(
    label: str = "",
    name: str = "",
    accept: str = "*",
    multiple: bool = False,
    **kwargs,
) -> Component:
    """File upload component."""
    wrapper = Component(tag="div", **kwargs)
    wrapper.class_names.append("pv-form-group")

    if label:
        lbl = Component(tag="label", content=label)
        lbl.class_names.append("pv-label")
        wrapper.children.append(lbl)

    drop_zone = Component(tag="div")
    drop_zone.class_names.extend(["pv-border", "pv-rounded-lg", "pv-p-32", "pv-text-center", "pv-cursor-pointer"])

    icon = Component(tag="div", content="📁")
    icon.style.font_size = "2rem"
    icon.style.margin_bottom = "8px"

    text = Component(tag="div", content="Klik atau seret file ke sini")
    text.class_names.append("pv-text-gray")

    inp = Component(tag="input", type="file")
    inp.class_names.append("pv-hidden")
    if name:
        inp.attrs["name"] = name
    inp.attrs["accept"] = accept
    if multiple:
        inp.attrs["multiple"] = "multiple"

    drop_zone.children = [icon, text, inp]
    wrapper.children.append(drop_zone)
    return wrapper


# ==================== Buttons ====================

def tombol(
    teks: str = "",
    warna: str = "ungu",
    ukuran: str = "sedang",
    icon: str = "",
    disabled: bool = False,
    onclick: str = "",
    **kwargs,
) -> Component:
    """Button component."""
    color_map = {
        "ungu": "pv-btn-primary", "biru": "pv-btn-primary",
        "hijau": "pv-btn-success", "merah": "pv-btn-danger",
        "kuning": "pv-btn-warning", "orange": "pv-btn-warning",
        "cyan": "pv-btn-primary", "abu": "pv-btn-secondary",
        "pink": "pv-btn-primary", "outline": "pv-btn-outline",
    }
    size_map = {
        "kecil": "pv-btn-sm", "sedang": "", "besar": "pv-btn-lg",
    }

    comp = Component(tag="button", content=teks, **kwargs)
    comp.class_names.append("pv-btn")
    comp.class_names.append(color_map.get(warna, "pv-btn-primary"))
    if ukuran in size_map and size_map[ukuran]:
        comp.class_names.append(size_map[ukuran])

    if disabled:
        comp.attrs["disabled"] = "disabled"
    if onclick:
        comp.attrs["onclick"] = onclick
    if icon:
        icon_span = Component(tag="span", content=icon)
        comp.children.insert(0, icon_span)

    return comp


def tombol_icon(icon: str, tooltip: str = "", **kwargs) -> Component:
    """Icon button."""
    comp = Component(tag="button", **kwargs)
    comp.class_names.extend(["pv-btn", "pv-btn-ghost", "pv-btn-sm"])

    if tooltip:
        comp.attrs["title"] = tooltip

    icon_span = Component(tag="span", content=icon)
    comp.children = [icon_span]
    return comp


def tombol_kirim(teks: str = "Kirim", **kwargs) -> Component:
    """Submit button for forms."""
    return tombol(teks, warna="ungu", **kwargs)
