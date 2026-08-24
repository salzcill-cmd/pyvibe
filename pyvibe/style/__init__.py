"""
PyVibe Style — comprehensive styling system with themes, animations, and responsive utilities.

Usage:
    from pyvibe.style import Theme, Animation, Responsive

    # Apply theme
    theme = Theme("dark")
    app.config["theme"] = theme

    # Use animations
    component.animasi("fade_in")

    # Responsive
    component.responsif(mobile="pv-text-center", desktop="pv-flex")
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
import json


# ==================== Theme System ====================

@dataclass
class ThemeColors:
    """Theme color palette."""
    primary: str = "#7C3AED"
    primary_light: str = "#7C3AED22"
    primary_hover: str = "#7C3AEDdd"
    secondary: str = "#06B6D4"
    success: str = "#22C55E"
    danger: str = "#EF4444"
    warning: str = "#EAB308"
    info: str = "#3B82F6"
    white: str = "#FFFFFF"
    black: str = "#000000"
    gray_50: str = "#F9FAFB"
    gray_100: str = "#F3F4F6"
    gray_200: str = "#E5E7EB"
    gray_300: str = "#D1D5DB"
    gray_400: str = "#9CA3AF"
    gray_500: str = "#6B7280"
    gray_600: str = "#4B5563"
    gray_700: str = "#374151"
    gray_800: str = "#1F2937"
    gray_900: str = "#111827"

    def to_css_variables(self) -> str:
        """Generate CSS variables from theme colors."""
        return f"""
    --pv-primary: {self.primary};
    --pv-primary-light: {self.primary_light};
    --pv-primary-hover: {self.primary_hover};
    --pv-secondary: {self.secondary};
    --pv-success: {self.success};
    --pv-success-light: {self.success}22;
    --pv-danger: {self.danger};
    --pv-danger-light: {self.danger}22;
    --pv-warning: {self.warning};
    --pv-warning-light: {self.warning}22;
    --pv-info: {self.info};
    --pv-info-light: {self.info}22;
    --pv-white: {self.white};
    --pv-black: {self.black};
    --pv-gray-50: {self.gray_50};
    --pv-gray-100: {self.gray_100};
    --pv-gray-200: {self.gray_200};
    --pv-gray-300: {self.gray_300};
    --pv-gray-400: {self.gray_400};
    --pv-gray-500: {self.gray_500};
    --pv-gray-600: {self.gray_600};
    --pv-gray-700: {self.gray_700};
    --pv-gray-800: {self.gray_800};
    --pv-gray-900: {self.gray_900};
"""


# Predefined themes
THEMES: Dict[str, ThemeColors] = {
    "default": ThemeColors(),
    "light": ThemeColors(
        primary="#3B82F6",
        secondary="#06B6D4",
        gray_50="#F8FAFC",
        gray_100="#F1F5F9",
        gray_900="#0F172A",
    ),
    "dark": ThemeColors(
        primary="#818CF8",
        primary_light="#818CF822",
        secondary="#22D3EE",
        white="#F9FAFB",
        black="#000000",
        gray_50="#18181B",
        gray_100="#27272A",
        gray_200="#3F3F46",
        gray_300="#52525B",
        gray_400="#71717A",
        gray_500="#A1A1AA",
        gray_600="#D4D4D8",
        gray_700="#E4E4E7",
        gray_800="#F4F4F5",
        gray_900="#FAFAFA",
    ),
    "nature": ThemeColors(
        primary="#16A34A",
        secondary="#059669",
        success="#22C55E",
        danger="#DC2626",
    ),
    "sunset": ThemeColors(
        primary="#F97316",
        secondary="#EC4899",
        success="#22C55E",
        danger="#EF4444",
        warning="#F59E0B",
    ),
    "ocean": ThemeColors(
        primary="#0EA5E9",
        secondary="#06B6D4",
        success="#10B981",
        danger="#F43F5E",
    ),
    "royal": ThemeColors(
        primary="#7C3AED",
        secondary="#A855F7",
        success="#22C55E",
        danger="#EF4444",
    ),
    "corporate": ThemeColors(
        primary="#1E40AF",
        secondary="#3B82F6",
        success="#059669",
        danger="#DC2626",
        gray_900="#111827",
    ),
    "pastel": ThemeColors(
        primary="#C084FC",
        secondary="#67E8F9",
        success="#86EFAC",
        danger="#FCA5A5",
        warning="#FDE68A",
    ),
    "neon": ThemeColors(
        primary="#A855F7",
        secondary="#22D3EE",
        success="#4ADE80",
        danger="#FB7185",
        warning="#FACC15",
    ),
}


class Theme:
    """
    Theme manager untuk PyVibe apps.

    Usage:
        theme = Theme("dark")
        css = theme.to_css()

        # Custom theme
        custom = Theme.custom(
            name="my-brand",
            primary="#FF6B6B",
            secondary="#4ECDC4",
        )
    """

    def __init__(self, name: str = "default", **overrides):
        self.name = name
        if name in THEMES:
            self.colors = ThemeColors(**{**THEMES[name].__dict__, **overrides})
        else:
            self.colors = ThemeColors(**overrides)

    @classmethod
    def custom(cls, name: str = "custom", **kwargs) -> "Theme":
        """Create custom theme."""
        return cls(name=name, **kwargs)

    def to_css(self) -> str:
        """Generate CSS for this theme."""
        return f"""
