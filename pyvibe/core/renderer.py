"""
Renderer — mengubah komponen PyVibe menjadi HTML/CSS/JS output.

v2: CSS class-based rendering untuk performance yang lebih baik.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
import json
import os
import hashlib

from pyvibe.core.component import Component, Style


def tampil(*children: Union[Component, str], **kwargs) -> List[Component]:
    """
    Helper function untuk render komponen.
    Return list of components yang bisa di-return dari route handler.
    """
    components = []
    for child in children:
        if isinstance(child, str):
            from pyvibe.core.component import Teks
            components.append(Teks(child))
        elif isinstance(child, list):
            components.extend(child)
        elif isinstance(child, Component):
            components.append(child)
    return components


class Renderer:
    """Render komponen PyVibe ke HTML output dengan CSS class-based system."""

    def __init__(self, app=None):
        self.app = app
        self._css_classes: Dict[str, str] = {}  # class_name -> css

    def render(self, *children: Union[Component, str], **kwargs) -> str:
        """Render children ke HTML string."""
        html_parts = []
        for child in children:
            if isinstance(child, str):
                html_parts.append(child)
            elif isinstance(child, list):
                for item in child:
                    if isinstance(item, Component):
                        html_parts.append(item.render())
            elif isinstance(child, Component):
                html_parts.append(child.render())
        return "\n".join(html_parts)

    def render_page(self, *children: Union[Component, str], **kwargs) -> str:
        """Render full page dengan HTML skeleton."""
        config = self.app.config if self.app else {}
        title = kwargs.get("title", config.get("title", "PyVibe App"))
        description = kwargs.get("description", config.get("description", ""))
        primary = config.get("primary_color", "#7C3AED")
        secondary = config.get("secondary_color", "#06B6D4")

        body_content = self.render(*children)
        styles = self._collect_styles(*children)

        return f'''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <title>{title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
{self._get_design_system(primary, secondary)}
{styles}
    </style>
</head>
<body>
{body_content}
<script>
{self._get_runtime_js()}
</script>
</body>
</html>'''

    def render_body(self, *children: Union[Component, str]) -> str:
        return self.render(*children)

    def render_component(self, component: Component) -> str:
        return component.render()

    # ==================== Static Export ====================

    def build_static(self, output_dir: str = ".pyvibe"):
        """Build static HTML files untuk semua routes."""
        os.makedirs(output_dir, exist_ok=True)

        if not self.app or not self.app.routes:
            return

        for path, route in self.app.routes.items():
            try:
                result = route.handler()
                if result is None:
                    continue

                if isinstance(result, list):
                    body = self.render(*result)
                elif isinstance(result, Component):
                    body = result.render()
                else:
                    body = str(result)

                page = self._wrap_in_page(body)

                file_path = os.path.join(output_dir, "index.html")
                if path != "/":
                    file_path = os.path.join(output_dir, path.strip("/"), "index.html")

                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(page)

            except Exception as e:
                print(f"⚠️ Error rendering route {path}: {e}")

    def _wrap_in_page(self, body: str) -> str:
        config = self.app.config if self.app else {}
        primary = config.get("primary_color", "#7C3AED")
        secondary = config.get("secondary_color", "#06B6D4")
        return f'''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{config.get("title", "PyVibe App")}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
{self._get_design_system(primary, secondary)}
    </style>
</head>
<body>
{body}
<script>{self._get_runtime_js()}</script>
</body>
</html>'''

    # ==================== CSS Generation ====================

    def _collect_styles(self, *children) -> str:
        styles = []
        for child in children:
            if isinstance(child, Component):
                css = child.style.to_css()
                if css:
                    class_name = f"pv-{child.__class__.__name__.lower()}-{abs(hash(child.content + str(id(child)))) % 100000}"
                    child.class_names.append(class_name)
                    styles.append(f".{class_name} {{ {css} }}")
                for subchild in child.children:
                    sub_styles = self._collect_styles(subchild)
                    if sub_styles:
                        styles.append(sub_styles)
        return "\n".join(styles)

    def _get_design_system(self, primary: str = "#7C3AED", secondary: str = "#06B6D4") -> str:
        return f'''/* ========================================
   🐍 PyVibe Design System v2
   ======================================== */

/* --- Reset --- */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

/* --- CSS Variables --- */
:root {{
    --pv-primary: {primary};
    --pv-primary-light: {primary}22;
    --pv-primary-hover: {primary}dd;
    --pv-secondary: {secondary};
    --pv-success: #22C55E;
    --pv-success-light: #22C55E22;
    --pv-danger: #EF4444;
    --pv-danger-light: #EF444422;
    --pv-warning: #EAB308;
    --pv-warning-light: #EAB30822;
    --pv-info: #3B82F6;
    --pv-info-light: #3B82F622;

    --pv-white: #FFFFFF;
    --pv-black: #000000;
    --pv-gray-50: #F9FAFB;
    --pv-gray-100: #F3F4F6;
    --pv-gray-200: #E5E7EB;
    --pv-gray-300: #D1D5DB;
    --pv-gray-400: #9CA3AF;
    --pv-gray-500: #6B7280;
    --pv-gray-600: #4B5563;
    --pv-gray-700: #374151;
    --pv-gray-800: #1F2937;
    --pv-gray-900: #111827;

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

/* --- Base --- */
html {{ scroll-behavior: smooth; }}
body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    line-height: 1.6;
    color: var(--pv-gray-900);
    background: var(--pv-white);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}}

/* --- Typography --- */
h1 {{ font-size: 2.5rem; font-weight: 700; line-height: 1.2; letter-spacing: -0.025em; }}
h2 {{ font-size: 2rem; font-weight: 600; line-height: 1.3; letter-spacing: -0.02em; }}
h3 {{ font-size: 1.5rem; font-weight: 600; line-height: 1.4; }}
h4 {{ font-size: 1.25rem; font-weight: 500; line-height: 1.5; }}
h5 {{ font-size: 1rem; font-weight: 500; line-height: 1.5; }}
p {{ margin-bottom: 1rem; color: var(--pv-gray-600); }}
a {{ color: var(--pv-primary); text-decoration: none; transition: var(--pv-transition); }}
a:hover {{ opacity: 0.85; }}
strong {{ font-weight: 600; }}
small {{ font-size: 0.875rem; color: var(--pv-gray-500); }}

/* --- Layout Utilities --- */
.pv-flex {{ display: flex; }}
.pv-flex-col {{ display: flex; flex-direction: column; }}
.pv-flex-row {{ display: flex; flex-direction: row; }}
.pv-flex-wrap {{ flex-wrap: wrap; }}
.pv-flex-1 {{ flex: 1; }}
.pv-items-center {{ align-items: center; }}
.pv-items-start {{ align-items: flex-start; }}
.pv-items-end {{ align-items: flex-end; }}
.pv-justify-center {{ justify-content: center; }}
.pv-justify-between {{ justify-content: space-between; }}
.pv-justify-end {{ justify-content: flex-end; }}
.pv-gap-4 {{ gap: 4px; }}
.pv-gap-8 {{ gap: 8px; }}
.pv-gap-12 {{ gap: 12px; }}
.pv-gap-16 {{ gap: 16px; }}
.pv-gap-24 {{ gap: 24px; }}
.pv-gap-32 {{ gap: 32px; }}

.pv-grid {{ display: grid; }}
.pv-grid-2 {{ grid-template-columns: repeat(2, 1fr); }}
.pv-grid-3 {{ grid-template-columns: repeat(3, 1fr); }}
.pv-grid-4 {{ grid-template-columns: repeat(4, 1fr); }}
.pv-grid-auto {{ grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); }}

/* --- Text Utilities --- */
.pv-text-center {{ text-align: center; }}
.pv-text-left {{ text-align: left; }}
.pv-text-right {{ text-align: right; }}
.pv-text-primary {{ color: var(--pv-primary); }}
.pv-text-success {{ color: var(--pv-success); }}
.pv-text-danger {{ color: var(--pv-danger); }}
.pv-text-warning {{ color: var(--pv-warning); }}
.pv-text-gray {{ color: var(--pv-gray-500); }}
.pv-text-white {{ color: var(--pv-white); }}
.pv-text-sm {{ font-size: 0.875rem; }}
.pv-text-lg {{ font-size: 1.125rem; }}
.pv-text-xl {{ font-size: 1.25rem; }}
.pv-text-2xl {{ font-size: 1.5rem; }}
.pv-text-bold {{ font-weight: 600; }}
.pv-text-light {{ font-weight: 300; }}
.pv-text-uppercase {{ text-transform: uppercase; letter-spacing: 0.05em; }}

/* --- Spacing --- */
.pv-m-0 {{ margin: 0; }}
.pv-m-4 {{ margin: 4px; }}
.pv-m-8 {{ margin: 8px; }}
.pv-m-16 {{ margin: 16px; }}
.pv-m-24 {{ margin: 24px; }}
.pv-m-32 {{ margin: 32px; }}
.pv-mx-auto {{ margin-left: auto; margin-right: auto; }}
.pv-mt-4 {{ margin-top: 4px; }}
.pv-mt-8 {{ margin-top: 8px; }}
.pv-mt-16 {{ margin-top: 16px; }}
.pv-mt-24 {{ margin-top: 24px; }}
.pv-mt-32 {{ margin-top: 32px; }}
.pv-mb-4 {{ margin-bottom: 4px; }}
.pv-mb-8 {{ margin-bottom: 8px; }}
.pv-mb-16 {{ margin-bottom: 16px; }}
.pv-mb-24 {{ margin-bottom: 24px; }}
.pv-mb-32 {{ margin-bottom: 32px; }}
.pv-p-0 {{ padding: 0; }}
.pv-p-8 {{ padding: 8px; }}
.pv-p-12 {{ padding: 12px; }}
.pv-p-16 {{ padding: 16px; }}
.pv-p-24 {{ padding: 24px; }}
.pv-p-32 {{ padding: 32px; }}
.pv-p-48 {{ padding: 48px; }}
.pv-p-64 {{ padding: 64px; }}
.pv-px-16 {{ padding-left: 16px; padding-right: 16px; }}
.pv-px-32 {{ padding-left: 32px; padding-right: 32px; }}
.pv-py-16 {{ padding-top: 16px; padding-bottom: 16px; }}
.pv-py-32 {{ padding-top: 32px; padding-bottom: 32px; }}
.pv-py-64 {{ padding-top: 64px; padding-bottom: 64px; }}
.pv-py-96 {{ padding-top: 96px; padding-bottom: 96px; }}

/* --- Sizing --- */
.pv-w-full {{ width: 100%; }}
.pv-h-full {{ height: 100%; }}
.pv-min-h-screen {{ min-height: 100vh; }}
.pv-max-w-sm {{ max-width: 640px; }}
.pv-max-w-md {{ max-width: 768px; }}
.pv-max-w-lg {{ max-width: 1024px; }}
.pv-max-w-xl {{ max-width: 1280px; }}
.pv-max-w-2xl {{ max-width: 1536px; }}

/* --- Display --- */
.pv-hidden {{ display: none; }}
.pv-block {{ display: block; }}
.pv-inline {{ display: inline; }}
.pv-inline-block {{ display: inline-block; }}
.pv-relative {{ position: relative; }}
.pv-absolute {{ position: absolute; }}
.pv-fixed {{ position: fixed; }}
.pv-sticky {{ position: sticky; top: 0; }}
.pv-inset-0 {{ top: 0; right: 0; bottom: 0; left: 0; }}
.pv-z-10 {{ z-index: 10; }}
.pv-z-50 {{ z-index: 50; }}
.pv-z-100 {{ z-index: 100; }}
.pv-overflow-hidden {{ overflow: hidden; }}
.pv-overflow-auto {{ overflow: auto; }}
.pv-cursor-pointer {{ cursor: pointer; }}

/* --- Border --- */
.pv-border {{ border: 1px solid var(--pv-gray-200); }}
.pv-border-t {{ border-top: 1px solid var(--pv-gray-200); }}
.pv-border-b {{ border-bottom: 1px solid var(--pv-gray-200); }}
.pv-border-0 {{ border: none; }}
.pv-rounded {{ border-radius: var(--pv-radius); }}
.pv-rounded-lg {{ border-radius: var(--pv-radius-lg); }}
.pv-rounded-xl {{ border-radius: var(--pv-radius-xl); }}
.pv-rounded-full {{ border-radius: var(--pv-radius-full); }}

/* --- Background --- */
.pv-bg-white {{ background: var(--pv-white); }}
.pv-bg-gray {{ background: var(--pv-gray-50); }}
.pv-bg-dark {{ background: var(--pv-gray-900); color: var(--pv-white); }}
.pv-bg-primary {{ background: var(--pv-primary); color: var(--pv-white); }}
.pv-bg-success {{ background: var(--pv-success); color: var(--pv-white); }}
.pv-bg-danger {{ background: var(--pv-danger); color: var(--pv-white); }}

/* --- Shadow --- */
.pv-shadow-none {{ box-shadow: none; }}
.pv-shadow-xs {{ box-shadow: var(--pv-shadow-xs); }}
.pv-shadow-sm {{ box-shadow: var(--pv-shadow-sm); }}
.pv-shadow {{ box-shadow: var(--pv-shadow); }}
.pv-shadow-lg {{ box-shadow: var(--pv-shadow-lg); }}
.pv-shadow-xl {{ box-shadow: var(--pv-shadow-xl); }}

/* --- Buttons --- */
.pv-btn {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 10px 20px;
    font-size: 0.875rem;
    font-weight: 500;
    border: none;
    border-radius: var(--pv-radius);
    cursor: pointer;
    transition: var(--pv-transition);
    text-decoration: none;
    line-height: 1.5;
}}
.pv-btn:hover {{ transform: translateY(-1px); box-shadow: var(--pv-shadow); }}
.pv-btn:active {{ transform: translateY(0); }}
.pv-btn:disabled {{ opacity: 0.5; cursor: not-allowed; transform: none; }}
.pv-btn-primary {{ background: var(--pv-primary); color: white; }}
.pv-btn-primary:hover {{ background: var(--pv-primary-hover); }}
.pv-btn-secondary {{ background: var(--pv-gray-100); color: var(--pv-gray-700); border: 1px solid var(--pv-gray-200); }}
.pv-btn-secondary:hover {{ background: var(--pv-gray-200); }}
.pv-btn-success {{ background: var(--pv-success); color: white; }}
.pv-btn-danger {{ background: var(--pv-danger); color: white; }}
.pv-btn-warning {{ background: var(--pv-warning); color: var(--pv-gray-900); }}
.pv-btn-outline {{ background: transparent; border: 2px solid var(--pv-primary); color: var(--pv-primary); }}
.pv-btn-outline:hover {{ background: var(--pv-primary); color: white; }}
.pv-btn-ghost {{ background: transparent; color: var(--pv-gray-600); }}
.pv-btn-ghost:hover {{ background: var(--pv-gray-100); }}
.pv-btn-sm {{ padding: 6px 12px; font-size: 0.8125rem; }}
.pv-btn-lg {{ padding: 14px 28px; font-size: 1rem; }}
.pv-btn-block {{ width: 100%; }}

/* --- Inputs --- */
.pv-input, .pv-textarea, .pv-select {{
    width: 100%;
    padding: 10px 14px;
    font-size: 0.875rem;
    border: 1px solid var(--pv-gray-300);
    border-radius: var(--pv-radius);
    outline: none;
    transition: var(--pv-transition);
    font-family: inherit;
    background: var(--pv-white);
}}
.pv-input:focus, .pv-textarea:focus, .pv-select:focus {{
    border-color: var(--pv-primary);
    box-shadow: 0 0 0 3px var(--pv-primary-light);
}}
.pv-input:disabled, .pv-textarea:disabled {{ background: var(--pv-gray-50); cursor: not-allowed; }}
.pv-textarea {{ resize: vertical; min-height: 100px; }}
.pv-select {{ cursor: pointer; appearance: none; background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='%23343a40' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M2 5l6 6 6-6'/%3e%3c/svg%3e"); background-repeat: no-repeat; background-position: right 12px center; background-size: 12px; padding-right: 36px; }}
.pv-label {{ display: block; margin-bottom: 6px; font-size: 0.875rem; font-weight: 500; color: var(--pv-gray-700); }}
.pv-checkbox {{ width: 18px; height: 18px; accent-color: var(--pv-primary); cursor: pointer; }}
.pv-form-group {{ margin-bottom: 16px; }}
.pv-form-error {{ color: var(--pv-danger); font-size: 0.8125rem; margin-top: 4px; }}

/* --- Cards --- */
.pv-card {{
    background: var(--pv-white);
    border-radius: var(--pv-radius-lg);
    border: 1px solid var(--pv-gray-200);
    padding: 24px;
    transition: var(--pv-transition);
}}
.pv-card-hover:hover {{ box-shadow: var(--pv-shadow-lg); transform: translateY(-2px); }}
.pv-card-flat {{ border: none; box-shadow: none; }}
.pv-card-title {{ font-size: 1.125rem; font-weight: 600; margin-bottom: 12px; color: var(--pv-gray-900); }}

/* --- Table --- */
.pv-table {{ width: 100%; border-collapse: collapse; font-size: 0.875rem; }}
.pv-table th {{ padding: 12px 16px; text-align: left; font-weight: 600; color: var(--pv-gray-700); background: var(--pv-gray-50); border-bottom: 2px solid var(--pv-gray-200); }}
.pv-table td {{ padding: 12px 16px; border-bottom: 1px solid var(--pv-gray-100); color: var(--pv-gray-600); }}
.pv-table tr:hover td {{ background: var(--pv-gray-50); }}
.pv-table-striped tr:nth-child(even) td {{ background: var(--pv-gray-50); }}

/* --- Badge --- */
.pv-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: var(--pv-radius-full);
    font-size: 0.75rem;
    font-weight: 600;
}}
.pv-badge-primary {{ background: var(--pv-primary-light); color: var(--pv-primary); }}
.pv-badge-success {{ background: var(--pv-success-light); color: var(--pv-success); }}
.pv-badge-danger {{ background: var(--pv-danger-light); color: var(--pv-danger); }}
.pv-badge-warning {{ background: var(--pv-warning-light); color: var(--pv-warning); }}
.pv-badge-info {{ background: var(--pv-info-light); color: var(--pv-info); }}
.pv-badge-gray {{ background: var(--pv-gray-100); color: var(--pv-gray-600); }}

/* --- Alert --- */
.pv-alert {{ padding: 16px 20px; border-radius: var(--pv-radius-lg); margin-bottom: 16px; font-size: 0.875rem; display: flex; align-items: flex-start; gap: 12px; }}
.pv-alert-info {{ background: var(--pv-info-light); border-left: 4px solid var(--pv-info); color: var(--pv-gray-700); }}
.pv-alert-success {{ background: var(--pv-success-light); border-left: 4px solid var(--pv-success); color: var(--pv-gray-700); }}
.pv-alert-danger {{ background: var(--pv-danger-light); border-left: 4px solid var(--pv-danger); color: var(--pv-gray-700); }}
.pv-alert-warning {{ background: var(--pv-warning-light); border-left: 4px solid var(--pv-warning); color: var(--pv-gray-700); }}

/* --- Toast --- */
.pv-toast {{ position: fixed; top: 20px; right: 20px; padding: 12px 20px; border-radius: var(--pv-radius-lg); color: white; font-size: 0.875rem; z-index: 10000; animation: pvSlideDown 0.3s ease-out; box-shadow: var(--pv-shadow-lg); }}

/* --- Modal --- */
.pv-modal {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: none; align-items: center; justify-content: center; z-index: 1000; backdrop-filter: blur(4px); }}
.pv-modal.active {{ display: flex; }}
.pv-modal-content {{ background: var(--pv-white); border-radius: var(--pv-radius-xl); box-shadow: var(--pv-shadow-xl); width: 90%; max-width: 500px; max-height: 90vh; overflow: auto; animation: pvScale 0.2s ease-out; }}
.pv-modal-header {{ padding: 20px 24px; border-bottom: 1px solid var(--pv-gray-200); display: flex; align-items: center; justify-content: space-between; }}
.pv-modal-body {{ padding: 24px; }}
.pv-modal-footer {{ padding: 16px 24px; border-top: 1px solid var(--pv-gray-200); display: flex; justify-content: flex-end; gap: 12px; }}

/* --- Dropdown --- */
.pv-dropdown {{ position: relative; display: inline-block; }}
.pv-dropdown-menu {{ position: absolute; top: 100%; left: 0; min-width: 180px; background: var(--pv-white); border: 1px solid var(--pv-gray-200); border-radius: var(--pv-radius-lg); box-shadow: var(--pv-shadow-lg); z-index: 100; margin-top: 4px; display: none; }}
.pv-dropdown-menu.active {{ display: block; animation: pvFadeIn 0.15s ease-out; }}
.pv-dropdown-item {{ display: block; padding: 10px 16px; color: var(--pv-gray-700); text-decoration: none; font-size: 0.875rem; transition: var(--pv-transition); }}
.pv-dropdown-item:hover {{ background: var(--pv-gray-50); }}

/* --- Spinner --- */
.pv-spinner {{ width: 40px; height: 40px; border: 3px solid var(--pv-gray-200); border-top-color: var(--pv-primary); border-radius: 50%; animation: pvSpin 0.8s linear infinite; }}
.pv-spinner-sm {{ width: 24px; height: 24px; border-width: 2px; }}
.pv-spinner-lg {{ width: 64px; height: 64px; border-width: 4px; }}

/* --- Skeleton --- */
.pv-skeleton {{ background: linear-gradient(90deg, var(--pv-gray-200) 25%, var(--pv-gray-100) 50%, var(--pv-gray-200) 75%); background-size: 200% 100%; animation: pvPulse 1.5s infinite; border-radius: var(--pv-radius); }}

/* --- Accordion --- */
.pv-accordion {{ border: 1px solid var(--pv-gray-200); border-radius: var(--pv-radius-lg); overflow: hidden; }}
.pv-accordion-item {{ border-bottom: 1px solid var(--pv-gray-200); }}
.pv-accordion-item:last-child {{ border-bottom: none; }}
.pv-accordion-header {{ padding: 16px 20px; cursor: pointer; display: flex; align-items: center; justify-content: space-between; transition: var(--pv-transition); font-weight: 500; }}
.pv-accordion-header:hover {{ background: var(--pv-gray-50); }}
.pv-accordion-arrow {{ transition: transform 0.2s; font-size: 0.75rem; color: var(--pv-gray-400); }}
.pv-accordion-item.active .pv-accordion-arrow {{ transform: rotate(180deg); }}
.pv-accordion-content {{ padding: 0 20px 16px; display: none; }}
.pv-accordion-item.active .pv-accordion-content {{ display: block; animation: pvFadeIn 0.2s ease-out; }}

/* --- Tabs --- */
.pv-tabs {{ border-bottom: 1px solid var(--pv-gray-200); }}
.pv-tabs-nav {{ display: flex; gap: 0; }}
.pv-tab {{ padding: 12px 20px; cursor: pointer; font-size: 0.875rem; font-weight: 500; color: var(--pv-gray-500); border-bottom: 2px solid transparent; transition: var(--pv-transition); }}
.pv-tab:hover {{ color: var(--pv-gray-700); }}
.pv-tab.active {{ color: var(--pv-primary); border-bottom-color: var(--pv-primary); }}
.pv-tab-content {{ padding: 24px 0; display: none; }}
.pv-tab-content.active {{ display: block; }}

/* --- Progress --- */
.pv-progress {{ height: 8px; background: var(--pv-gray-200); border-radius: var(--pv-radius-full); overflow: hidden; }}
.pv-progress-bar {{ height: 100%; background: var(--pv-primary); border-radius: var(--pv-radius-full); transition: width 0.5s ease; }}

/* --- Avatar --- */
.pv-avatar {{ border-radius: 50%; object-fit: cover; border: 2px solid var(--pv-gray-200); }}

/* --- Gradient Backgrounds --- */
.pv-gradient-purple {{ background: linear-gradient(135deg, #7C3AED, #06B6D4); }}
.pv-gradient-blue {{ background: linear-gradient(135deg, #3B82F6, #06B6D4); }}
.pv-gradient-pink {{ background: linear-gradient(135deg, #EC4899, #7C3AED); }}
.pv-gradient-green {{ background: linear-gradient(135deg, #22C55E, #06B6D4); }}
.pv-gradient-orange {{ background: linear-gradient(135deg, #F97316, #EC4899); }}
.pv-gradient-dark {{ background: linear-gradient(135deg, #1F2937, #111827); }}

/* --- Animations --- */
@keyframes pvFadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
@keyframes pvFadeOut {{ from {{ opacity: 1; }} to {{ opacity: 0; }} }}
@keyframes pvSlideUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
@keyframes pvSlideDown {{ from {{ opacity: 0; transform: translateY(-20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
@keyframes pvSlideLeft {{ from {{ opacity: 0; transform: translateX(20px); }} to {{ opacity: 1; transform: translateX(0); }} }}
@keyframes pvSlideRight {{ from {{ opacity: 0; transform: translateX(-20px); }} to {{ opacity: 1; transform: translateX(0); }} }}
@keyframes pvBounce {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-10px); }} }}
@keyframes pvPulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.5; }} }}
@keyframes pvSpin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
@keyframes pvScale {{ from {{ transform: scale(0.95); opacity: 0; }} to {{ transform: scale(1); opacity: 1; }} }}

.pv-animate-fade-in {{ animation: pvFadeIn 0.3s ease-in; }}
.pv-animate-slide-up {{ animation: pvSlideUp 0.3s ease-out; }}
.pv-animate-slide-down {{ animation: pvSlideDown 0.3s ease-out; }}
.pv-animate-bounce {{ animation: pvBounce 0.5s ease-in-out; }}
.pv-animate-pulse {{ animation: pvPulse 2s infinite; }}
.pv-animate-spin {{ animation: pvSpin 1s linear infinite; }}
.pv-animate-scale {{ animation: pvScale 0.3s ease-out; }}

/* --- Responsive --- */
@media (max-width: 1024px) {{
    .pv-grid-4 {{ grid-template-columns: repeat(2, 1fr); }}
    .pv-lg\:hidden {{ display: none; }}
    .pv-lg\:block {{ display: block; }}
}}

@media (max-width: 768px) {{
    h1 {{ font-size: 1.75rem; }}
    h2 {{ font-size: 1.5rem; }}
    h3 {{ font-size: 1.25rem; }}
    .pv-grid-2, .pv-grid-3, .pv-grid-4 {{ grid-template-columns: 1fr; }}
    .pv-md\:hidden {{ display: none; }}
    .pv-md\:block {{ display: block; }}
    .pv-md\:flex {{ display: flex; }}
    .pv-p-64 {{ padding: 32px 16px; }}
    .pv-py-64 {{ padding-top: 32px; padding-bottom: 32px; }}
    .pv-py-96 {{ padding-top: 48px; padding-bottom: 48px; }}
}}

@media (max-width: 640px) {{
    .pv-sm\:hidden {{ display: none; }}
    .pv-sm\:block {{ display: block; }}
    .pv-sm\:flex {{ display: flex; }}
    .pv-px-32 {{ padding-left: 16px; padding-right: 16px; }}
}}
'''

    def _get_runtime_js(self) -> str:
        return '''
// 🐍 PyVibe Runtime v2
class PyVibe {
    constructor() {
        this.state = {};
        this.listeners = {};
        this.init();
    }

    init() {
        document.addEventListener('click', (e) => {
            // Handle dropdowns
            const dropdown = e.target.closest('.pv-dropdown');
            if (dropdown) {
                const menu = dropdown.querySelector('.pv-dropdown-menu');
                if (menu) {
                    document.querySelectorAll('.pv-dropdown-menu.active').forEach(m => {
                        if (m !== menu) m.classList.remove('active');
                    });
                    menu.classList.toggle('active');
                }
            } else {
                document.querySelectorAll('.pv-dropdown-menu.active').forEach(m => m.classList.remove('active'));
            }

            // Handle accordion
            const accordionHeader = e.target.closest('.pv-accordion-header');
            if (accordionHeader) {
                const item = accordionHeader.parentElement;
                const isActive = item.classList.contains('active');
                // Close all
                item.parentElement.querySelectorAll('.pv-accordion-item').forEach(i => i.classList.remove('active'));
                // Toggle current
                if (!isActive) item.classList.add('active');
            }

            // Handle tabs
            const tab = e.target.closest('.pv-tab');
            if (tab) {
                const tabsContainer = tab.closest('.pv-tabs');
                if (tabsContainer) {
                    tabsContainer.querySelectorAll('.pv-tab').forEach(t => t.classList.remove('active'));
                    tab.classList.add('active');
                    const target = tab.dataset.target;
                    if (target) {
                        tabsContainer.querySelectorAll('.pv-tab-content').forEach(c => c.classList.remove('active'));
                        const content = tabsContainer.querySelector(target);
                        if (content) content.classList.add('active');
                    }
                }
            }

            // Handle navigation
            const nav = e.target.closest('[data-navigate]');
            if (nav) {
                e.preventDefault();
                this.navigate(nav.dataset.navigate);
            }

            // Handle modal open
            const modalTrigger = e.target.closest('[data-modal-open]');
            if (modalTrigger) {
                e.preventDefault();
                this.openModal(modalTrigger.dataset.modalOpen);
            }

            // Handle modal close
            const modalClose = e.target.closest('[data-modal-close]');
            if (modalClose) {
                e.preventDefault();
                const modal = modalClose.closest('.pv-modal');
                if (modal) this.closeModal(modal.id);
            }

            // Close modal on backdrop click
            if (e.target.classList.contains('pv-modal')) {
                this.closeModal(e.target.id);
            }
        });

        // Handle form submissions
        document.addEventListener('submit', (e) => {
            const form = e.target;
            if (form.dataset.ajax === 'true') {
                e.preventDefault();
                this.handleFormSubmit(form);
            }
        });

        // Handle input bindings
        document.addEventListener('input', (e) => {
            const bind = e.target.dataset.bind;
            if (bind) {
                this.setState(bind, e.target.value);
            }
        });

        // Initial route
        this.resolveRoute();
    }

    // Navigation
    navigate(path) {
        window.history.pushState(null, '', path);
        this.resolveRoute();
    }

    resolveRoute() {
        const path = window.location.pathname;
        document.querySelectorAll('[data-route]').forEach(el => {
            el.style.display = el.dataset.route === path ? '' : 'none';
        });
    }

    // State management
    setState(key, value) {
        this.state[key] = value;
        this.notify(key, value);
    }

    getState(key) {
        return this.state[key];
    }

    notify(key, value) {
        document.querySelectorAll(`[data-bind="${key}"]`).forEach(el => {
            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.tagName === 'SELECT') {
                el.value = value;
            } else {
                el.textContent = value;
            }
        });
        // Notify watchers
        if (this.listeners[key]) {
            this.listeners[key].forEach(cb => cb(value));
        }
    }

    watch(key, callback) {
        if (!this.listeners[key]) this.listeners[key] = [];
        this.listeners[key].push(callback);
    }

    // UI utilities
    show(id) { const el = document.getElementById(id); if (el) el.classList.remove('pv-hidden'); }
    hide(id) { const el = document.getElementById(id); if (el) el.classList.add('pv-hidden'); }
    toggle(id) { const el = document.getElementById(id); if (el) el.classList.toggle('pv-hidden'); }

    // Modal
    openModal(id) {
        const modal = document.getElementById(id);
        if (modal) {
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    }

    closeModal(id) {
        const modal = document.getElementById(id);
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }
    }

    // Toast notification
    toast(message, type = 'info', duration = 3000) {
        const colors = { success: '#22C55E', danger: '#EF4444', warning: '#EAB308', info: '#3B82F6' };
        const icons = { success: '✅', danger: '❌', warning: '⚠️', info: 'ℹ️' };
        const toast = document.createElement('div');
        toast.className = 'pv-toast';
        toast.style.background = colors[type] || colors.info;
        toast.innerHTML = `<span>${icons[type] || ''} ${message}</span>`;
        document.body.appendChild(toast);
        setTimeout(() => {
            toast.style.animation = 'pvFadeOut 0.3s ease-out';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }

    // Form handling
    async handleFormSubmit(form) {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        const action = form.action || window.location.href;
        const method = form.method || 'POST';

        try {
            const response = await fetch(action, {
                method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });
            if (response.ok) {
                this.toast('Berhasil disimpan!', 'success');
                form.reset();
            } else {
                this.toast('Gagal menyimpan data.', 'danger');
            }
        } catch (err) {
            this.toast('Terjadi kesalahan.', 'danger');
        }
    }

    // Fetch data
    async fetch(url, options = {}) {
        try {
            const response = await fetch(url, options);
            return await response.json();
        } catch (err) {
            console.error('PyVibe fetch error:', err);
            return null;
        }
    }

    // DOM manipulation
    setHTML(id, html) {
        const el = document.getElementById(id);
        if (el) el.innerHTML = html;
    }

    setText(id, text) {
        const el = document.getElementById(id);
        if (el) el.textContent = text;
    }

    addClass(id, className) {
        const el = document.getElementById(id);
        if (el) el.classList.add(className);
    }

    removeClass(id, className) {
        const el = document.getElementById(id);
        if (el) el.classList.remove(className);
    }
}

// Utilities
function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func(...args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Initialize
const pv = new PyVibe();
'''
