# 🎨 Styling & Design System

> Panduan lengkap styling, themes, responsive design, dan animations di PyVibe.

---

## 📋 Daftar Isi

1. [Builder Pattern](#builder-pattern)
2. [CSS Classes](#css-classes)
3. [Colors & Themes](#colors--themes)
4. [Responsive Design](#responsive-design)
5. [Animations](#animations)
6. [Dark Mode](#dark-mode)
7. [Custom Styling](#custom-styling)

---

## Builder Pattern

PyVibe pakai **builder pattern** yang chainable. Lo bisa style komponen dengan method chaining:

```python
# Chaining style methods
judul("Hello").besar().tengah().warna("biru").tebal()

# Chain multiple methods
paragraf("Text")
    .tengah()
    .warna("abu")
    .besar()

# Layout helpers
baris(kolom1, kolom2)
    .gap(4)
    .justify("between")
    .items("center")

# Grid
grid(kartu1, kartu2, kartu3)
    .kolom(3)
    .gap(24)
```

### Style Methods Reference

| Method | Fungsi | Contoh |
|--------|--------|--------|
| `.tengah()` | Center align | `.tengah()` |
| `.kiri()` | Left align | `.kiri()` |
| `.kanan()` | Right align | `.kanan()` |
| `.besar()` | Large size | `.besar()` |
| `.kecil()` | Small size | `.kecil()` |
| `.tebal()` | Bold | `.tebal()` |
| `.miring()` | Italic | `.miring()` |
| `.warna(color)` | Text color | `.warna("biru")` |
| `.lebar(width)` | Width | `.lebar("full")` |
| `.bulat()` | Rounded border | `.bulat()` |
| `.bayangan()` | Box shadow | `.bayangan()` |
| `.border()` | Add border | `.border()` |

---

## CSS Classes

PyVibe generate CSS classes otomatis. Lo bisa pakai class-name langsung:

### Utility Classes

```
Text:      pv-text-sm, pv-text-md, pv-text-lg, pv-text-xl, pv-text-bold
Color:     pv-text-primary, pv-text-secondary, pv-text-gray
Bg:        pv-bg-primary, pv-bg-secondary, pv-bg-dark
Padding:   pv-p-4, pv-p-8, pv-p-12, pv-p-16, pv-p-24, pv-p-32
Margin:    pv-m-4, pv-m-8, pv-m-12, pv-m-16, pv-m-24, pv-m-32
Gap:       pv-gap-2, pv-gap-4, pv-gap-6, pv-gap-8
```

### Layout Classes

```
Flex:      pv-flex, pv-flex-col, pv-flex-row
Grid:      pv-grid, pv-grid-2, pv-grid-3, pv-grid-4
Align:     pv-items-center, pv-items-start, pv-items-end
Justify:   pv-justify-between, pv-justify-center, pv-justify-start
```

### Component Classes

```
Button:    pv-btn, pv-btn-primary, pv-btn-secondary, pv-btn-ghost
Card:      pv-card, pv-card-hover, pv-card-bordered
Input:     pv-input, pv-input-lg, pv-input-sm
Badge:     pv-badge, pv-badge-primary, pv-badge-success
Alert:     pv-alert, pv-alert-info, pv-alert-success, pv-alert-warning, pv-alert-danger
```

---

## Colors & Themes

### Default Colors

| Nama | Hex | Deskripsi |
|------|-----|-----------|
| `biru` | `#3B82F6` | Primary blue |
| `merah` | `#EF4444` | Error/danger |
| `hijau` | `#22C55E` | Success |
| `kuning` | `#EAB308` | Warning |
| `ungu` | `#7C3AED` | Purple accent |
| `cyan` | `#06B6D4` | Cyan accent |
| `pink` | `#EC4899` | Pink accent |
| `abu` | `#6B7280` | Gray |

### Gradient Backgrounds

```python
bagian(bg="gradient-biru")    # Blue gradient
bagian(bg="gradient-ungu")    # Purple gradient
bagian(bg="gradient-hijau")   # Green gradient
bagian(bg="gradient-kuning")  # Yellow gradient
```

### Color Shortcuts in Components

```python
# Button colors
tombol("Click", warna="biru")
tombol("Click", warna="merah")
tombol("Click", warna="hijau")
tombol("Click", warna="ungu")

# Badge colors
badge("NEW", warna="hijau")
badge("SALE", warna="merah")

# Text colors
paragraf("Text").warna("biru")
judul("Title").warna("ungu")
```

---

## Responsive Design

PyVibe auto-generate responsive CSS. Semua komponen responsive by default!

### Breakpoints

| Breakpoint | Width | Device |
|------------|-------|--------|
| Desktop | > 1024px | Laptop, Desktop |
| Tablet | 768px - 1024px | Tablet |
| Mobile | < 768px | HP |

### Responsive Grid

```python
# Auto responsive grid
grid(kartu1, kartu2, kartu3, kolom=3)
# → 3 columns on desktop, 2 on tablet, 1 on mobile

# Manual responsive
baris(
    kolom(8, konten_utama),   # 66% on desktop
    kolom(4, sidebar),        # 33% on desktop
)
# → Stacks on mobile
```

### Responsive Navigation

```python
# Navbar otomatis responsive
navbar(
    judul("My App"),
    baris(
        tautan("Home"),
        tautan("About"),
        tautan("Contact"),
    ),
    tombol("Login"),
)
# → Menu hamburger on mobile
```

---

## Animations

PyVibe support berbagai animation presets:

### Built-in Animations

```python
# Fade in
paragraf("Fade In").animate("fade-in")

# Slide in
kartu(content).animate("slide-up")

# Bounce
tombol("Bounce").animate("bounce")

# Pulse
loader().animate("pulse")

# Spin
loader().animate("spin")
```

### Animation on Scroll

```python
# Animasi muncul saat scroll
bagian(
    judul("Appear on scroll").animate("fade-in"),
    paragraf("Slide up when visible").animate("slide-up"),
)
```

### Hover Effects

```python
# Hover scale
kartu(content).hover("scale")

# Hover shadow
kartu(content).hover("shadow")

# Hover color
tombol("Hover me").hover("color")
```

---

## Dark Mode

PyVibe built-in dark mode support!

### Activate Dark Mode

```python
app = App("My Website", theme="gelap")
```

### Toggle Dark Mode

```python
# Add dark mode toggle button
tombol("🌙 Dark Mode", onclick="toggleDarkMode()")
```

### Dark Mode CSS

```css
/* PyVibe auto-generates dark mode CSS */
:root {
    --pv-bg-primary: #ffffff;
    --pv-text-primary: #111827;
}

[data-theme="dark"] {
    --pv-bg-primary: #111827;
    --pv-text-primary: #ffffff;
}
```

---

## Custom Styling

### Inline Styles

```python
paragraf("Custom style").style("color: red; font-size: 20px;")
kartu(content).style("background: linear-gradient(45deg, #667eea, #764ba2)")
```

### Custom CSS Classes

```python
# Add custom class
paragraf("Text").class_name("my-custom-class")

# Multiple classes
tombol("Click").class_name("btn-primary btn-lg")
```

### CSS Variables

```python
# Use CSS variables
paragraf("Themed text").style("color: var(--pv-text-primary)")
bagian(content).style("background: var(--pv-bg-secondary)")
```

---

## 🎨 Design Tokens

### Spacing Scale

```
4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px, 96px
```

### Font Sizes

```
xs:   12px
sm:   14px
md:   16px
lg:   18px
xl:   24px
2xl:  30px
3xl:  36px
```

### Border Radius

```
sm:   4px
md:   8px
lg:   12px
xl:   16px
2xl:  24px
full: 9999px (pill shape)
```

### Shadows

```
sm:   0 1px 2px rgba(0,0,0,0.05)
md:   0 4px 6px rgba(0,0,0,0.1)
lg:   0 10px 15px rgba(0,0,0,0.1)
xl:   0 20px 25px rgba(0,0,0,0.15)
```

---

## 📱 Responsive Examples

### Mobile-First Layout

```python
app = App("Mobile First")

@app.route("/")
def beranda():
    return tampil(
        # Mobile: 1 column, Desktop: 3 columns
        grid(
            kartu(judul("Card 1"), paragraf("Content 1")),
            kartu(judul("Card 2"), paragraf("Content 2")),
            kartu(judul("Card 3"), paragraf("Content 3")),
            kolom=3,  # Auto responsive
        ),
    )
```

### Responsive Sidebar

```python
baris(
    # Sidebar: hidden on mobile
    kolom(3, sidebar_content),
    # Main: full width on mobile
    kolom(9, main_content),
)
```

### Responsive Grid

```python
grid(
    kartu1, kartu2, kartu3, kartu4,
    kolom=4,  # 4 cols desktop, 2 cols tablet, 1 col mobile
    gap=16,
)
```

---

## 💡 Tips Styling

### 1. Konsisten pakai Design Tokens
```python
# ✅ Good: pakai spacing scale
bagian(content, padding="24px")
spacer("16px")

# ❌ Avoid: arbitrary values
bagian(content, padding="23px")
```

### 2. Mobile-First
```python
# ✅ Good: responsive by default
grid(cards, kolom=3)  # Auto responsive

# ❌ Avoid: fixed layout
baris(kolom(6, c1), kolom(6, c2))  # Manual responsive
```

### 3. Gunakan CSS Variables
```python
# ✅ Good: theme-aware
paragraf("Text").style("color: var(--pv-text-primary)")

# ❌ Avoid: hard-coded colors
paragraf("Text").style("color: #111827")
```

---

## 📚 Selanjutnya

- [Komponen Reference](./components.md) — Detail semua komponen
- [Routing Guide](./routing.md) — Multi-page routing

---

Made with ❤️ in Indonesia 🇮🇩
