"""
Natural Language Parser — mengubah syntax bahasa Indonesia jadi komponen PyVibe.

Contoh input:
    tampilin judul "Selamat Datang" di tengah
    tampilin paragraf "Halo, ini website gue."
    tampilin tombol "Klik Saya" warna ungu
    tampilin gambar "photo.jpg" bulat
    tampilin kartu judul "Produk A" isi "Ini deskripsi produk"
    bikin navbar dengan logo "MyBrand" dan menu "Home", "About"
    tambah section dengan judul "Fitur Kami" dan background gelap
"""

from __future__ import annotations
import re
from typing import Any, Dict, List, Optional, Tuple


# ==================== Keyword Maps ====================

COMPONENT_KEYWORDS = {
    # Basic
    "judul": "judul",
    "heading": "judul",
    "subjudul": "subjudul",
    "subtitle": "subjudul",
    "paragraf": "paragraf",
    "paragraph": "paragraf",
    "p": "paragraf",
    "teks": "teks",
    "text": "teks",
    "gambar": "gambar",
    "image": "gambar",
    "img": "gambar",
    "foto": "gambar",
    "photo": "gambar",
    "tautan": "tautan",
    "link": "tautan",
    "ikon": "ikon",
    "icon": "ikon",
    "badge": "badge",
    "label": "badge",
    "chip": "chip",
    "tag": "chip",
    "avatar": "avatar",
    "progress": "progress_bar",

    # Input
    "tombol": "tombol",
    "button": "tombol",
    "btn": "tombol",
    "input": "input_teks",
    "input_teks": "input_teks",
    "text_input": "input_teks",
    "input_angka": "input_angka",
    "number_input": "input_angka",
    "input_email": "input_email",
    "email_input": "input_email",
    "input_sandi": "input_sandi",
    "password_input": "input_sandi",
    "textarea": "textarea",
    "text_area": "textarea",
    "centang": "centang",
    "checkbox": "centang",
    "pilihan": "pilihan",
    "select": "pilihan",
    "dropdown": "pilihan",

    # Layout
    "kartu": "kartu",
    "card": "kartu",
    "kolom": "kolom",
    "column": "kolom",
    "col": "kolom",
    "baris": "baris",
    "row": "baris",
    "flex": "baris",
    "bagian": "bagian",
    "section": "bagian",
    "grid": "grid",
    "kontainer": "kontainer",
    "container": "kontainer",
    "wrapper": "kontainer",

    # Navigation
    "navbar": "navbar",
    "nav": "navbar",
    "navigation": "navbar",
    "sidebar": "sidebar",
    "footer": "footer",
    "tabs": "tabs",
    "tab": "tabs",
    "breadcrumb": "breadcrumb",

    # Feedback
    "notifikasi": "notifikasi",
    "notification": "notifikasi",
    "toast": "notifikasi",
    "alert": "alert",
    "peringatan": "alert",
    "loader": "loader",
    "loading": "loader",
    "spinner": "loader",
    "skeleton": "skeleton",

    # Data
    "tabel": "tabel",
    "table": "tabel",
    "grafik": "grafik_sederhana",
    "chart": "grafik_sederhana",
    "daftar": "daftar",
    "list": "daftar",
    "statistik": "statistik",
    "stats": "statistik",
    "counter": "count_down",
    "count_down": "count_down",

    # Advanced
    "carousel": "carousel",
    "slider": "carousel",
    "accordion": "accordion",
    "collapse": "accordion",
    "modal": "modal",
    "popup": "modal",
    "dialog": "modal",
    "tooltip": "tooltip",
    "dropdown_menu": "dropdown",

    # Decorative
    "spasi": "spasi",
    "space": "spasi",
    "gap": "spasi",
    "pemisah": "pemisah",
    "divider": "pemisah",
    "hr": "pemisah",
    "garis": "pemisah",
    "line": "pemisah",
}

