"""
Form Validation — validasi form dengan pesan error Bahasa Indonesia.

Usage:
    from pyvibe.forms.validation import FormValidator, required, email, min_length

    validator = FormValidator({
        "nama": [required(), min_length(3)],
        "email": [required(), email()],
        "password": [required(), min_length(8)],
    })

    errors = validator.validate(data)
    if errors:
        # Tampilkan error
        for field, message in errors.items():
            print(f"{field}: {message}")
"""

from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
import re


class ValidationError:
    """Validation error untuk satu field."""

    def __init__(self, field: str, message: str, code: str = "invalid"):
        self.field = field
        self.message = message
        self.code = code

    def __str__(self):
        return self.message

    def to_dict(self):
        return {"field": self.field, "message": self.message, "code": self.code}


class ValidationResult:
    """Hasil validasi."""

    def __init__(self):
        self.errors: List[ValidationError] = []
        self.is_valid = True

    def add_error(self, field: str, message: str, code: str = "invalid"):
        self.errors.append(ValidationError(field, message, code))
        self.is_valid = False

    def get_error(self, field: str) -> Optional[str]:
        for error in self.errors:
            if error.field == field:
                return error.message
        return None

    def get_errors(self) -> Dict[str, str]:
        return {error.field: error.message for error in self.errors}

    def __bool__(self):
        return self.is_valid


class Validator:
    """Base validator class."""

    def __init__(self, message: Optional[str] = None):
        self.message = message

    def validate(self, value: Any, field: str = "") -> Optional[str]:
        """Return error message jika invalid, None jika valid."""
        raise NotImplementedError


class RequiredValidator(Validator):
    """Validasi field wajib diisi."""

    def validate(self, value: Any, field: str = "") -> Optional[str]:
        if value is None or value == "" or value == []:
            return self.message or f"{field} wajib diisi."
        return None


class EmailValidator(Validator):
    """Validasi format email."""

    def validate(self, value: Any, field: str = "") -> Optional[str]:
        if not value:
            return None
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, str(value)):
            return self.message or f"{field} harus berisi alamat email yang valid."
        return None


class MinLengthValidator(Validator):
    """Validasi panjang minimal."""

    def __init__(self, min_len: int, message: Optional[str] = None):
        super().__init__(message)
        self.min_len = min_len

    def validate(self, value: Any, field: str = "") -> Optional[str]:
        if not value:
            return None
        if len(str(value)) < self.min_len:
            return self.message or f"{field} minimal {self.min_len} karakter."
        return None


class MaxLengthValidator(Validator):
    """Validasi panjang maksimal."""

    def __init__(self, max_len: int, message: Optional[str] = None):
        super().__init__(message)
        self.max_len = max_len

    def validate(self, value: Any, field: str = "") -> Optional[str]:
        if not value:
            return None
        if len(str(value)) > self.max_len:
            return self.message or f"{field} maksimal {self.max_len} karakter."
        return None


class MinValueValidator(Validator):
    """Validasi nilai minimal."""

    def __init__(self, min_val: float, message: Optional[str] = None):
        super().__init__(message)
        self.min_val = min_val

    def validate(self, value: Any, field: str = "") -> Optional[str]:
        if value is None or value == "":
            return None
        try:
            if float(value) < self.min_val:
                return self.message or f"{field} minimal {self.min_val}."
        except (ValueError, TypeError):
            return self.message or f"{field} harus berisi angka."
        return None


class MaxValueValidator(Validator):
    """Validasi nilai maksimal."""

    def __init__(self, max_val: float, message: Optional[str] = None):
        super().__init__(message)
        self.max_val = max_val

    def validate(self, value: Any, field: str = "") -> Optional[str]:
        if value is None or value == "":
            return None
        try:
            if float(value) > self.max_val:
                return self.message or f"{field} maksimal {self.max_val}."
        except (ValueError, TypeError):
            return self.message or f"{field} harus berisi angka."
        return None


