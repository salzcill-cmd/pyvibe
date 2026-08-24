"""
Advanced Components — carousel, accordion, modal v2.
"""

from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, Union
from pyvibe.core.component import Component


def carousel(
    *items: Union[str, Component],
    auto_play: bool = False,
    interval: int = 3000,
    show_dots: bool = True,
    show_arrows: bool = True,
    tinggi: str = "400px",
    **kwargs,
) -> Component:
    """Image/content carousel."""
    comp = Component(tag="div", id=f"carousel-{id(items) % 10000}", **kwargs)
    comp.class_names.extend(["pv-relative", "pv-overflow-hidden", "pv-rounded-lg"])
    comp.style.height = tinggi

    slides = Component(tag="div")
    slides.class_names.extend(["pv-flex", "pv-transition"])
    slides.style.height = "100%"

    for i, item in enumerate(items):
        slide = Component(tag="div")
        slide.style.min_width = "100%"
        slide.style.height = "100%"
        if isinstance(item, str):
            img = Component(tag="img", src=item)
            img.class_names.append("pv-w-full")
            img.style.height = "100%"
            img.style.object_fit = "cover"
            slide.children.append(img)
        else:
            slide.children.append(item)
        slides.children.append(slide)

    comp.children.append(slides)

    if show_dots:
        dots = Component(tag="div")
        dots.class_names.extend(["pv-absolute", "pv-bottom-16", "pv-flex", "pv-gap-8", "pv-z-10"])
        dots.style.left = "50%"
        dots.style.transform = "translateX(-50%)"

        for i in range(len(items)):
            dot = Component(tag="span")
            dot.class_names.append("pv-rounded-full")
            dot.style.width = "8px"
            dot.style.height = "8px"
            dot.style.bg = "#FFFFFF" if i == 0 else "rgba(255,255,255,0.5)"
            dot.style.cursor = "pointer"
            dots.children.append(dot)

        comp.children.append(dots)

    if show_arrows:
        prev = Component(tag="button", content="‹")
        prev.class_names.extend(["pv-btn", "pv-btn-ghost", "pv-absolute", "pv-z-10"])
        prev.style.left = "12px"
        prev.style.top = "50%"
        prev.style.transform = "translateY(-50%)"
        prev.style.bg = "rgba(255,255,255,0.8)"
        prev.style.border_radius = "50%"
        prev.style.width = "40px"
        prev.style.height = "40px"
        prev.style.font_size = "1.5rem"

        next_arrow = Component(tag="button", content="›")
        next_arrow.class_names.extend(["pv-btn", "pv-btn-ghost", "pv-absolute", "pv-z-10"])
        next_arrow.style.right = "12px"
        next_arrow.style.top = "50%"
        next_arrow.style.transform = "translateY(-50%)"
        next_arrow.style.bg = "rgba(255,255,255,0.8)"
        next_arrow.style.border_radius = "50%"
        next_arrow.style.width = "40px"
        next_arrow.style.height = "40px"
        next_arrow.style.font_size = "1.5rem"

        comp.children.extend([prev, next_arrow])

    return comp


def accordion(
    *items: tuple,
    **kwargs,
) -> Component:
    """Accordion / collapsible component."""
    comp = Component(tag="div", **kwargs)
    comp.class_names.append("pv-accordion")

    for i, (title, content) in enumerate(items):
        item = Component(tag="div")
        item.class_names.append("pv-accordion-item")

        header = Component(tag="div")
        header.class_names.append("pv-accordion-header")
        header.attrs["onclick"] = "this.parentElement.classList.toggle('active')"

        title_el = Component(tag="div", content=title)
        title_el.style.font_weight = "500"

        arrow = Component(tag="span", content="▼")
        arrow.class_names.append("pv-accordion-arrow")

        header.children = [title_el, arrow]

        content_div = Component(tag="div")
        content_div.class_names.append("pv-accordion-content")
        if isinstance(content, Component):
            content_div.children.append(content)
        else:
            content_div.children.append(Component(tag="p", content=str(content)))

        item.children = [header, content_div]
        comp.children.append(item)

    return comp


