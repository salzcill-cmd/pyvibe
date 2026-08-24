"""
🐍 PyVibe Bundler — Optimasi output untuk production.

"Kecil, cepat, hemat bandwidth."

Features:
- Bundler — Bundle & optimize HTML/CSS/JS
- CSSPurger — Remove unused CSS
- JSMinifier — Minify JavaScript
- HTMLMinifier — Minify HTML
- AssetOptimizer — Optimize images & assets
- BuildReport — Report build size & optimization

Usage:
    from pyvibe.bundler import Bundler, BuildReport

    bundler = Bundler()
    bundler.minify_html("dist/index.html")
    bundler.purge_css("dist/style.css", "dist/index.html")
    bundler.build("dist/")
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Set
from dataclasses import dataclass, field
import re
import os
import json
import hashlib


class HTMLMinifier:
    """Minify HTML content."""

    @staticmethod
    def minify(html: str, remove_comments: bool = True,
               remove_whitespace: bool = True) -> str:
        """Minify HTML string."""
        result = html

        if remove_comments:
            result = re.sub(r'<!--.*?-->', '', result, flags=re.DOTALL)

        if remove_whitespace:
            # Remove leading/trailing whitespace
            result = re.sub(r'>\s+<', '><', result)
            # Collapse multiple spaces
            result = re.sub(r'\s+', ' ', result)
            # Remove spaces around tags
            result = re.sub(r'\s*/>', '/>', result)

        return result.strip()


class CSSPurger:
    """Remove unused CSS rules."""

    @staticmethod
    def purge(css: str, html: str) -> str:
        """Remove CSS rules not used in HTML."""
        # Extract class names from HTML
        html_classes = set()
        for match in re.finditer(r'class="([^"]*)"', html):
            html_classes.update(match.group(1).split())
        for match in re.finditer(r"class='([^']*)'", html):
            html_classes.update(match.group(1).split())

        # Extract IDs from HTML
        html_ids = set()
        for match in re.finditer(r'id="([^"]*)"', html):
            html_ids.add(match.group(1))

        # Also check for tag names used
        html_tags = set()
        for match in re.finditer(r'<(\w+)', html):
            html_tags.add(match.group(1).lower())

        # Parse and filter CSS rules
        rules = CSSPurger._parse_rules(css)
        kept = []
        removed = 0

        for rule in rules:
            if rule.strip().startswith('@') or rule.strip().startswith(':'):
                # Keep at-rules and pseudo-class definitions
                kept.append(rule)
                continue

            # Check if any selector matches HTML
            if CSSPurger._is_used(rule, html_classes, html_ids, html_tags):
                kept.append(rule)
            else:
                removed += 1

        return "\n".join(kept)

    @staticmethod
    def _parse_rules(css: str) -> List[str]:
        """Parse CSS into rules."""
        rules = []
        current = ""
        depth = 0
        for char in css:
            if char == '{':
                depth += 1
                current += char
            elif char == '}':
                depth -= 1
                current += char
                if depth == 0:
                    rules.append(current.strip())
                    current = ""
            elif depth == 0 and char == ';':
                current += char
                if current.strip():
                    rules.append(current.strip())
                current = ""
            else:
                current += char
        if current.strip():
            rules.append(current.strip())
        return rules

    @staticmethod
    def _is_used(rule: str, classes: Set, ids: Set, tags: Set) -> bool:
        """Check if a CSS rule is used in HTML."""
        # Extract selectors from rule
        match = re.match(r'([^@{]+)\{', rule)
        if not match:
            return True

        selectors = match.group(1).split(',')
        for sel in selectors:
            sel = sel.strip()
            # Remove pseudo-classes/elements for base check
            base_sel = re.sub(r'::?\w+', '', sel)
            base_sel = re.sub(r'\[.*?\]', '', base_sel)
            base_sel = re.sub(r'[>+~]', ' ', base_sel).strip()

            parts = base_sel.split()
            if not parts:
                continue

            last = parts[-1].lstrip('.')
            if last.startswith('#'):
                if last[1:] in ids:
                    return True
            elif last.startswith('.'):
                if last[1:] in classes:
                    return True
            elif last in tags:
                return True
            # Keep universal selectors and complex ones
            if last in ('*', 'html', 'body', 'div', 'a', 'button', 'input'):
                return True

        return False


class JSMinifier:
    """Minify JavaScript content."""

    @staticmethod
    def minify(js: str) -> str:
        """Basic JS minification."""
        result = js
        # Remove single-line comments (but not URLs)
        result = re.sub(r'(?<!:)//[^\n]*', '', result)
        # Remove multi-line comments
        result = re.sub(r'/\*.*?\*/', '', result, flags=re.DOTALL)
        # Remove leading/trailing whitespace per line
        result = '\n'.join(line.strip() for line in result.split('\n'))
        # Collapse multiple newlines
        result = re.sub(r'\n\s*\n', '\n', result)
        # Remove spaces around operators
        result = re.sub(r'\s*([{};,:=+\-<>!&|])\s*', r'\1', result)
        return result.strip()


class Bundler:
    """
    Build bundler for optimizing PyVibe output.

    Usage:
        bundler = Bundler()
        bundler.minify_html("dist/index.html")
        bundler.build_report("dist/")
    """

    def __init__(self):
        self._html_minifier = HTMLMinifier()
        self._css_purger = CSSPurger()
        self._js_minifier = JSMinifier()

    def minify_html_file(self, filepath: str, output: Optional[str] = None):
        """Minify an HTML file."""
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        minified = self._html_minifier.minify(content)
        out = output or filepath
        with open(out, "w", encoding="utf-8") as f:
            f.write(minified)
        return len(content), len(minified)

    def purge_css_file(self, css_path: str, html_path: str,
                       output: Optional[str] = None):
        """Purge unused CSS."""
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
        purged = self._css_purger.purge(css, html)
        out = output or css_path
        with open(out, "w", encoding="utf-8") as f:
            f.write(purged)
        return len(css), len(purged)

    def minify_js_file(self, filepath: str, output: Optional[str] = None):
        """Minify a JS file."""
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        minified = self._js_minifier.minify(content)
        out = output or filepath
        with open(out, "w", encoding="utf-8") as f:
            f.write(minified)
        return len(content), len(minified)

    def build_report(self, directory: str) -> Dict:
        """Generate build report for directory."""
        report = {
            "files": {},
            "total_size": 0,
            "file_count": 0,
        }

        for root, dirs, files in os.walk(directory):
            for f in files:
                filepath = os.path.join(root, f)
                size = os.path.getsize(filepath)
                rel = os.path.relpath(filepath, directory)
                ext = os.path.splitext(f)[1].lower()

                report["files"][rel] = {
                    "size": size,
                    "size_human": self._human_size(size),
                    "type": ext,
                }
                report["total_size"] += size
                report["file_count"] += 1

        report["total_size_human"] = self._human_size(report["total_size"])
        return report

    def _human_size(self, size: int) -> str:
        """Convert bytes to human-readable."""
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"


# ==================== Asset Optimizer ====================

class AssetOptimizer:
    """
    Optimize static assets.

    Usage:
        opt = AssetOptimizer("dist/")
        opt.fingerprint("style.css")  # style.a1b2c3.css
        opt.generate_hash_map()  # asset-hashes.json
    """

    def __init__(self, base_dir: str = "dist"):
        self.base_dir = base_dir
        self._hashes: Dict[str, str] = {}

    def fingerprint(self, filename: str) -> str:
        """Add content hash to filename."""
        filepath = os.path.join(self.base_dir, filename)
        if not os.path.exists(filepath):
            return filename

        with open(filepath, "rb") as f:
            content_hash = hashlib.md5(f.read()).hexdigest()[:8]

        base, ext = os.path.splitext(filename)
        new_name = f"{base}.{content_hash}{ext}"
        self._hashes[filename] = new_name

        # Rename file
        new_path = os.path.join(self.base_dir, new_name)
        os.rename(filepath, new_path)

        return new_name

    def generate_hash_map(self) -> str:
        """Generate asset hash mapping JSON."""
        path = os.path.join(self.base_dir, "asset-hashes.json")
        with open(path, "w") as f:
            json.dump(self._hashes, f, indent=2)
        return path

    def get_hash(self, original: str) -> Optional[str]:
        """Get fingerprinted name for original filename."""
        return self._hashes.get(original)
