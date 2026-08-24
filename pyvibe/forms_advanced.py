"""
🐍 PyVibe Advanced Forms — Form builder yang lebih powerful.

"Multi-step, conditional, auto-save — form gak ribet."

Features:
- MultiStepForm — Multi-step wizard form
- ConditionalField — Show/hide fields based on conditions
- AutoSaveForm — Auto-save form data
- FormArray — Dynamic list of fields
- FormSection — Group related fields
- Advanced validation — Cross-field validation

Usage:
    from pyvibe.forms_advanced import MultiStepForm, ConditionalField

    # Multi-step form
    form = MultiStepForm("registration")
    form.step("Personal Info", [
        Field.text("nama", label="Nama", required=True),
        Field.email("email", label="Email"),
    ])
    form.step("Address", [
        Field.text("alamat", label="Alamat"),
        Field.text("kota", label="Kota"),
    ])
    form.step("Confirmation", [
        Field.checkbox("agree", label="Saya setuju"),
    ])
    html = form.render()

    # Conditional field
    html = ConditionalField(
        trigger_field="tipe",
        trigger_value="personal",
        children=[Field.text("nama_lengkap")],
        else_children=[Field.text("nama_perusahaan")],
    ).render()
"""

from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, Union
from dataclasses import dataclass, field
import json
import time
import hashlib


# ==================== Multi-Step Form ====================

class FormStep:
    """A single step in a multi-step form."""

    def __init__(self, title: str, description: str = ""):
        self.title = title
        self.description = description
        self.fields: List[Any] = []
        self.validation: List[Callable] = []

    def add_field(self, field) -> FormStep:
        """Add a field to this step."""
        self.fields.append(field)
        return self

    def add_fields(self, *fields) -> FormStep:
        """Add multiple fields."""
        self.fields.extend(fields)
        return self

    def validate(self, func: Callable) -> FormStep:
        """Add step validation."""
        self.validation.append(func)
        return self


class MultiStepForm:
    """
    Multi-step wizard form.

    Usage:
        form = MultiStepForm("registration")
        form.step("Info Personal", [...fields])
        form.step("Alamat", [...fields])
        form.step("Konfirmasi", [...fields])
        html = form.render()
    """

    def __init__(self, name: str, **kwargs):
        self.name = name
        self.steps: List[FormStep] = []
        self.current_step = 0
        self._submit_text = kwargs.get("submit_text", "Selesai")
        self._next_text = kwargs.get("next_text", "Selanjutnya")
        self._prev_text = kwargs.get("prev_text", "Sebelumnya")
        self._auto_save = kwargs.get("auto_save", False)
        self._animation = kwargs.get("animation", "fade")

    def step(self, title: str, fields: Optional[List] = None,
             description: str = "") -> MultiStepForm:
        """Add a step."""
        s = FormStep(title, description)
        if fields:
            s.fields = fields
        self.steps.append(s)
        return self

    def render(self) -> str:
        """Render multi-step form HTML."""
        if not self.steps:
            return "<div>No steps defined</div>"

        # Step indicators
        indicators = []
        for i, step in enumerate(self.steps):
            active = "active" if i == 0 else ""
            indicators.append(
                f'<div class="step-indicator" data-step="{i}">'
                f'<span class="step-number">{i + 1}</span>'
                f'<span class="step-title">{step.title}</span>'
                f'</div>'
            )

        # Step contents
        contents = []
        for i, step in enumerate(self.steps):
            fields_html = []
            for f in step.fields:
                if hasattr(f, "render"):
                    fields_html.append(f.render())
                else:
                    fields_html.append(str(f))

            desc = f'<p class="step-description">{step.description}</p>' if step.description else ""

            visibility = "block" if i == 0 else "none"
            contents.append(
                f'<div class="form-step" data-step="{i}" '
                f'style="display:{visibility};"> '
                f'<h3>{step.title}</h3>{desc}'
                f'{"".join(fields_html)}'
                f'</div>'
            )

        # Navigation buttons
        nav = f"""
<div class="form-navigation">
    <button type="button" class="prev-btn" onclick="prevStep()" style="display:none;">
        {self._prev_text}
    </button>
    <button type="button" class="next-btn" onclick="nextStep()">
        {self._next_text}
    </button>
    <button type="submit" class="submit-btn" style="display:none;">
        {self._submit_text}
    </button>
</div>"""

        # JavaScript
        total = len(self.steps)
        auto_save_js = ""
        if self._auto_save:
            auto_save_js = f"""
        // Auto-save to localStorage
        var formData = new FormData(form);
        var data = Object.fromEntries(formData);
        localStorage.setItem('form-{self.name}', JSON.stringify(data));"""

        js = f"""
<script>
(function() {{
    var currentStep = 0;
    var totalSteps = {total};
    var form = document.querySelector('.multi-step-form[data-form="{self.name}"]');
    var indicators = form.querySelectorAll('.step-indicator');
    var steps = form.querySelectorAll('.form-step');
    var prevBtn = form.querySelector('.prev-btn');
    var nextBtn = form.querySelector('.next-btn');
    var submitBtn = form.querySelector('.submit-btn');

    function showStep(n) {{
        steps.forEach(function(s, i) {{
            s.style.display = i === n ? 'block' : 'none';
        }});
        indicators.forEach(function(ind, i) {{
            ind.classList.toggle('active', i === n);
            ind.classList.toggle('completed', i < n);
        }});
        prevBtn.style.display = n > 0 ? 'inline-block' : 'none';
        nextBtn.style.display = n < totalSteps - 1 ? 'inline-block' : 'none';
        submitBtn.style.display = n === totalSteps - 1 ? 'inline-block' : 'none';
        currentStep = n;
    }}

    window.nextStep = function() {{
        if (currentStep < totalSteps - 1) showStep(currentStep + 1);
    }};
    window.prevStep = function() {{
        if (currentStep > 0) showStep(currentStep - 1);
    }};

    // Load auto-saved data
    var saved = localStorage.getItem('form-{self.name}');
    if (saved) {{
        try {{
            var data = JSON.parse(saved);
            Object.keys(data).forEach(function(key) {{
                var el = form.querySelector('[name="' + key + '"]');
                if (el) el.value = data[key];
            }});
        }} catch(e) {{}}
    }}

    // Auto-save on input
    form.addEventListener('input', function() {{ {auto_save_js} }});
}})();
</script>"""

        return f"""<div class="multi-step-form" data-form="{self.name}">
    <div class="step-indicators">
        {"".join(indicators)}
    </div>
    <form method="post">
        {"".join(contents)}
        {nav}
    </form>
    {js}
</div>"""


