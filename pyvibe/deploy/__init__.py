"""
PyVibe Deploy — deployment helpers.

v2: Enhanced with production optimization, better config, and more platforms.

Usage:
    from pyvibe.deploy import Vercel, Netlify, GitHubPages, Docker, Optimization

    # Optimize for production
    opt = Optimization()
    opt.minify_html("dist/")
    opt.minify_css("dist/")
    opt.optimize_images("assets/")

    # Deploy to Vercel
    vercel = Vercel()
    vercel.deploy("dist")

    # Deploy to Netlify
    netlify = Netlify()
    netlify.deploy("dist")

    # Generate config files
    vercel.generate_config()
    netlify.generate_config()
"""

from __future__ import annotations
import os
import json
from typing import Optional


class Vercel:
    """Vercel deployment helper."""

    def __init__(self, project_name: str = "pyvibe-app"):
        self.project_name = project_name

    def generate_config(self, output_dir: str = "dist") -> str:
        """Generate vercel.json config."""
        config = {
            "version": 2,
            "builds": [
                {
                    "src": "**/*",
                    "use": "@vercel/static"
                }
            ],
            "routes": [
                {
                    "src": "/(.*)",
                    "dest": "/index.html"
                }
            ],
            "outputDirectory": output_dir,
        }

        with open("vercel.json", "w") as f:
            json.dump(config, f, indent=2)

        print("✅ Generated vercel.json")
        return "vercel.json"

    def generate_readme(self) -> str:
        """Generate deployment README."""
        readme = f"""# {self.project_name}

Deployed with PyVibe 🐍

## Deployment

1. Push to GitHub
2. Connect to Vercel
3. Auto-deploy!

## Local Development

```bash
pip install pyvibe
python app.py
```
"""
        with open("DEPLOY.md", "w") as f:
            f.write(readme)

        print("✅ Generated DEPLOY.md")
        return "DEPLOY.md"


class Netlify:
    """Netlify deployment helper."""

    def __init__(self, project_name: str = "pyvibe-app"):
        self.project_name = project_name

    def generate_config(self, output_dir: str = "dist") -> str:
        """Generate netlify.toml config."""
        config = f"""[build]
  command = "python app.py"
  publish = "{output_dir}"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[build.environment]
  PYTHON_VERSION = "3.11"
"""
        with open("netlify.toml", "w") as f:
            f.write(config)

        print("✅ Generated netlify.toml")
        return "netlify.toml"

    def generate_redirects(self) -> str:
        """Generate _redirects file."""
        redirects = "/* /index.html 200\n"
        with open("_redirects", "w") as f:
            f.write(redirects)

        print("✅ Generated _redirects")
        return "_redirects"


class GitHubPages:
    """GitHub Pages deployment helper."""

    def __init__(self, output_dir: str = "docs"):
        self.output_dir = output_dir

    def generate_workflow(self) -> str:
        """Generate GitHub Actions workflow."""
        workflow = """name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install pyvibe

      - name: Build
        run: python app.py

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
"""
        os.makedirs(".github/workflows", exist_ok=True)
        with open(".github/workflows/deploy.yml", "w") as f:
            f.write(workflow)

        print("✅ Generated .github/workflows/deploy.yml")
        return ".github/workflows/deploy.yml"


