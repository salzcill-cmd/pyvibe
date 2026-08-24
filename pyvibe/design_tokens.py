"""
🐍 PyVibe Design Tokens — Sistem desain yang konsisten.

"Ganti warna sekali, berubah di semua tempat."

Features:
- DesignTokens — Centralized design values
- ColorPalette — Color system
- Typography — Font scale & weights
- Spacing — Spacing scale
- Shadows — Box shadow tokens
- Borders — Border tokens
- Breakpoints — Responsive breakpoints
- Export — Export to CSS, JSON, Tailwind config

Usage:
    from pyvibe.design_tokens import DesignTokens

    tokens = DesignTokens()
    tokens.colors.primary = "#7C3AED"
    tokens.colors.secondary = "#06B6D4"
    tokens.typography.font_family = "'Inter', sans-serif"

    # Generate CSS variables
    css = tokens.to_css_variables()

    # Generate JSON
    json_str = tokens.to_json()
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
import json


@dataclass
class ColorTokens:
    """Color design tokens."""
    primary: str = "#7C3AED"
    primary_light: str = "#A78BFA"
    primary_dark: str = "#5B21B6"
    secondary: str = "#06B6D4"
    secondary_light: str = "#67E8F9"
    secondary_dark: str = "#0891B2"
    accent: str = "#F59E0B"
    success: str = "#22C55E"
    warning: str = "#EAB308"
    error: str = "#EF4444"
    info: str = "#3B82F6"

    # Neutrals
    white: str = "#FFFFFF"
    black: str = "#000000"
    gray50: str = "#F9FAFB"
    gray100: str = "#F3F4F6"
    gray200: str = "#E5E7EB"
    gray300: str = "#D1D5DB"
    gray400: str = "#9CA3AF"
    gray500: str = "#6B7280"
    gray600: str = "#4B5563"
    gray700: str = "#374151"
    gray800: str = "#1F2937"
    gray900: str = "#111827"

    def to_dict(self) -> Dict[str, str]:
        return {k: v for k, v in self.__dict__.items()}


@dataclass
class TypographyTokens:
    """Typography design tokens."""
    font_family: str = "'Inter', -apple-system, BlinkMacSystemFont, sans-serif"
    font_family_mono: str = "'JetBrains Mono', 'Fira Code', monospace"

    # Font sizes
    xs: str = "0.75rem"
    sm: str = "0.875rem"
    base: str = "1rem"
    lg: str = "1.125rem"
    xl: str = "1.25rem"
    xxl: str = "1.5rem"
    xxxl: str = "1.875rem"
    xxxxl: str = "2.25rem"
    xxxxxl: str = "3rem"
    xxxxxxl: str = "3.75rem"

    # Font weights
    light: str = "300"
    regular: str = "400"
    medium: str = "500"
    semibold: str = "600"
    bold: str = "700"
    extrabold: str = "800"

    # Line heights
    tight: str = "1.25"
    snug: str = "1.375"
    normal: str = "1.5"
    relaxed: str = "1.625"
    loose: str = "2"

    def to_dict(self) -> Dict[str, str]:
        return {k: v for k, v in self.__dict__.items()}


@dataclass
class SpacingTokens:
    """Spacing design tokens."""
    px: str = "1px"
    s0: str = "0"
    s1: str = "0.25rem"
    s2: str = "0.5rem"
    s3: str = "0.75rem"
    s4: str = "1rem"
    s5: str = "1.25rem"
    s6: str = "1.5rem"
    s8: str = "2rem"
    s10: str = "2.5rem"
    s12: str = "3rem"
    s16: str = "4rem"
    s20: str = "5rem"
    s24: str = "6rem"
    s32: str = "8rem"
    s40: str = "10rem"
    s48: str = "12rem"
    s64: str = "16rem"

    def to_dict(self) -> Dict[str, str]:
        return {k: v for k, v in self.__dict__.items()}


@dataclass
class ShadowTokens:
    """Box shadow design tokens."""
    xs: str = "0 1px 2px rgba(0,0,0,0.05)"
    sm: str = "0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06)"
    md: str = "0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.06)"
    lg: str = "0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05)"
    xl: str = "0 20px 25px rgba(0,0,0,0.1), 0 10px 10px rgba(0,0,0,0.04)"
    xxl: str = "0 25px 50px rgba(0,0,0,0.25)"
    inner: str = "inset 0 2px 4px rgba(0,0,0,0.06)"
    none: str = "none"

    def to_dict(self) -> Dict[str, str]:
        return {k: v for k, v in self.__dict__.items()}


@dataclass
class BorderTokens:
    """Border design tokens."""
    none: str = "none"
    thin: str = "1px solid"
    medium: str = "2px solid"
    thick: str = "4px solid"

    # Radii
    radius_none: str = "0"
    radius_sm: str = "0.25rem"
    radius_md: str = "0.5rem"
    radius_lg: str = "0.75rem"
    radius_xl: str = "1rem"
    radius_2xl: str = "1.5rem"
    radius_full: str = "9999px"

    def to_dict(self) -> Dict[str, str]:
        return {k: v for k, v in self.__dict__.items()}


@dataclass
class BreakpointTokens:
    """Responsive breakpoint tokens."""
    mobile: str = "640px"
    tablet: str = "768px"
    desktop: str = "1024px"
    wide: str = "1280px"
    ultrawide: str = "1536px"

    def to_dict(self) -> Dict[str, str]:
        return {k: v for k, v in self.__dict__.items()}


@dataclass
class TransitionTokens:
    """Animation transition tokens."""
    fast: str = "150ms ease"
    normal: str = "200ms ease"
    slow: str = "300ms ease"
    slower: str = "500ms ease"

    def to_dict(self) -> Dict[str, str]:
        return {k: v for k, v in self.__dict__.items()}


@dataclass
class ZIndexTokens:
    """Z-index design tokens."""
    dropdown: str = "1000"
    sticky: str = "1020"
    fixed: str = "1030"
    modal_backdrop: str = "1040"
    modal: str = "1050"
    popover: str = "1060"
    tooltip: str = "1070"
    toast: str = "1080"

    def to_dict(self) -> Dict[str, str]:
        return {k: v for k, v in self.__dict__.items()}


class DesignTokens:
    """
    Centralized design tokens for PyVibe.

    Usage:
        tokens = DesignTokens()
        tokens.colors.primary = "#FF6B6B"
        css = tokens.to_css_variables()
    """

    def __init__(self):
        self.colors = ColorTokens()
        self.typography = TypographyTokens()
        self.spacing = SpacingTokens()
        self.shadows = ShadowTokens()
        self.borders = BorderTokens()
        self.breakpoints = BreakpointTokens()
        self.transitions = TransitionTokens()
        self.z_index = ZIndexTokens()

    def to_css_variables(self, prefix: str = "--pv") -> str:
        """Generate CSS custom properties."""
        lines = [":root {"]

        # Colors
        for k, v in self.colors.to_dict().items():
            lines.append(f"  {prefix}-color-{k}: {v};")

        # Typography
        for k, v in self.typography.to_dict().items():
            lines.append(f"  {prefix}-font-{k}: {v};")

        # Spacing
        for k, v in self.spacing.to_dict().items():
            lines.append(f"  {prefix}-space-{k}: {v};")

        # Shadows
        for k, v in self.shadows.to_dict().items():
            lines.append(f"  {prefix}-shadow-{k}: {v};")

        # Borders
        for k, v in self.borders.to_dict().items():
            lines.append(f"  {prefix}-border-{k}: {v};")

        # Breakpoints
        for k, v in self.breakpoints.to_dict().items():
            lines.append(f"  {prefix}-bp-{k}: {v};")

        # Transitions
        for k, v in self.transitions.to_dict().items():
            lines.append(f"  {prefix}-transition-{k}: {v};")

        # Z-Index
        for k, v in self.z_index.to_dict().items():
            lines.append(f"  {prefix}-z-{k}: {v};")

        lines.append("}")
        return "\n".join(lines)

    def to_json(self, indent: int = 2) -> str:
        """Generate JSON tokens."""
        return json.dumps({
            "colors": self.colors.to_dict(),
            "typography": self.typography.to_dict(),
            "spacing": self.spacing.to_dict(),
            "shadows": self.shadows.to_dict(),
            "borders": self.borders.to_dict(),
            "breakpoints": self.breakpoints.to_dict(),
            "transitions": self.transitions.to_dict(),
            "z_index": self.z_index.to_dict(),
        }, indent=indent, ensure_ascii=False)

    def to_tailwind_config(self) -> str:
        """Generate Tailwind CSS config object."""
        config = {
            "theme": {
                "extend": {
                    "colors": self.colors.to_dict(),
                    "fontSize": {
                        k: v for k, v in self.typography.to_dict().items()
                        if k in ["xs", "sm", "base", "lg", "xl", "2xl", "3xl", "4xl", "5xl"]
                    },
                    "spacing": self.spacing.to_dict(),
                    "boxShadow": self.shadows.to_dict(),
                    "borderRadius": {
                        k: v for k, v in self.borders.to_dict().items()
                        if k.startswith("radius_")
                    },
                    "screens": self.breakpoints.to_dict(),
                    "transitionDuration": {
                        k: v.split("ms")[0] + "ms"
                        for k, v in self.transitions.to_dict().items()
                    },
                    "zIndex": self.z_index.to_dict(),
                }
            }
        }
        return json.dumps(config, indent=2)

    def to_scss_variables(self, prefix: str = "pv") -> str:
        """Generate SCSS variables."""
        lines = []

        for k, v in self.colors.to_dict().items():
            lines.append(f"${prefix}-{k}: {v};")

        for k, v in self.spacing.to_dict().items():
            lines.append(f"${prefix}-space-{k}: {v};")

        for k, v in self.shadows.to_dict().items():
            lines.append(f"${prefix}-shadow-{k}: {v};")

        return "\n".join(lines)

    def apply_theme(self, theme_name: str):
        """Apply a built-in theme preset."""
        presets = {
            "dark": {
                "primary": "#818CF8", "primary_light": "#A5B4FC",
                "primary_dark": "#6366F1",
                "secondary": "#22D3EE",
                "gray50": "#18181B", "gray100": "#27272A",
                "gray800": "#F4F4F5", "gray900": "#FAFAFA",
            },
            "nature": {
                "primary": "#059669", "primary_light": "#34D399",
                "primary_dark": "#047857",
                "secondary": "#0D9488",
                "accent": "#F59E0B",
            },
            "sunset": {
                "primary": "#EA580C", "primary_light": "#FB923C",
                "primary_dark": "#C2410C",
                "secondary": "#DC2626",
                "accent": "#F59E0B",
            },
        }

        if theme_name in presets:
            for k, v in presets[theme_name].items():
                if hasattr(self.colors, k):
                    setattr(self.colors, k, v)