# ==================== Conditional Field ====================

class ConditionalField:
    """
    Show/hide field based on another field's value.

    Usage:
        cf = ConditionalField(
            trigger_field="tipe_akun",
            trigger_value="personal",
            children=[Field.text("nama_lengkap")],
            else_children=[Field.text("nama_perusahaan")],
        )
        html = cf.render()
    """

    def __init__(self, trigger_field: str, trigger_value: Any,
                 children: Optional[List] = None,
                 else_children: Optional[List] = None,
                 operator: str = "equals"):
        self.trigger_field = trigger_field
        self.trigger_value = trigger_value
        self.children = children or []
        self.else_children = else_children or []
        self.operator = operator
        self._id = f"cf-{hashlib.md5(trigger_field.encode()).hexdigest()[:8]}"

    def render(self) -> str:
        """Render conditional field group."""
        from pyvibe.core.renderer import Renderer
        renderer = Renderer()

        # Render children
        main_html = []
        for child in self.children:
            if hasattr(child, "render"):
                main_html.append(child.render())
            else:
                main_html.append(str(child))

        # Render else children
        else_html = []
        for child in self.else_children:
            if hasattr(child, "render"):
                else_html.append(child.render())
            else:
                else_html.append(str(child))

        # Build condition
        if self.operator == "equals":
            condition = f"el.value === '{self.trigger_value}'"
        elif self.operator == "not_equals":
            condition = f"el.value !== '{self.trigger_value}'"
        elif self.operator == "contains":
            condition = f"el.value.includes('{self.trigger_value}')"
        elif self.operator == "greater_than":
            condition = f"parseFloat(el.value) > {self.trigger_value}"
        elif self.operator == "less_than":
            condition = f"parseFloat(el.value) < {self.trigger_value}"
        else:
            condition = f"el.value === '{self.trigger_value}'"

        return f"""<div class="conditional-field" id="{self._id}">
    <div class="cf-main">{"".join(main_html)}</div>
    <div class="cf-else" style="display:none;">{"".join(else_html)}</div>
</div>
<script>
(function() {{
    var container = document.getElementById('{self._id}');
    var main = container.querySelector('.cf-main');
    var elseBlock = container.querySelector('.cf-else');
    var form = container.closest('form') || document;
    var el = form.querySelector('[name="{self.trigger_field}"]');

    function check() {{
        if (!el) return;
        var show = {condition};
        main.style.display = show ? '' : 'none';
        elseBlock.style.display = show ? 'none' : '';
    }}

    if (el) {{
        el.addEventListener('input', check);
        el.addEventListener('change', check);
        check();
    }}
}})();
</script>"""


