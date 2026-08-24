# 🧩 Komponen Reference

> Panduan lengkap semua 58 komponen PyVibe dengan contoh kode.

---

## 📋 Daftar Isi

1. [Basic Components (17)](#basic-components)
2. [Input Components (10)](#input-components)
3. [Layout Components (10)](#layout-components)
4. [Navigation Components (5)](#navigation-components)
5. [Feedback Components (5)](#feedback-components)
6. [Data Components (4)](#data-components)
7. [Advanced Components (5)](#advanced-components)
8. [Extras Components (11)](#extras-components)

---

## Basic Components

### `judul(teks, **kwargs)`
Heading h1.

```python
judul("Selamat Datang")
judul("Title").besar()
judul("Centered").tengah()
judul("Colored").warna("biru")
judul("Bold").tebal()
```

| Parameter | Tipe | Default | Deskripsi |
|-----------|------|---------|-----------|
| `teks` | str | - | Teks heading |
| `size` | str | "lg" | ukuran: sm, md, lg, xl |

---

### `subjudul(teks, **kwargs)`
Heading h2.

```python
subjudul("Sub Judul")
subjudul("Centered").tengah()
```

---

### `paragraf(teks, **kwargs)`
Paragraph text.

```python
paragraf("Ini adalah paragraf.")
paragraf("Centered text").tengah()
paragraf("Small text").kecil()
paragraf("Colored").warna("abu")
paragraf("Italic").miring()
```

---

### `teks(teks, **kwargs)`
Inline text span.

```python
teks("Inline text")
teks("Bold").tebal()
teks("Colored").warna("merah")
```

---

### `teks_teal(teks, **kwargs)`
Teal colored text.

```python
teks_teal("Teks teal")
```

---

### `teks_tipis(teks, **kwargs)`
Thin/light weight text.

```python
teks_tipis("Thin text")
```

---

### `teks_balik(teks, **kwargs)`
Flip/rotate text effect.

```python
teks_balik("Flipped!")
```

---

### `gambar(src, **kwargs)`
Image component.

```python
gambar("photo.jpg")
gambar("profile.png").bulat()
gambar("banner.jpg").lebar("full")
gambar("icon.svg").ukuran("32px")
```

| Parameter | Tipe | Default | Deskripsi |
|-----------|------|---------|-----------|
| `src` | str | - | Image source URL |
| `alt` | str | "" | Alt text |
| `width` | str | - | Width |
| `height` | str | - | Height |

---

### `tautan(teks, url="#", **kwargs)`
Link/anchor component.

```python
tautan("Klik di sini")
tautan("Google", "https://google.com")
tautan("External", "https://example.com").target("_blank")
```

---

### `spasi(tinggi="24px")`
Spacing/blank space.

```python
spasi()
spasi("16px")
spasi("48px")
```

---

### `pemisah()`
Horizontal divider/separator.

```python
pemisah()
```

---

### `gradien_teks(teks, **kwargs)`
Gradient text effect.

```python
gradien_teks("Gradient Text!")
```

---

### `badge(teks, **kwargs)`
Badge/label component.

```python
badge("NEW")
badge("Baru!", warna="hijau")
badge("Sale", warna="merah")
badge("Pro", warna="ungu")
```

**Warna:** biru, merah, hijau, kuning, ungu, cyan, pink, abu

---

### `avatar(nama, **kwargs)`
User avatar with initials.

```python
avatar("Budi")
avatar("Sari", size="lg")
avatar("Andi", size="sm")
```

| Parameter | Tipe | Default | Deskripsi |
|-----------|------|---------|-----------|
| `nama` | str | - | Nama user |
| `size` | str | "md" | ukuran: sm, md, lg |

---

### `progress_bar(persen, **kwargs)`
Progress bar.

```python
progress_bar(75)
progress_bar(50).warna("hijau")
progress_bar(90).warna("biru")
```

---

### `chip(teks, **kwargs)`
Chip/tag component.

```python
chip("Python")
chip("JavaScript")
chip("React").warna("biru")
```

---

### `count_down(detik, **kwargs)`
Countdown timer display.

```python
count_down(60)
count_down(300)
```

---

## Input Components

### `tombol(teks, **kwargs)`
Button component.

```python
tombol("Klik Saya")
tombol("Primary", warna="biru")
tombol("Success", warna="hijau")
tombol("Danger", warna="merah")
tombol("Warning", warna="kuning")
tombol("Purple", warna="ungu")
tombol("Outline", warna="outline")
tombol("Full Width", lebar="full")
```

**Warna:** biru, merah, hijau, kuning, ungu, cyan, pink, outline

---

### `tombol_icon(icon, tooltip="", **kwargs)`
Icon button.

```python
tombol_icon("🔔")
tombol_icon("❤️", tooltip="Like")
```

---

### `input_teks(label, **kwargs)`
Text input field.

```python
input_teks("Nama Lengkap")
input_teks("Username", placeholder="Masukkan username")
input_teks("Email", required=True)
```

---

### `input_angka(label, **kwargs)`
Number input field.

```python
input_angka("Usia")
input_angka("Jumlah", min=0, max=100)
```

---

### `input_email(label, **kwargs)`
Email input field.

```python
input_email("Email Address")
input_email("Email", placeholder="email@contoh.com")
```

---

### `input_sandi(label, **kwargs)`
Password input field.

```python
input_sandi("Password")
input_sandi("Kata Sandi", placeholder="Masukkan password")
```

---

### `textarea(label, **kwargs)`
Textarea/multiline input.

```python
textarea("Pesan")
textarea("Komentar", rows=4, placeholder="Tulis komentar...")
```

---

### `centang(label, **kwargs)`
Checkbox.

```python
centang("Saya setuju")
centang("Remember me")
```

---

### `pilihan(label, options, **kwargs)`
Select/dropdown input.

```python
pilihan("Pilih Kategori", ["Makanan", "Minuman", "Lainnya"])
pilihan("Kota", ["Jakarta", "Bandung", "Surabaya"])
```

---

### `unggah_file(**kwargs)`
File upload input.

```python
unggah_file()
unggah_file(label="Upload Foto", accept="image/*")
```

---

## Layout Components

### `kartu(*children, **kwargs)`
Card container.

```python
kartu(paragraf("Ini kartu sederhana."))
kartu(
    judul("Card Title"),
    paragraf("Card content here."),
    tombol("Action"),
    padding="24px",
    border="1px solid #374151",
    radius="12px",
)
```

---

### `kartu_stat(judul, nilai, perubahan, **kwargs)`
Statistics card.

```python
kartu_stat("Total Users", "1,234", "+12%")
kartu_stat("Revenue", "Rp 45M", "+8%")
```

---

### `kolom(lebar, *children, **kwargs)`
Column in grid layout (1-12 grid system).

```python
kolom(6, paragraf("50% width"))
kolom(4, paragraf("33% width"))
kolom(12, paragraf("100% width"))
```

---

### `baris(*children, **kwargs)`
Row/flex container.

```python
baris(kolom1, kolom2)
baris(kolom1, kolom2).gap(4)
baris(kolom1, kolom2).justify("between")
baris(kolom1, kolom2).items("center")
```

---

### `bagian(*children, **kwargs)`
Section container with padding.

```python
bagian(
    judul("Section Title"),
    paragraf("Section content."),
    padding="64px 0",
)
```

---

### `grid(*children, kolom=3, gap=16, **kwargs)`
Grid layout.

```python
grid(kartu1, kartu2, kartu3, kolom=3)
grid(kartu1, kartu2, kolom=2, gap=24)
```

---

### `kontainer(*children, **kwargs)`
Content container with max-width.

```python
kontainer(konten)
kontainer(konten, max_width="1200px")
kontainer(konten, padding="0 24px")
```

---

### `spacer(height="24px")`
Spacer element.

```python
spacer()
spacer("48px")
```

---

### `judul_kartu(teks, **kwargs)`
Card header/title.

```python
judul_kartu("Card Title")
judul_kartu("Section Header")
```

---

### `overlay(**kwargs)`
Overlay container.

```python
overlay()
```

---

## Navigation Components

### `navbar(*children, **kwargs)`
Navigation bar.

```python
navbar(
    judul("My App"),
    baris(
        tautan("Home"),
        tautan("About"),
        tautan("Contact"),
    ),
    tombol("Login", warna="biru"),
)
```

---

### `sidebar(judul, items, **kwargs)`
Sidebar navigation.

```python
sidebar(
    "Menu",
    "Dashboard",
    "Users",
    "Settings",
    judul="My App",
)
```

---

### `footer(*children, **kwargs)`
Page footer.

```python
footer(
    paragraf("© 2026 My App").tengah(),
)
```

---

### `tabs(items, **kwargs)`
Tab navigation.

```python
tabs(["Tab 1", "Tab 2", "Tab 3"])
```

---

### `breadcrumb(items, **kwargs)`
Breadcrumb navigation.

```python
breadcrumb(["Home", "Products", "Detail"])
```

---

## Feedback Components

### `notifikasi(teks, **kwargs)`
Notification/toast.

```python
notifikasi("Message sent!")
notifikasi("Error!", warna="merah")
```

---

### `loader(**kwargs)`
Loading spinner.

```python
loader()
```

---

### `badge_status(teks, warna, **kwargs)`
Status badge.

```python
badge_status("Active", "green")
badge_status("Pending", "yellow")
badge_status("Inactive", "red")
```

---

### `alert(teks, **kwargs)`
Alert message.

```python
alert("Warning! Check your input.")
alert("Success! Data saved.", warna="hijau")
```

---

### `skeleton(**kwargs)`
Skeleton loading placeholder.

```python
skeleton()
```

---

## Data Components

### `tabel(data, kolom, **kwargs)`
Data table.

```python
tabel(
    [{"nama": "Budi", "email": "budi@mail.com"}],
    kolom=["nama", "email"],
)
```

---

### `grafik_sederhana(data, **kwargs)`
Simple bar chart.

```python
grafik_sederhana([
    {"label": "Jan", "value": 100},
    {"label": "Feb", "value": 200},
    {"label": "Mar", "value": 150},
])
```

---

### `daftar(items, **kwargs)`
List component.

```python
daftar(["Item 1", "Item 2", "Item 3"])
```

---

### `statistik(items, **kwargs)`
Statistics grid.

```python
statistik([
    {"judul": "Views", "nilai": "10,000", "ikon": "👁️"},
    {"judul": "Likes", "nilai": "5,000", "ikon": "❤️"},
])
```

---

## Advanced Components

### `carousel(items, **kwargs)`
Image/content carousel.

```python
carousel([gambar1, gambar2, gambar3])
```

---

### `accordion(*items, **kwargs)`
Collapsible/accordion. Items must be tuples of (title, content).

```python
accordion(
    ("Pertanyaan 1", "Jawaban 1"),
    ("Pertanyaan 2", "Jawaban 2"),
)
```

---

### `modal(judul, *children, **kwargs)`
Modal dialog.

```python
modal(
    "Konfirmasi",
    paragraf("Yakin ingin menghapus?"),
    tombol("Ya, Hapus", warna="merah"),
)
```

---

### `dropdown(label, items, **kwargs)`
Dropdown menu.

```python
dropdown("Menu", ["Profile", "Settings", "Logout"])
```

---

### `tooltip(content, teks, **kwargs)`
Tooltip on hover.

```python
tooltip(tombol("Hover me"), "Ini tooltip!")
```

---

## Extras Components

### `stepper(steps, aktif=0, **kwargs)`
Step/wizard progress indicator.

```python
stepper(["Info Dasar", "Upload", "Konfirmasi"], aktif=1)
```

---

### `timeline(*items, **kwargs)`
Timeline component.

```python
timeline(
    {"tanggal": "24 Agustus", "judul": "Project Start", "isi": "Mulai development."},
    {"tanggal": "25 Agustus", "judul": "Alpha Release", "isi": "Release versi alpha."},
)
```

---

### `rating(bintang=5, max_bintang=5, **kwargs)`
Star rating.

```python
rating(bintang=4)
rating(bintang=5, warna="#F97316")
```

---

### `countdown(detik, label="Tersisa", **kwargs)`
Countdown timer.

```python
countdown(300, label="Waktu tersisa")
```

---

### `typing_effect(texts, speed=100, **kwargs)`
Typing animation effect.

```python
typing_effect(["Halo!", "Selamat Datang", "di PyVibe"])
```

---

### `scroll_to_top(**kwargs)`
Scroll to top button.

```python
scroll_to_top()
```

---

### `gambar(images, kolom=3, **kwargs)`
Image gallery.

```python
galeri(["img1.jpg", "img2.jpg", "img3.jpg"], kolom=3)
```

---

### `code_block(kode, bahasa="python", **kwargs)`
Code block with syntax highlighting.

```python
code_block('print("Hello World")', bahasa="python")
```

---

### `markdown(content, **kwargs)`
Simple markdown renderer.

```python
markdown("# Hello\\n\\nThis is **bold** and *italic*.")
```

---

### `empty_state(judul, deskripsi, icon, **kwargs)`
Empty state placeholder.

```python
empty_state("Belum ada data", "Buat data pertama kamu!", icon="📭")
```

---

### `stat_card(icon, nilai, label, **kwargs)`
Stat card alternative.

```python
stat_card("👥", "1,234", "Users")
stat_card("💰", "Rp 45M", "Revenue", perubahan="+8%")
```

---

## 🎨 Style Methods (Builder Pattern)

Semua komponen mendukung **builder pattern** untuk styling:

```python
# Alignment
judul("Hello").tengah()    # Center
judul("Hello").kiri()      # Left
judul("Hello").kanan()     # Right

# Size
judul("Hello").besar()     # Large
judul("Hello").kecil()     # Small

# Color
judul("Hello").warna("biru")
tombol("Click").warna("merah")

# Font weight
judul("Hello").tebal()     # Bold

# Width
tombol("Click").lebar("full")

# Border
kartu(content).bulat()     # Rounded
kartu(content).border()    # Border
kartu(content).bayangan()  # Shadow

# Grid
grid(c1, c2, c3, kolom=3, gap=24)
baris(c1, c2).gap(4).justify("between").items("center")

# Container
kontainer(content, max_width="1200px")
bagian(content, padding="64px 0")
```

---

Made with ❤️ in Indonesia 🇮🇩