class PatternValidator(Validator):
    """Validasi dengan regex pattern."""

    def __init__(self, pattern: str, message: Optional[str] = None):
        super().__init__(message)
        self.pattern = pattern

    def validate(self, value: Any, field: str = "") -> Optional[str]:
        if not value:
            return None
        if not re.match(self.pattern, str(value)):
            return self.message or f"{field} format tidak valid."
        return None


class PhoneValidator(Validator):
    """Validasi nomor telepon Indonesia."""

    def validate(self, value: Any, field: str = "") -> Optional[str]:
        if not value:
            return None
        cleaned = re.sub(r'[\s\-\(\)]', '', str(value))
        if not re.match(r'^(08|06|\+62|62)[0-9]{8,13}$', cleaned):
            return self.message or f"{field} harus berisi nomor telepon Indonesia yang valid."
        return None


class URLValidator(Validator):
    """Validasi URL."""

    def validate(self, value: Any, field: str = "") -> Optional[str]:
        if not value:
            return None
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        if not re.match(pattern, str(value)):
            return self.message or f"{field} harus berisi URL yang valid."
        return None


class MatchValidator(Validator):
    """Validasi kesamaan dengan field lain (untuk password confirmation)."""

    def __init__(self, other_field: str, other_value: Any = None, message: Optional[str] = None):
        super().__init__(message)
        self.other_field = other_field
        self.other_value = other_value

    def validate(self, value: Any, field: str = "") -> Optional[str]:
        if self.other_value is not None and value != self.other_value:
            return self.message or f"{field} tidak cocok dengan {self.other_field}."
        return None


# ==================== Convenience Functions ====================

def required(message: Optional[str] = None) -> RequiredValidator:
    """Field wajib diisi."""
    return RequiredValidator(message)

def email(message: Optional[str] = None) -> EmailValidator:
    """Format email valid."""
    return EmailValidator(message)

def min_length(min_len: int, message: Optional[str] = None) -> MinLengthValidator:
    """Panjang minimal."""
    return MinLengthValidator(min_len, message)

def max_length(max_len: int, message: Optional[str] = None) -> MaxLengthValidator:
    """Panjang maksimal."""
    return MaxLengthValidator(max_len, message)

def min_value(min_val: float, message: Optional[str] = None) -> MinValueValidator:
    """Nilai minimal."""
    return MinValueValidator(min_val, message)

def max_value(max_val: float, message: Optional[str] = None) -> MaxValueValidator:
    """Nilai maksimal."""
    return MaxValueValidator(max_val, message)

def pattern(pat: str, message: Optional[str] = None) -> PatternValidator:
    """Regex pattern."""
    return PatternValidator(pat, message)

def phone(message: Optional[str] = None) -> PhoneValidator:
    """Nomor telepon Indonesia."""
    return PhoneValidator(message)

def url(message: Optional[str] = None) -> URLValidator:
    """URL valid."""
    return URLValidator(message)

def matches(other_field: str, message: Optional[str] = None) -> MatchValidator:
    """Cocok dengan field lain."""
    return MatchValidator(other_field, message=message)


# ==================== Form Validator ====================

class FormValidator:
    """
    Form validator.

    Usage:
        validator = FormValidator({
            "nama": [required(), min_length(3)],
            "email": [required(), email()],
            "password": [required(), min_length(8)],
            "confirm_password": [required(), matches("password")],
        })

        result = validator.validate(data)
        if not result:
            print(result.get_errors())
    """

    def __init__(self, rules: Dict[str, List[Validator]]):
        self.rules = rules

    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validasi semua fields."""
        result = ValidationResult()

        for field, validators in self.rules.items():
            value = data.get(field)
            for validator in validators:
                error = validator.validate(value, field)
                if error:
                    result.add_error(field, error)
                    break  # Stop on first error per field

        return result

    def validate_field(self, field: str, value: Any) -> Optional[str]:
        """Validasi satu field."""
        if field not in self.rules:
            return None

        for validator in self.rules[field]:
            error = validator.validate(value, field)
            if error:
                return error

        return None