STYLE_KEYWORDS = {
    # Alignment
    "di tengah": "tengah",
    "tengah": "tengah",
    "center": "tengah",
    "rata tengah": "tengah",
    "centered": "tengah",
    "di kiri": "kiri",
    "kiri": "kiri",
    "left": "kiri",
    "rata kiri": "kiri",
    "aligned left": "kiri",
    "di kanan": "kanan",
    "kanan": "kanan",
    "right": "kanan",
    "rata kanan": "kanan",
    "aligned right": "kanan",

    # Colors
    "warna biru": "warna_biru",
    "biru": "warna_biru",
    "blue": "warna_biru",
    "warna merah": "warna_merah",
    "merah": "warna_merah",
    "red": "warna_merah",
    "warna hijau": "warna_hijau",
    "hijau": "warna_hijau",
    "green": "warna_hijau",
    "warna ungu": "warna_ungu",
    "ungu": "warna_ungu",
    "purple": "warna_ungu",
    "warna kuning": "warna_kuning",
    "kuning": "warna_kuning",
    "yellow": "warna_kuning",
    "warna cyan": "warna_cyan",
    "cyan": "warna_cyan",
    "warna pink": "warna_pink",
    "pink": "warna_pink",
    "warna abu": "warna_abu",
    "abu": "warna_abu",
    "gray": "warna_abu",
    "grey": "warna_abu",
    "warna orange": "warna_orange",
    "orange": "warna_orange",
    "warna putih": "warna_putih",
    "putih": "warna_putih",
    "white": "warna_putih",
    "warna hitam": "warna_hitam",
    "hitam": "warna_hitam",
    "black": "warna_hitam",

    # Size
    "besar": "besar",
    "large": "besar",
    "big": "besar",
    "kecil": "kecil",
    "small": "kecil",
    "sedang": "sedang",
    "medium": "sedang",
    "normal": "sedang",

    # Style
    "tebal": "tebal",
    "bold": "tebal",
    "tipis": "tipis",
    "thin": "tipis",
    "light": "tipis",

    # Shape
    "bulat": "bulat",
    "rounded": "bulat",
    "circle": "bulat",
    "pill": "bulat",

    # Shadow
    "bayangan": "bayangan",
    "shadow": "bayangan",
    "berbayang": "bayangan",

    # Gradient
    "gradient": "gradient",
    "gradien": "gradient",

    # Width
    "lebar penuh": "lebar_penuh",
    "full width": "lebar_penuh",
    "width 100%": "lebar_penuh",
    "stretch": "lebar_penuh",
}

ACTION_KEYWORDS = {
    "tampilin": "render",
    "tampilkan": "render",
    "show": "render",
    "render": "render",
    "pasang": "render",
    "taruh": "render",
    "letakkan": "render",
    "kasih": "render",
    "add": "add",
    "tambah": "add",
    "insert": "add",
    "create": "create",
    "buat": "create",
    "bikin": "create",
    "hapus": "delete",
    "delete": "delete",
    "remove": "delete",
    "buang": "delete",
    "edit": "edit",
    "update": "edit",
    "ubah": "edit",
    "ganti": "edit",
    "rubah": "edit",
}

# Indonesian stopwords to ignore
STOPWORDS = {
    "yang", "dan", "di", "ini", "itu", "dengan", "untuk", "pada",
    "ke", "dari", "ada", "adalah", "ialah", "yaitu", "yakni",
    "akan", "telah", "sudah", "sedang", "lagi", "akan",
    "bisa", "dapat", "mampu", "harus", "wajib",
    "atau", "maupun", "pun", "juga", "serta",
    "tidak", "bukan", "tak", "tiada", "tanpa",
    "hanya", "cuma", "sekedar", "hanya",
    "sangat", "sekali", "amat", "paling",
    "lebih", "lagi", "lain", "lainnya",
    "mereka", "kami", "kita", "anda", "lo", "gue", "gw",
    "saya", "aku", "kamu", "dia", "ia",
    "sini", "situ", "sana", "sono",
    "begini", "begitu", "seperti",
    "kalau", "jika", "apabila", "bila",
    "maka", "sehingga", "oleh karena itu",
    "karena", "sebab", "lantaran",
    "tetapi", "namun", "tapi",
    "walaupun", "meskipun", "meski",
    "serta", "juga", "pula",
}


# ==================== Parser Class ====================

