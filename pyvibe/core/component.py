"""
Component Base Class — komponen dasar PyVibe dengan builder pattern.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field


@dataclass
class Style:
    """CSS Style container."""
    display: str = ""
    flex_direction: str = ""
    justify_content: str = ""
    align_items: str = ""
    gap: str = ""
    grid_columns: str = ""
    padding: str = ""
    margin: str = ""
    width: str = ""
    height: str = ""
    min_width: str = ""
    max_width: str = ""
    min_height: str = ""
    max_height: str = ""
    border: str = ""
    border_radius: str = ""
    box_shadow: str = ""
    background: str = ""
    background_color: str = ""
    color: str = ""
    font_size: str = ""
    font_weight: str = ""
    font_style: str = ""
    text_align: str = ""
    text_decoration: str = ""
    text_transform: str = ""
    line_height: str = ""
    letter_spacing: str = ""
    overflow: str = ""
    position: str = ""
    top: str = ""
    right: str = ""
    bottom: str = ""
    left: str = ""
    z_index: str = ""
    opacity: str = ""
    cursor: str = ""
    transition: str = ""
    animation: str = ""
    transform: str = ""
    white_space: str = ""
    word_break: str = ""
    object_fit: str = ""
    responsive: Dict[str, str] = field(default_factory=dict)
    
    def to_css(self) -> str:
        """Convert to CSS string."""
        css_parts = []
        for key, value in self.__dict__.items():
            if value and key != "responsive":
                css_key = key.replace("_", "-")
                css_parts.append(f"{css_key}: {value};")
        return " ".join(css_parts)


@dataclass
class EventBinding:
    """Event handler binding."""
    event: str
    handler: str
    debounce: int = 0


class Component:
    """Base component class untuk semua komponen PyVibe."""

    def __init__(self, tag: str = "div", content: str = "", **kwargs):
        self.tag = tag
        self.content = content
        self.children: List[Component] = []
        self.class_names: List[str] = []
        self.style = Style()
        self.events: List[EventBinding] = []
        self.id = kwargs.pop("id", "")
        self.attrs: Dict[str, str] = {k: str(v) for k, v in kwargs.items()}

    # ==================== Builder Methods ====================

    def warna(self, warna: str) -> Component:
        """Set text color. Contoh: .warna("biru")"""
        color_map = {
            "biru": "#3B82F6", "merah": "#EF4444", "hijau": "#22C55E",
            "kuning": "#EAB308", "ungu": "#7C3AED", "cyan": "#06B6D4",
            "pink": "#EC4899", "abu": "#6B7280", "putih": "#FFFFFF",
            "hitam": "#000000", "abu-100": "#F3F4F6", "abu-200": "#E5E7EB",
            "abu-300": "#D1D5DB", "abu-400": "#9CA3AF", "abu-500": "#6B7280",
            "abu-600": "#4B5563", "abu-700": "#374151", "abu-800": "#1F2937",
            "abu-900": "#111827",
        }
        self.style.color = color_map.get(warna, warna)
        return self

    def bg(self, warna: str) -> Component:
        """Set background color."""
        color_map = {
            "biru": "#3B82F6", "merah": "#EF4444", "hijau": "#22C55E",
            "kuning": "#EAB308", "ungu": "#7C3AED", "gradient-biru": "linear-gradient(135deg, #667eea, #764ba2)",
            "gradient-ungu": "linear-gradient(135deg, #7c3aed, #a855f7)",
            "gradient-hijau": "linear-gradient(135deg, #22c55e, #06b6d4)",
            "bg-gray-900": "#111827",
        }
        self.style.background = color_map.get(warna, warna)
        return self

    def ukuran(self, ukuran: str) -> Component:
        """Set font size."""
        self.style.font_size = ukuran
        return self

    def besar(self) -> Component:
        """Set large size."""
        self.style.font_size = "2rem"
        return self

    def kecil(self) -> Component:
        """Set small size."""
        self.style.font_size = "0.875rem"
        return self

    def tebal(self, tebal: bool = True) -> Component:
        """Set bold."""
        self.style.font_weight = "700" if tebal else "400"
        return self

    def tipis(self, tipis: bool = True) -> Component:
        """Set thin/light weight."""
        self.style.font_weight = "300" if tipis else "400"
        return self

    def tengah(self) -> Component:
        """Center align text."""
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
        """Left align (alias)."""
        return self.kiri()

    def rata_kanan(self) -> Component:
        """Right align (alias)."""
        return self.kanan()

    def rata_tengah(self) -> Component:
        """Center align (alias)."""
        return self.tengah()

    def lebar(self, lebar: str) -> Component:
        """Set width."""
        self.style.width = lebar
        return self

    def tinggi(self, tinggi: str) -> Component:
        """Set height."""
        self.style.height = tinggi
        return self

    def padding(self, padding: str) -> Component:
        """Set padding."""
        self.style.padding = padding
        return self

    def margin(self, margin: str) -> Component:
        """Set margin."""
        self.style.margin = margin
        return self

    def bulat(self, radius: str = "8px") -> Component:
        """Set border radius."""
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
        """Set opacity."""
        self.style.opacity = str(val)
        return self

    def cursor(self, cursor: str) -> Component:
        """Set cursor."""
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

    # ==================== Layout Methods ====================

    def flex(self, direction: str = "row", justify: str = "flex-start",
             align: str = "stretch", gap: str = "0") -> Component:
        """Set flexbox."""
        self.style.display = "flex"
        self.style.flex_direction = direction
        self.style.justify_content = justify
        self.style.align_items = align
        self.style.gap = gap
        return self

    def grid(self, columns: int = 1, gap: str = "16px") -> Component:
        """Set CSS Grid."""
        self.style.display = "grid"
        self.style.grid_columns = f"repeat({columns}, 1fr)"
        self.style.gap = gap
        return self

    def gap(self, gap: str) -> Component:
        """Set gap between children."""
        if not gap.endswith("px"):
            gap = f"{gap}px"
        self.style.gap = gap
        return self

    def wrap(self) -> Component:
        """Enable flex wrap."""
        self.class_names.append("pv-flex-wrap")
        return self

    def justify(self, value: str) -> Component:
        """Set justify-content."""
        justify_map = {
            "center": "center",
            "between": "space-between",
            "around": "space-around",
            "evenly": "space-evenly",
            "start": "flex-start",
            "end": "flex-end",
        }
        self.style.justify_content = justify_map.get(value, value)
        return self

    def items(self, value: str) -> Component:
        """Set align-items."""
        items_map = {
            "center": "center",
            "start": "flex-start",
            "end": "flex-end",
            "stretch": "stretch",
            "baseline": "baseline",
        }
        self.style.align_items = items_map.get(value, value)
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

    # ==================== Event Methods ====================

    def on(self, event: str, handler: str, debounce: int = 0) -> Component:
        """Add event handler."""
        self.events.append(EventBinding(event, handler, debounce))
        return self

    def on_klik(self, handler: str) -> Component:
        """Shorthand for click event."""
        return self.on("click", handler)

    # ==================== Children Methods ====================

    def tambah(self, *children: Union[Component, str]) -> Component:
        """Add child components."""
        from pyvibe.core.component import Teks
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

        # Render style
        css = self.style.to_css()
        if css:
            attrs.append(f'style="{css}"')

        # Render class names
        if self.class_names:
            attrs.append(f'class="{" ".join(self.class_names)}"')

        # Render other attributes
        for key, value in self.attrs.items():
            attrs.append(f'{key}="{value}"')

        # Render events
        for event in self.events:
            attrs.append(f'on{event.event}="{event.handler}()"')

        return " ".join(attrs)

    def render(self) -> str:
        """Render component to HTML."""
        attrs = self.render_attrs()
        attrs_str = f" {attrs}" if attrs else ""

        # Self-closing tags
        if self.tag in ("img", "input", "br", "hr", "meta", "link"):
            return f"<{self.tag}{attrs_str} />"

        # Render children
        children_html = ""
        if self.content:
            children_html = self.content
        for child in self.children:
            children_html += child.render()

        return f"<{self.tag}{attrs_str}>{children_html}</{self.tag}>"


class Teks(Component):
    """Text component."""

    def __init__(self, content: str, **kwargs):
        super().__init__(tag="span", content=content, **kwargs)
