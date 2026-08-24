"""
🐍 PyVibe Web Components — Export komponen sebagai Web Components.

"Komponen PyVibe bisa dipakai di framework apapun."

Features:
- web_component — Decorator to create web components
- register_all — Register all PyVibe components
- WebComponentRegistry — Manage registered components

Usage:
    from pyvibe.webcomponents import web_component, register_all

    # Create web component from PyVibe component
    @web_component("pv-button")
    def pv_button(name="Klik", color="#7C3AED"):
        return tombol(name, warna=color)

    # Register all built-in components
    register_all()
"""

from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
import hashlib


class WebComponentRegistry:
    """Registry for PyVibe web components."""

    def __init__(self):
        self._components: Dict[str, Dict] = {}

    def register(self, tag: str, render_fn: Callable,
                 observed_attrs: Optional[List[str]] = None,
                 shadow_dom: bool = False):
        """Register a component."""
        self._components[tag] = {
            "render": render_fn,
            "observed_attrs": observed_attrs or [],
            "shadow_dom": shadow_dom,
        }

    def get(self, tag: str) -> Optional[Dict]:
        return self._components.get(tag)

    @property
    def tags(self) -> List[str]:
        return list(self._components.keys())

    def generate_js(self) -> str:
        """Generate JavaScript for all registered components."""
        classes = []
        for tag, config in self._components.items():
            class_name = tag.replace("-", "_").title().replace("_", "")
            attrs = config["observed_attrs"]
            shadow = "this.attachShadow({mode:'open'})" if config["shadow_dom"] else "this"

            attrs_observed = f"static get observedAttributes() {{ return {attrs}; }}" if attrs else ""

            classes.append(f"""
class {class_name} extends HTMLElement {{
    {attrs_observed}
    connectedCallback() {{
        this.render();
    }}
    attributeChangedCallback() {{
        this.render();
    }}
    render() {{
        const root = {shadow};
        root.innerHTML = this.getAttribute('content') || '';
    }}
}}
customElements.define('{tag}', {class_name});
""")

        return "\n".join(classes)


# Global registry
_registry = WebComponentRegistry()


def web_component(tag: str, observed_attrs: Optional[List[str]] = None,
                  shadow_dom: bool = False):
    """
    Decorator to create a web component from a PyVibe function.

    Usage:
        @web_component("pv-card")
        def pv_card(title="", body=""):
            return kartu(judul_kartu(title), paragraf(body))
    """
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Register
        _registry.register(
            tag=tag,
            render_fn=func,
            observed_attrs=observed_attrs or [],
            shadow_dom=shadow_dom,
        )

        wrapper._web_component_tag = tag
        wrapper._render = func
        return wrapper

    return decorator


def register_all():
    """Register all common PyVibe components as web components."""
    from pyvibe.components.basic import judul, paragraf, badge
    from pyvibe.components.input import tombol
    from pyvibe.components.layout import kartu

    @web_component("pv-heading")
    def pv_heading(text="", level="1"):
        return judul(text, level=int(level))

    @web_component("pv-paragraph")
    def pv_paragraph(text=""):
        return paragraf(text)

    @web_component("pv-button")
    def pv_button(label="Klik", color="#7C3AED"):
        return tombol(label, warna=color)

    @web_component("pv-badge", observed_attrs=["text", "color"])
    def pv_badge(text="", color="ungu"):
        return badge(text)

    @web_component("pv-card", shadow_dom=True)
    def pv_card(title="", body=""):
        from pyvibe.components.layout import judul_kartu
        return kartu(judul_kartu(title), paragraf(body))


def get_registry() -> WebComponentRegistry:
    """Get the global web component registry."""
    return _registry


def generate_web_components_script() -> str:
    """Generate JavaScript for all registered web components."""
    return f"""<script>
// PyVibe Web Components
{_registry.generate_js()}
</script>"""
