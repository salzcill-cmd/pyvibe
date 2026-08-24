"""
PyVibe i18n — internationalization support.

Usage:
    from pyvibe.i18n import t, set_locale

    # Set locale
    set_locale("id")

    # Translate
    print(t("hello"))  # "Halo!"
    print(t("welcome"))  # "Selamat Datang!"
"""

from __future__ import annotations
from typing import Dict, Optional


# Default translations
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "id": {
        "hello": "Halo!",
        "welcome": "Selamat Datang",
        "goodbye": "Selamat Tinggal",
        "yes": "Ya",
        "no": "Tidak",
        "save": "Simpan",
        "cancel": "Batal",
        "delete": "Hapus",
        "edit": "Edit",
        "add": "Tambah",
        "search": "Cari",
        "loading": "Memuat...",
        "error": "Kesalahan",
        "success": "Berhasil",
        "warning": "Peringatan",
        "info": "Informasi",
        "confirm": "Konfirmasi",
        "back": "Kembali",
        "next": "Selanjutnya",
        "previous": "Sebelumnya",
        "submit": "Kirim",
        "reset": "Reset",
        "login": "Masuk",
        "logout": "Keluar",
        "register": "Daftar",
        "email": "Email",
        "password": "Password",
        "name": "Nama",
        "phone": "Telepon",
        "address": "Alamat",
        "city": "Kota",
        "country": "Negara",
        "postal_code": "Kode Pos",
        "date": "Tanggal",
        "time": "Waktu",
        "total": "Total",
        "price": "Harga",
        "quantity": "Jumlah",
        "subtotal": "Subtotal",
        "discount": "Diskon",
        "tax": "Pajak",
        "shipping": "Pengiriman",
        "payment": "Pembayaran",
        "order": "Pesanan",
        "cart": "Keranjang",
        "checkout": "Checkout",
        "profile": "Profil",
        "settings": "Pengaturan",
        "help": "Bantuan",
        "about": "Tentang",
        "contact": "Kontak",
        "home": "Beranda",
        "no_data": "Tidak ada data",
        "loading_data": "Memuat data...",
        "required": "Wajib diisi",
        "invalid_email": "Email tidak valid",
        "password_min": "Password minimal 8 karakter",
        "password_match": "Password tidak cocok",
    },
    "en": {
        "hello": "Hello!",
        "welcome": "Welcome",
        "goodbye": "Goodbye",
        "yes": "Yes",
        "no": "No",
        "save": "Save",
        "cancel": "Cancel",
        "delete": "Delete",
        "edit": "Edit",
        "add": "Add",
        "search": "Search",
        "loading": "Loading...",
        "error": "Error",
        "success": "Success",
        "warning": "Warning",
        "info": "Information",
        "confirm": "Confirm",
        "back": "Back",
        "next": "Next",
        "previous": "Previous",
        "submit": "Submit",
        "reset": "Reset",
        "login": "Login",
        "logout": "Logout",
        "register": "Register",
        "email": "Email",
        "password": "Password",
        "name": "Name",
        "phone": "Phone",
        "address": "Address",
        "city": "City",
        "country": "Country",
        "postal_code": "Postal Code",
        "date": "Date",
        "time": "Time",
        "total": "Total",
        "price": "Price",
        "quantity": "Quantity",
        "subtotal": "Subtotal",
        "discount": "Discount",
        "tax": "Tax",
        "shipping": "Shipping",
        "payment": "Payment",
        "order": "Order",
        "cart": "Cart",
        "checkout": "Checkout",
        "profile": "Profile",
        "settings": "Settings",
        "help": "Help",
        "about": "About",
        "contact": "Contact",
        "home": "Home",
        "no_data": "No data",
        "loading_data": "Loading data...",
        "required": "Required",
        "invalid_email": "Invalid email",
        "password_min": "Password must be at least 8 characters",
        "password_match": "Passwords do not match",
    },
}

_current_locale = "id"


def set_locale(locale: str):
    """Set current locale."""
    global _current_locale
    _current_locale = locale


def get_locale() -> str:
    """Get current locale."""
    return _current_locale


def t(key: str, **kwargs) -> str:
    """
    Translate a key.

    Usage:
        print(t("hello"))  # "Halo!"
        print(t("welcome"))  # "Selamat Datang"
    """
    translations = TRANSLATIONS.get(_current_locale, TRANSLATIONS["id"])
    text = translations.get(key, key)

    # Simple string formatting
    for k, v in kwargs.items():
        text = text.replace(f"{{{k}}}", str(v))

    return text


def add_translations(locale: str, translations: Dict[str, str]):
    """Add translations for a locale."""
    if locale not in TRANSLATIONS:
        TRANSLATIONS[locale] = {}
    TRANSLATIONS[locale].update(translations)


def get_available_locales() -> list:
    """Get available locales."""
    return list(TRANSLATIONS.keys())