class NaturalLanguageParser:
    """
    Parser untuk syntax bahasa Indonesia → PyVibe components.

    Usage:
        parser = NaturalLanguageParser()
        component = parser.parse('tampilin judul "Halo Dunia" di tengah')
    """

    def __init__(self):
        self.errors: List[str] = []

    def parse(self, line: str) -> Optional[Dict[str, Any]]:
        """
        Parse satu baris natural language jadi component definition.

        Returns:
            Dict dengan keys: component, args, kwargs, styles
            Atau None kalau line gak valid
        """
        line = line.strip()
        if not line or line.startswith("#"):
            return None

        # Detect action
        action = self._detect_action(line)
        if not action:
            return None

        # Detect component
        component_name = self._detect_component(line)
        if not component_name:
            return None

        # Extract content (text in quotes)
        content = self._extract_content(line)

        # Extract styles/modifiers
        styles = self._extract_styles(line)

        # Extract properties
        props = self._extract_properties(line)

        return {
            "action": action,
            "component": component_name,
            "content": content,
            "styles": styles,
            "props": props,
            "raw": line,
        }

    def parse_block(self, text: str) -> List[Dict[str, Any]]:
        """Parse multiple lines of natural language."""
        results = []
        for line in text.split("\n"):
            parsed = self.parse(line)
            if parsed:
                results.append(parsed)
        return results

    def to_python(self, text: str) -> str:
        """
        Convert natural language code ke Python PyVibe code.

        Usage:
            parser = NaturalLanguageParser()
            python_code = parser.to_python('tampilin judul "Halo" di tengah')
            # → judul("Halo").tengah()
        """
        lines = text.strip().split("\n")
        python_lines = []

        for line in lines:
            parsed = self.parse(line)
            if parsed:
                python_line = self._generate_python(parsed)
                python_lines.append(python_line)
            elif line.strip():
                # Keep comments and empty lines
                if line.strip().startswith("#"):
                    python_lines.append(line)
                else:
                    python_lines.append(f"# ??? {line.strip()}")

        return "\n".join(python_lines)

    def _detect_action(self, line: str) -> Optional[str]:
        """Detect action keyword."""
        line_lower = line.lower()
        for keyword, action in ACTION_KEYWORDS.items():
            if keyword in line_lower:
                return action
        # Default: if line starts with a component name, assume render
        for keyword in COMPONENT_KEYWORDS:
            if line_lower.startswith(keyword):
                return "render"
        return None

    def _detect_component(self, line: str) -> Optional[str]:
        """Detect component type from keywords."""
        line_lower = line.lower()

        # Check for component keywords (longest match first)
        sorted_keywords = sorted(COMPONENT_KEYWORDS.keys(), key=len, reverse=True)
        for keyword in sorted_keywords:
            if keyword in line_lower:
                return COMPONENT_KEYWORDS[keyword]

        return None

    def _extract_content(self, line: str) -> str:
        """Extract content between quotes."""
        # Match "content" or 'content'
        match = re.search(r'["\']([^"\']+)["\']', line)
        if match:
            return match.group(1)

        # If no quotes, try to extract text after component keyword
        for keyword in COMPONENT_KEYWORDS:
            if keyword in line.lower():
                idx = line.lower().index(keyword) + len(keyword)
                remaining = line[idx:].strip()
                # Remove stopwords and action words
                words = remaining.split()
                content_words = []
                for word in words:
                    if word.lower() not in STOPWORDS and word.lower() not in ACTION_KEYWORDS:
                        content_words.append(word)
                if content_words:
                    return " ".join(content_words)
                break

        return ""

    def _extract_styles(self, line: str) -> List[str]:
        """Extract style modifiers."""
        styles = []
        line_lower = line.lower()

        # Check for style keywords
        sorted_style_keys = sorted(STYLE_KEYWORDS.keys(), key=len, reverse=True)
        for keyword in sorted_style_keys:
            if keyword in line_lower:
                style = STYLE_KEYWORDS[keyword]
                if style not in styles:
                    styles.append(style)

        return styles

    def _extract_properties(self, line: str) -> Dict[str, str]:
        """Extract key-value properties."""
        props = {}

        # Match pattern: key value
        patterns = [
            (r'warna\s+(\w+)', 'warna'),
            (r'color\s+(\w+)', 'warna'),
            (r'ukuran\s+(\w+)', 'ukuran'),
            (r'size\s+(\w+)', 'ukuran'),
            (r'width\s+(\S+)', 'width'),
            (r'height\s+(\S+)', 'height'),
            (r'padding\s+(\S+)', 'padding'),
            (r'margin\s+(\S+)', 'margin'),
            (r'src\s+["\']([^"\']+)["\']', 'src'),
            (r'url\s+["\']([^"\']+)["\']', 'url'),
            (r'href\s+["\']([^"\']+)["\']', 'href'),
            (r'id\s+["\']([^"\']+)["\']', 'id'),
            (r'name\s+["\']([^"\']+)["\']', 'name'),
            (r'level\s+(\d+)', 'level'),
            (r'kolom\s+(\d+)', 'columns'),
            (r'columns\s+(\d+)', 'columns'),
            (r'gap\s+(\S+)', 'gap'),
            (r'isi\s+["\']([^"\']+)["\']', 'content'),
            (r'teks\s+["\']([^"\']+)["\']', 'text'),
        ]

        for pattern, prop_name in patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                props[prop_name] = match.group(1)

        return props

    def _generate_python(self, parsed: Dict[str, Any]) -> str:
        """Generate Python code from parsed definition."""
        component = parsed["component"]
        content = parsed["content"]
        styles = parsed["styles"]
        props = parsed["props"]

        # Build component call
        if component == "tombol":
            args = f'"{content}"' if content else ""
            if "warna" in props:
                args += f', warna="{props["warna"]}"'
            call = f"tombol({args})"
        elif component == "judul":
            args = f'"{content}"' if content else ""
            if "level" in props:
                args += f', level={props["level"]}'
            call = f"judul({args})"
        elif component == "subjudul":
            args = f'"{content}"' if content else ""
            call = f"subjudul({args})"
        elif component == "paragraf":
            args = f'"{content}"' if content else ""
            call = f"paragraf({args})"
        elif component == "teks":
            args = f'"{content}"' if content else ""
            call = f"teks({args})"
        elif component == "gambar":
            src = props.get("src", content)
            args = f'"{src}"' if src else ""
            call = f"gambar({args})"
        elif component == "tautan":
            text = content or "Link"
            url = props.get("url", props.get("href", "#"))
            call = f'tautan("{text}", url="{url}")'
        elif component == "kartu":
            args = f'judul="{content}"' if content else ""
            call = f"kartu({args})"
        elif component == "input_teks":
            label = content or props.get("name", "")
            call = f'input_teks(label="{label}")'
        elif component == "input_angka":
            label = content or props.get("name", "")
            call = f'input_angka(label="{label}")'
        elif component == "input_email":
            call = f'input_email(label="{content}")'
        elif component == "input_sandi":
            call = f'input_sandi(label="{content}")'
        elif component == "textarea":
            call = f'textarea(label="{content}")'
        elif component == "centang":
            call = f'centang("{content}")'
        elif component == "pilihan":
            call = f'pilihan(label="{content}")'
        elif component == "tabel":
            call = "tabel(data=[...])"
        elif component == "notifikasi":
            tipe = props.get("tipe", "info")
            call = f'notifikasi("{content}", tipe="{tipe}")'
        elif component == "alert":
            tipe = props.get("tipe", "info")
            call = f'alert("{content}", tipe="{tipe}")'
        elif component == "loader":
            call = "loader()"
        elif component == "spasi":
            tinggi = props.get("height", "24px")
            call = f'spasi("{tinggi}")'
        elif component == "pemisah":
            call = "pemisah()"
        elif component == "navbar":
            logo = content or "PyVibe"
            call = f'navbar(logo="{logo}")'
        elif component == "sidebar":
            call = "sidebar(...)"
        elif component == "footer":
            call = f'footer(copyright="{content}")'
        elif component == "tabs":
            call = "tabs(...)"
        elif component == "breadcrumb":
            call = "breadcrumb(...)"
        elif component == "carousel":
            call = "carousel(...)"
        elif component == "accordion":
            call = "accordion(...)"
        elif component == "modal":
            call = f'modal("{content}")'
        elif component == "tooltip":
            call = f'tooltip(content, "{content}")'
        elif component == "dropdown":
            call = "dropdown(trigger, ...)"
        elif component == "badge":
            call = f'badge("{content}")'
        elif component == "chip":
            call = f'chip("{content}")'
        elif component == "avatar":
            call = f'avatar("{content}")'
        elif component == "progress_bar":
            call = f'progress_bar({content})' if content else "progress_bar(0)"
        elif component == "count_down":
            call = f'count_down({content})' if content else "count_down(0)"
        elif component == "kolom":
            width = props.get("columns", props.get("width", "6"))
            call = f"kolom({width}, ...)"
        elif component == "baris":
            call = "baris(...)"
        elif component == "bagian":
            call = "bagian(...)"
        elif component == "grid":
            call = "grid(...)"
        elif component == "kontainer":
            call = "kontainer(...)"
        elif component == "statistik":
            call = "statistik([...])"
        elif component == "grafik_sederhana":
            call = "grafik_sederhana(...)"
        elif component == "daftar":
            call = "daftar(...)"
        elif component == "skeleton":
            call = "skeleton()"
        else:
            call = f'{component}("{content}")'

        # Apply styles
        style_methods = []
        for style in styles:
            if style == "tengah":
                style_methods.append(".tengah()")
            elif style == "kiri":
                style_methods.append(".kiri()")
            elif style == "kanan":
                style_methods.append(".kanan()")
            elif style.startswith("warna_"):
                # Skip if warna already passed as prop (for tombol, etc.)
                if component in ("tombol", "button", "btn") and "warna" in props:
                    continue
                color = style.replace("warna_", "")
                style_methods.append(f'.warna("{color}")')
            elif style == "besar":
                style_methods.append(".besar()")
            elif style == "kecil":
                style_methods.append(".kecil()")
            elif style == "tebal":
                style_methods.append(".tebal()")
            elif style == "tipis":
                style_methods.append(".tipis()")
            elif style == "bulat":
                style_methods.append(".bulat()")
            elif style == "bayangan":
                style_methods.append('.bayangan("md")')
            elif style == "gradient":
                style_methods.append('.bg("gradient-ungu")')
            elif style == "lebar_penuh":
                style_methods.append('.lebar("100%")')

        # Build final expression
        result = call
        for method in style_methods:
            result += method

        return result


