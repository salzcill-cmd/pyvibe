"""
Modern Components — pagination, toast, date picker, color picker, switch, avatar group, etc.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from pyvibe.core.component import Component


# ==================== Pagination ====================

def pagination(
    total_pages: int,
    current_page: int = 1,
    max_visible: int = 5,
    **kwargs,
) -> Component:
    """
    Pagination component.

    Usage:
        pagination(total_pages=10, current_page=3)
    """
    comp = Component(tag="nav", **kwargs)
    comp.class_names.extend(["pv-flex", "pv-items-center", "pv-gap-4"])

    # Previous button
    prev = Component(tag="button", content="‹")
    prev.class_names.extend(["pv-btn", "pv-btn-secondary", "pv-btn-sm"])
    if current_page <= 1:
        prev.attrs["disabled"] = "disabled"
    prev.attrs["onclick"] = f"goToPage({current_page - 1})"
    comp.children.append(prev)

    # Calculate visible pages
    start = max(1, current_page - max_visible // 2)
    end = min(total_pages, start + max_visible - 1)
    if end - start < max_visible - 1:
        start = max(1, end - max_visible + 1)

    # First page + ellipsis
    if start > 1:
        btn = Component(tag="button", content="1")
        btn.class_names.extend(["pv-btn", "pv-btn-secondary", "pv-btn-sm"])
        btn.attrs["onclick"] = "goToPage(1)"
        comp.children.append(btn)
        if start > 2:
            ellipsis = Component(tag="span", content="...")
            ellipsis.class_names.extend(["pv-text-gray", "pv-px-8"])
            comp.children.append(ellipsis)

    # Page numbers
    for i in range(start, end + 1):
        btn = Component(tag="button", content=str(i))
        btn.class_names.extend(["pv-btn", "pv-btn-sm"])
        if i == current_page:
            btn.class_names.append("pv-btn-primary")
        else:
            btn.class_names.append("pv-btn-secondary")
        btn.attrs["onclick"] = f"goToPage({i})"
        comp.children.append(btn)

    # Last page + ellipsis
    if end < total_pages:
        if end < total_pages - 1:
            ellipsis = Component(tag="span", content="...")
            ellipsis.class_names.extend(["pv-text-gray", "pv-px-8"])
            comp.children.append(ellipsis)
        btn = Component(tag="button", content=str(total_pages))
        btn.class_names.extend(["pv-btn", "pv-btn-secondary", "pv-btn-sm"])
        btn.attrs["onclick"] = f"goToPage({total_pages})"
        comp.children.append(btn)

    # Next button
    next_btn = Component(tag="button", content="›")
    next_btn.class_names.extend(["pv-btn", "pv-btn-secondary", "pv-btn-sm"])
    if current_page >= total_pages:
        next_btn.attrs["disabled"] = "disabled"
    next_btn.attrs["onclick"] = f"goToPage({current_page + 1})"
    comp.children.append(next_btn)

    return comp


# ==================== Toast ====================

def toast(
    message: str,
    tipe: str = "info",
    position: str = "top-right",
    duration: int = 3000,
    dismissible: bool = True,
    **kwargs,
) -> Component:
    """
    Toast notification component.

    Usage:
        toast("Berhasil disimpan!", tipe="sukses")
        toast("Error!", tipe="error", position="bottom-center")
    """
    type_map = {
        "sukses": ("pv-bg-success", "✅"),
        "berhasil": ("pv-bg-success", "✅"),
        "success": ("pv-bg-success", "✅"),
        "error": ("pv-bg-danger", "❌"),
        "gagal": ("pv-bg-danger", "❌"),
        "peringatan": ("pv-bg-warning", "⚠️"),
        "warning": ("pv-bg-warning", "⚠️"),
        "info": ("pv-bg-info", "ℹ️"),
    }

    bg_class, icon = type_map.get(tipe, type_map["info"])

    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-toast", bg_class])

    # Position
    pos_map = {
        "top-right": "top: 20px; right: 20px;",
        "top-left": "top: 20px; left: 20px;",
        "bottom-right": "bottom: 20px; right: 20px;",
        "bottom-left": "bottom: 20px; left: 20px;",
        "top-center": "top: 20px; left: 50%; transform: translateX(-50%);",
        "bottom-center": "bottom: 20px; left: 50%; transform: translateX(-50%);",
    }
    comp.attrs["style"] = pos_map.get(position, pos_map["top-right"])

    icon_span = Component(tag="span", content=icon)
    text = Component(tag="span", content=message)

    if dismissible:
        close = Component(tag="span", content="✕")
        close.class_names.extend(["pv-cursor-pointer", "pv-ml-auto"])
        close.attrs["onclick"] = "this.parentElement.style.display='none'"
        comp.children = [icon_span, text, close]
    else:
        comp.children = [icon_span, text]

    return comp


# ==================== Switch / Toggle ====================

def switch(
    label: str = "",
    name: str = "",
    checked: bool = False,
    disabled: bool = False,
    **kwargs,
) -> Component:
    """
    Switch / toggle component.

    Usage:
        switch("Dark Mode", name="dark_mode")
        switch("Notifications", checked=True)
    """
    wrapper = Component(tag="label", **kwargs)
    wrapper.class_names.extend(["pv-flex", "pv-items-center", "pv-gap-8", "pv-cursor-pointer"])

    # Hidden checkbox
    checkbox = Component(tag="input", type="checkbox")
    checkbox.attrs["name"] = name
    if checked:
        checkbox.attrs["checked"] = "checked"
    if disabled:
        checkbox.attrs["disabled"] = "disabled"
    checkbox.class_names.append("pv-hidden")

    # Toggle track
    track = Component(tag="div")
    track.class_names.extend(["pv-relative", "pv-rounded-full"])
    track.style.width = "44px"
    track.style.height = "24px"
    track.style.background = "#D1D5DB" if not checked else "#7C3AED"
    track.style.transition = "background 0.2s"

    # Toggle thumb
    thumb = Component(tag="div")
    thumb.class_names.extend(["pv-absolute", "pv-rounded-full", "pv-bg-white", "pv-shadow-sm"])
    thumb.style.width = "20px"
    thumb.style.height = "20px"
    thumb.style.top = "2px"
    thumb.style.left = "2px" if not checked else "22px"
    thumb.style.transition = "left 0.2s"

    track.children.append(thumb)

    # Label text
    if label:
        label_el = Component(tag="span", content=label)
        label_el.class_names.append("pv-text-sm")

    wrapper.children = [checkbox, track]
    if label:
        wrapper.children.append(label_el)

    return wrapper


# ==================== Avatar Group ====================

def avatar_group(
    avatars: List[str],
    max_visible: int = 4,
    ukuran: str = "40px",
    **kwargs,
) -> Component:
    """
    Avatar group component.

    Usage:
        avatar_group(["img1.jpg", "img2.jpg", "img3.jpg", "img4.jpg", "img5.jpg"], max_visible=3)
    """
    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-flex", "pv-items-center"])

    visible = avatars[:max_visible]
    remaining = len(avatars) - max_visible

    for i, src in enumerate(visible):
        img = Component(tag="img", src=src)
        img.class_names.extend(["pv-avatar", "pv-rounded-full", "pv-object-cover"])
        img.style.width = ukuran
        img.style.height = ukuran
        img.style.border = "3px solid white"
        img.style.margin_left = "-12px" if i > 0 else "0"
        img.style.z_index = str(max_visible - i)
        comp.children.append(img)

    if remaining > 0:
        badge = Component(tag="div", content=f"+{remaining}")
        badge.class_names.extend(["pv-rounded-full", "pv-bg-gray", "pv-text-gray", "pv-flex", "pv-items-center", "pv-justify-center", "pv-text-sm", "pv-text-bold"])
        badge.style.width = ukuran
        badge.style.height = ukuran
        badge.style.margin_left = "-12px"
        badge.style.border = "3px solid white"
        badge.style.z_index = "0"
        comp.children.append(badge)

    return comp


# ==================== Date Picker ====================

def date_picker(
    label: str = "",
    name: str = "",
    placeholder: str = "Pilih tanggal",
    value: str = "",
    min_date: str = "",
    max_date: str = "",
    **kwargs,
) -> Component:
    """
    Date picker component.

    Usage:
        date_picker("Tanggal Lahir", name="birth_date")
        date_picker("Mulai", name="start_date", min_date="2026-01-01")
    """
    wrapper = Component(tag="div", **kwargs)
    wrapper.class_names.append("pv-form-group")

    if label:
        lbl = Component(tag="label", content=label)
        lbl.class_names.append("pv-label")
        wrapper.children.append(lbl)

    inp = Component(tag="input", type="date")
    inp.class_names.append("pv-input")
    if name:
        inp.attrs["name"] = name
    if value:
        inp.attrs["value"] = value
    if min_date:
        inp.attrs["min"] = min_date
    if max_date:
        inp.attrs["max"] = max_date
    if placeholder:
        inp.attrs["placeholder"] = placeholder

    wrapper.children.append(inp)
    return wrapper


# ==================== Color Picker ====================

def color_picker(
    label: str = "",
    name: str = "",
    value: str = "#7C3AED",
    **kwargs,
) -> Component:
    """
    Color picker component.

    Usage:
        color_picker("Warna Tema", name="theme_color")
    """
    wrapper = Component(tag="div", **kwargs)
    wrapper.class_names.append("pv-form-group")

    if label:
        lbl = Component(tag="label", content=label)
        lbl.class_names.append("pv-label")
        wrapper.children.append(lbl)

    inp = Component(tag="input", type="color")
    inp.class_names.append("pv-input")
    inp.style.padding = "4px"
    inp.style.height = "44px"
    inp.style.width = "80px"
    if name:
        inp.attrs["name"] = name
    if value:
        inp.attrs["value"] = value

    wrapper.children.append(inp)
    return wrapper


# ==================== Range Slider ====================

def range_slider(
    label: str = "",
    name: str = "",
    min_val: int = 0,
    max_val: int = 100,
    value: int = 50,
    step: int = 1,
    show_value: bool = True,
    **kwargs,
) -> Component:
    """
    Range slider component.

    Usage:
        range_slider("Volume", name="volume", min_val=0, max_val=100, value=75)
    """
    wrapper = Component(tag="div", **kwargs)
    wrapper.class_names.append("pv-form-group")

    if label:
        lbl = Component(tag="label", content=label)
        lbl.class_names.append("pv-label")
        wrapper.children.append(lbl)

    slider_container = Component(tag="div")
    slider_container.class_names.extend(["pv-flex", "pv-items-center", "pv-gap-12"])

    inp = Component(tag="input", type="range")
    inp.class_names.append("pv-range")
    inp.style.flex = "1"
    inp.style.accent_color = "#7C3AED"
    if name:
        inp.attrs["name"] = name
    inp.attrs["min"] = str(min_val)
    inp.attrs["max"] = str(max_val)
    inp.attrs["value"] = str(value)
    inp.attrs["step"] = str(step)

    slider_container.children.append(inp)

    if show_value:
        value_display = Component(tag="span", content=str(value))
        value_display.class_names.extend(["pv-text-sm", "pv-text-bold", "pv-text-primary"])
        value_display.style.min_width = "40px"
        slider_container.children.append(value_display)

    wrapper.children.append(slider_container)
    return wrapper


# ==================== Empty State Enhanced ====================

def empty_state_modern(
    judul: str = "Tidak ada data",
    deskripsi: str = "",
    icon: str = "📭",
    tombol_text: str = "",
    tombol_url: str = "#",
    tombol_warna: str = "ungu",
    **kwargs,
) -> Component:
    """
    Modern empty state with action.

    Usage:
        empty_state_modern(
            judul="Belum ada pesanan",
            deskripsi="Mulai belanja sekarang!",
            icon="🛒",
            tombol_text="Mulai Belanja",
        )
    """
    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-text-center", "pv-p-48", "pv-py-64"])

    # Icon with background
    icon_container = Component(tag="div")
    icon_container.style.width = "80px"
    icon_container.style.height = "80px"
    icon_container.style.border_radius = "50%"
    icon_container.style.background = "#F3F4F6"
    icon_container.style.display = "flex"
    icon_container.style.align_items = "center"
    icon_container.style.justify_content = "center"
    icon_container.style.margin = "0 auto 24px"

    icon_el = Component(tag="span", content=icon)
    icon_el.style.font_size = "2.5rem"
    icon_container.children.append(icon_el)

    title = Component(tag="h3", content=judul)
    title.class_names.extend(["pv-mb-8", "pv-text-gray-700"])

    comp.children.extend([icon_container, title])

    if deskripsi:
        desc = Component(tag="p", content=deskripsi)
        desc.class_names.extend(["pv-text-gray", "pv-mb-24", "pv-mx-auto"])
        desc.style.max_width = "400px"
        comp.children.append(desc)

    if tombol_text:
        from pyvibe.components.input import tombol
        btn = tombol(tombol_text, warna=tombol_warna)
        btn.attrs["href"] = tombol_url
        comp.children.append(btn)

    return comp


# ==================== Command Palette ====================

def command_palette(
    placeholder: str = "Ketik command...",
    commands: Optional[List[Dict[str, str]]] = None,
    **kwargs,
) -> Component:
    """
    Command palette / search component.

    Usage:
        command_palette(
            placeholder="Cari command...",
            commands=[
                {"label": "Copy", "shortcut": "⌘C"},
                {"label": "Paste", "shortcut": "⌘V"},
            ]
        )
    """
    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-modal", "pv-fixed", "pv-inset-0", "pv-z-100"])

    # Backdrop
    backdrop = Component(tag="div")
    backdrop.class_names.extend(["pv-absolute", "pv-inset-0", "pv-bg-black", "pv-opacity-50"])

    # Content
    content = Component(tag="div")
    content.class_names.extend(["pv-relative", "pv-bg-white", "pv-rounded-xl", "pv-shadow-xl", "pv-mx-auto", "pv-mt-24"])
    content.style.max_width = "600px"
    content.style.max_height = "400px"
    content.style.overflow = "auto"

    # Search input
    search = Component(tag="div")
    search.class_names.extend(["pv-flex", "pv-items-center", "pv-gap-12", "pv-p-16", "pv-border-b"])

    search_icon = Component(tag="span", content="🔍")
    search_icon.style.font_size = "1.25rem"

    search_input = Component(tag="input", type="text", placeholder=placeholder)
    search_input.class_names.extend(["pv-input", "pv-border-0"])
    search_input.style.box_shadow = "none"

    search.children = [search_icon, search_input]
    content.children.append(search)

    # Commands list
    if commands:
        cmd_list = Component(tag="div")
        cmd_list.class_names.extend(["pv-p-8"])

        for cmd in commands:
            item = Component(tag="div")
            item.class_names.extend(["pv-flex", "pv-items-center", "pv-justify-between", "pv-p-12", "pv-rounded", "pv-cursor-pointer"])
            item.attrs["onmouseenter"] = "this.style.background='#F3F4F6'"
            item.attrs["onmouseleave"] = "this.style.background='transparent'"

            label = Component(tag="span", content=cmd.get("label", ""))
            label.class_names.extend(["pv-text-sm"])

            item.children.append(label)

            if "shortcut" in cmd:
                shortcut = Component(tag="kbd", content=cmd["shortcut"])
                shortcut.class_names.extend(["pv-text-xs", "pv-text-gray", "pv-bg-gray", "pv-rounded", "pv-px-8", "pv-py-4"])
                item.children.append(shortcut)

            cmd_list.children.append(item)

        content.children.append(cmd_list)

    comp.children = [backdrop, content]
    return comp


# ==================== Stat Grid ====================

def stat_grid(
    stats: List[Dict[str, Any]],
    columns: int = 4,
    **kwargs,
) -> Component:
    """
    Statistics grid with icons and trends.

    Usage:
        stat_grid([
            {"label": "Users", "value": "1,234", "icon": "👥", "trend": "+12%", "up": True},
            {"label": "Revenue", "value": "Rp 45M", "icon": "💰", "trend": "+8%", "up": True},
            {"label": "Orders", "value": "567", "icon": "📦", "trend": "-3%", "up": False},
        ], columns=3)
    """
    from pyvibe.components.layout import grid, kartu

    cards = []
    for stat in stats:
        card = Component(tag="div")
        card.class_names.extend(["pv-card", "pv-card-hover"])

        # Header with icon
        header = Component(tag="div")
        header.class_names.extend(["pv-flex", "pv-items-center", "pv-justify-between", "pv-mb-8"])

        icon = Component(tag="span", content=stat.get("icon", "📊"))
        icon.style.font_size = "1.5rem"
        header.children.append(icon)

        if stat.get("badge"):
            from pyvibe.components.basic import badge
            b = badge(stat["badge"], warna=stat.get("badge_warna", "ungu"))
            header.children.append(b)

        card.children.append(header)

        # Value
        value = Component(tag="div", content=stat.get("value", "0"))
        value.class_names.extend(["pv-text-2xl", "pv-text-bold", "pv-mb-4"])

        card.children.append(value)

        # Label
        label = Component(tag="div", content=stat.get("label", ""))
        label.class_names.extend(["pv-text-sm", "pv-text-gray", "pv-mb-8"])
        card.children.append(label)

        # Trend
        if stat.get("trend"):
            trend_color = "pv-text-success" if stat.get("up", True) else "pv-text-danger"
            trend_icon = "↑" if stat.get("up", True) else "↓"
            trend = Component(tag="div", content=f"{trend_icon} {stat['trend']}")
            trend.class_names.extend([trend_color, "pv-text-sm", "pv-text-bold"])
            card.children.append(trend)

        cards.append(card)

    return grid(*cards, kolom=columns, gap="24px", **kwargs)
