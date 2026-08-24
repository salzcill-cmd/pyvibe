# 🗣️ Natural Language Syntax

> Tulis kode Python kayak lo lagi ngobrol. PyVibe convert otomatis!

---

## 💡 Konsep

PyVibe punya fitur unik: **Natural Language Parser**. Lo bisa nulis komponen pakai bahasa sehari-hari, dan PyVibe convert ke kode Python yang valid.

```python
# Lo tulis kayak gini:
tampilin judul "Halo Dunia" di tengah

# PyVibe convert ke:
judul("Halo Dunia").tengah()
```

---

## 🔑 Kata Kunci yang Tersedia

| Kata Kunci | Fungsi | Contoh |
|------------|--------|--------|
| `tampilin` | Tampilkan komponen | `tampilin judul "Hello"` |
| `judul` | Heading (h1) | `tampilin judul "Title"` |
| `paragraf` | Paragraph text | `tampilin paragraf "Text"` |
| `tombol` | Button | `tampilin tombol "Click"` |
| `gambar` | Image | `tampilin gambar "photo.jpg"` |
| `badge` | Badge/label | `tampilin badge "NEW"` |
| `chip` | Chip/tag | `tampilin chip "Python"` |
| `input_teks` | Text input | `tampilin input_teks "Nama"` |
| `centang` | Checkbox | `tampilin centang "Setuju"` |
| `spasi` | Spacing | `tampilin spasi` |
| `pemisah` | Divider | `tampilin pemisah` |

---

## 🎨 Modifiers (Pengubah)

### Alignment
| Modifier | Fungsi | Contoh |
|----------|--------|--------|
| `di tengah` | Center align | `tampilin judul "Hello" di tengah` |
| `di kiri` | Left align | `tampilin judul "Hello" di kiri` |
| `di kanan` | Right align | `tampilin judul "Hello" di kanan` |

### Colors
| Modifier | Fungsi | Contoh |
|----------|--------|--------|
| `warna [warna]` | Set color | `tampilin tombol "Click" warna biru` |
| `bg [warna]` | Background color | `tampilin bagian bg ungu` |

**Warna yang tersedia:** biru, merah, hijau, kuning, ungu, cyan, pink, abu

### Size
| Modifier | Fungsi | Contoh |
|----------|--------|--------|
| `besar` | Large size | `tampilin judul "Title" besar` |
| `kecil` | Small size | `tampilin judul "Title" kecil` |

### Style
| Modifier | Fungsi | Contoh |
|----------|--------|--------|
| `tebal` | Bold text | `tampilin judul "Title" tebal` |
| `miring` | Italic text | `tampilin paragraf "Text" miring` |
| `bulat` | Rounded | `tampilin gambar "img.jpg" bulat` |

---

## 📝 Contoh Lengkap

### 1. Judul Sederhana
```python
# Natural Language
tampilin judul "Selamat Datang!" di tengah

# Hasil Python
judul("Selamat Datang!").tengah()
```

### 2. Tombol dengan Warna
```python
# Natural Language
tampilin tombol "Mulai Sekarang" warna biru

# Hasil Python
tombol("Mulai Sekarang", warna="biru")
```

### 3. Badge
```python
# Natural Language
tampilin badge "Baru!" warna hijau

# Hasil Python
badge("Baru!", warna="hijau")
```

### 4. Input Form
```python
# Natural Language
tampilin input_teks "Nama Lengkap"
tampilin input_email "Email"
tampilin centang "Saya setuju dengan syarat"

# Hasil Python
input_teks("Nama Lengkap")
input_email("Email")
centang("Saya setuju dengan syarat")
```

### 5. Gambar Bulat
```python
# Natural Language
tampilin gambar "profile.jpg" bulat

# Hasil Python
gambar("profile.jpg").bulat()
```

### 6. Paragraf Tengah
```python
# Natural Language
tampilin paragraf "Ini paragraf yang di tengah." di tengah

# Hasil Python
paragraf("Ini paragraf yang di tengah.").tengah()
```

---

## 🔧 Cara Pakai

### Method 1: Langsung dalam `tampil()`

```python
from pyvibe import *
from pyvibe.nl import nl

app = App("My Website")

@app.route("/")
def beranda():
    return tampil(
        *nl(
            'tampilin judul "Selamat Datang!" di tengah',
            'tampilin paragraf "Ini website gue." di tengah',
            'tampilin tombol "Klik Saya" warna ungu',
            'tampilin badge "NEW" warna hijau',
        )
    )

app.jalan()
```

### Method 2: Convert ke Python Code

```python
from pyvibe.parser.natural import nl

# Convert satu baris
code = nl('tampilin judul "Hello" di tengah')
print(code)  # Output: judul("Hello").tengah()

# Convert banyak baris
lines = [
    'tampilin judul "Hello"',
    'tampilin paragraf "World"',
    'tampilin tombol "Click" warna biru',
]

for line in lines:
    print(nl(line))
```

### Method 3: Jalankan Langsung

```python
from pyvibe.nl import *

# Jalankan NL syntax langsung
tampilin_judul("Hello", tengah=True)
tampilin_paragraf("World")
tampilin_tombol("Click", warna="biru")
```

---

## 🎯 Cheat Sheet

```
KOMPOEN        SYNTAX NL                        HASIL PYTHON
─────────────────────────────────────────────────────────────
Judul          tampilin judul "Hello"            judul("Hello")
               tampilin judul "Hello" di tengah  judul("Hello").tengah()
               tampilin judul "Hello" besar      judul("Hello").besar()

Paragraf       tampilin paragraf "Text"          paragraf("Text")
               tampilin paragraf "Text" di tengah paragraf("Text").tengah()

Tombol         tampilin tombol "Click"           tombol("Click")
               tampilin tombol "Click" warna biru tombol("Click", warna="biru")

Gambar         tampilin gambar "img.jpg"         gambar("img.jpg")
               tampilin gambar "img.jpg" bulat   gambar("img.jpg").bulat()

Badge          tampilin badge "NEW"              badge("NEW")
               tampilin badge "NEW" warna hijau  badge("NEW", warna="hijau")

Input          tampilin input_teks "Nama"        input_teks("Nama")
               tampilin centang "Setuju"         centang("Setuju")

Layout         tampilin spasi                    spasi()
               tampilin pemisah                  pemisah()
```

---

## 💡 Tips

### 1. Gabungkan Multiple NL
```python
return tampil(
    *nl(
        'tampilin judul "Header" di tengah',
        'tampilin paragraf "Body text"',
        'tampilin tombol "Action"',
    )
)
```

### 2. Mix NL dengan Python Code
```python
return tampil(
    *nl('tampilin judul "Hello" di tengah'),
    paragraf("Ini kode Python biasa."),
    tombol("Click", warna="biru"),
)
```

### 3. Loop dengan NL
```python
items = ["Python", "JavaScript", "Go", "Rust"]

komponen = []
for item in items:
    komponen.extend(nl(f'tampilin chip "{item}"'))

return tampil(*komponen)
```

---

## ⚠️ Limitasi

1. **Nested components** — Belum support untuk nest complex components
2. **Custom styling** — Untuk styling advance, pakai Python code langsung
3. **Event handling** — Pakai Python code untuk onclick, dll

---

## 📚 Selanjutnya

- [Komponen Reference](./components.md) — Detail semua komponen
- [Styling Guide](./styling.md) — Design system lengkap

---

Made with ❤️ in Indonesia 🇮🇩