# ==================== Convenience Functions ====================

def nl(text: str) -> str:
    """
    Convert natural language code ke Python PyVibe code.

    Usage:
        print(nl('tampilin judul "Halo Dunia" di tengah'))
        # → judul("Halo Dunia").tengah()
    """
    parser = NaturalLanguageParser()
    return parser.to_python(text)


def nl_parse(text: str) -> List[Dict[str, Any]]:
    """Parse natural language code ke component definitions."""
    parser = NaturalLanguageParser()
    return parser.parse_block(text)


def nl_test():
    """Test cases untuk natural language parser."""
    test_cases = [
        ('tampilin judul "Halo Dunia"', 'judul("Halo Dunia")'),
        ('tampilin judul "Selamat Datang" di tengah', 'judul("Selamat Datang").tengah()'),
        ('tampilin paragraf "Ini website gue."', 'paragraf("Ini website gue.")'),
        ('tampilin tombol "Klik Saya" warna ungu', 'tombol("Klik Saya", warna="ungu")'),
        ('tampilin tombol "Simpan" warna hijau besar', 'tombol("Simpan", warna="hijau").besar()'),
        ('tampilin gambar "photo.jpg" bulat', 'gambar("photo.jpg").bulat()'),
        ('tampilin tautan "GitHub" url "https://github.com"', 'tautan("GitHub", url="https://github.com")'),
        ('tampilin input_teks "Nama Lengkap"', 'input_teks(label="Nama Lengkap")'),
        ('tampilin badge "NEW"', 'badge("NEW")'),
        ('tampilin spasi', 'spasi("24px")'),
        ('tampilin pemisah', 'pemisah()'),
        ('tampilin subjudul "Fitur Kami"', 'subjudul("Fitur Kami")'),
        ('tampilin chip "Python"', 'chip("Python")'),
        ('tampilin avatar "photo.jpg"', 'avatar("photo.jpg")'),
        ('tampilin centang "Saya setuju"', 'centang("Saya setuju")'),
        ('tampilin textarea "Pesan"', 'textarea(label="Pesan")'),
    ]

    parser = NaturalLanguageParser()
    print("🧪 Natural Language Parser Tests")
    print("=" * 50)

    passed = 0
    total = len(test_cases)

    for input_text, expected in test_cases:
        result = parser.to_python(input_text)
        status = "✅" if result.strip() == expected.strip() else "❌"
        if status == "✅":
            passed += 1
        print(f"{status} Input: {input_text}")
        if status == "❌":
            print(f"   Expected: {expected}")
            print(f"   Got:      {result}")
        print()

    print(f"Results: {passed}/{total} passed")
    return passed == total


if __name__ == "__main__":
    nl_test()