# ==================== Form Array (Dynamic Fields) ====================

class FormArray:
    """
    Dynamic list of fields (add/remove).

    Usage:
        items = FormArray("items", fields=[
            Field.text("name", label="Item Name"),
            Field.number("qty", label="Quantity"),
        ])
        html = items.render()
    """

    def __init__(self, name: str, fields: Optional[List] = None,
                 min_items: int = 1, max_items: int = 10):
        self.name = name
        self.fields = fields or []
        self.min_items = min_items
        self.max_items = max_items
        self._id = f"fa-{hashlib.md5(name.encode()).hexdigest()[:8]}"

    def render(self) -> str:
        """Render dynamic field array."""
        from pyvibe.core.renderer import Renderer
        renderer = Renderer()

        # Render template for one item
        template_fields = []
        for f in self.fields:
            if hasattr(f, "render"):
                template_fields.append(f.render())
            else:
                template_fields.append(str(f))

        template_html = "".join(template_fields)

        return f"""<div class="form-array" id="{self._id}">
    <div class="array-items">
        <div class="array-item" data-index="0">
            {template_html}
        </div>
    </div>
    <button type="button" class="add-item-btn" onclick="addArrayItem('{self.name}')">
        + Tambah Item
    </button>
</div>
<script>
(function() {{
    var counts = {{'{self.name}': 1 }};

    window.addArrayItem = function(name) {{
        var container = document.querySelector('#{self._id} .array-items');
        var items = container.querySelectorAll('.array-item');
        var count = items.length;
        if (count >= {self.max_items}) return;

        var template = items[0].cloneNode(true);
        template.setAttribute('data-index', count);
        // Update field names
        template.querySelectorAll('[name]').forEach(function(el) {{
            el.name = el.name.replace(/\\[\\d+\\]/, '[' + count + ']');
            el.value = '';
        }});
        container.appendChild(template);
        counts[name] = count + 1;
    }};
}})();
</script>"""


# ==================== Auto-Save Form ====================

class AutoSaveForm:
    """
    Form that auto-saves to localStorage.

    Usage:
        form = AutoSaveForm("my-form", auto_save_key="draft")
        form.add_field(Field.text("nama"))
        form.add_field(Field.email("email"))
        html = form.render()
    """

    def __init__(self, name: str, auto_save_key: Optional[str] = None,
                 auto_save_delay: int = 1000):
        self.name = name
        self.auto_save_key = auto_save_key or f"form-{name}"
        self.auto_save_delay = auto_save_delay
        self.fields: List[Any] = []

    def add_field(self, field) -> AutoSaveForm:
        self.fields.append(field)
        return self

    def render(self) -> str:
        """Render auto-save form."""
        fields_html = []
        for f in self.fields:
            if hasattr(f, "render"):
                fields_html.append(f.render())
            else:
                fields_html.append(str(f))

        return f"""<form class="autosave-form" data-form="{self.name}"
      oninput="autoSaveForm('{self.name}', '{self.auto_save_key}')">
    {"".join(fields_html)}
    <button type="submit">Submit</button>
</form>
<script>
(function() {{
    // Load saved data
    var saved = localStorage.getItem('{self.auto_save_key}');
    if (saved) {{
        try {{
            var data = JSON.parse(saved);
            var form = document.querySelector('[data-form="{self.name}"]');
            Object.keys(data).forEach(function(key) {{
                var el = form.querySelector('[name="' + key + '"]');
                if (el) el.value = data[key];
            }});
        }} catch(e) {{}}
    }}

    var timers = {{}};
    window.autoSaveForm = function(formName, storageKey) {{
        clearTimeout(timers[formName]);
        timers[formName] = setTimeout(function() {{
            var form = document.querySelector('[data-form="' + formName + '"]');
            var formData = new FormData(form);
            var data = Object.fromEntries(formData);
            localStorage.setItem(storageKey, JSON.stringify(data));
            // Dispatch event
            form.dispatchEvent(new CustomEvent('pyvibe:auto-saved', {{ detail: data }}));
        }}, {self.auto_save_delay});
    }};
}})();
</script>"""
