"""
🐍 PyVibe Image Optimizer — Optimasi gambar otomatis.

"Gambar cepat, SEO mantap, data hemat."

Features:
- OptimizedImage — Image component with lazy loading
- ResponsiveImage — Responsive images with srcset
- BlurPlaceholder — Blur placeholder while loading
- ImageGallery — Optimized image gallery
- AvatarOptimizer — Avatar with fallback
- generate_srcset — Generate responsive srcset

Usage:
    from pyvibe.image_optimizer import (
        OptimizedImage, ResponsiveImage, BlurPlaceholder,
        ImageGallery, AvatarOptimizer, generate_srcset,
    )

    # Lazy loaded image
    img = OptimizedImage("photo.jpg", alt="Photo")
    html = img.render()

    # Responsive image
    img = ResponsiveImage(
        "photo.jpg",
        alt="Photo",
        sizes=[(640, "small"), (1024, "medium"), (1920, "large")],
    )

    # Image gallery with lazy load
    gallery = ImageGallery(["img1.jpg", "img2.jpg", "img3.jpg"])
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import hashlib
import os
import html as html_module


# ==================== Optimized Image ====================

class OptimizedImage:
    """
    Image component with lazy loading and optimization.

    Usage:
        img = OptimizedImage("photo.jpg", alt="Beautiful photo")
        html = img.render()
    """

    def __init__(self, src: str, alt: str = "", width: int = 0,
                 height: int = 0, loading: str = "lazy",
                 decoding: str = "async", class_name: str = "",
                 placeholder: str = "", blur_data: str = "",
                 **kwargs):
        self.src = src
        self.alt = alt
        self.width = width
        self.height = height
        self.loading = loading
        self.decoding = decoding
        self.class_name = class_name
        self.placeholder = placeholder
        self.blur_data = blur_data
        self.attrs = kwargs
        self._id = f"img-{hashlib.md5(src.encode()).hexdigest()[:8]}"

    def render(self) -> str:
        """Render optimized image HTML."""
        attrs = [
            f'src="{html_module.escape(self.src)}"',
            f'alt="{html_module.escape(self.alt)}"',
            f'loading="{self.loading}"',
            f'decoding="{self.decoding}"',
        ]

        if self.width:
            attrs.append(f'width="{self.width}"')
        if self.height:
            attrs.append(f'height="{self.height}"')
        if self.class_name:
            attrs.append(f'class="{html_module.escape(self.class_name)}"')

        # Add custom attributes
        for key, value in self.attrs.items():
            attrs.append(f'{key}="{html_module.escape(str(value))}"')

        # Blur placeholder
        if self.blur_data:
            style = (
                f'background-image: url({self.blur_data}); '
                f'background-size: cover; filter: blur(10px); '
                f'transition: filter 0.3s;'
            )
            attrs.append(f'style="{style}"')
            attrs.append(
                f'onload="this.style.filter=\'none\'"'
            )

        attrs_str = " ".join(attrs)
        return f'<img {attrs_str} />'

    def render_picture(self, formats: Optional[List[str]] = None) -> str:
        """Render as <picture> element with format alternatives."""
        formats = formats or ["webp", "jpg"]
        base, ext = os.path.splitext(self.src)

        sources = []
        for fmt in formats:
            src = f"{base}.{fmt}"
            type_map = {"webp": "image/webp", "jpg": "image/jpeg",
                       "jpeg": "image/jpeg", "png": "image/png",
                       "avif": "image/avif"}
            mime = type_map.get(fmt, f"image/{fmt}")
            sources.append(f'<source srcset="{html_module.escape(src)}" type="{mime}">')

        img_html = self.render()
        return f"<picture>\n{''.join(sources)}\n{img_html}\n</picture>"


# ==================== Responsive Image ====================

class ResponsiveImage:
    """
    Responsive image with srcset and sizes.

    Usage:
        img = ResponsiveImage(
            "photo.jpg",
            alt="Photo",
            sizes=[(640, "100vw"), (1024, "50vw"), (1920, "33vw")],
        )
        html = img.render()
    """

    def __init__(self, src: str, alt: str = "",
                 sizes: Optional[List[Tuple[int, str]]] = None,
                 base_width: int = 1920, loading: str = "lazy"):
        self.src = src
        self.alt = alt
        self.sizes = sizes or [(640, "100vw"), (1024, "50vw"), (1920, "33vw")]
        self.base_width = base_width
        self.loading = loading

    def render(self) -> str:
        """Render responsive image."""
        base, ext = os.path.splitext(self.src)

        # Generate srcset
        srcset_parts = []
        for width, _ in self.sizes:
            srcset_parts.append(f"{base}-{width}w{ext} {width}w")

        # Generate sizes attribute
        sizes_parts = []
        for i, (width, size) in enumerate(self.sizes):
            if i == len(self.sizes) - 1:
                sizes_parts.append(size)
            else:
                sizes_parts.append(f"(max-width: {width}px) {size}")

        srcset = ", ".join(srcset_parts)
        sizes = ", ".join(sizes_parts)

        attrs = (
            f'src="{html_module.escape(self.src)}" '
            f'srcset="{html_module.escape(srcset)}" '
            f'sizes="{html_module.escape(sizes)}" '
            f'alt="{html_module.escape(self.alt)}" '
            f'loading="{self.loading}" decoding="async"'
        )

        return f"<img {attrs} />"


# ==================== Blur Placeholder ====================

class BlurPlaceholder:
    """
    Image with blur-up placeholder technique.

    Usage:
        bp = BlurPlaceholder(
            src="photo.jpg",
            alt="Photo",
            blur_data_url="data:image/jpeg;base64,...",
            width=800,
            height=600,
        )
        html = bp.render()
    """

    def __init__(self, src: str, alt: str = "", blur_data_url: str = "",
                 width: int = 0, height: int = 0):
        self.src = src
        self.alt = alt
        self.blur_data_url = blur_data_url
        self.width = width
        self.height = height
        self._id = f"blur-{hashlib.md5(src.encode()).hexdigest()[:8]}"

    def render(self) -> str:
        """Render blur placeholder image."""
        width_attr = f' width="{self.width}"' if self.width else ""
        height_attr = f' height="{self.height}"' if self.height else ""

        placeholder_style = ""
        if self.blur_data_url:
            placeholder_style = (
                f' style="background-image: url({self.blur_data_url}); '
                f'background-size: cover; filter: blur(20px); '
                f'transition: filter 0.5s ease;"'
            )

        return f"""<div class="blur-placeholder" style="position:relative;overflow:hidden;">
    <img
        src="{html_module.escape(self.src)}"
        alt="{html_module.escape(self.alt)}"{width_attr}{height_attr}
        loading="lazy" decoding="async"{placeholder_style}
        onload="this.style.filter='none';this.parentElement.classList.add('loaded')"
    />
