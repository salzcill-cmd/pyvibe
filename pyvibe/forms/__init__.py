"""
PyVibe Forms — comprehensive form handling and validation.

Usage:
    from pyvibe.forms import Form, Field, Validators

    # Create form
    form = Form("register")
    form.add_field("nama", Field.text(required=True, min_length=2))
    form.add_field("email", Field.email(required=True))
    form.add_field("password", Field.password(required=True, min_length=8))
    form.add_field("agree", Field.checkbox(required=True))

    # Validate
    errors = form.validate({"nama": "Andi", "email": "andi@test.com", "password": "12345678", "agree": True})

    # Render form
    html = form.render()
"""

from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, Union
from dataclasses import dataclass, field
from pyvibe.core.component import Component
from pyvibe.components.basic import judul, paragraf, badge
from pyvibe.components.input import (
    input_teks, input_angka, input_email, input_sandi,
    textarea, centang, pilihan, tombol, tombol_kirim,
)


# ==================== Validators ====================

class Validators:
    """Collection of form validators."""

    @staticmethod
    def required(value: Any) -> Optional[str]:
        """Check if value is not empty."""
        if value is None or value == "" or value is False:
            return "Field ini wajib diisi"
        return None

    @staticmethod
    def min_length(min_len: int):
        """Check minimum length."""
        def validator(value: Any) -> Optional[str]:
            if isinstance(value, str) and len(value) < min_len:
                return f"Minimal {min_len} karakter"
            return None
        return validator

    @staticmethod
    def max_length(max_len: int):
        """Check maximum length."""
        def validator(value: Any) -> Optional[str]:
            if isinstance(value, str) and len(value) > max_len:
                return f"Maksimal {max_len} karakter"
            return None
        return validator

    @staticmethod
    def email(value: Any) -> Optional[str]:
        """Validate email format."""
        import re
        if isinstance(value, str):
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, value):
                return "Format email tidak valid"
        return None

    @staticmethod
    def url(value: Any) -> Optional[str]:
        """Validate URL format."""
        import re
        if isinstance(value, str):
            pattern = r'^https?://[^\s/$.?#].[^\s]*$'
            if not re.match(pattern, value):
                return "Format URL tidak valid"
        return None

    @staticmethod
    def phone(value: Any) -> Optional[str]:
        """Validate phone number."""
        import re
        if isinstance(value, str):
            pattern = r'^[+]?[0-9]{10,15}$'
            if not re.match(pattern, value.replace(" ", "").replace("-", "")):
                return "Format nomor telepon tidak valid"
        return None

    @staticmethod
    def numeric(value: Any) -> Optional[str]:
        """Check if value is numeric."""
        if value is not None and value != "":
            try:
                float(value)
                return None
            except (ValueError, TypeError):
                return "Harus berupa angka"
        return None

    @staticmethod
    def min_value(min_val: float):
        """Check minimum value."""
        def validator(value: Any) -> Optional[str]:
            try:
                if float(value) < min_val:
                    return f"Minimal {min_val}"
            except (ValueError, TypeError):
                pass
            return None
        return validator

    @staticmethod
    def max_value(max_val: float):
        """Check maximum value."""
        def validator(value: Any) -> Optional[str]:
            try:
                if float(value) > max_val:
                    return f"Maksimal {max_val}"
            except (ValueError, TypeError):
                pass
            return None
        return validator

    @staticmethod
    def one_of(options: List[Any]):
        """Check if value is in allowed options."""
        def validator(value: Any) -> Optional[str]:
            if value not in options:
                return f"Harus salah satu dari: {', '.join(str(o) for o in options)}"
            return None
        return validator

    @staticmethod
    def matches(field_name: str):
        """Check if value matches another field."""
        def validator(value: Any, data: Optional[Dict] = None) -> Optional[str]:
            if data and data.get(field_name) != value:
                return f"Tidak cocok dengan {field_name}"
            return None
        return validator

    @staticmethod
    def pattern(regex: str, message: str = "Format tidak valid"):
        """Check regex pattern."""
        import re
        def validator(value: Any) -> Optional[str]:
            if isinstance(value, str) and not re.match(regex, value):
                return message
            return None
        return validator

    @staticmethod
    def custom(func: Callable[[Any], Optional[str]]):
        """Custom validator function."""
        return func


