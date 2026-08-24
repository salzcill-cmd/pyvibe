"""
🐍 PyVibe Context — Context/Provider pattern untuk state sharing.

"State bisa dipakai dimana aja tanpa passing props."

Features:
- createContext — Create a context with default value
- Provider — Provide value to child components
- useContext — Consume context value
- ContextProvider — HTML-based provider with JS

Usage:
    from pyvibe.context import createContext, Provider, useContext

    # Create context
    ThemeContext = createContext("light")
    UserContext = createContext({"name": "Guest"})

    # Use provider
    html = Provider(ThemeContext, "dark",
        judul("Hello"),  # Can access theme via useContext
    )

    # Or using HTML provider
    html = ContextProvider(
        contexts={"theme": "dark", "lang": "id"},
        children=[judul("Hello")],
    )
"""

from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, TypeVar, Generic
from dataclasses import dataclass, field
import hashlib
import json


T = TypeVar("T")


class Context(Generic[T]):
    """
    A context object for sharing data through component tree.

    Usage:
        ThemeContext = createContext("light")
        print(ThemeContext.default_value)  # "light"
    """

    def __init__(self, default_value: T, name: str = ""):
        self.default_value = default_value
        self.name = name or f"ctx-{id(self)}"
        self._id = f"ctx-{hashlib.md5(self.name.encode()).hexdigest()[:8]}"
        self._providers: List[T] = []
        self._current: Optional[T] = None

    def get_current(self) -> T:
        """Get current context value."""
        if self._current is not None:
            return self._current
        if self._providers:
            return self._providers[-1]
        return self.default_value

    def set_current(self, value: T):
        """Set current context value."""
        self._current = value

    def push(self, value: T):
        """Push a new value (for nested providers)."""
        self._providers.append(value)

    def pop(self):
        """Pop the last value."""
        if self._providers:
            self._providers.pop()

    @property
    def id(self) -> str:
        return self._id

    def __repr__(self):
        return f"<Context name='{self.name}' value={self.get_current()}>"


def createContext(default_value: Any = None, name: str = "") -> Context:
    """
    Create a new context.

    Usage:
        ThemeContext = createContext("light")
        LangContext = createContext("id", name="language")
    """
    return Context(default_value, name)


def useContext(context: Context) -> Any:
    """
    Get current context value.

    Usage:
        theme = useContext(ThemeContext)
        print(theme)  # "light" or current provider value
    """
    return context.get_current()


class Provider:
    """
    Context provider wrapper component.

    Usage:
        html = Provider(ThemeContext, "dark",
            judul("Hello"),
            paragraf("World"),
        )
    """

    def __init__(self, context: Context, value: Any,
                 *children, **kwargs):
        self.context = context
        self.value = value
        self.children = list(children)
        self.attrs = kwargs

    def render(self) -> str:
        """Render provider with children."""
        self.context.push(self.value)
        from pyvibe.core.renderer import Renderer
        renderer = Renderer()
        child_htmls = []
        for child in self.children:
            if hasattr(child, "render"):
                child_htmls.append(child.render())
            elif isinstance(child, str):
                child_htmls.append(child)
            else:
                child_htmls.append(str(child))
        self.context.pop()
        return "\n".join(child_htmls)


class ContextProvider:
    """
    HTML-based context provider with JavaScript state management.

    Usage:
        html = ContextProvider(
            contexts={"theme": "dark", "lang": "id", "user": {"name": "Andi"}},
            children=[judul("Hello")],
        )
    """

    def __init__(self, contexts: Optional[Dict[str, Any]] = None,
                 children: Optional[List] = None):
        self.contexts = contexts or {}
        self.children = children or []

    def render(self) -> str:
        """Render HTML provider with inline JS state."""
        from pyvibe.core.renderer import Renderer

        # Render children
        renderer = Renderer()
        child_htmls = []
        for child in self.children:
            if hasattr(child, "render"):
                child_htmls.append(child.render())
            elif isinstance(child, str):
                child_htmls.append(child)
            else:
                child_htmls.append(str(child))

        children_html = "\n".join(child_htmls)

        # Generate context data
        ctx_json = json.dumps(self.contexts, ensure_ascii=False)
        ctx_id = f"ctx-{hashlib.md5(json.dumps(self.contexts, sort_keys=True).encode()).hexdigest()[:8]}"

        return f"""<div id="{ctx_id}" class="pyvibe-context-provider" data-context='{ctx_json}'>
{children_html}
</div>
<script>
(function() {{
    var el = document.getElementById('{ctx_id}');
    var ctx = JSON.parse(el.getAttribute('data-context') || '{{}}');
    window.__PYVIBE_CONTEXT__ = window.__PYVIBE_CONTEXT__ || {{}};
    Object.assign(window.__PYVIBE_CONTEXT__, ctx);

    // Custom event for context changes
    el.dispatchEvent(new CustomEvent('pyvibe:context-ready', {{ detail: ctx }}));
}})();
</script>"""


# ==================== Multi-Provider ====================

class MultiProvider:
    """
    Multiple context providers in one wrapper.

    Usage:
        html = MultiProvider({
            "theme": ("dark", ThemeContext),
            "lang": ("id", LangContext),
            "user": ({"name": "Andi"}, UserContext),
        },
            judul("Hello"),
        )
    """

    def __init__(self, providers: Optional[Dict[str, tuple]] = None,
                 children: Optional[List] = None):
        self.providers = providers or {}
        self.children = children or []

    def render(self) -> str:
        """Render nested providers."""
        # Nest providers from inside out
        result = self.children

        for name, (value, context) in self.providers.items():
            provider = Provider(context, value, *result)
            result = [provider]

        from pyvibe.core.renderer import Renderer
        renderer = Renderer()
        if result and hasattr(result[0], "render"):
            return result[0].render()
        return ""


# ==================== Built-in Contexts ====================

# Theme context
ThemeContext = createContext("default", name="theme")

# Language context
LangContext = createContext("id", name="language")

# User context
UserContext = createContext({"name": "Guest", "role": "user"}, name="user")

# Auth context
AuthContext = createContext({"authenticated": False, "token": None}, name="auth")

# App config context
ConfigContext = createContext({"debug": False, "version": "0.4.0"}, name="config")
