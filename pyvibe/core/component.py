"""
Component Base Class — komponen dasar PyVibe dengan builder pattern.

v2: Enhanced with more builder methods, accessibility, and better rendering.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, Union
from dataclasses import dataclass, field
import html as html_module


@dataclass
class Style:
    """CSS Style container."""
    display: str = ""
    flex_direction: str = ""
    justify_content: str = ""
    align_items: str = ""
    align_self: str = ""
    gap: str = ""
    grid_columns: str = ""
    grid_template_columns: str = ""
    grid_template_rows: str = ""
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
    font_family: str = ""
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
    backdrop_filter: str = ""
    list_style: str = ""
    vertical_align: str = ""
    resize: str = ""
    outline: str = ""
    box_sizing: str = ""
    flex_shrink: str = ""
    flex_grow: str = ""
    flex_basis: str = ""
    order: str = ""
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
    """
    Base component class untuk semua komponen PyVibe.
    
    Supports:
    - Chainable builder pattern
    - Accessibility (ARIA attributes)
    - Responsive design
    - Event handling
    - CSS class-based styling
    - HTML escaping for security
    """

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
            "hitam": "#000000", "orange": "#F97316",
            "abu-100": "#F3F4F6", "abu-200": "#E5E7EB",
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
            "kuning": "#EAB308", "ungu": "#7C3AED", "cyan": "#06B6D4",
            "pink": "#EC4899", "orange": "#F97316",
            "gradient-biru": "linear-gradient(135deg, #667eea, #764ba2)",
            "gradient-ungu": "linear-gradient(135deg, #7c3aed, #a855f7)",
            "gradient-hijau": "linear-gradient(135deg, #22c55e, #06b6d4)",
            "gradient-pink": "linear-gradient(135deg, #EC4899, #7C3AED)",
            "gradient-orange": "linear-gradient(135deg, #F97316, #EC4899)",
            "bg-gray-900": "#111827", "bg-gray-800": "#1F2937",
            "gelap": "#111827", "terang": "#F9FAFB",
        }
        self.style.background = color_map.get(warna, warna)
        return self

    def ukuran(self, ukuran: str) -> Component:
        """Set font size."""
        size_map = {
            "xs": "0.75rem", "sm": "0.875rem", "md": "1rem",
            "lg": "1.125rem", "xl": "1.25rem", "2xl": "1.5rem",
            "3xl": "1.875rem", "4xl": "2.25rem",
            "kecil": "0.875rem", "sedang": "1rem", "besar": "2rem",
        }
        self.style.font_size = size_map.get(ukuran, ukuran)
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

    def miring(self) -> Component:
        """Set italic."""
        self.style.font_style = "italic"
        return self

    def garis_bawah(self) -> Component:
        """Set underline."""
        self.style.text_decoration = "underline"
        return self

    def huruf_besar(self) -> Component:
        """Set uppercase."""
        self.style.text_transform = "uppercase"
        self.style.letter_spacing = "0.05em"
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

    def min_lebar(self, val: str) -> Component:
        """Set min-width."""
        self.style.min_width = val
        return self

    def max_lebar(self, val: str) -> Component:
        """Set max-width."""
        self.style.max_width = val
        return self

    def min_tinggi(self, val: str) -> Component:
        """Set min-height."""
        self.style.min_height = val
        return self

    def max_tinggi(self, val: str) -> Component:
        """Set max-height."""
        self.style.max_height = val
        return self

    def padding(self, padding: str) -> Component:
        """Set padding."""
        self.style.padding = padding
        return self

    def padding_x(self, val: str) -> Component:
        """Set horizontal padding."""
        self.style.padding = f"0 {val}"
        return self

    def padding_y(self, val: str) -> Component:
        """Set vertical padding."""
        self.style.padding = f"{val} 0"
        return self

    def margin(self, margin: str) -> Component:
        """Set margin."""
        self.style.margin = margin
        return self

    def margin_x(self, val: str) -> Component:
        """Set horizontal margin."""
        self.style.margin = f"0 {val}"
        return self

    def margin_y(self, val: str) -> Component:
        """Set vertical margin."""
        self.style.margin = f"{val} 0"
        return self

    def bulat(self, radius: str = "8px") -> Component:
        """Set border radius."""
        radius_map = {
            "sm": "4px", "md": "8px", "lg": "12px", "xl": "16px",
            "2xl": "24px", "full": "9999px", "pill": "9999px",
        }
        self.style.border_radius = radius_map.get(radius, radius)
        return self

    def bayangan(self, shadow: str = "0 4px 6px rgba(0,0,0,0.1)") -> Component:
        """Set box shadow."""
        shadow_map = {
            "xs": "0 1px 2px rgba(0,0,0,0.05)",
            "sm": "0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06)",
            "md": "0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.06)",
            "lg": "0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05)",
            "xl": "0 20px 25px rgba(0,0,0,0.1), 0 10px 10px rgba(0,0,0,0.04)",
            "2xl": "0 25px 50px rgba(0,0,0,0.25)",
            "none": "none",
        }
        self.style.box_shadow = shadow_map.get(shadow, shadow)
        return self

    def border(self, border: str = "1px solid #E5E7EB") -> Component:
        """Set border."""
        self.style.border = border
        return self

    def border_top(self, border: str = "1px solid #E5E7EB") -> Component:
        """Set top border."""
        self.style.border = border
        return self

    def border_bottom(self, border: str = "1px solid #E5E7EB") -> Component:
        """Set bottom border."""
        self.style.border = border
        return self

    def tanpa_border(self) -> Component:
        """Remove border."""
        self.style.border = "none"
        return self

    def opacity(self, val: float) -> Component:
        """Set opacity."""
        self.style.opacity = str(val)
        return self

    def cursor(self, cursor: str) -> Component:
        """Set cursor."""
        cursor_map = {
            "pointer": "pointer", "default": "default", "not-allowed": "not-allowed",
            "grab": "grab", "move": "move", "text": "text",
        }
        self.style.cursor = cursor_map.get(cursor, cursor)
        return self

    def overflow(self, overflow: str) -> Component:
        """Set overflow."""
        self.style.overflow = overflow
        return self

    def position(self, pos: str) -> Component:
        """Set position."""
        self.style.position = pos
        return self

    def absolute(self) -> Component:
        """Set position absolute."""
        self.style.position = "absolute"
        return self

    def relative(self) -> Component:
        """Set position relative."""
        self.style.position = "relative"
        return self

    def fixed(self) -> Component:
        """Set position fixed."""
        self.style.position = "fixed"
        return self

    def sticky(self) -> Component:
        """Set position sticky."""
        self.style.position = "sticky"
        self.style.top = "0"
        return self

    def z_index(self, val: str) -> Component:
        """Set z-index."""
        self.style.z_index = val
        return self

    def transisi(self, transition: str = "all 0.2s ease") -> Component:
        """Set CSS transition."""
        self.style.transition = transition
        return self

    def animasi(self, animation: str) -> Component:
        """Set CSS animation."""
        from pyvibe.style import Animation
        self.style.animation = Animation.get(animation)
        return self

    def transform(self, transform: str) -> Component:
        """Set CSS transform."""
        self.style.transform = transform
        return self

    def blur(self, radius: str = "10px") -> Component:
        """Set backdrop blur (glass effect)."""
        self.style.backdrop_filter = f"blur({radius})"
        return self

    def font(self, family: str) -> Component:
        """Set font family."""
        self.style.font_family = family
        return self

    def monospace(self) -> Component:
        """Set monospace font."""
        self.style.font_family = "'JetBrains Mono', monospace"
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
        if not gap.endswith("px") and not gap.endswith("rem"):
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
            "center": "center", "between": "space-between",
            "around": "space-around", "evenly": "space-evenly",
            "start": "flex-start", "end": "flex-end",
        }
        self.style.justify_content = justify_map.get(value, value)
        return self

    def items(self, value: str) -> Component:
        """Set align-items."""
        items_map = {
            "center": "center", "start": "flex-start", "end": "flex-end",
            "stretch": "stretch", "baseline": "baseline",
        }
        self.style.align_items = items_map.get(value, value)
        return self

    def self_align(self, value: str) -> Component:
        """Set align-self."""
        align_map = {
            "center": "center", "start": "flex-start", "end": "flex-end",
            "stretch": "stretch", "auto": "auto",
        }
        self.style.align_self = align_map.get(value, value)
        return self

    def order(self, val: str) -> Component:
        """Set order."""
        self.style.order = val
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

    def visible_on(self, device: str = "all") -> Component:
        """Control visibility on devices."""
        if device == "mobile":
            self.style.responsive["640"] = "display: none;"
        elif device == "desktop":
            self.style.responsive["1024"] = "display: none;"
        elif device == "print":
            self.style.responsive["print"] = "display: none;"
        return self

    # ==================== Accessibility Methods ====================

    def aria_label(self, label: str) -> Component:
        """Set aria-label."""
        self.attrs["aria-label"] = label
        return self

    def aria_hidden(self, hidden: bool = True) -> Component:
        """Set aria-hidden."""
        self.attrs["aria-hidden"] = "true" if hidden else "false"
        return self

    def aria_describedby(self, element_id: str) -> Component:
        """Set aria-describedby."""
        self.attrs["aria-describedby"] = element_id
        return self

    def role(self, role: str) -> Component:
        """Set role attribute."""
        self.attrs["role"] = role
        return self

    def tabindex(self, val: str = "0") -> Component:
        """Set tabindex."""
        self.attrs["tabindex"] = val
        return self

    def tooltip(self, text: str) -> Component:
        """Set title tooltip."""
        self.attrs["title"] = text
        return self

    # ==================== Event Methods ====================

    def on(self, event: str, handler: str, debounce: int = 0) -> Component:
        """Add event handler."""
        self.events.append(EventBinding(event, handler, debounce))
        return self

    def on_klik(self, handler: str) -> Component:
        """Shorthand for click event."""
        return self.on("click", handler)

    def on_hover(self, handler: str) -> Component:
        """Shorthand for mouseenter event."""
        return self.on("mouseenter", handler)

    def on_submit(self, handler: str) -> Component:
        """Shorthand for submit event."""
        return self.on("submit", handler)

    def on_change(self, handler: str) -> Component:
        """Shorthand for change event."""
        return self.on("change", handler)

    def on_input(self, handler: str) -> Component:
        """Shorthand for input event."""
        return self.on("input", handler)

    # ==================== Children Methods ====================

    def tambah(self, *children: Union[Component, str]) -> Component:
        """Add child components."""
        for child in children:
            if isinstance(child, str):
                self.children.append(Teks(child))
            elif isinstance(child, list):
                for item in child:
                    if isinstance(item, Component):
                        self.children.append(item)
                    else:
                        self.children.append(Teks(str(item)))
            elif isinstance(child, Component):
                self.children.append(child)
        return self

    def bersihkan(self) -> Component:
        """Remove all children."""
        self.children.clear()
        return self

    def ganti(self, index: int, child: Union[Component, str]) -> Component:
        """Replace child at index."""
        if 0 <= index < len(self.children):
            if isinstance(child, str):
                self.children[index] = Teks(child)
            else:
                self.children[index] = child
        return self

    def hapus(self, index: int) -> Component:
        """Remove child at index."""
        if 0 <= index < len(self.children):
            self.children.pop(index)
        return self

    # ==================== Clone ====================

    def clone(self) -> Component:
        """Clone this component."""
        import copy
        return copy.deepcopy(self)

    # ==================== Rendering ====================

    def render_attrs(self) -> str:
        """Render HTML attributes."""
        attrs = []
        if self.id:
            attrs.append(f'id="{self.id}"')

        # Render style
        css = self.style.to_css()
        if css:
            attrs.append(f'style="{html_module.escape(css)}"')

        # Render class names
        if self.class_names:
            valid_classes = [c for c in self.class_names if c.strip()]
            if valid_classes:
                attrs.append(f'class="{" ".join(valid_classes)}"')

        # Render other attributes
        for key, value in self.attrs.items():
            attrs.append(f'{key}="{html_module.escape(str(value))}"')

        # Render events
        for event in self.events:
            attrs.append(f'on{event.event}="{html_module.escape(event.handler)}"')

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
            children_html = html_module.escape(self.content)
        
        # Support innerHTML for raw HTML content (used by charts)
        inner_html = self.attrs.get("innerHTML", "")
        if inner_html:
            children_html = inner_html
        
        for child in self.children:
            children_html += child.render()

        return f"<{self.tag}{attrs_str}>{children_html}</{self.tag}>"

    def __repr__(self) -> str:
        """String representation."""
        return f"<{self.tag} class='{' '.join(self.class_names[:2])}'>"


class Teks(Component):
    """Text component."""

    def __init__(self, content: str, **kwargs):
        super().__init__(tag="span", content=content, **kwargs)