</div>"""


# ==================== Image Gallery ====================

class ImageGallery:
    """
    Optimized image gallery with lazy loading.

    Usage:
        gallery = ImageGallery(
            images=[
                {"src": "img1.jpg", "alt": "Photo 1"},
                {"src": "img2.jpg", "alt": "Photo 2"},
            ],
            columns=3,
            gap="8px",
            lightbox=True,
        )
        html = gallery.render()
    """

    def __init__(self, images: Optional[List] = None, columns: int = 3,
                 gap: str = "8px", lightbox: bool = True,
                 thumbnail_size: str = "100%"):
        self.images = images or []
        self.columns = columns
        self.gap = gap
        self.lightbox = lightbox
        self.thumbnail_size = thumbnail_size

    def render(self) -> str:
        """Render image gallery."""
        items = []
        for i, img in enumerate(self.images):
            if isinstance(img, str):
                src, alt = img, f"Gallery {i + 1}"
            elif isinstance(img, dict):
                src = img.get("src", "")
                alt = img.get("alt", f"Gallery {i + 1}")
            else:
                continue

            opt = OptimizedImage(src, alt, loading="lazy")
            img_html = opt.render()

            if self.lightbox:
                items.append(
                    f'<div class="gallery-item" style="cursor:pointer;" '
                    f'onclick="openLightbox(\'{html_module.escape(src)}\')">'
                    f'{img_html}</div>'
                )
            else:
                items.append(f'<div class="gallery-item">{img_html}</div>')

        gallery_html = "\n".join(items)
        lightbox_js = ""
        if self.lightbox:
            lightbox_js = """
