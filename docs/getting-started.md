# 🚀 Getting Started dengan PyVibe

> Panduan lengkap dari install sampai bikin website pertama lo.

---

## 📋 Prasyarat

Sebelum mulai, pastikan lo udah punya:

| Tool | Minimal | Cek versi |
|------|---------|-----------|
| **Python** | 3.8+ | `python --version` |
| **pip** | 20+ | `pip --version` |
| **Terminal** | Apapun | Terminal, CMD, PowerShell |

> 💡 **Tips:** Kalau belum punya Python, download di [python.org](https://python.org) atau pakai [Anaconda](https://anaconda.com).

---

## 📦 Step 1: Install PyVibe

Buka terminal, lalu jalankan:

```bash
pip install pyvibe
```

Kalau berhasil, lo akan lihat:
```
Successfully installed pyvibe-0.1.0
```

### ✅ Verifikasi Install

```bash
pyvibe version
# Output: 🐍 PyVibe v0.1.0
```

---

## 🆕 Step 2: Buat Project Baru

### Cara Cepat (Recommended)

```bash
pyvibe create my-first-website
```

Ini akan bikin folder `my-first-website/` dengan isi:
```
my-first-website/
├── app.py           # File utama website
├── requirements.txt # List dependencies
├── README.md        # Dokumentasi project
└── .gitignore       # Git ignore rules
```

### Cara Manual

Kalau mau bikin sendiri:

```bash
mkdir my-first-website
cd my-first-website
```

Buat file `app.py`:

```python
"""
🐍 My First Website — Built with PyVibe
"""
from pyvibe import *

app = App("My First Website")

@app.route("/")
def beranda():
    return tampil(
        judul("Halo Dunia! 🌍").besar().tengah(),
        paragraf("Ini website pertama gue pakai PyVibe.").tengah(),
        tombol("Mulai Sekarang", warna="biru"),
    )

app.jalan()
```

---

## ▶️ Step 3: Jalankan Website

```bash
cd my-first-website
python app.py
```

Lo akan lihat output:
```
🐍 PyVibe server running on http://localhost:3000
🔥 Hot reload: ON
```

Buka browser, ketik: **http://localhost:3000**

🎉 **Selamat!** Website lo udah online!

---

## 🎨 Step 4: Explore Fitur

### Edit dan Lihat Perubahan

Buka `app.py`, edit teksnya:

```python
@app.route("/")
def beranda():
    return tampil(
        judul("Halo, Nama Gue! 👋").besar().tengah(),
        paragraf("Gue lagi belajar PyVibe.").tengah(),
        tombol("Lihat Project Gue", warna="hijau"),
    )
```

Save file, lalu refresh browser. Perubahan langsung keliatan!

---

## 🗣️ Step 5: Coba Natural Language

PyVibe punya fitur unik: **Natural Language Syntax**. Lo bisa tulis kode kayak ngobrol!

```python
from pyvibe import *
from pyvibe.nl import *

app = App("NL Demo")

@app.route("/")
def beranda():
    return tampil(
        *nl(
            'tampilin judul "Selamat Datang!" di tengah',
            'tampilin paragraf "Website ini dibuat pakai Bahasa Indonesia!"',
            'tampilin tombol "Klik Saya" warna ungu',
            'tampilin badge "Baru!" warna hijau',
        )
    )

app.jalan()
```

---

## 🎯 Step 6: Buat Website Lengkap

### Contoh: Landing Page

```python
from pyvibe import *

app = App("Landing Page Saya")

@app.route("/")
def beranda():
    return tampil(
        # Navigation
        navbar(
            judul("🚀 BrandGue"),
            tombol("Daftar", warna="biru"),
        ),
        
        # Hero Section
        bagian(
            judul("Bangun Bisnis Digital").besar().tengah(),
            paragraf("Solusi lengkap untuk go digital.").tengah(),
            tombol("Mulai Gratis", warna="biru"),
            padding="96px 0",
            bg="gradient-biru",
        ),
        
        # Features
        bagian(
            judul("Kenapa Pilih Kami?").tengah(),
            grid(
                kartu(judul_kartu("⚡ Cepat"), paragraf("Loading 2 detik.")),
                kartu(judul_kartu("🔒 Aman"), paragraf("Data terenkripsi.")),
                kartu(judul_kartu("💰 Murah"), paragraf("Mulai Rp 0/bulan.")),
                kolom=3,
                gap=24,
            ),
            padding="64px 0",
        ),
        
        # Footer
        footer(
            paragraf("© 2026 BrandGue. Made with 🐍 PyVibe").tengah(),
        ),
    )

app.jalan()
```

---

## 🛠️ Step 7: CLI Commands

PyVibe punya CLI tool yang powerful:

```bash
# Buat project baru
pyvibe create my-site

# Lihat semua komponen
pyvibe components

# Lihat semua template
pyvibe templates

# Jalankan dev server
pyvibe dev

# Build untuk production
pyvibe build

# Lihat versi
pyvibe version
```

---

## 📁 Struktur Project

```
my-first-website/
├── app.py              # File utama (routes + pages)
├── components/         # Custom components (opsional)
│   └── __init__.py
├── static/             # Static files (opsional)
│   ├── css/
│   ├── js/
│   └── images/
├── templates/          # HTML templates (opsional)
├── requirements.txt    # Dependencies
├── README.md          # Project documentation
└── .gitignore         # Git ignore rules
```

---

## 🎨 Tips & Tricks

### 1. Builder Pattern (Chainable)
```python
# Lo bisa chain method untuk styling
judul("Hello").besar().tengah().warna("biru")
tombol("Click").lebar("full")
paragraf("Text").tebal().warna("merah")
```

### 2. Layout Helper
```python
# Grid layout gampang
grid(kartu1, kartu2, kartu3, kolom=3)

# Flex layout
baris(kolom1, kolom2).justify("between").items("center")

# Container
kontainer(konten, max_width="1200px")
```

### 3. Color Shortcuts
```python
# Warna yang tersedia:
# biru, merah, hijau, kuning, ungu, cyan, pink, abu
tombol("Click", warna="biru")
paragraf("Text").warna("merah")
badge("New", warna="hijau")
```

### 4. Responsive Grid
```python
# Responsive columns
grid(kartu1, kartu2, kartu3, kolom=3)  # Auto responsive

# Manual columns
baris(
    kolom(8, konten_utama),
    kolom(4, sidebar),
)
```

---

## ❓ Troubleshooting

### "ModuleNotFoundError: No module named 'pyvibe'"
```bash
pip install pyvibe
# atau
pip install --upgrade pyvibe
```

### "Port 3000 sudah digunakan"
```python
app.jalan(port=8000)  # Ganti port
```

### "Website gak keliatan responsive"
Pastikan lo pake `<meta name="viewport">` (otomatis ditambah PyVibe).

---

## 📚 Langkah Selanjutnya

1. **[Natural Language Syntax](./syntax.md)** — Tulis kode kayak ngobrol
2. **[Komponen Reference](./components.md)** — 58 komponen lengkap
3. **[Styling Guide](./styling.md)** — Design system & themes
4. **[Routing Guide](./routing.md)** — Multi-page routing

---

Made with ❤️ in Indonesia 🇮🇩