# ==================== Field ====================

@dataclass
class Field:
    """Form field definition."""

    name: str = ""
    field_type: str = "text"
    label: str = ""
    placeholder: str = ""
    default: Any = ""
    required: bool = False
    disabled: bool = False
    validators: List[Callable] = field(default_factory=list)
    options: Optional[List[str]] = None
    min_val: Optional[int] = None
    max_val: Optional[int] = None
    rows: int = 4
    accept: str = "*"
    multiple: bool = False
    help_text: str = ""
    css_class: str = ""

    @classmethod
    def text(cls, name: str = "", **kwargs) -> "Field":
        """Create text field."""
        return cls(name=name, field_type="text", **kwargs)

    @classmethod
    def number(cls, name: str = "", **kwargs) -> "Field":
        """Create number field."""
        return cls(name=name, field_type="number", **kwargs)

    @classmethod
    def email(cls, name: str = "", **kwargs) -> "Field":
        """Create email field."""
        return cls(name=name, field_type="email", **kwargs)

    @classmethod
    def password(cls, name: str = "", **kwargs) -> "Field":
        """Create password field."""
        return cls(name=name, field_type="password", **kwargs)

    @classmethod
    def textarea(cls, name: str = "", **kwargs) -> "Field":
        """Create textarea field."""
        return cls(name=name, field_type="textarea", **kwargs)

    @classmethod
    def checkbox(cls, name: str = "", **kwargs) -> "Field":
        """Create checkbox field."""
        return cls(name=name, field_type="checkbox", **kwargs)

    @classmethod
    def select(cls, options: List[str], name: str = "", **kwargs) -> "Field":
        """Create select field."""
        return cls(name=name, field_type="select", options=options, **kwargs)

    @classmethod
    def radio(cls, options: List[str], name: str = "", **kwargs) -> "Field":
        """Create radio field."""
        return cls(name=name, field_type="radio", options=options, **kwargs)

    @classmethod
    def file(cls, name: str = "", **kwargs) -> "Field":
        """Create file upload field."""
        return cls(name=name, field_type="file", **kwargs)

    def render(self, value: Any = None, error: Optional[str] = None) -> Component:
        """Render field to component."""
        wrapper = Component(tag="div")
        wrapper.class_names.extend([f"pv-form-group {self.css_class}".strip()])

        # Label
        if self.label:
            lbl = Component(tag="label", content=self.label)
            lbl.class_names.append("pv-label")
            if self.required:
                req = Component(tag="span", content=" *")
                req.style.color = "#EF4444"
                lbl.children.append(req)
            wrapper.children.append(lbl)

        # Field
        display_value = value if value is not None else self.default

        if self.field_type == "text":
            inp = input_teks(
                placeholder=self.placeholder,
                name=self.name,
                value=str(display_value),
                required=self.required,
                disabled=self.disabled,
            )
        elif self.field_type == "number":
            inp = input_angka(
                placeholder=self.placeholder,
                name=self.name,
                value=str(display_value),
                min_val=self.min_val,
                max_val=self.max_val,
                required=self.required,
            )
        elif self.field_type == "email":
            inp = input_email(
                placeholder=self.placeholder,
                name=self.name,
                required=self.required,
            )
        elif self.field_type == "password":
            inp = input_sandi(
                placeholder=self.placeholder,
                name=self.name,
                required=self.required,
            )
        elif self.field_type == "textarea":
            inp = textarea(
                placeholder=self.placeholder,
                name=self.name,
                rows=self.rows,
                required=self.required,
            )
        elif self.field_type == "checkbox":
            inp = centang(self.label, name=self.name, checked=bool(display_value))
        elif self.field_type == "select":
            inp = pilihan(
                label="",
                options=self.options or [],
                name=self.name,
                placeholder=self.placeholder or "Pilih salah satu...",
            )
        elif self.field_type == "radio":
            inp = Component(tag="div")
            for opt in (self.options or []):
                radio = Component(tag="label")
                radio.class_names.extend(["pv-flex", "pv-items-center", "pv-gap-8", "pv-mb-8"])
                radio_input = Component(tag="input", type="radio", name=self.name, value=opt.lower().replace(" ", "_"))
                radio_text = Component(tag="span", content=opt)
                radio.children = [radio_input, radio_text]
                inp.children.append(radio)
        elif self.field_type == "file":
            from pyvibe.components.input import unggah_file
            inp = unggah_file(
                name=self.name,
                accept=self.accept,
                multiple=self.multiple,
            )
        else:
            inp = input_teks(
                placeholder=self.placeholder,
                name=self.name,
                value=str(display_value),
            )

        wrapper.children.append(inp)

        # Help text
        if self.help_text:
            help_el = Component(tag="div", content=self.help_text)
            help_el.class_names.extend(["pv-text-sm", "pv-text-gray", "pv-mt-4"])
            wrapper.children.append(help_el)

        # Error message
        if error:
            error_el = Component(tag="div", content=error)
            error_el.class_names.append("pv-form-error")
            wrapper.children.append(error_el)

        return wrapper