def modal(
    judul: str = "",
    *children: Union[Component, str],
    id: str = "modal",
    lebar: str = "500px",
    **kwargs,
) -> Component:
    """Modal dialog component."""
    comp = Component(tag="div", id=id, **kwargs)
    comp.class_names.extend(["pv-modal", "pv-fixed", "pv-inset-0", "pv-z-100"])

    modal_content = Component(tag="div")
    modal_content.class_names.extend(["pv-modal-content", "pv-mx-auto"])
    modal_content.style.width = lebar
    modal_content.style.max_width = "90vw"

    if judul:
        header = Component(tag="div")
        header.class_names.append("pv-modal-header")

        title = Component(tag="h3", content=judul)
        title.style.margin = "0"

        close_btn = Component(tag="span", content="✕")
        close_btn.class_names.extend(["pv-cursor-pointer", "pv-text-gray"])
        close_btn.style.font_size = "1.25rem"
        close_btn.attrs["onclick"] = f"pv.closeModal('{id}')"

        header.children = [title, close_btn]
        modal_content.children.append(header)

    body = Component(tag="div")
    body.class_names.append("pv-modal-body")
    for child in children:
        if isinstance(child, str):
            body.children.append(Component(tag="p", content=child))
        else:
            body.children.append(child)
    modal_content.children.append(body)

    comp.children.append(modal_content)
    return comp


def tooltip(
    content: Component,
    teks: str,
    posisi: str = "atas",
    **kwargs,
) -> Component:
    """Tooltip wrapper component."""
    wrapper = Component(tag="div", **kwargs)
    wrapper.class_names.extend(["pv-relative", "pv-inline-block"])

    tip = Component(tag="div", content=teks)
    tip.class_names.extend(["pv-absolute", "pv-bg-dark", "pv-text-white", "pv-rounded", "pv-text-sm"])
    tip.style.padding = "6px 12px"
    tip.style.white_space = "nowrap"
    tip.style.opacity = "0"
    tip.style.pointer_events = "none"
    tip.style.transition = "opacity 0.2s"
    tip.style.z_index = "1000"

    pos_map = {
        "atas": "bottom: 100%; left: 50%; transform: translateX(-50%); margin-bottom: 8px;",
        "bawah": "top: 100%; left: 50%; transform: translateX(-50%); margin-top: 8px;",
        "kiri": "right: 100%; top: 50%; transform: translateY(-50%); margin-right: 8px;",
        "kanan": "left: 100%; top: 50%; transform: translateY(-50%); margin-left: 8px;",
    }
    tip.attrs["style"] = f"{tip.style.to_css()} {pos_map.get(posisi, pos_map['atas'])}"

    wrapper.attrs["onmouseenter"] = "this.querySelector('[class*=pv-absolute]').style.opacity='1'"
    wrapper.attrs["onmouseleave"] = "this.querySelector('[class*=pv-absolute]').style.opacity='0'"

    wrapper.children = [content, tip]
    return wrapper


def dropdown(
    trigger: Union[str, Component],
    *items: Union[str, Dict[str, str]],
    **kwargs,
) -> Component:
    """Dropdown menu component."""
    comp = Component(tag="div", **kwargs)
    comp.class_names.append("pv-dropdown")

    if isinstance(trigger, str):
        trigger_el = Component(tag="button", content=trigger)
        trigger_el.class_names.extend(["pv-btn", "pv-btn-secondary"])
    else:
        trigger_el = trigger

    trigger_el.attrs["onclick"] = "this.nextElementSibling.classList.toggle('active')"
    comp.children.append(trigger_el)

    menu = Component(tag="div")
    menu.class_names.append("pv-dropdown-menu")

    for item in items:
        if isinstance(item, str):
            item_el = Component(tag="a", content=item)
            item_el.class_names.append("pv-dropdown-item")
            item_el.style.text_decoration = "none"
            item_el.attrs["onclick"] = "this.parentElement.classList.remove('active')"
            menu.children.append(item_el)
        elif isinstance(item, dict):
            item_el = Component(tag="a", content=item.get("text", ""))
            item_el.class_names.append("pv-dropdown-item")
            if item.get("danger"):
                item_el.class_names.append("pv-text-danger")
            menu.children.append(item_el)

    comp.children.append(menu)
    return comp