/* PyVibe Theme: {self.name} */
:root {{
    {self.colors.to_css_variables()}
    --pv-radius-sm: 6px;
    --pv-radius: 8px;
    --pv-radius-lg: 12px;
    --pv-radius-xl: 16px;
    --pv-radius-full: 9999px;
    --pv-shadow-xs: 0 1px 2px rgba(0,0,0,0.05);
    --pv-shadow-sm: 0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06);
    --pv-shadow: 0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.06);
    --pv-shadow-lg: 0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05);
    --pv-shadow-xl: 0 20px 25px rgba(0,0,0,0.1), 0 10px 10px rgba(0,0,0,0.04);
    --pv-transition: all 0.2s ease;
    --pv-transition-slow: all 0.3s ease;
}}
"""

    @classmethod
    def list_themes(cls) -> List[str]:
        """List available themes."""
        return list(THEMES.keys())


# ==================== Animation System ====================

class Animation:
    """
    Animation presets untuk PyVibe components.

    Usage:
        comp = judul("Hello")
        comp.animasi("fade_in")
        comp.animasi("bounce")
        comp.animasi("slide_up")
    """

    PRESETS = {
        "fade_in": "pvFadeIn 0.3s ease-in",
        "fade_out": "pvFadeOut 0.3s ease-out",
        "slide_up": "pvSlideUp 0.3s ease-out",
        "slide_down": "pvSlideDown 0.3s ease-out",
        "slide_left": "pvSlideLeft 0.3s ease-out",
        "slide_right": "pvSlideRight 0.3s ease-out",
        "bounce": "pvBounce 0.5s ease-in-out",
        "pulse": "pvPulse 2s infinite",
        "spin": "pvSpin 1s linear infinite",
        "scale": "pvScale 0.3s ease-out",
        "shake": "pvShake 0.5s ease-in-out",
        "wiggle": "pvWiggle 0.5s ease-in-out",
        "float": "pvFloat 3s ease-in-out infinite",
        "heartbeat": "pvHeartbeat 1.5s ease-in-out infinite",
        "flip": "pvFlip 0.6s ease-in-out",
        "zoom_in": "pvZoomIn 0.3s ease-out",
        "zoom_out": "pvZoomOut 0.3s ease-out",
        "roll_in": "pvRollIn 0.6s ease-out",
        "rubber_band": "pvRubberBand 0.8s ease-in-out",
        "jello": "pvJello 0.8s ease-in-out",
        "swing": "pvSwing 0.8s ease-in-out",
        "typewriter": "pvTypewriter 2s steps(40) forwards",
    }

    @classmethod
    def get(cls, name: str, duration: Optional[str] = None, delay: Optional[str] = None, iteration: Optional[str] = None) -> str:
        """Get animation CSS value."""
        anim = cls.PRESETS.get(name, name)
        if duration:
            parts = anim.split()
            if len(parts) >= 2:
                parts[1] = duration
            anim = " ".join(parts)
        if delay:
            anim += f" {delay}"
        if iteration:
            anim += f" {iteration}"
        return anim

    @classmethod
    def list_animations(cls) -> List[str]:
        """List available animations."""
        return list(cls.PRESETS.keys())

    @classmethod
    def custom(cls, name: str, keyframes: str, duration: str = "0.3s", timing: str = "ease", fill_mode: str = "forwards") -> str:
        """Create custom animation CSS."""
        return f"""