# ==================== Form ====================

class Form:
    """
    Form builder with validation.

    Usage:
        form = Form("contact")
        form.add_field("nama", Field.text(required=True, label="Nama"))
        form.add_field("email", Field.email(required=True, label="Email"))
        form.add_field("pesan", Field.textarea(label="Pesan"))

        errors = form.validate(data)
        if not errors:
            # Process form
            pass

        html = form.render(data=data, errors=errors)
    """

    def __init__(self, name: str = "", action: str = "", method: str = "POST"):
        self.name = name
        self.action = action
        self.method = method.upper()
        self.fields: Dict[str, Field] = {}
        self._on_submit: Optional[Callable] = None

    def add_field(self, name: str, field: Field) -> "Form":
        """Add field to form."""
        field.name = name
        if not field.label:
            field.label = name.replace("_", " ").title()
        self.fields[name] = field
        return self

    def on_submit(self, callback: Callable) -> "Form":
        """Set submit callback."""
        self._on_submit = callback
        return self

    def validate(self, data: Dict[str, Any]) -> Dict[str, str]:
        """
        Validate form data.

        Returns:
            Dict of field_name -> error_message. Empty if valid.
        """
        errors = {}

        for name, field in self.fields.items():
            value = data.get(name, field.default)

            # Run validators
            for validator in field.validators:
                if hasattr(validator, "__call__"):
                    # Check if validator expects data parameter
                    import inspect
                    sig = inspect.signature(validator)
                    if len(sig.parameters) > 1:
                        error = validator(value, data)
                    else:
                        error = validator(value)
                    if error:
                        errors[name] = error
                        break

        return errors

    def render(self, data: Optional[Dict[str, Any]] = None, errors: Optional[Dict[str, str]] = None) -> Component:
        """Render form as component."""
        data = data or {}
        errors = errors or {}

        form = Component(tag="form")
        form.attrs["method"] = self.method
        if self.action:
            form.attrs["action"] = self.action
        if self.name:
            form.attrs["name"] = self.name
        form.class_names.extend(["pv-form", "pv-flex", "pv-flex-col", "pv-gap-16"])

        for name, field in self.fields.items():
            field_component = field.render(
                value=data.get(name),
                error=errors.get(name),
            )
            form.children.append(field_component)

        return form

    def get_initial_data(self) -> Dict[str, Any]:
        """Get initial form data with defaults."""
        return {name: field.default for name, field in self.fields.items()}

    def get_field_names(self) -> List[str]:
        """Get list of field names."""
        return list(self.fields.keys())

    def to_dict(self) -> Dict[str, Any]:
        """Serialize form definition."""
        return {
            "name": self.name,
            "action": self.action,
            "method": self.method,
            "fields": [
                {
                    "name": name,
                    "type": field.field_type,
                    "label": field.label,
                    "required": field.required,
                }
                for name, field in self.fields.items()
            ],
        }