<script>
function openLightbox(src) {
    var lb = document.createElement('div');
    lb.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.9);display:flex;align-items:center;justify-content:center;z-index:9999;cursor:pointer;';
    lb.onclick = function() { lb.remove(); };
    lb.innerHTML = '<img src="' + src + '" style="max-width:90vw;max-height:90vh;border-radius:8px;">';
    document.body.appendChild(lb);
}
</script>"""

        return f"""<div class="image-gallery" style="display:grid;grid-template-columns:repeat({self.columns},1fr);gap:{self.gap};">
{gallery_html}
</div>
{lightbox_js}"""


# ==================== Avatar Optimizer ====================

class AvatarOptimizer:
    """
    Optimized avatar with initials fallback.

    Usage:
        avatar = AvatarOptimizer(
            src="user-photo.jpg",
            name="Andi Pratama",
            size="48px",
            fallback_color="#7C3AED",
        )
        html = avatar.render()
    """

    def __init__(self, src: str = "", name: str = "",
                 size: str = "48px", fallback_color: str = "#7C3AED",
                 border: str = ""):
        self.src = src
        self.name = name
        self.size = size
        self.fallback_color = fallback_color
        self.border = border

    def _get_initials(self) -> str:
        """Get initials from name."""
        parts = self.name.strip().split()
        if len(parts) >= 2:
            return (parts[0][0] + parts[1][0]).upper()
        elif parts:
            return parts[0][0].upper()
        return "?"

    def render(self) -> str:
        """Render optimized avatar."""
        initials = self._get_initials()
        border_style = f"border: {self.border};" if self.border else ""

        if self.src:
            return (
                f'<div style="width:{self.size};height:{self.size};'
                f'border-radius:50%;overflow:hidden;flex-shrink:0;{border_style}">'
                f'<img src="{html_module.escape(self.src)}" '
                f'alt="{html_module.escape(self.name)}" '
                f'loading="lazy" decoding="async" '
                f'style="width:100%;height:100%;object-fit:cover;" />'
                f'</div>'
            )
        else:
            return (
                f'<div style="width:{self.size};height:{self.size};'
                f'border-radius:50%;background:{self.fallback_color};'
                f'color:white;display:flex;align-items:center;justify-content:center;'
                f'font-weight:600;font-size:calc({self.size} * 0.4);flex-shrink:0;{border_style}">'
                f'{initials}</div>'
            )


# ==================== Utility ====================

def generate_srcset(src: str, widths: List[int],
                    base_dir: str = "") -> str:
    """
    Generate srcset attribute string.

    Usage:
        srcset = generate_srcset("photo.jpg", [640, 1024, 1920])
        # Returns: "photo-640w.jpg 640w, photo-1024w.jpg 1024w, photo-1920w.jpg 1920w"
    """
    base, ext = os.path.splitext(src)
    parts = []
    for w in widths:
        if base_dir:
            path = f"{base_dir}/{base}-{w}w{ext}"
        else:
            path = f"{base}-{w}w{ext}"
        parts.append(f"{path} {w}w")
    return ", ".join(parts)


def lazy_image(src: str, alt: str = "", **kwargs) -> OptimizedImage:
    """Shorthand for creating a lazy-loaded image."""
    return OptimizedImage(src, alt, loading="lazy", **kwargs)


def avatar(src: str = "", name: str = "", size: str = "48px", **kwargs) -> AvatarOptimizer:
    """Shorthand for creating an optimized avatar."""
    return AvatarOptimizer(src=src, name=name, size=size, **kwargs)
