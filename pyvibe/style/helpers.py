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
