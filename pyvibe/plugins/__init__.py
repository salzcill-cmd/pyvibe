"""
PyVibe Plugins — plugin system untuk extend framework.

Usage:
    from pyvibe.plugins import Plugin, PluginManager

    # Create a plugin
    class MyPlugin(Plugin):
        name = "My Plugin"
        version = "1.0.0"

        def setup(self, app):
            # Tambah route baru
            @app.route("/api/data")
            def api_data():
                return {"data": "hello"}

        def install(self):
            print("Plugin installed!")

    # Register plugin
    manager = PluginManager()
    manager.register(MyPlugin())
    manager.setup_all(app)
"""

from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional


class Plugin:
    """Base class untuk PyVibe plugins."""

    name: str = "Unnamed Plugin"
    version: str = "0.1.0"
    description: str = ""
    author: str = ""

    def setup(self, app: Any) -> None:
        """Setup plugin dengan app instance."""
        pass

    def install(self) -> None:
        """Install plugin."""
        pass

    def uninstall(self) -> None:
        """Uninstall plugin."""
        pass


class PluginManager:
    """Manager untuk plugins."""

    def __init__(self):
        self.plugins: List[Plugin] = []
        self._installed: Dict[str, bool] = {}

    def register(self, plugin: Plugin) -> None:
        """Register a plugin."""
        self.plugins.append(plugin)

    def unregister(self, plugin: Plugin) -> None:
        """Unregister a plugin."""
        self.plugins.remove(plugin)
        self._installed.pop(plugin.name, None)

    def setup_all(self, app: Any) -> None:
        """Setup semua registered plugins."""
        for plugin in self.plugins:
            if plugin.name not in self._installed:
                plugin.setup(app)
                self._installed[plugin.name] = True

    def get_plugin(self, name: str) -> Optional[Plugin]:
        """Get plugin by name."""
        for plugin in self.plugins:
            if plugin.name == name:
                return plugin
        return None

    def list_plugins(self) -> List[Dict[str, str]]:
        """List all plugins."""
        return [
            {
                "name": p.name,
                "version": p.version,
                "description": p.description,
                "installed": p.name in self._installed,
            }
            for p in self.plugins
        ]


# ==================== Built-in Plugins ====================

class DarkModePlugin(Plugin):
    """Plugin untuk dark mode toggle."""

    name = "Dark Mode"
    version = "1.0.0"
    description = "Toggle dark mode"

    def setup(self, app):
        pass

    def get_dark_mode_css(self) -> str:
        return """
/* Dark Mode */
.pv-dark-mode {
    --pv-bg: #111827;
    --pv-surface: #1F2937;
    --pv-text: #F9FAFB;
    --pv-text-dim: #9CA3AF;
    --pv-border: #374151;
}
.pv-dark-mode body {
    background: var(--pv-bg);
    color: var(--pv-text);
}
.pv-dark-mode .pv-card {
    background: var(--pv-surface);
    border-color: var(--pv-border);
}
.pv-dark-mode .pv-btn-secondary {
    background: var(--pv-surface);
    color: var(--pv-text);
    border-color: var(--pv-border);
}
.pv-dark-mode .pv-input,
.pv-dark-mode .pv-textarea,
.pv-dark-mode .pv-select {
    background: var(--pv-surface);
    color: var(--pv-text);
    border-color: var(--pv-border);
}
"""


class AnalyticsPlugin(Plugin):
    """Plugin untuk analytics tracking."""

    name = "Analytics"
    version = "1.0.0"
    description = "Basic analytics tracking"

    def __init__(self, tracking_id: str = ""):
        self.tracking_id = tracking_id

    def setup(self, app):
        pass

    def get_analytics_js(self) -> str:
        if not self.tracking_id:
            return ""
        return f"""
<!-- Analytics -->
<script>
(function() {{
    // Simple page view tracking
    const page = window.location.pathname;
    console.log('PyVibe Analytics: Page view -', page);
}})();
</script>
"""