@keyframes {name} {{
{keyframes}
}}
.pv-animate-{name.replace('_', '-')} {{
    animation: {name} {duration} {timing} {fill_mode};
}}
"""


# ==================== Responsive System ====================

class Responsive:
    """
    Responsive breakpoints dan utilities.

    Usage:
        comp.responsif(mobile="pv-text-center", desktop="pv-flex pv-items-center")
    """

    BREAKPOINTS = {
        "mobile": 640,
        "tablet": 768,
        "desktop": 1024,
        "wide": 1280,
        "ultrawide": 1536,
    }

    @classmethod
    def media_query(cls, breakpoint: str, css: str) -> str:
        """Generate media query CSS."""
        width = cls.BREAKPOINTS.get(breakpoint, 768)
        return f"""
@media (min-width: {width}px) {{
    {css}
}}
"""

    @classmethod
    def mobile_only(cls, css: str) -> str:
        """CSS for mobile only."""
        return f"""
@media (max-width: {cls.BREAKPOINTS['tablet'] - 1}px) {{
    {css}
}}
"""

    @classmethod
    def tablet_and_up(cls, css: str) -> str:
        """CSS for tablet and up."""
        return cls.media_query("tablet", css)

    @classmethod
    def desktop_and_up(cls, css: str) -> str:
        """CSS for desktop and up."""
        return cls.media_query("desktop", css)


# ==================== Utility Functions ====================

def get_theme(name: str = "default") -> Theme:
    """Get theme by name."""
    return Theme(name)


def list_themes() -> List[str]:
    """List all available themes."""
    return Theme.list_themes()


def list_animations() -> List[str]:
    """List all available animations."""
    return Animation.list_animations()


# ==================== Style Helpers ====================

def tengah(comp):
    """Center align text."""
    comp.style.text_align = "center"
    return comp

def kiri(comp):
    """Left align text."""
    comp.style.text_align = "left"
    return comp

def kanan(comp):
    """Right align text."""
    comp.style.text_align = "right"
    return comp

def rata_kiri(comp):
    """Left align (alias)."""
    return kiri(comp)

def rata_kanan(comp):
    """Right align (alias)."""
    return kanan(comp)

def rata_tengah(comp):
    """Center align (alias)."""
    return tengah(comp)

def gelap(comp):
    """Dark background."""
    comp.style.background = "#111827"
    comp.style.color = "#FFFFFF"
    return comp

def terang(comp):
    """Light background."""
    comp.style.background = "#F9FAFB"
    return comp

def gradient(comp, colors: str = "ungu-ke-biru"):
    """Gradient background."""
    gradient_map = {
        "ungu-ke-biru": "linear-gradient(135deg, #7C3AED, #06B6D4)",
        "biru-ke-cyan": "linear-gradient(135deg, #3B82F6, #06B6D4)",
        "pink-ke-ungu": "linear-gradient(135deg, #EC4899, #7C3AED)",
        "hijau-ke-cyan": "linear-gradient(135deg, #22C55E, #06B6D4)",
        "orange-ke-pink": "linear-gradient(135deg, #F97316, #EC4899)",
    }
    comp.style.background = gradient_map.get(colors, colors)
    return comp

def bulat(comp, radius: str = "8px"):
    """Set border radius."""
    comp.style.border_radius = radius
    return comp

def bayangan(comp, shadow: str = "0 4px 6px rgba(0,0,0,0.1)"):
    """Set box shadow."""
    comp.style.box_shadow = shadow
    return comp

def border(comp, border: str = "1px solid #E5E7EB"):
    """Set border."""
    comp.style.border = border
    return comp

def responsif(comp, mobile: Optional[str] = None, tablet: Optional[str] = None, desktop: Optional[str] = None):
    """Set responsive styles."""
    if mobile:
        comp.style.responsive["640"] = mobile
    if tablet:
        comp.style.responsive["768"] = tablet
    if desktop:
        comp.style.responsive["1024"] = desktop
    return comp

def flex(comp, direction: str = "row", justify: str = "flex-start", align: str = "stretch", gap: str = "0"):
    """Set flexbox."""
    comp.style.display = "flex"
    comp.style.flex_direction = direction
    comp.style.justify_content = justify
    comp.style.align_items = align
    comp.style.gap = gap
    return comp