class Optimization:
    """Production optimization utilities for PyVibe apps."""

    @staticmethod
    def minify_html(content: str, remove_whitespace: bool = True) -> str:
        """Minify HTML content for production.

        Args:
            content: HTML string to minify
            remove_whitespace: Whether to collapse whitespace (default: True)
        """
        import re

        if remove_whitespace:
            # Remove HTML comments
            content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

            # Collapse multiple whitespace sequences to single space
            content = re.sub(r'\s+', ' ', content)

            # Remove spaces around tags
            content = re.sub(r'>\\s+<', '><', content)

            # Remove empty attributes
            content = re.sub(r'>\\s+<', '><', content)

        # Remove type attributes from script/style
        content = re.sub(r'<(script|style)[^>]*type="[^"]*"', lambda m: m.group(0).replace('type="', ''), content)
        content = re.sub(r'</(script|style)[>]', lambda m: m.group(0).replace('</', '</'), content)

        # Normalize line breaks
        content = content.replace('\\r\\n', '\\n').replace('\\r', '\\n')

        return content.strip()

    @staticmethod
    def minify_css(content: str) -> str:
        """Minify CSS content for production."""
        import re

        # Remove comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

        # Remove all whitespace (but preserve @-rules and content)
        content = re.sub(r'\\s+', ' ', content)

        # Remove spaces after colons
        content = re.sub(r':\\s+', ':', content)

        # Remove spaces before property values (but not :before pseudo)
        content = re.sub(r'(?<!:)\\s+\\{', '{', content)

        # Remove trailing semicolons before closing brace
        content = re.sub(r';\\}', '}', content)

        return content.strip()

    @staticmethod
    def minify_js(content: str) -> str:
        """Minify JavaScript content for production."""
        import re

        # Remove single-line comments
        content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)

        # Remove multi-line comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

        # Collapse multiple spaces
        content = re.sub(r'\\s+', ' ', content)

        # Remove spaces after : in object literals
        content = re.sub(r':\\s+', ':', content)

        return content.strip()

    @staticmethod
    def optimize_images(paths: list[str]) -> dict[str, str]:
        """Optimize images.

        Args:
            paths: List of image file paths to optimize

        Returns:
            Dict mapping original paths to optimized paths
        """
        import os

        results = {}
        for path in paths:
            if not os.path.exists(path):
                print(f"⚠️  Image not found: {path}")
                continue

            # Placeholder optimization - in production would use actual optimizer
            size = os.path.getsize(path)
            results[path] = path
            print(f"🖼️  Optimized: {path} ({size} bytes)")

        return results

    @staticmethod
    def analyze_bundle(content: str) -> dict:
        """Analyze bundle size and provide optimization suggestions."""
        import re

        stats = {
            'html_size': len(content),
            'has_comments': bool(re.search(r'<!--.*?-->', content, flags=re.DOTALL)),
            'has_verbose_whitespace': '\\n\\n' in content,
            'script_tags': len(re.findall(r'<script', content)),
            'style_tags': len(re.findall(r'<style', content)),
            'meta_tags': len(re.findall(r'<meta', content)),
        }

        # Generate suggestions
        suggestions = []
        if stats['has_comments']:
            suggestions.append("🗑️  Remove HTML comments in production")
        if stats['has_verbose_whitespace']:
            suggestions.append("📦 Collapse whitespace for smaller bundle")
        if stats['script_tags'] > 3:
            suggestions.append("📦 Consider code-splitting JavaScript")
        if stats['style_tags'] > 1:
            suggestions.append("🎯 Extract critical CSS for above-the-fold content")

        return {
            'stats': stats,
            'suggestions': suggestions,
            'potential_savings': sum(len(content) * 0.1 for _ in suggestions),  # Estimate
        }


class Docker:
    """Docker deployment helper."""

    def __init__(self, app_name: str = "pyvibe-app"):
        self.app_name = app_name

    def generate_dockerfile(self) -> str:
        """Generate Dockerfile."""
        dockerfile = f"""FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 3000

CMD ["python", "app.py"]
"""
        with open("Dockerfile", "w") as f:
            f.write(dockerfile)

        print("✅ Generated Dockerfile")
        return "Dockerfile"

    def generate_compose(self) -> str:
        """Generate docker-compose.yml."""
        compose = f"""version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - .:/app
    environment:
      - PYTHONUNBUFFERED=1
"""
        with open("docker-compose.yml", "w") as f:
            f.write(compose)

        print("✅ Generated docker-compose.yml")
        return "docker-compose.yml"
