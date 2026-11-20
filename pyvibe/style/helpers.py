"""
Style Helpers — chainable styling functions.

Usage:
    from pyvibe.style.helpers import tengah, gelap

    paragraf("Teks tengah").tengah()
    bagian(bg="gelap")
"""

from typing import Optional


def tengah(component):
    """Center align text."""
    component.style.text_align = "center"
    return component


def kiri(component):
    """Left align text."""
    component.style.text_align = "left"
    return component


def kanan(component):
    """Right align text."""
    component.style.text_align = "right"
    return component


def rata_kiri(component):
    """Left align text."""
    return kiri(component)


def rata_kanan(component):
    """Right align text."""
    return kanan(component)


def rata_tengah(component):
    """Center align text."""
    return tengah(component)


def gelap(component):
    """Dark background."""
    component.style.bg = "#111827"
    component.style.color = "#FFFFFF"
    return component


def terang(component):
    """Light background."""
    component.style.bg = "#F9FAFB"
    return component


def gradient(component, colors: str = "ungu-ke-biru"):
    """Gradient background."""
    gradients = {
        "ungu-ke-biru": "linear-gradient(135deg, #7C3AED, #06B6D4)",
        "biru-ke-cyan": "linear-gradient(135deg, #3B82F6, #06B6D4)",
        "pink-ke-ungu": "linear-gradient(135deg, #EC4899, #7C3AED)",
        "hijau-ke-cyan": "linear-gradient(135deg, #22C55E, #06B6D4)",
        "orange-ke-pink": "linear-gradient(135deg, #F97316, #EC4899)",
    }
    component.style.bg = gradients.get(colors, colors)
    return component


def bulat(component, radius: str = "8px"):
    """Set border radius."""
    component.style.border_radius = radius
    return component


def bayangan(component, shadow: str = "md"):
    """Set box shadow."""
    shadows = {
        "sm": "0 1px 2px rgba(0,0,0,0.05)",
        "md": "0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06)",
        "lg": "0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05)",
        "xl": "0 20px 25px rgba(0,0,0,0.1), 0 10px 10px rgba(0,0,0,0.04)",
    }
    component.style.box_shadow = shadows.get(shadow, shadow)
    return component


def border(component, border: str = "1px solid #E5E7EB"):
    """Set border."""
    component.style.border = border
    return component


def rounded(component, radius: str = "lg"):
    """Set border radius (alias for bulat)."""
    return bulat(component, radius)


def radius_sm(component):
    """Set small border radius."""
    return bulat(component, "sm")


def radius_md(component):
    """Set medium border radius."""
    return bulat(component, "md")


def radius_lg(component):
    """Set large border radius."""
    return bulat(component, "lg")


def radius_xl(component):
    """Set extra large border radius."""
    return bulat(component, "xl")


def radius_full(component):
    """Set full/pill border radius."""
    return bulat(component, "full")


def glass(component, opacity: float = 0.1):
    """Add glassmorphism effect."""
    component.style.background = f"rgba(255, 255, 255, {opacity})"
    component.style.backdrop_filter = "blur(10px)"
    component.style.border = "1px solid rgba(255, 255, 255, 0.2)"
    return component


def dark_glass(component, opacity: float = 0.3):
    """Add dark glassmorphism effect."""
    component.style.background = f"rgba(0, 0, 0, {opacity})"
    component.style.backdrop_filter = "blur(10px)"
    component.style.border = "1px solid rgba(255, 255, 255, 0.1)"
    component.style.color = "white"
    return component


def neon(component, color: str = "#7C3AED"):
    """Add neon glow effect."""
    component.style.text_shadow = f"0 0 10px {color}, 0 0 40px {color}"
    return component


def glow(component, color: str = "#7C3AED", radius: str = "20px"):
    """Add glow effect."""
    component.style.box_shadow = f"0 0 {radius} {color}40"
    return component


def pulse(component):
    """Add pulse animation."""
    component.style.animation = "pv-pulse 2s infinite"
    return component


def float_(component):
    """Add floating animation."""
    component.style.animation = "pv-float 3s ease-in-out infinite"
    return component


def skeleton(component, width: str = "100%", height: str = "20px"):
    """Add skeleton loading effect."""
    component.style.background = "linear-gradient(90deg, #E5E7EB 25%, #F3F4F6 50%, #E5E7EB 75%)"
    component.style.background_size = "200% 100%"
    component.style.animation = "pv-skeleton 1.5s infinite"
    component.style.border_radius = "4px"
    component.style.width = width
    component.style.height = height
    return component


def typing_cursor(component):
    """Add typing cursor effect."""
    component.style.border_right = "2px solid currentColor"
    component.style.animation = "pv-blink 1s step-end infinite"
    return component


def shake(component):
    """Add shake animation."""
    component.style.animation = "pv-shake 0.5s ease-in-out"
    return component


def marquee(component, direction: str = "left", speed: str = "20s"):
    """Add marquee/scrolling effect."""
    component.style.overflow = "hidden"
    component.style.white_space = "nowrap"
    component.style.animation = f"pv-marquee {speed} linear infinite"
    return component


def zoom_in(component):
    """Add zoom in animation."""
    component.style.animation = "pvZoomIn 0.3s ease-out"
    return component


def zoom_out(component):
    """Add zoom out animation."""
    component.style.animation = "pvZoomOut 0.3s ease-out"
    return component


def responsif(component, mobile: Optional[str] = None,
              tablet: Optional[str] = None,
              desktop: Optional[str] = None):
    """Set responsive breakpoints."""
    component.style.responsive = {}
    if mobile:
        component.style.responsive["640"] = mobile
    if tablet:
        component.style.responsive["768"] = tablet
    if desktop:
        component.style.responsive["1024"] = desktop
    return component


def flex(component, direction: str = "row",
         justify: str = "flex-start",
         align: str = "stretch",
         gap: str = "0"):
    """Set flexbox layout."""
    component.style.display = "flex"
    component.style.flex_direction = direction
    component.style.justify_content = justify
    component.style.align_items = align
    component.style.gap = gap
    return component
