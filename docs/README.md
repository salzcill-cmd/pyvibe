# 🐍 PyVibe Documentation

> **Build frontend websites in Python as easy as chatting.**
> *"Gak perlu ribet, yang penting gacor."*

## 📚 Table of Contents

1. [Getting Started](#getting-started)
2. [Quick Start](#quick-start)
3. [Components](#components)
4. [Natural Language Syntax](#natural-language-syntax)
5. [Form Validation](#form-validation)
6. [Routing](#routing)
7. [State Management](#state-management)
8. [Theming](#theming)
9. [Deployment](#deployment)
10. [API Reference](#api-reference)

---

## 🚀 Getting Started

### Installation

```bash
pip install pyvibe
```

### System Requirements

- Python 3.9+
- No JavaScript/Node.js required
- No build tools required

### First Project

```bash
# Create new project
pyvibe create my-website

# Navigate to project
cd my-website

# Start development server
python app.py

# Open browser
open http://localhost:3000
```

---

## ⚡ Quick Start

### Minimal Example

```python
from pyvibe import *

app = App("My Website")

@app.route("/")
def beranda():
    return tampil(
        judul("Halo Dunia!").tengah(),
        paragraf("Ini website pertama gue pakai PyVibe.").tengah(),
        tombol("Mulai Coding", warna="ungu"),
    )

app.jalan()
```

### Run It

```bash
python app.py
# 🐍 PyVibe Development Server
# 🌐 URL: http://localhost:3000
```

---

## 🧩 Components

### Basic Components

```python
# Typography
judul("Heading 1")              # <h1>
subjudul("Heading 2")           # <h2>
paragraf("Paragraph text")      # <p>
teks("Inline text")             # <span>

# Media
gambar("photo.jpg", alt="Foto") # <img>
tautan("Click me", url="/page") # <a>

# Decorative
badge("NEW")                    # Badge label
chip("Python")                  # Chip/tag
avatar("photo.jpg")             # Circular image
progress_bar(75)                # Progress bar
count_down(100, label="Users")  # Counter stat
```

### Input Components

```python
# Buttons
tombol("Click me", warna="ungu")        # Primary button
tombol("Outline", warna="outline")      # Outline button
tombol("Large", ukuran="besar")         # Large button

# Forms
input_teks(label="Nama", placeholder="Masukkan nama...")
input_angka(label="Harga", min_val=0, max_val=100)
input_email(label="Email")
input_sandi(label="Password")
textarea(label="Pesan", rows=5)
centang("Saya setuju")
pilihan(label="Kota", options=["Jakarta", "Bandung"])
unggah_file(label="Upload Foto")
```

### Layout Components

```python
# Grid System
grid(
    kartu(judul_kartu("Card 1"), paragraf("Content 1")),
    kartu(judul_kartu("Card 2"), paragraf("Content 2")),
    kartu(judul_kartu("Card 3"), paragraf("Content 3")),
    kolom=3, gap="24px",
)

# Flexbox
baris(
    paragraf("Left"),
    paragraf("Right"),
    justify="between", align="center",
)

# Sections
bagian(
    judul("Section Title"),
    paragraf("Section content..."),
    bg="gradient-ungu",
    padding="64px 32px",
)
```

### Navigation Components

```python
# Navbar
navbar(
    logo="🐍 MyBrand",
    menu=["Home", "About", "Contact"],
    tombol_daftar="Sign Up",
)

# Sidebar
sidebar(
    "Dashboard",
    "Products",
    "Settings",
    judul="Menu",
    aktif="Dashboard",
)

# Footer
footer(
    links=["GitHub", "Twitter", "Discord"],
    copyright="© 2026 MyBrand",
)

# Breadcrumb
breadcrumb("Home", "Products", "Nike Air Max")
```

### Data Components

```python
# Table
tabel(
    data=[
        {"nama": "Andi", "email": "andi@test.com", "role": "Admin"},
        {"nama": "Budi", "email": "budi@test.com", "role": "User"},
    ],
    kolom=["nama", "email", "role"],
)

# Chart
grafik_sederhana(
    data=[
        {"label": "Januari", "value": 75},
        {"label": "Februari", "value": 60},
        {"label": "Maret", "value": 90},
    ],
    warna="#7C3AED",
)

# Statistics
statistik([
    {"nilai": "1,234", "label": "Users", "icon": "👥"},
    {"nilai": "Rp 50M", "label": "Revenue", "icon": "💰"},
])
```

### Advanced Components

```python
# Accordion
accordion(
    ("Apa itu PyVibe?", paragraf("PyVibe adalah framework Python...")),
    ("Bagaimana cara install?", paragraf("pip install pyvibe")),
)

# Modal
modal(
    judul="Konfirmasi",
    paragraf("Yakin ingin menghapus?"),
    id="modal-hapus",
)

# Carousel
carousel(
    gambar("img1.jpg"),
    gambar("img2.jpg"),
    gambar("img3.jpg"),
)

# Dropdown
dropdown(
    tombol("Menu ▼"),
    "Profile",
    "Settings",
    "Logout",
)

# Stepper
stepper(["Info Dasar", "Upload Foto", "Konfirmasi"], aktif=1)

# Timeline
timeline(
    {"tanggal": "24 Agustus", "judul": "Project Started", "isi": "Memulai development."},
    {"tanggal": "25 Agustus", "judul": "Alpha Release", "isi": "Release versi alpha."},
)

# Rating
rating(bintang=4, max_bintang=5)

# Code Block
code_block('print("Hello World")', bahasa="python")

# Markdown
markdown("# Hello\\n\\nThis is **bold** and *italic*.")

# Empty State
empty_state("Belum ada data", "Buat pesanan pertama kamu!")
```

---

## 🗣️ Natural Language Syntax

PyVibe supports natural language syntax for writing components:

```python
from pyvibe.nl import *

# Convert NL to Python code
python_code = nl_convert('tampilin judul "Halo" di tengah')
# → judul("Halo").tengah()

# Use NL directly in components
components = nl(
    'tampilin judul "Selamat Datang" di tengah',
    'tampilin paragraf "Halo, ini website gue."',
    'tampilin tombol "Klik Saya" warna ungu',
)

# Full page with NL
app = App("NL Demo")

@app.route("/")
def demo():
    return tampil(
        navbar(logo="🗣️ NL Demo"),
        *nl(
            'tampilin judul "Natural Language!" di tengah',
            'tampilin paragraf "Tulis kayak ngobrol."',
        ),
        footer(copyright="© 2026"),
    )
```

### NL Keywords

| Keyword | Component | Example |
|---------|-----------|---------|
| `judul` | Heading | `tampilin judul "Halo" di tengah` |
| `paragraf` | Paragraph | `tampilin paragraf "Text here"` |
| `tombol` | Button | `tampilin tombol "Click" warna ungu` |
| `gambar` | Image | `tampilin gambar "img.jpg" bulat` |
| `badge` | Badge | `tampilin badge "NEW"` |
| `chip` | Chip | `tampilin chip "Python"` |
| `input_teks` | Text Input | `tampilin input_teks "Nama"` |
| `centang` | Checkbox | `tampilin centang "Agree"` |
| `spasi` | Spacer | `tampilin spasi` |
| `pemisah` | Divider | `tampilin pemisah` |

---

## 📝 Form Validation

```python
from pyvibe.forms.validation import FormValidator, required, email, min_length, matches

# Define validation rules
validator = FormValidator({
    "nama": [required(), min_length(3)],
    "email": [required(), email()],
    "password": [required(), min_length(8)],
    "confirm_password": [required(), matches("password")],
})

# Validate data
data = {
    "nama": "An",
    "email": "invalid",
    "password": "123",
    "confirm_password": "456",
}

result = validator.validate(data)
if not result:
    errors = result.get_errors()
    # {"nama": "nama minimal 3 karakter.", "email": "email harus berisi alamat email yang valid."}
```

### Available Validators

| Validator | Description | Example |
|-----------|-------------|---------|
| `required()` | Field wajib diisi | `required()` |
| `email()` | Format email valid | `email()` |
| `min_length(n)` | Panjang minimal | `min_length(3)` |
| `max_length(n)` | Panjang maksimal | `max_length(100)` |
| `min_value(n)` | Nilai minimal | `min_value(0)` |
| `max_value(n)` | Nilai maksimal | `max_value(100)` |
| `phone()` | Nomor telepon ID | `phone()` |
| `url()` | URL valid | `url()` |
| `matches(field)` | Cocok dengan field lain | `matches("password")` |
| `pattern(regex)` | Regex pattern | `pattern(r'^[0-9]+$')` |

---

## 🛣️ Routing

```python
from pyvibe import *

app = App("My Website")

# Static routes
@app.route("/")
def beranda():
    return tampil(judul("Beranda"))

@app.route("/tentang")
def tentang():
    return tampil(judul("Tentang Kami"))

@app.route("/kontak")
def kontak():
    return tampil(judul("Kontak"))

# Dynamic routes
@app.route("/produk/<id>")
def detail_produk(id):
    return tampil(judul(f"Produk #{id}"))

# Multiple methods
@app.route("/api/data", methods=["GET", "POST"])
def api_data():
    return {"data": "hello"}

app.jalan()
```

---

## 📊 State Management

```python
from pyvibe import *

# Create state
state = State(
    nama="Andi",
    umur=20,
    items=[],
)

# Update state
state.nama = "Budi"  # UI otomatis update
state.umur = 21

# Listen to changes
state.on_change("nama", lambda baru, lama: print(f"Nama: {lama} → {baru}"))

# Get state as dict/JSON
print(state.to_dict())  # {"nama": "Budi", "umur": 21, "items": []}
print(state.to_json())  # '{"nama": "Budi", "umur": 21, "items": []}'
```

---

## 🎨 Theming

### CSS Variables

```python
app = App(
    "My Website",
    primary_color="#7C3AED",
    secondary_color="#06B6D4",
)
```

### Dark Mode

```python
from pyvibe.plugins import DarkModePlugin

app = App("My Website")
plugin = DarkModePlugin()
# Add dark mode CSS to your page
```

### Custom Themes

```python
# Use background classes
bagian(bg="gradient-ungu", padding="64px")  # Purple gradient
bagian(bg="gelap", padding="64px")          # Dark background
bagian(bg="terang", padding="64px")         # Light background
```

---

## 🚀 Deployment

### Export to Static Files

```python
app.export("dist")
# Creates dist/ folder with HTML files
```

### Deploy to Vercel

1. Export your app: `app.export("dist")`
2. Push to GitHub
3. Connect to Vercel
4. Set build command: `python app.py`
5. Set output directory: `dist`

### Deploy to Netlify

1. Export your app: `app.export("dist")`
2. Push to GitHub
3. Connect to Netlify
4. Set publish directory: `dist`

### Deploy to GitHub Pages

1. Export your app: `app.export("docs")`
2. Push to GitHub
3. Enable GitHub Pages in Settings
4. Set source to `docs/` folder

---

## 📖 API Reference

### App

```python
app = App(
    name="My App",
    title="My Website",
    description="Website description",
    primary_color="#7C3AED",
    secondary_color="#06B6D4",
    theme="default",
    port=3000,
)

@app.route("/")
def beranda():
    return tampil(...)

app.jalan(port=8080)
app.export("dist")
```

### State

```python
state = State(key1="value1", key2="value2")
state.key1 = "new_value"
state.on_change("key1", callback)
print(state.to_dict())
print(state.to_json())
```

### Components

All components support builder pattern:

```python
judul("Hello").tengah().besar().warna("biru").tebal()
```

### Style Classes

Use CSS utility classes:

```python
# Text
paragraf("Text").class_names.append("pv-text-center")

# Layout
baris().class_names.append("pv-justify-between")

# Colors
tombol("Click").class_names.append("pv-bg-primary")
```

---

## 🤝 Contributing

PyVibe is open source! Contributions welcome.

```bash
git clone https://github.com/pyvibe/pyvibe.git
cd pyvibe
pip install -e .
python examples/01_hello_world.py
```

## 📄 License

MIT License — see [LICENSE](../LICENSE) for details.

---

*Made with ❤️ in Indonesia 🇮🇩*
