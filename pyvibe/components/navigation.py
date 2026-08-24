"""
Navigation Components — navbar, sidebar, footer, tabs, breadcrumb.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from pyvibe.core.component import Component


def navbar(*children, **kwargs) -> Component:
    """Navbar component with flexible children."""
    comp = Component(tag="nav", **kwargs)
    comp.class_names.extend([
        "pv-flex", "pv-items-center", "pv-justify-between",
        "pv-p-16", "pv-px-32", "pv-bg-white",
        "pv-border-b", "pv-sticky", "pv-z-100",
    ])

    for child in children:
        if isinstance(child, Component):
            comp.children.append(child)
        elif isinstance(child, str):
            comp.children.append(Component(tag="span", content=child))

    return comp


def sidebar(*items, judul: str = "", **kwargs) -> Component:
    """Sidebar navigation."""
    comp = Component(tag="aside", **kwargs)
    comp.class_names.extend([
        "pv-fixed", "pv-left-0", "pv-top-0",
        "pv-bg-dark", "pv-text-white",
        "pv-p-24", "pv-py-32", "pv-overflow-auto",
    ])
    comp.style.width = "260px"
    comp.style.height = "100vh"

    if judul:
        title = Component(tag="div", content=judul)
        title.class_names.extend(["pv-mb-24", "pv-text-2xl", "pv-text-bold"])
        comp.children.append(title)

    for item in items:
        if isinstance(item, str):
            link = Component(tag="a", content=item)
            link.class_names.extend([
                "pv-block", "pv-py-8", "pv-text-gray",
                "pv-text-sm", "pv-text-decoration-none",
            ])
            link.attrs["href"] = f"#{item.lower().replace(' ', '-')}"
            comp.children.append(link)

    return comp


def footer(*children, **kwargs) -> Component:
    """Page footer."""
    comp = Component(tag="footer", **kwargs)
    comp.class_names.extend([
        "pv-bg-dark", "pv-text-white", "pv-p-24",
    ])

    for child in children:
        if isinstance(child, Component):
            comp.children.append(child)

    return comp


def tabs(items: List[str], **kwargs) -> Component:
    """Tab navigation."""
    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-flex", "pv-gap-4", "pv-border-b"])

    for item in items:
        tab = Component(tag="div", content=item)
        tab.class_names.extend([
            "pv-p-12", "pv-px-24", "pv-text-sm", "pv-text-bold",
            "pv-text-gray", "pv-cursor-pointer",
        ])
        tab.style.border_bottom = "2px solid transparent"
        comp.children.append(tab)

    return comp


def breadcrumb(items: List[str], **kwargs) -> Component:
    """Breadcrumb navigation."""
    comp = Component(tag="nav", **kwargs)
    comp.class_names.extend(["pv-flex", "pv-items-center", "pv-gap-8", "pv-text-sm"])

    for i, item in enumerate(items):
        if i > 0:
            sep = Component(tag="span", content="›")
            sep.class_names.append("pv-text-gray")
            comp.children.append(sep)

        link = Component(tag="a", content=item)
        if i < len(items) - 1:
            link.class_names.append("pv-text-primary")
            link.attrs["href"] = f"#{item.lower().replace(' ', '-')}"
        else:
            link.class_names.append("pv-text-gray")
        comp.children.append(link)

    return comp
