"""
Navigation Components — navbar, sidebar, footer, tabs, breadcrumb v2.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from pyvibe.core.component import Component


def navbar(
    logo: str = "🐍 PyVibe",
    menu: Optional[List[str]] = None,
    tombol_daftar: str = "",
    tombol_login: str = "",
    **kwargs,
) -> Component:
    """Navbar component."""
    comp = Component(tag="nav", **kwargs)
    comp.class_names.extend(["pv-flex", "pv-items-center", "pv-justify-between", "pv-p-16", "pv-px-32", "pv-bg-white", "pv-border-b", "pv-sticky", "pv-z-100"])

    logo_el = Component(tag="a", content=logo)
    logo_el.style.font_size = "1.25rem"
    logo_el.style.font_weight = "700"
    logo_el.style.color = "#111827"
    logo_el.style.text_decoration = "none"
    logo_el.attrs["href"] = "/"

    menu_container = Component(tag="div")
    menu_container.class_names.extend(["pv-flex", "pv-gap-32", "pv-items-center"])

    if menu:
        for item in menu:
            link = Component(tag="a", content=item)
            link.class_names.extend(["pv-text-gray", "pv-text-sm", "pv-text-bold"])
            link.style.text_decoration = "none"
            link.attrs["href"] = f"/{item.lower().replace(' ', '-')}"
            menu_container.children.append(link)

    actions = Component(tag="div")
    actions.class_names.extend(["pv-flex", "pv-gap-12", "pv-items-center"])

    if tombol_login:
        login_btn = Component(tag="a", content=tombol_login)
        login_btn.class_names.extend(["pv-text-gray", "pv-text-sm", "pv-text-bold"])
        login_btn.style.text_decoration = "none"
        login_btn.attrs["href"] = "/login"
        actions.children.append(login_btn)

    if tombol_daftar:
        daftar_btn = Component(tag="a", content=tombol_daftar)
        daftar_btn.class_names.extend(["pv-btn", "pv-btn-primary"])
        daftar_btn.attrs["href"] = "/register"
        actions.children.append(daftar_btn)

    comp.children = [logo_el, menu_container, actions]
    return comp


def sidebar(
    *items: Union[str, Dict[str, str]],
    judul: str = "",
    aktif: str = "",
    **kwargs,
) -> Component:
    """Sidebar component."""
    comp = Component(tag="aside", **kwargs)
    comp.class_names.extend(["pv-fixed", "pv-left-0", "pv-top-0", "pv-bg-dark", "pv-text-white", "pv-p-24", "pv-py-32", "pv-overflow-auto"])
    comp.style.width = "260px"
    comp.style.height = "100vh"

    if judul:
        title = Component(tag="div", content=judul)
        title.class_names.extend(["pv-mb-24", "pv-text-2xl", "pv-text-bold"])
        comp.children.append(title)

    menu = Component(tag="ul")
    menu.style.list_style = "none"

    for item in items:
        li = Component(tag="li")
        text = item if isinstance(item, str) else item.get("text", "")

        link = Component(tag="a", content=text)
        is_aktif = text == aktif
        link.class_names.extend(["pv-block", "pv-p-12", "pv-px-24", "pv-rounded", "pv-text-sm", "pv-text-bold" if is_aktif else "pv-text-gray"])
        link.style.text_decoration = "none"
        link.style.transition = "all 0.2s"
        if is_aktif:
            link.style.bg = "rgba(124, 58, 237, 0.2)"

        li.children.append(link)
        menu.children.append(li)

    comp.children.append(menu)
    return comp


def footer(
    teks: str = "",
    links: Optional[List[str]] = None,
    copyright: str = "",
    **kwargs,
) -> Component:
    """Footer component."""
    comp = Component(tag="footer", **kwargs)
    comp.class_names.extend(["pv-p-48", "pv-bg-dark", "pv-text-gray", "pv-text-center"])

    if links:
        link_container = Component(tag="div")
        link_container.class_names.extend(["pv-flex", "pv-justify-center", "pv-gap-24", "pv-mb-16"])

        for link_text in links:
            link = Component(tag="a", content=link_text)
            link.class_names.extend(["pv-text-white", "pv-text-sm"])
            link.style.text_decoration = "none"
            link.attrs["href"] = f"/{link_text.lower()}"
            link_container.children.append(link)

        comp.children.append(link_container)

    if copyright:
        copy_text = Component(tag="div", content=copyright)
    elif teks:
        copy_text = Component(tag="div", content=teks)
    else:
        copy_text = Component(tag="div", content="Built with 🐍 PyVibe")

    copy_text.class_names.extend(["pv-text-sm", "pv-text-gray"])
    comp.children.append(copy_text)
    return comp


def tabs(
    *tab_items: tuple,
    aktif: str = "",
    **kwargs,
) -> Component:
    """Tabs component."""
    comp = Component(tag="div", **kwargs)
    comp.class_names.append("pv-tabs")

    headers = Component(tag="div")
    headers.class_names.append("pv-tabs-nav")

    content_container = Component(tag="div")

    for tab_name, tab_content in tab_items:
        is_active = tab_name == aktif
        header = Component(tag="div", content=tab_name)
        header.class_names.extend(["pv-tab"])
        if is_active:
            header.class_names.append("active")
        header.attrs["data-target"] = f"#tab-{tab_name.lower().replace(' ', '-')}"

        headers.children.append(header)

        content_div = Component(tag="div")
        content_div.id = f"tab-{tab_name.lower().replace(' ', '-')}"
        content_div.class_names.extend(["pv-tab-content"])
        if is_active:
            content_div.class_names.append("active")

        if isinstance(tab_content, Component):
            content_div.children.append(tab_content)
        else:
            content_div.children.append(Component(tag="div", content=str(tab_content)))

        content_container.children.append(content_div)

    comp.children = [headers, content_container]
    return comp


def breadcrumb(
    *items: str,
    **kwargs,
) -> Component:
    """Breadcrumb component."""
    comp = Component(tag="nav", **kwargs)
    comp.class_names.extend(["pv-flex", "pv-items-center", "pv-gap-8", "pv-py-12", "pv-text-sm"])

    for i, item in enumerate(items):
        if i > 0:
            separator = Component(tag="span", content=" / ")
            separator.class_names.append("pv-text-gray")
            comp.children.append(separator)

        if i < len(items) - 1:
            link = Component(tag="a", content=item)
            link.class_names.append("pv-text-primary")
            link.style.text_decoration = "none"
            comp.children.append(link)
        else:
            current = Component(tag="span", content=item)
            current.class_names.extend(["pv-text-gray", "pv-text-bold"])
            comp.children.append(current)

    return comp