# ==================== Form Builder (Fluent API) ====================

class FormBuilder:
    """
    Fluent form builder.

    Usage:
        form = (FormBuilder("login")
            .text("email", label="Email", required=True, validators=[Validators.email])
            .password("password", label="Password", required=True)
            .checkbox("remember", label="Ingat saya")
            .submit("Masuk")
            .build())
    """

    def __init__(self, name: str = ""):
        self.form = Form(name)
        self._submit_text = "Kirim"
        self._submit_color = "ungu"

    def text(self, name: str, **kwargs) -> "FormBuilder":
        """Add text field."""
        self.form.add_field(name, Field.text(**kwargs))
        return self

    def number(self, name: str, **kwargs) -> "FormBuilder":
        """Add number field."""
        self.form.add_field(name, Field.number(**kwargs))
        return self

    def email(self, name: str, **kwargs) -> "FormBuilder":
        """Add email field."""
        self.form.add_field(name, Field.email(**kwargs))
        return self

    def password(self, name: str, **kwargs) -> "FormBuilder":
        """Add password field."""
        self.form.add_field(name, Field.password(**kwargs))
        return self

    def textarea(self, name: str, **kwargs) -> "FormBuilder":
        """Add textarea field."""
        self.form.add_field(name, Field.textarea(**kwargs))
        return self

    def checkbox(self, name: str, **kwargs) -> "FormBuilder":
        """Add checkbox field."""
        self.form.add_field(name, Field.checkbox(**kwargs))
        return self

    def select(self, name: str, options: List[str], **kwargs) -> "FormBuilder":
        """Add select field."""
        self.form.add_field(name, Field.select(options, **kwargs))
        return self

    def radio(self, name: str, options: List[str], **kwargs) -> "FormBuilder":
        """Add radio field."""
        self.form.add_field(name, Field.radio(options, **kwargs))
        return self

    def file(self, name: str, **kwargs) -> "FormBuilder":
        """Add file upload field."""
        self.form.add_field(name, Field.file(**kwargs))
        return self

    def submit(self, text: str = "Kirim", warna: str = "ungu") -> "FormBuilder":
        """Set submit button."""
        self._submit_text = text
        self._submit_color = warna
        return self

    def build(self) -> Form:
        """Build and return the form."""
        return self.form


# ==================== Contact Form Preset ====================

def form_kontak(**kwargs) -> Form:
    """Pre-built contact form."""
    return (FormBuilder("kontak")
        .text("nama", label="Nama Lengkap", required=True)
        .email("email", label="Email", required=True, validators=[Validators.email])
        .text("telepon", label="Telepon", validators=[Validators.phone])
        .textarea("pesan", label="Pesan", required=True, rows=5)
        .submit("Kirim Pesan")
        .build())


def form_login(**kwargs) -> Form:
    """Pre-built login form."""
    return (FormBuilder("login")
        .email("email", label="Email", required=True, validators=[Validators.email])
        .password("password", label="Password", required=True)
        .checkbox("remember", label="Ingat saya")
        .submit("Masuk")
        .build())


def form_register(**kwargs) -> Form:
    """Pre-built registration form."""
    return (FormBuilder("register")
        .text("nama", label="Nama Lengkap", required=True)
        .email("email", label="Email", required=True, validators=[Validators.email])
        .password("password", label="Password", required=True, validators=[Validators.min_length(8)])
        .password("password_confirm", label="Konfirmasi Password", required=True)
        .checkbox("agree", label="Saya setuju dengan syarat & ketentuan", required=True)
        .submit("Daftar")
        .build())


def form_search(placeholder: str = "Cari...") -> Form:
    """Pre-built search form."""
    return (FormBuilder("search")
        .text("q", label="", placeholder=placeholder)
        .submit("Cari")
        .build())
