"""
Base Component class — fondasi semua elemen UI di PyVibe.

Setiap komponen PyVibe extends class ini dan bisa di-chain
dengan method builder pattern.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Callable, Union
from dataclasses import dataclass, field
import html
import json


@dataclass
class EventBinding:
    """Event binding untuk komponen."""
    event: str
    handler: str  # JavaScript handler name atau inline code
    debounce: int = 0


@dataclass
class StyleProps:
    """Style properties yang di-serialize ke CSS."""
    width: Optional[str] = None
    height: Optional[str] = None
    min_height: Optional[str] = None
    max_width: Optional[str] = None
    padding: Optional[str] = None
    margin: Optional[str] = None
    bg: Optional[str] = None
    color: Optional[str] = None
    font_size: Optional[str] = None
    font_weight: Optional[str] = None
    text_align: Optional[str] = None
    border: Optional[str] = None
    border_radius: Optional[str] = None
    box_shadow: Optional[str] = None
    display: Optional[str] = None
    flex_direction: Optional[str] = None
    align_items: Optional[str] = None
    justify_content: Optional[str] = None
    gap: Optional[str] = None
    grid_columns: Optional[int] = None
    position: Optional[str] = None
    top: Optional[str] = None
    right: Optional[str] = None
    bottom: Optional[str] = None
    left: Optional[str] = None
    z_index: Optional[int] = None
    opacity: Optional[float] = None
    transition: Optional[str] = None
    cursor: Optional[str] = None
    overflow: Optional[str] = None
    overflow_x: Optional[str] = None
    overflow_y: Optional[str] = None

    # Responsive
    responsive: Optional[Dict[str, str]] = None

    def to_css(self) -> str:
        """Convert ke CSS string."""
        css_parts = []
        mapping = {
            "width": "width", "height": "height", "min_height": "min-height",
            "max_width": "max-width", "padding": "padding", "margin": "margin",
            "bg": "background", "color": "color", "font_size": "font-size",
            "font_weight": "font-weight", "text_align": "text-align",
            "border": "border", "border_radius": "border-radius",
            "box_shadow": "box-shadow", "display": "display",
            "flex_direction": "flex-direction", "align_items": "align-items",
            "justify_content": "justify-content", "gap": "gap",
            "grid_columns": "grid-template-columns",
            "position": "position", "top": "top", "right": "right",
            "bottom": "bottom", "left": "left", "z_index": "z-index",
            "opacity": "opacity", "transition": "transition",
            "cursor": "cursor", "overflow": "overflow",
            "overflow_x": "overflow-x", "overflow_y": "overflow-y",
        }
        for py_name, css_name in mapping.items():
            val = getattr(self, py_name)
            if val is not None:
                if py_name == "grid_columns":
                    val = f"repeat({val}, 1fr)"
                css_parts.append(f"{css_name}: {val};")
        return " ".join(css_parts)

    def to_responsive_css(self, class_name: str) -> str:
        """Generate responsive CSS media queries."""
        if not self.responsive:
            return ""
        css = ""
        for breakpoint, styles in self.responsive.items():
            css += f"@media (max-width: {breakpoint}px) {{ {class_name} {{ {styles} }} }} "
        return css


class Component:
    """
    Base class untuk semua komponen PyVibe.

    Semua komponen bisa di-chain dengan method builder pattern:
        judul("Halo").tengah().besar().warna("biru")
    """

    def __init__(self, tag: str = "div", content: str = "", **kwargs):
        self.tag = tag
        self.content = content
        self.children: List[Component] = []
        self.attrs: Dict[str, Any] = {}
        self.events: List[EventBinding] = []
        self.style = StyleProps()
        self.class_names: List[str] = []
        self.id: Optional[str] = None
        self._data_attrs: Dict[str, str] = {}

        # Apply kwargs
        for key, value in kwargs.items():
            if key == "id":
                self.id = value
                self.attrs["id"] = value
            elif key == "class_name":
                self.class_names.append(value)
            elif key.startswith("data_"):
                self._data_attrs[key[5:]] = str(value)
            else:
                self.attrs[key] = value

    # ==================== Builder Pattern ====================

    def warna(self, warna: str) -> Component:
        """Set text color. Contoh: .warna("biru")"""
        color_map = {
            "biru": "#3B82F6", "merah": "#EF4444", "hijau": "#22C55E",
            "kuning": "#EAB308", "ungu": "#7C3AED", "pink": "#EC4899",
            "cyan": "#06B6D4", "orange": "#F97316", "abu": "#6B7280",
            "putih": "#FFFFFF", "hitam": "#000000",
        }
        self.style.color = color_map.get(warna, warna)
        return self

    def bg(self, warna: str) -> Component:
        """Set background color. Contoh: .bg("biru")"""
        color_map = {
            "biru": "#3B82F6", "merah": "#EF4444", "hijau": "#22C55E",
            "kuning": "#EAB308", "ungu": "#7C3AED", "pink": "#EC4899",
            "cyan": "#06B6D4", "orange": "#F97316", "abu": "#6B7280",
            "putih": "#FFFFFF", "hitam": "#111827", "gelap": "#1F2937",
        }
        self.style.bg = color_map.get(warna, warna)
        return self

    def ukuran(self, ukuran: str) -> Component:
        """Set size. Contoh: .ukuran("besar")"""
        sizes = {
            "kecil": "0.875rem", "sedang": "1rem",
            "besar": "1.25rem", "sangat_besar": "1.5rem", "raksasa": "2rem",
        }
        self.style.font_size = sizes.get(ukuran, ukuran)
        return self

    def besar(self) -> Component:
        """Set font size to large (shorthand)."""
        self.style.font_size = "1.5rem"
        return self

    def kecil(self) -> Component:
        """Set font size to small (shorthand)."""
        self.style.font_size = "0.875rem"
        return self

    def tebal(self, tebal: bool = True) -> Component:
        """Set font weight bold. Contoh: .tebal()"""
        self.style.font_weight = "bold" if tebal else "normal"
        return self

    def tipis(self, tipis: bool = True) -> Component:
        """Set font weight light."""
        self.style.font_weight = "300" if tipis else "normal"
        return self

    def tengah(self) -> Component:
        """Center align text. Contoh: .tengah()"""
        self.style.text_align = "center"
        return self

    def kiri(self) -> Component:
        """Left align text."""
        self.style.text_align = "left"
        return self

    def kanan(self) -> Component:
        """Right align text."""
        self.style.text_align = "right"
        return self

    def rata_kiri(self) -> Component:
        """Left align text."""
        return self.kiri()

    def rata_kanan(self) -> Component:
        """Right align text."""
        return self.kanan()

    def rata_tengah(self) -> Component:
        """Center align text."""
        return self.tengah()

    def lebar(self, lebar: str) -> Component:
        """Set width. Contoh: .lebar("100%")"""
        self.style.width = lebar
        return self

    def tinggi(self, tinggi: str) -> Component:
        """Set height."""
        self.style.height = tinggi
        return self

    def padding(self, padding: str) -> Component:
        """Set padding. Contoh: .padding("16px")"""
        self.style.padding = padding
        return self

    def margin(self, margin: str) -> Component:
        """Set margin."""
        self.style.margin = margin
        return self

    def bulat(self, radius: str = "8px") -> Component:
        """Set border radius. Contoh: .bulat()"""
        self.style.border_radius = radius
        return self

    def bayangan(self, shadow: str = "0 4px 6px rgba(0,0,0,0.1)") -> Component:
        """Set box shadow."""
        self.style.box_shadow = shadow
        return self

    def border(self, border: str = "1px solid #E5E7EB") -> Component:
        """Set border."""
        self.style.border = border
        return self

    def opacity(self, val: float) -> Component:
        """Set opacity (0.0 - 1.0)."""
        self.style.opacity = val
        return self

    def cursor(self, cursor: str) -> Component:
        """Set cursor. Contoh: .cursor("pointer")"""
        self.style.cursor = cursor
        return self

    def animasi(self, animation: str) -> Component:
        """Set CSS animation."""
        animations = {
            "fade_in": "fadeIn 0.3s ease-in",
            "fade_out": "fadeOut 0.3s ease-out",
            "slide_up": "slideUp 0.3s ease-out",
            "slide_down": "slideDown 0.3s ease-out",
            "bounce": "bounce 0.5s ease-in-out",
            "pulse": "pulse 2s infinite",
            "spin": "spin 1s linear infinite",
        }
        self.style.transition = animations.get(animation, animation)
        return self

    # ==================== Layout ====================

    def flex(self, direction: str = "row", justify: str = "flex-start",
             align: str = "stretch", gap: str = "0") -> Component:
        """Set flexbox. Contoh: .flex("row", "center", "center", "16px")"""
        self.style.display = "flex"
        self.style.flex_direction = direction
        self.style.justify_content = justify
        self.style.align_items = align
        self.style.gap = gap
        return self

    def grid(self, columns: int = 1, gap: str = "16px") -> Component:
        """Set CSS Grid. Contoh: .grid(3, "24px")"""
        self.style.display = "grid"
        self.style.grid_columns = columns
        self.style.gap = gap
        return self

    def responsif(self, mobile: Optional[str] = None,
                  tablet: Optional[str] = None,
                  desktop: Optional[str] = None) -> Component:
        """Set responsive styles."""
        self.style.responsive = {}
        if mobile:
            self.style.responsive["640"] = mobile
        if tablet:
            self.style.responsive["768"] = tablet
        if desktop:
            self.style.responsive["1024"] = desktop
        return self

    # ==================== Events ====================

    def on(self, event: str, handler: str, debounce: int = 0) -> Component:
        """Add event handler. Contoh: .on("click", "handleClick")"""
        self.events.append(EventBinding(event, handler, debounce))
        return self

    def on_klik(self, handler: str) -> Component:
        """Shorthand for click event."""
        return self.on("click", handler)

    # ==================== Children ====================

    def tambah(self, *children: Union[Component, str]) -> Component:
        """Add child components."""
        for child in children:
            if isinstance(child, str):
                self.children.append(Teks(child))
            else:
                self.children.append(child)
        return self

    # ==================== Rendering ====================

    def render_attrs(self) -> str:
        """Render HTML attributes."""
        attrs = []
        if self.id:
            attrs.append(f'id="{self.id}"')
        if self.class_names:
            attrs.append(f'class="{" ".join(self.class_names)}"')
        for key, value in self.attrs.items():
            if key != "id" and key != "class_name":
                attrs.append(f'{key}="{html.escape(str(value))}"')
        for key, value in self._data_attrs.items():
            attrs.append(f'data-{key}="{html.escape(str(value))}"')
        for event in self.events:
            event_name = event.event.replace("_", "-")
            handler = event.handler
            if event.debounce:
                handler = f"debounce(() => {handler}, {event.debounce})"
            attrs.append(f'on{event_name}="{handler}"')
        return " ".join(attrs)

    def render_style(self) -> str:
        """Render inline style."""
        css = self.style.to_css()
        return f' style="{css}"' if css else ""

    def render(self, indent: int = 0) -> str:
        """Render ke HTML string."""
        indentation = "  " * indent
        attrs = self.render_attrs()
        style = self.render_style()
        tag_str = f"{self.tag}"
        if attrs or style:
            tag_str += f" {attrs}{style}"

        if self.content and not self.children:
            if self.tag in ("script", "style"):
                return f"{indentation}<{tag_str}>\n{self.content}\n{indentation}</{self.tag}>"
            return f"{indentation}<{tag_str}>{self.content}</{self.tag}>"

        if not self.children:
            return f"{indentation}<{tag_str}></{tag_str}>"

        children_html = ""
        for child in self.children:
            children_html += child.render(indent + 1) + "\n"

        return f"{indentation}<{tag_str}>\n{children_html}{indentation}</{self.tag}>"

    def to_dict(self) -> Dict[str, Any]:
        """Serialize component ke dictionary."""
        return {
            "type": self.__class__.__name__,
            "tag": self.tag,
            "content": self.content,
            "attrs": self.attrs,
            "style": self.style.to_css(),
            "children": [c.to_dict() for c in self.children],
        }


# ==================== Helper Components ====================

class Teks(Component):
    """Komponen teks dasar."""
    def __init__(self, content: str, **kwargs):
        super().__init__(tag="span", content=content, **kwargs)


class TeksBlock(Component):
    """Komponen teks block (paragraf)."""
    def __init__(self, content: str, **kwargs):
        super().__init__(tag="p", content=content, **kwargs)
