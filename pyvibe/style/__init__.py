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
    accent: str = "#F59E0B"
    background: str = "#FFFFFF"
    foreground: str = "#000000"

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


# Predefined themes - v1.3.0 with 25 themes
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
    "forest": ThemeColors(
        primary="#059669",
        secondary="#0D9488",
        accent="#F59E0B",
    ),
    "sunrise": ThemeColors(
        primary="#F97316",
        secondary="#F59E0B",
        accent="#EC4899",
    ),
    "lavender": ThemeColors(
        primary="#8B5CF6",
        secondary="#06B6D4",
        accent="#EC4899",
    ),
    "cyber": ThemeColors(
        primary="#F87171",
        secondary="#06B6D4",
        accent="#10B981",
    ),
    "pastel2": ThemeColors(
        primary="#F472B6",
        secondary="#67E8F9",
        success="#86EFAC",
        danger="#FCA5A5",
        warning="#FDE68A",
    ),
    # v1.2.0 themes
    "dracula": ThemeColors(
        primary="#FF79C6",
        secondary="#F8F8F2",
        accent="#FF5555",
    ),
    "matrix": ThemeColors(
        primary="#00FF00",
        secondary="#00FF00",
    ),
    "synthwave": ThemeColors(
        primary="#FF00FF",
        secondary="#FF007F",
    ),
    "pastel_light": ThemeColors(
        primary="#FDF2F8",
        secondary="#FAE8F5",
    ),
    "high_contrast": ThemeColors(
        primary="#000000",
        secondary="#FFFFFF",
    ),
    # v1.3.0 NEW themes (using only ThemeColors fields)
    "aqua": ThemeColors(
        primary="#06B6D4",
        secondary="#0891b2",
    ),
    "rose": ThemeColors(
        primary="#F87171",
        secondary="#EC4899",
    ),
    "emerald": ThemeColors(
        primary="#10B981",
        secondary="#34D399",
    ),
    "sulfur": ThemeColors(
        primary="#F59E0B",
        secondary="#FBBF24",
    ),
    "sky": ThemeColors(
        primary="#0891b2",
        secondary="#67E8F9",
    ),
    "purple": ThemeColors(
        primary="#8B5CF6",
        secondary="#A78BFA",
    ),
    "orange": ThemeColors(
        primary="#F97316",
        secondary="#FB923C",
    ),
    "lime": ThemeColors(
        primary="#84CC16",
        secondary="#A3E635",
    ),
    "violet": ThemeColors(
        primary="#A855F7",
        secondary="#C4B5FD",
    ),
    "teal": ThemeColors(
        primary="#14B8A6",
        secondary="#2DD4BF",
    ),
    "brown": ThemeColors(
        primary="#A16207",
        secondary="#D97706",
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
        # v1.3.0 NEW animations
        "fade_in_up": "pvFadeInUp 0.5s ease-out",
        "fade_in_down": "pvFadeInDown 0.5s ease-out",
        "fade_in_left": "pvFadeInLeft 0.5s ease-out",
        "fade_in_right": "pvFadeInRight 0.5s ease-out",
        "bounce_in": "pvBounceIn 0.5s ease-out",
        "bounce_out": "pvBounceOut 0.5s ease-out",
        "light_speed_in": "pvLightSpeedIn 0.4s ease-out",
        "light_speed_out": "pvLightSpeedOut 0.4s ease-out",
        "rotate_in": "pvRotateIn 0.5s ease-out",
        "rotate_in_down": "pvRotateInDown 0.5s ease-out",
        "roll_out": "pvRollOut 0.5s ease-out",
        "zoom_out": "pvZoomOut 0.3s ease-out",
        "flip_in_y": "pvFlipInY 0.5s ease-out",
        "flip_out_y": "pvFlipOutY 0.5s ease-out",
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


# Enhanced style helpers v1.2.0 & v1.3.0
def glass(comp, opacity: float = 0.1):
    """Add glassmorphism effect."""
    comp.style.background = f"rgba(255, 255, 255, {opacity})"
    comp.style.backdrop_filter = "blur(10px)"
    comp.style.border = "1px solid rgba(255, 255, 255, 0.2)"
    return comp


def dark_glass(comp, opacity: float = 0.3):
    """Add dark glassmorphism effect."""
    comp.style.background = f"rgba(0, 0, 0, {opacity})"
    comp.style.backdrop_filter = "blur(10px)"
    comp.style.border = "1px solid rgba(255, 255, 255, 0.1)"
    comp.style.color = "white"
    return comp


def neon(comp, color: str = "#7C3AED"):
    """Add neon glow effect."""
    comp.style.text_shadow = f"0 0 10px {color}, 0 0 40px {color}"
    return comp


def glow(comp, color: str = "#7C3AED", radius: str = "20px"):
    """Add glow effect."""
    comp.style.box_shadow = f"0 0 {radius} {color}40"
    return comp


def pulse(comp):
    """Add pulse animation."""
    comp.style.animation = "pv-pulse 2s infinite"
    return comp


def float_(comp):
    """Add floating animation."""
    comp.style.animation = "pv-float 3s ease-in-out infinite"
    return comp


def skeleton(comp, width: str = "100%", height: str = "20px"):
    """Add skeleton loading effect."""
    comp.style.background = "linear-gradient(90deg, #E5E7EB 25%, #F3F4F6 50%, #E5E7EB 75%)"
    comp.style.background_size = "200% 100%"
    comp.style.animation = "pv-skeleton 1.5s infinite"
    comp.style.border_radius = "4px"
    comp.style.width = width
    comp.style.height = height
    return comp


def typing_cursor(comp):
    """Add typing cursor effect."""
    comp.style.border_right = "2px solid currentColor"
    comp.style.animation = "pv-blink 1s step-end infinite"
    return comp


def shake(comp):
    """Add shake animation."""
    comp.style.animation = "pv-shake 0.5s ease-in-out"
    return comp


def marquee(comp, direction: str = "left", speed: str = "20s"):
    """Add marquee/scrolling effect."""
    comp.style.overflow = "hidden"
    comp.style.white_space = "nowrap"
    comp.style.animation = f"pv-marquee {speed} linear infinite"
    return comp


def zoom_in(comp):
    """Add zoom in animation."""
    comp.style.animation = "pvZoomIn 0.3s ease-out"
    return comp


def zoom_out(comp):
    """Add zoom out animation."""
    comp.style.animation = "pvZoomOut 0.3s ease-out"
    return comp


# v1.2.0 NEW style helpers
def marble(comp, color: str = "#7C3AED"):
    """Marble/swirl effect background."""
    comp.style.background = f"radial-gradient(circle at 30% 20%, {color}30 0%, transparent 50%), radial-gradient(circle at 70% 80%, {color}20 0%, transparent 50%)"
    return comp


def neumorph(comp, light_color: str = "#FFFFFF", dark_color: str = "#000000", depth: str = "2px"):
    """Neumorphic (emboss) effect."""
    comp.style.background = light_color
    comp.style.box_shadow = f"""
        {depth} 5px 10px rgba({int(dark_color.lstrip('#')[0:2], 16)}, {int(dark_color.lstrip('#')[2:4], 16)}, {int(dark_color.lstrip('#')[4:6], 16)}, 0.3),
        {-int(depth.replace('px', ''))} 5px 10px rgba(0,0,0,0.2)
    """
    comp.style.border_radius = "10px"
    return comp


def gradient_border(comp, colors: str = "ungu-ke-biru", width: str = "2px"):
    """Gradient border effect."""
    gradient_map = {
        "ungu-ke-biru": "linear-gradient(135deg, #7C3AED, #06B6D4)",
        "biru-ke-cyan": "linear-gradient(135deg, #3B82F6, #06B6D4)",
        "pink-ke-ungu": "linear-gradient(135deg, #EC4899, #7C3AED)",
        "hijau-ke-cyan": "linear-gradient(135deg, #22C55E, #06B6D4)",
        "orange-ke-pink": "linear-gradient(135deg, #F97316, #EC4899)",
    }
    comp.style.border = f"{width} solid {gradient_map.get(colors, colors)}"
    comp.style.border_radius = "8px"
    return comp


def neon_text(comp, color: str = "#7C3AED", intensity: str = "strong"):
    """Neon text effect."""
    intensities = {
        "strong": "0 0 10px, 0 0 40px",
        "medium": "0 0 5px, 0 0 20px",
        "weak": "0 0 3px, 0 0 10px",
    }
    shadow_intensity = intensities.get(intensity, intensities["strong"])
    comp.style.text_shadow = f"{shadow_intensity} {color}"
    return comp


def bounce(comp):
    """Add bounce animation."""
    comp.style.animation = "pvBounce 0.5s ease-in-out"
    return comp


def spin(comp):
    """Add spin animation."""
    comp.style.animation = "pvSpin 1s linear infinite"
    return comp


def scale(comp):
    """Add scale animation."""
    comp.style.animation = "pvScale 0.3s ease-out"
    return comp


def slide_up(comp):
    """Slide up animation."""
    comp.style.animation = "pvSlideUp 0.3s ease-out"
    return comp


def slide_down(comp):
    """Slide down animation."""
    comp.style.animation = "pvSlideDown 0.3s ease-out"
    return comp


def slide_left(comp):
    """Slide left animation."""
    comp.style.animation = "pvSlideLeft 0.3s ease-out"
    return comp


def slide_right(comp):
    """Slide right animation."""
    comp.style.animation = "pvSlideRight 0.3s ease-out"
    return comp


def roll_in(comp):
    """Roll in animation."""
    comp.style.animation = "pvRollIn 0.6s ease-out"
    return comp


def rubber_band(comp):
    """Rubber band animation."""
    comp.style.animation = "pvRubberBand 0.8s ease-in-out"
    return comp


def jello(comp):
    """Jello animation."""
    comp.style.animation = "pvJello 0.8s ease-in-out"
    return comp


def swing(comp):
    """Swing animation."""
    comp.style.animation = "pvSwing 0.8s ease-in-out"
    return comp


def typewriter(comp):
    """Typewriter animation."""
    comp.style.animation = "pvTypewriter 2s steps(40) forwards"
    return comp


# v1.3.0 NEW style helpers
def frost(comp, color: str = "#7C3AED"):
    """Frost/ice effect background with subtle gradient."""
    comp.style.background = f"""
        linear-gradient(135deg, {color}10 0%, {color}5 50%, transparent 50%),
        linear-gradient(135deg, transparent 50%, {color}5 100%, {color}10 100%)
    """
    comp.style.backdrop_filter = "blur(20px)"
    comp.style.border_radius = "12px"
    return comp


def glass_morphism(comp, opacity: float = 0.1, blur: str = "15px"):
    """Enhanced glassmorphism effect."""
    comp.style.background = f"rgba(255, 255, 255, {opacity})"
    comp.style.backdrop_filter = f"blur({blur})"
    comp.style.border = f"1px solid rgba(255, 255, 255, {1-opacity * 0.5})"
    comp.style.border_radius = "12px"
    return comp


def neon_glow(comp, color: str = "#7C3AED", intensity: str = "strong"):
    """Enhanced neon glow with multiple layers."""
    intensities = {
        "strong": "0 0 10px, 0 0 40px, 0 0 80px",
        "medium": "0 0 5px, 0 0 25px, 0 0 50px",
        "weak": "0 0 3px, 0 0 15px, 0 0 30px",
    }
    shadow_tiers = intensities.get(intensity, intensities["strong"])
    comp.style.text_shadow = f"{shadow_tiers} {color}"
    return comp


def glass_kit(comp, color: str = "#7C3AED"):
    """Complete glass kit with background, border, and shadow."""
    comp.style.background = f"rgba(255, 255, 255, 0.1)"
    comp.style.backdrop_filter = "blur(12px)"
    comp.style.border = "1px solid rgba(255, 255, 255, 0.3)"
    comp.style.border_radius = "16px"
    comp.style.box_shadow = "0 4px 20px rgba(0,0,0,0.1)"
    return comp


def neumorphic(comp, light_color: str = "#FFFFFF", dark_color: str = "#000000", depth: str = "4px"):
    """Enhanced neumorphic effect with multiple shadow layers."""
    comp.style.background = light_color
    r, g, b = int(dark_color.lstrip('#')[0:2], 16), int(dark_color.lstrip('#')[2:4], 16), int(dark_color.lstrip('#')[4:6], 16)
    comp.style.box_shadow = f"""
        {depth} 8px 16px rgba({r}, {g}, {b}, 0.3),
        {-depth} 8px 16px rgba({r}, {g}, {b}, 0.2),
        inset {depth} 4px 6px rgba({r}, {g}, {b}, 0.1),
        inset {-depth} 4px 6px rgba({r}, {g}, {b}, 0.1)
    """
    comp.style.border_radius = "16px"
    return comp


def border_glass(comp, color: str = "#7C3AED", opacity: float = 0.2):
    """Glass-like border effect."""
    comp.style.border = f"{width} solid {color}40"
    comp.style.border_radius = "8px"
    return comp


def neon_border(comp, color: str = "#7C3AED", width: str = "2px"):
    """Neon border effect."""
    comp.style.border = f"{width} solid {color}"
    comp.style.box_shadow = f"0 0 10px {color}, 0 0 25px {color}"
    return comp


def morph(comp, progress: float = 0.5):
    """Morphing effect based on progress value."""
    # Create smooth transition between states
    comp.style.transition = "all 0.3s ease"
    return comp


def float_label(comp, label: str = "Label"):
    """Float label effect for input fields."""
    comp.style.position = "relative"
    comp.style.margin_bottom = "15px"
    return comp


def input_shadow(comp, color: str = "#7C3AED"):
    """Input field focus shadow effect."""
    comp.style.box_shadow = f"0 0 0 2px {color}"
    return comp


def ripple(comp, x: float = 0.5, y: float = 0.5):
    """Ripple effect for buttons (CSS-only)."""
    comp.style.position = "relative"
    comp.style.overflow = "hidden"
    return comp


def count_up(comp, end_value: int, duration: str = "2s"):
    """Count-up animation for numeric displays."""
    comp.style.animation = f"pvCountUp {duration} ease-out"
    # Set the target value as a data attribute
    comp.style.set('data-target', str(end_value))
    return comp