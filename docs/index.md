# 🐍 PyVibe Documentation

> **"Gak perlu ribet, yang penting gacor."**

Selamat datang di dokumentasi PyVibe! Framework Python untuk bikin website frontend yang keren, responsive, dan interaktif — pakai Bahasa Indonesia.

---

## 🚀 Mulai Dalam 30 Detik

```bash
# 1. Install PyVibe
pip install pyvibe

# 2. Buat project baru
pyvibe create my-website

# 3. Jalankan
cd my-website
python app.py

# 4. Buka browser
# 🌐 http://localhost:3000
```

---

## 📚 Dokumentasi

### 🎯 Pemula
| Dokumen | Deskripsi |
|---------|-----------|
| [Getting Started](./getting-started.md) | Install, setup, dan project pertama |
| [Natural Language Syntax](./syntax.md) | Tulis kode kayak ngobrol |
| [Komponen Dasar](./components.md#basic) | judul, paragraf, tombol, gambar, dll |

### 🔧 Menengah
| Dokumen | Deskripsi |
|---------|-----------|
| [Semua Komponen](./components.md) | 58 komponen lengkap dengan contoh |
| [Styling & Design System](./styling.md) | CSS classes, themes, responsive |
| [Routing & Navigation](./routing.md) | Multi-page routing |
| [State Management](./state.md) | Reactive state, data binding |

### 🛡️ Lanjutan
| Dokumen | Deskripsi |
|---------|-----------|
| [Keamanan](./security.md) | CSRF, XSS, rate limiting |
| [Deployment](./deployment.md) | Deploy ke Vercel, Netlify, Docker |
| [FAQ & Troubleshooting](./faq.md) | Pertanyaan umum & solusi |

---

## 💡 Contoh Kode Singkat

### Cara 1: Python Biasa
```python
from pyvibe import *

app = App("My Website")

@app.route("/")
def beranda():
    return tampil(
        judul("Selamat Datang!").besar().tengah(),
        paragraf("Ini website pertama gue pakai PyVibe.").tengah(),
        tombol("Mulai Sekarang", warna="biru"),
    )

app.jalan()
```

### Cara 2: Natural Language 🗣️
```python
from pyvibe import *
from pyvibe.nl import *

app = App("My Website")

@app.route("/")
def beranda():
    return tampil(
        *nl(
            'tampilin judul "Selamat Datang!" di tengah',
            'tampilin paragraf "Ini website keren!" di tengah',
            'tampilin tombol "Mulai" warna biru',
        )
    )

app.jalan()
```

---

## 🧩 58 Komponen Siap Pakai

```
Basic (17):    judul, subjudul, paragraf, teks, teks_teal, teks_tipis,
               teks_balik, gambar, tautan, spasi, pemisah, gradien_teks,
               badge, avatar, progress_bar, chip, count_down

Input (10):    tombol, tombol_icon, input_teks, input_angka, input_email,
               input_sandi, textarea, centang, pilihan, unggah_file

Layout (10):   kartu, kartu_stat, kolom, baris, bagian, grid, kontainer,
               spacer, judul_kartu, overlay

Navigation (5): navbar, sidebar, footer, tabs, breadcrumb

Feedback (5):  notifikasi, loader, badge_status, alert, skeleton

Data (4):      tabel, grafik_sederhana, daftar, statistik

Advanced (5):  carousel, accordion, modal, dropdown, tooltip

Extras (11):   stepper, timeline, rating, countdown, typing_effect,
               scroll_to_top, galeri, code_block, markdown,
               empty_state, stat_card
```

---

## ⚡ Quick Links

- 📦 **Install:** `pip install pyvibe`
- 🐙 **GitHub:** github.com/pyvibe/pyvibe
- 💬 **Discord:** discord.gg/pyvibe
- 📧 **Email:** hello@pyvibe.dev

---

## 🏗️ Roadmap

- [x] v0.1.0 — MVP Release (58 components, NL syntax, CLI)
- [ ] v0.2.0 — Backend Integration (SQLite, Auth, API)
- [ ] v0.3.0 — Plugin Ecosystem
- [ ] v0.4.0 — Real-time & WebSocket
- [ ] v1.0.0 — Production Ready

---

Made with ❤️ in Indonesia 🇮🇩
