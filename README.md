# 🐍 PyVibe

> **Build frontend websites in Python as easy as chatting.**
> *"Gak perlu ribet, yang penting gacor."*

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/Version-0.1.0-7C3AED?style=flat-square)](https://pypi.org/project/pyvibe)

---

## 🚀 Quick Start

```bash
# Install PyVibe
pip install pyvibe

# Create new project
pyvibe create my-website

# Start development server
cd my-website
python app.py

# Open browser
open http://localhost:3000
```

## 💡 Why PyVibe?

| Pain Point | PyVibe Solution |
|------------|-----------------|
| Kodenya ribet & banyak | Syntax natural, 3 baris udah jadi website |
| Error susah dimengerti | Error message Bahasa Indonesia |
| Setup ribet | Zero config, `pip install` langsung jalan |
| Ga tau mulai dari mana | Dokumentasi storytelling, interactive playground |
| Responsive susah | Semua komponen auto responsive |

## 📝 Syntax

PyVibe mendukung 3 gaya syntax:

### Gaya 1: Natural Language 🗣️

```python
tampilin judul "Selamat Datang" di tengah
tampilin paragraf "Halo, ini website gue."
tampilin tombol "Klik Saya" warna ungu
```

### Gaya 2: OOP Pythonic 🐍

```python
from pyvibe import *

app = App("My Website")

@app.route("/")
def beranda():
    return tampil(
        judul("Selamat Datang", level=1),
        paragraf("Halo, ini website gue."),
        tombol("Klik Saya", warna="ungu"),
    )

app.jalan()
```

### Gaya 3: Hybrid 🔀

```python
from pyvibe import *

app = App("Toko Gacor")

@app.route("/")
def beranda():
    return tampil(
        navbar(logo="🛍️ Toko", menu=["Beranda", "Produk"]),
        bagian(
            judul("Toko Gacor").besar().tengah(),
            grid(
                kartu(gambar("produk1.jpg"), heading("Nike"), harga("Rp 1.2M")),
                kartu(gambar("produk2.jpg"), heading("Adidas"), harga("Rp 900K")),
                kolom=2, gap="24px",
            ),
        ),
        footer(copyright="© 2026 Toko Gacor"),
    )

app.jalan()
```

## 🧩 Components

### Basic
```python
judul("Heading")           # <h1>
subjudul("Sub Heading")    # <h2>
paragraf("Text")           # <p>
teks("Inline")             # <span>
gambar("img.jpg")          # <img>
tautan("Link", url="/")    # <a>
ikon("🚀")                 # <span>🚀</span>
badge("NEW")               # Badge label
chip("Python")             # Chip/tag
```

### Input
```python
input_teks(label="Nama")       # Text input
input_angka(label="Harga")     # Number input
input_email(label="Email")     # Email input
input_sandi(label="Password")  # Password input
textarea(label="Deskripsi")    # Textarea
centang("Setuju")              # Checkbox
pilihan("Kota", [...])         # Select dropdown
tombol("Submit")               # Button
```

### Layout
```python
kartu(content)             # Card
kolom(6, content)          # Column (6/12)
baris(col1, col2)          # Row/Flexbox
bagian(content)            # Section
grid(c1, c2, c3, kolom=3) # CSS Grid
kontainer(content)         # Max-width container
```

### Navigation
```python
navbar(logo, menu)         # Navigation bar
sidebar(items)             # Sidebar
footer(teks, links)        # Footer
tabs(tab1, tab2)           # Tab navigation
breadcrumb("A", "B", "C") # Breadcrumb
```

### Data
```python
tabel(data, kolom=[...])   # Data table
grafik_sederhana(data)     # Simple bar chart
daftar("A", "B", "C")     # List
statistik([{...}])         # Stats grid
```

### Feedback
```python
notifikasi("Berhasil!", tipe="sukses")  # Toast
alert("Info penting", tipe="info")      # Alert
loader()                                 # Loading spinner
skeleton()                              # Skeleton loader
```

### Advanced
```python
carousel(img1, img2)       # Image carousel
accordion(item1, item2)    # Collapsible sections
modal(judul, content)      # Modal dialog
dropdown(trigger, items)   # Dropdown menu
```

## 🎨 Styling

All components support chainable styling:

```python
judul("Hello").tengah().besar().warna("biru")
paragraf("Text").tebal().warna("abu")
tombol("Click").bg("hijau").bulat("16px")
kartu(content).bayangan("lg").lebar("100%")
```

### Style Methods

| Method | Description | Example |
|--------|-------------|---------|
| `.warna("biru")` | Text color | `.warna("merah")` |
| `.bg("gelap")` | Background | `.bg("gradient-ungu")` |
| `.besar()` | Font size | `.ukuran("kecil")` |
| `.tebal()` | Bold text | `.tipis()` |
| `.tengah()` | Center align | `.kiri()`, `.kanan()` |
| `.bulat()` | Border radius | `.bulat("16px")` |
| `.bayangan()` | Box shadow | `.bayangan("lg")` |
| `.padding("24px")` | Padding | `.margin("16px")` |

## 🎯 Examples

Check out the `examples/` directory:

```bash
# Hello World
python examples/01_hello_world.py

# Landing Page
python examples/02_landing_page.py

# Dashboard Admin
python examples/03_dashboard.py
```

## 🤝 Contributing

PyVibe is open source! Contributions are welcome.

```bash
git clone https://github.com/pyvibe/pyvibe.git
cd pyvibe
pip install -e .
python examples/01_hello_world.py
```

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

*Made with ❤️ in Indonesia 🇮🇩*
