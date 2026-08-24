# 🐍 PyVibe

> **Build frontend websites in Python as easy as chatting.**
> *"Gak perlu ribet, yang penting gacor."*

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/Version-0.5.0-7C3AED?style=flat-square)](https://pypi.org/project/pyvibe)
[![Tests](https://img.shields.io/badge/Tests-396%20passing-22C55E?style=flat-square)](#testing)

---

## 🚀 Quick Start

```bash
# Install PyVibe
pip install pyvibe-id

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
| CSS ribet | Built-in design system dengan 9 themes + Design Tokens |
| Charts ribet | 6 chart types tanpa dependency |
| Forms ribet | Multi-step, conditional, auto-save forms built-in |
| SEO ribet | Built-in meta tags, sitemap, OG tags |
| SSR ribet | Built-in SSR + Streaming renderer |
| PWA ribet | Built-in manifest, service worker, offline page |
| GraphQL ribet | Built-in query/mutation builder |
| Error handling ribet | Error boundaries dengan fallback UI |
| Real-time ribet | WebSocket client dengan auto-reconnect |

---

## 📝 Syntax Styles

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

---

## 🤩 Easy API — Sesimpel Ngobrol

> *"Gak perlu ribet, tinggal bilang maunya apa."*

### Hello World — 1 Baris!

```python
from pyvibe.easy import *

halo("Developer")
# Output: <h1>Halo, Developer!</h1>
```

### One-Liner Templates

```python
from pyvibe.easy import *

# 🚀 Landing Page — satu fungsi langsung jadi
landing(
    judul="Toko Gacor",
    subjudul="Belanja gampang, harga mantap!",
    fitur=["Cepat", "Murah", "Aman"],
)

# 📊 Dashboard — satu fungsi langsung jadi
dashboard(
    judul="Admin Panel",
    stats=[
        {"judul": "Users", "nilai": "1,234", "perubahan": "+12%"},
        {"judul": "Revenue", "nilai": "Rp 45M", "perubahan": "+8%"},
    ],
    data=[{"Action": "User Signup", "Time": "2 min ago"}],
)

# 👋 Portofolio — satu fungsi langsung jadi
portofolio("Andi", skill=["Python", "PyVibe", "React"])

# 🛍️ Toko — satu fungsi langsung jadi
toko("Toko Gacor", produk=[
    {"nama": "Nike Air", "harga": "Rp 1.2M"},
    {"nama": "Adidas Run", "harga": "Rp 900K"},
])

# 🎉 Selamat Datang
selamat_datang("Developer")
```

### Super Simple Components

```python
from pyvibe.easy import *

# Render komponen langsung jadi HTML
html = ringkas(
    judul("Hello"),
    paragraf("World"),
    tombol("Click"),
)

# Form sederhana dari list nama field
html = form_sederhana("Nama", "Email", "Pesan", submit_text="Kirim")

# Tabel sederhana dari list of dict
html = tabel_sederhana([
    {"Nama": "Andi", "Email": "andi@test.com"},
    {"Nama": "Budi", "Email": "budi@test.com"},
])

# Halaman sederhana
html = halaman_sederhana("Selamat Datang!", "Ini website gue.")
```

### Smart Shortcuts

```python
from pyvibe.easy import *

# Pendek-pendek aja
e = judul_teks("Hello")         # judul
p = par("Ini paragraf")          # paragraf
t = tombol("Submit", "biru")    # tombol
i = gambar("photo.jpg")          # gambar
l = tautilan("Click", "/home")  # tautan

# Layout pendek
grid_items = grid(kartu_sederhana("Card 1"), kartu_sederhana("Card 2"), kolom=2)
row_items = baris(kolom(6, par("Kiri")), kolom(6, par("Kanan")))
```

### Easy API vs Regular API

| Task | Easy API | Regular API |
|------|----------|-------------|
| Hello World | `halo("Dunia")` | `App("X"); app.tampil(judul("Halo"))` |
| Landing Page | `landing(judul="X", fitur=[...])` | 20+ baris kode |
| Form | `form_sederhana("Nama", "Email")` | 10+ baris kode |
| Tabel | `tabel_sederhana([{...}])` | 5+ baris kode |
| Dashboard | `dashboard(judul="X", stats=[...])` | 30+ baris kode |
| Portofolio | `portofolio("Andi", skill=[...])` | 15+ baris kode |
| Toko | `toko("Toko A", produk=[...])` | 20+ baris kode |

---

## 📡 SSR & Streaming

Server-Side Rendering untuk SEO & performance.

```python
from pyvibe import SSRRenderer, StreamingRenderer, hydrate_script

# SSR Renderer
ssr = SSRRenderer(app)
html = ssr.render_route("/")
full_page = ssr.render_page("/", title="My App", meta={"description": "..."})

# Streaming Renderer
stream = StreamingRenderer(app)
for chunk in stream.stream_route("/"):
    response.write(chunk)  # Stream to client

# Client-side hydration
script = hydrate_script("app")
# <script>{script}</script>

# Pre-render at build time
pre = PreRenderer(app)
pre.add_routes(["/", "/about", "/contact"])
pre.render_all("dist/")
```

---

## 📱 PWA Support

Progressive Web App — installable, offline-capable.

```python
from pyvibe import PWAManifest, ServiceWorker, OfflinePage, PWABuilder

# Generate manifest.json
manifest = PWAManifest(
    name="My App",
    short_name="MyApp",
    theme_color="#7C3AED",
)
manifest.add_default_icons()
manifest.save("manifest.json")

# Generate service worker
sw = ServiceWorker()
sw.add_cache("static-v1", ["/style.css", "/app.js"])
sw.add_cache_first("/images/", "images-v1")
sw.add_network_first("/api/", "api-cache")
sw.add_stale_while_revalidate("/fonts/", "fonts-v1")
sw.save("sw.js")

# Offline page
offline = OfflinePage(title="Offline", message="No internet")
offline.save("offline.html")

# All-in-one PWA setup
pwa = PWABuilder(name="My App", theme_color="#7C3AED")
pwa.setup("dist/")  # Generates manifest.json, sw.js, offline.html
print(pwa.get_html_tags())  # All HTML tags needed
```

---

## 🖼️ Image Optimizer

Optimized images dengan lazy loading & responsive.

```python
from pyvibe import OptimizedImage, ResponsiveImage, BlurPlaceholder
from pyvibe import ImageGallery, AvatarOptimizer, generate_srcset

# Lazy loaded image
img = OptimizedImage("photo.jpg", alt="Photo", width=800, height=600)
html = img.render()

# With blur placeholder
img = BlurPlaceholder(
    src="photo.jpg",
    alt="Photo",
    blur_data_url="data:image/jpeg;base64,...",
    width=800,
    height=600,
)

# Responsive image
img = ResponsiveImage(
    "photo.jpg",
    alt="Photo",
    sizes=[(640, "100vw"), (1024, "50vw"), (1920, "33vw")],
)

# Image gallery with lightbox
gallery = ImageGallery(
    images=[{"src": "img1.jpg", "alt": "Photo 1"}, "img2.jpg"],
    columns=3,
    lightbox=True,
)

# Avatar with initials fallback
av = AvatarOptimizer(name="Andi Pratama", size="48px")

# Generate srcset
srcset = generate_srcset("photo.jpg", [640, 1024, 1920])
```

---

## 🎨 Design Tokens

Sistem desain yang konsisten — ganti warna sekali, berubah di semua tempat.

```python
from pyvibe import DesignTokens

tokens = DesignTokens()
tokens.colors.primary = "#FF6B6B"
tokens.colors.secondary = "#4ECDC4"
tokens.typography.font_family = "'Inter', sans-serif"

# Generate CSS custom properties
print(tokens.to_css_variables())
# :root {
#   --pv-color-primary: #FF6B6B;
#   --pv-color-secondary: #4ECDC4;
#   --pv-font-family: 'Inter', sans-serif;
#   ...
# }

# Generate Tailwind config
print(tokens.to_tailwind_config())

# Generate SCSS variables
print(tokens.to_scss_variables())

# Apply built-in theme
tokens.apply_theme("dark")
tokens.apply_theme("nature")
tokens.apply_theme("sunset")
```

---

## 🛡️ Error Boundaries

Tangkap error, tampilkan fallback UI — error gak bikin crash.

```python
from pyvibe import ErrorBoundary, FallbackRenderer, RecoveryBoundary

# Wrap components with error boundary
boundary = ErrorBoundary(
    fallback=paragraf("Terjadi kesalahan!"),
    on_error=lambda e: print(f"Error: {e.message}"),
)
boundary.add(judul("Hello"))
boundary.add(broken_component)  # If this fails, shows fallback
html = boundary.render()

# Pre-built fallback UIs
html = FallbackRenderer.error_card("Something broke!", details="Error message")
html = FallbackRenderer.not_found("Page not found", code="404")
html = FallbackRenderer.loading_skeleton(lines=3)

# Auto-retry on error
recovery = RecoveryBoundary(max_retries=3, retry_delay=1.0)
recovery.add(unstable_component)
html = recovery.render()
```

---

## 📦 Bundler & Optimizer

Optimasi output untuk production.

```python
from pyvibe import Bundler, HTMLMinifier, CSSPurger, JSMinifier

# Minify HTML
minified = HTMLMinifier.minify("<div>  Hello  </div>")
# Output: <div>Hello</div>

# Purge unused CSS
purged = CSSPurger.purge(css_content, html_content)

# Minify JavaScript
minified_js = JSMinifier.minify(js_content)

# Full build report
bundler = Bundler()
report = bundler.build_report("dist/")
print(report["total_size_human"])  # "45.2 KB"
```

---

## 🧩 Web Components

Export PyVibe components sebagai Web Components — dipakai di framework apapun.

```python
from pyvibe import web_component, register_all

# Create web component from PyVibe function
@web_component("pv-button")
def pv_button(name="Klik", color="#7C3AED"):
    return tombol(name, warna=color)

# Register all built-in components
register_all()

# Get JS for all components
script = generate_web_components_script()
```

---

## 📊 GraphQL Client

GraphQL client tanpa ribet.

```python
from pyvibe import GraphQLClient, Query, Mutation, Fragment

# Create client
client = GraphQLClient("https://api.example.com/graphql")
client.set_header("Authorization", "Bearer token123")

# Query
result = client.query("""
    query { users { id name email } }
""")
if result.ok:
    print(result.data)

# Query builder
q = Query("users").fields("id", "name", "email").args(first=10)
result = client.execute(q)

# Nested fields
q = Query("users").fields("id", "name").nested("posts", ["id", "title"])

# Mutation
m = Mutation("createUser").args(name="Andi", email="andi@test.com").fields("id", "name")
result = client.execute(m)

# Fragments
user_fields = Fragment("UserFields", "User").fields("id", "name", "email")
```

---

## 🤖 AI Integration

AI-powered UI generation & code suggestions.

```python
from pyvibe import AIUIBuilder, PromptTemplates, CodeGenerator

# Generate UI from description
ai = AIUIBuilder()
suggestions = ai.generate("Bikin landing page untuk kopi shop")
for s in suggestions:
    print(f"{s.component}: {s.code}")

# Generate complete code
code = CodeGenerator.landing_page(
    title="Kopi Gacor",
    subtitle="Kopi terenak di Indonesia",
    features=["Enak", "Murah", "Cepat"],
)
print(code)

code = CodeGenerator.dashboard(title="Admin Panel")
code = CodeGenerator.form_page(fields=["Nama", "Email", "Pesan"])

# Prompt templates
prompt = PromptTemplates.landing_page("My Brand", "Best products")
```

---

## 🔗 Context/Provider Pattern

Share state tanpa passing props.

```python
from pyvibe import createContext, useContext, Provider, ContextProvider

# Create contexts
ThemeContext = createContext("light")
UserContext = createContext({"name": "Guest"})

# Python provider
html = Provider(ThemeContext, "dark",
    judul("Hello"),
    paragraf("World"),
)

# HTML+JS provider
html = ContextProvider(
    contexts={"theme": "dark", "lang": "id", "user": {"name": "Andi"}},
    children=[judul("Hello")],
)

# Built-in contexts
from pyvibe import ThemeContext, LangContext, UserContext, AuthContext
```

---

## 📋 Advanced Forms

Multi-step, conditional, auto-save forms.

```python
from pyvibe import MultiStepForm, ConditionalField, FormArray, AutoSaveForm
from pyvibe import Field

# Multi-step form
form = MultiStepForm("registration")
form.step("Personal Info", [
    Field.text("nama", label="Nama", required=True),
    Field.email("email", label="Email"),
])
form.step("Address", [
    Field.text("alamat", label="Alamat"),
    Field.text("kota", label="Kota"),
])
form.step("Confirmation", [
    Field.checkbox("agree", label="Saya setuju"),
])
html = form.render()

# Conditional field
html = ConditionalField(
    trigger_field="tipe_akun",
    trigger_value="personal",
    children=[Field.text("nama_lengkap")],
    else_children=[Field.text("nama_perusahaan")],
).render()

# Dynamic field array
items = FormArray("items", fields=[
    Field.text("name", label="Item Name"),
    Field.number("qty", label="Quantity"),
], min_items=1, max_items=10)

# Auto-save form
form = AutoSaveForm("my-form", auto_save_key="draft")
form.add_field(Field.text("nama"))
form.add_field(Field.email("email"))
html = form.render()
```

---

## 🔌 WebSocket Client

Real-time connection dengan auto-reconnect.

```python
from pyvibe import WebSocketClient, WebSocketManager, Channel

# Single connection
ws = WebSocketClient("ws://localhost:8080", auto_reconnect=True)

@ws.on_event("message")
def handle(data):
    print(f"Received: {data}")

ws.connect()
ws.send({"type": "chat", "text": "Hello!"})
ws.send_json({"type": "typing", "user": "Andi"})

# Multiple connections
mgr = WebSocketManager()
mgr.add("chat", "ws://localhost:8080/chat")
mgr.add("notifications", "ws://localhost:8080/notify")
mgr.on_all("message", lambda name, data: print(f"{name}: {data}"))
mgr.connect_all()

# Channel system
channel = Channel("chat", ws)
channel.join("room-1")
channel.send({"text": "Hello room!"})
channel.on("message", lambda data: print(data))
```

---

## ⚡ Lazy Loading & Code Splitting

Muat komponen saat dibutuhkan.

```python
from pyvibe import lazy, suspense, ChunkManager, dynamic_import

# Lazy load komponen
Chart = lazy("pyvibe.components.charts", "chart_bar")
# Only loads when called!
html = Chart(data=[...])

# Suspense wrapper
page = suspense(
    loading=loader(),
    children=[Chart(data=[...])],
)

# Code splitting
chunks = ChunkManager()
chunks.define("charts", ["pyvibe.components.charts"], components=["chart_bar"])
chunks.define("forms", ["pyvibe.forms"], components=["FormBuilder"])
chunks.load("charts")  # Only load when needed
chunks.load_parallel(["charts", "forms"])  # Parallel loading

# Dynamic import
charts = dynamic_import("pyvibe.components.charts")
html = charts.chart_bar(data=[...])
```

---

## 🎭 Component Effects

Visual effects yang bisa di-chain.

```python
# Glassmorphism
card().glass().render()  # Semi-transparent blur background

dark_card().dark_glass().render()  # Dark glass

# Glow effect
card().glow("#7C3AED", "20px").render()  # Purple glow

# Skeleton loading
skeleton().skeleton(width="200px", height="20px").render()

# Neon text
teks("Hello").neon("#7C3AED").render()  # Neon glow text

# Material depth
card().depth(3).render()  # 5 levels of elevation

# Scale transform
card().scale(1.05).render()  # Scale up

# Floating animation
icon().float().render()  # Gentle floating motion

# Marquee
teks("Scrolling text").marquee().render()  # Scrolling text

# Pulse
badge().pulse().render()  # Pulsing animation

# Typing cursor
teks("| ").typing_cursor().render()  # Blinking cursor
```

---

## 🧩 Components (82+)

### Basic Components (17)

```python
judul("Heading")                    # <h1>
subjudul("Sub Heading")             # <h2>
paragraf("Text")                    # <p>
teks("Inline")                      # <span>
gambar("img.jpg")                   # <img>
tautan("Link", url="/")             # <a>
ikon("🚀")                          # <span>🚀</span>
badge("NEW")                        # Badge label
chip("Python")                      # Chip/tag
avatar("photo.jpg")                 # Avatar image
progress_bar(75)                    # Progress bar
count_down(60, label="Tersisa")     # Counter
gradien_teks("Gradient")            # Gradient text
spasi("24px")                       # Spacing
pemisah()                           # Divider
teks_teal("Teal Text")              # Colored text
teks_tipis("Thin Text")             # Light weight text
```

### Input Components (11)

```python
tombol("Submit", warna="ungu")      # Button
tombol_icon("🚀", tooltip="Go")    # Icon button
input_teks(label="Nama")            # Text input
input_angka(label="Harga")          # Number input
input_email(label="Email")          # Email input
input_sandi(label="Password")       # Password input
textarea(label="Deskripsi")         # Textarea
centang("Setuju")                   # Checkbox
pilihan("Kota", ["Jakarta", "Bandung"])  # Select dropdown
unggah_file("Upload foto")          # File upload
```

### Layout Components (10)

```python
kartu(content)                      # Card
kolom(6, content)                   # Column (6/12)
baris(col1, col2)                   # Row/Flexbox
bagian(content)                     # Section
grid(c1, c2, c3, kolom=3)         # CSS Grid
kontainer(content)                  # Max-width container
kartu_stat("Users", "1,234", "+12%") # Stat card
judul_kartu("Title")                # Card title
spacer("24px")                      # Spacer
overlay(content)                    # Overlay/modal backdrop
```

### Navigation Components (5)

```python
navbar(logo, menu)                  # Navigation bar
sidebar(items)                      # Sidebar
footer(teks, links)                 # Footer
tabs(tab1, tab2)                    # Tab navigation
breadcrumb("A", "B", "C")          # Breadcrumb
```

### Feedback Components (5)

```python
notifikasi("Berhasil!", tipe="sukses")  # Toast notification
alert("Info penting", tipe="info")       # Alert banner
loader()                                 # Loading spinner
skeleton()                               # Skeleton loader
badge_status("Active", status="sukses")  # Status badge
```

### Data Components (4)

```python
tabel(data, kolom=[...])            # Data table
grafik_sederhana(data)              # Simple bar chart
daftar("A", "B", "C")              # List
statistik([{...}])                  # Stats grid
```

### Advanced Components (5)

```python
carousel(img1, img2)                # Image carousel
accordion(item1, item2)             # Collapsible sections
modal(judul, content)               # Modal dialog
dropdown(trigger, items)            # Dropdown menu
tooltip(content, "Tooltip text")    # Tooltip
```

### Modern Components (10)

```python
pagination(total_pages=10, current_page=1)  # Pagination
toast("Success!", tipe="sukses")            # Toast notification
switch("Dark Mode")                          # Toggle switch
avatar_group(["a.jpg", "b.jpg"])           # Avatar group
date_picker(label="Tanggal")               # Date picker
color_picker(label="Warna")                # Color picker
range_slider(label="Volume")               # Range slider
stat_grid([{...}])                          # Statistics grid
command_palette(placeholder="Cari...")     # Command palette
empty_state_modern("Tidak ada data")       # Empty state
```

### Chart Components (6)

```python
# Bar Chart
chart_bar([
    {"label": "Jan", "value": 45},
    {"label": "Feb", "value": 52},
], color="#7C3AED")

# Line Chart
chart_line([
    {"label": "Jan", "value": 45},
    {"label": "Feb", "value": 52},
], fill=True)

# Pie Chart
chart_pie([
    {"label": "Elektronik", "value": 45},
    {"label": "Fashion", "value": 30},
])

# Doughnut Chart
chart_doughnut([
    {"label": "Active", "value": 70},
    {"label": "Inactive", "value": 30},
], center_text="70%")

# Sparkline
chart_sparkline([10, 15, 13, 18, 22, 20, 25])

# Progress Ring
chart_progress_ring(75, label="Score")
```

### Advanced UI Components (8)

```python
# Calendar
calendar_component(year=2026, month=8, events=[
    {"day": 15, "title": "Meeting", "color": "#7C3AED"},
])

# Kanban Board
kanban([
    {"title": "To Do", "color": "#EF4444", "items": [{"title": "Task 1"}]},
    {"title": "Done", "color": "#22C55E", "items": []},
])

# Video Player
video_player("video.mp4", poster="thumb.jpg")
video_player("https://youtube.com/watch?v=abc123")

# Timeline
timeline_enhanced([
    {"date": "24 Agustus", "title": "Started", "icon": "🚀", "color": "#7C3AED"},
])

# Theme Toggle
theme_toggle()

# Search Command
search_command(placeholder="Cari...", shortcut="⌘K")

# Notification Center
notification_center(notifications=[
    {"title": "New message", "time": "2 min ago", "read": False},
])

# Infinite Scroll
infinite_scroll(loader_text="Loading more...")
```

### Extras Components (11)

```python
stepper(["Step 1", "Step 2", "Step 3"], aktif=1)  # Stepper/wizard
timeline({"tanggal": "24 Ag", "judul": "Title"})    # Timeline
rating(4, max_bintang=5)                             # Star rating
countdown(detik=300, label="Tersisa")               # Countdown timer
typing_effect(["Hello", "World"])                   # Typing effect
scroll_to_top()                                      # Scroll to top button
galeri(["img1.jpg", "img2.jpg"])                    # Image gallery
code_block('print("Hello")', bahasa="python")       # Code block
markdown("# Title\n\nContent")                      # Markdown renderer
empty_state("No data")                              # Empty state
stat_card(icon="👥", nilai="1,234", label="Users") # Stat card
```

---

## 🎨 Styling

### Builder Pattern

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
| `.miring()` | Italic | `.garis_bawah()` |
| `.huruf_besar()` | Uppercase | |
| `.blur("10px")` | Glass effect | |
| `.monospace()` | Mono font | |

### Layout Methods

| Method | Description | Example |
|--------|-------------|---------|
| `.flex()` | Flexbox | `.flex(direction="column")` |
| `.grid(3)` | CSS Grid | `.grid(columns=2, gap="16px")` |
| `.gap("16px")` | Gap | `.gap("24px")` |
| `.justify("center")` | Justify | `.justify("between")` |
| `.items("center")` | Align items | `.items("start")` |
| `.wrap()` | Flex wrap | |

### Accessibility

| Method | Description | Example |
|--------|-------------|---------|
| `.aria_label("Name")` | ARIA label | `.aria_hidden(True)` |
| `.role("button")` | Role | `.tabindex("0")` |
| `.tooltip("Help")` | Title tooltip | |

### Themes

```python
from pyvibe import Theme, list_themes

# Available themes
print(list_themes())  # ['default', 'light', 'dark', 'nature', 'sunset', 'ocean', 'royal', 'corporate', 'pastel', 'neon']

# Apply theme
app = App("My Website", theme="dark")

# Custom theme
custom = Theme.custom("my-brand", primary="#FF6B6B", secondary="#4ECDC4")
```

### Animations

```python
from pyvibe import Animation, list_animations

# Available animations
print(list_animations())
# ['fade_in', 'fade_out', 'slide_up', 'slide_down', 'bounce', 'pulse', 'spin', ...]

# Apply animation
judul("Hello").animasi("fade_in")
paragraf("World").animasi("bounce")
```

---

## 📋 Forms System

### Basic Form

```python
from pyvibe import *

form = Form("contact")
form.add_field("nama", Field.text(required=True, label="Nama"))
form.add_field("email", Field.email(required=True, validators=[Validators.email]))
form.add_field("pesan", Field.textarea(label="Pesan"))

# Validate
errors = form.validate({"nama": "Andi", "email": "andi@test.com", "pesan": "Hello"})

# Render
html = form.render(data=data, errors=errors)
```

### Fluent API (FormBuilder)

```python
form = (FormBuilder("login")
    .email("email", label="Email", required=True)
    .password("password", label="Password", required=True)
    .checkbox("remember", label="Ingat saya")
    .submit("Masuk")
    .build())
```

### Pre-built Forms

```python
form_login()      # Login form
form_register()   # Registration form
form_kontak()     # Contact form
form_search()     # Search form
```

### Validators

```python
from pyvibe import Validators

Validators.required(value)           # Wajib diisi
Validators.email(value)             # Email format
Validators.url(value)               # URL format
Validators.phone(value)             # Phone number
Validators.numeric(value)           # Numeric
Validators.min_length(8)(value)     # Min length
Validators.max_length(100)(value)   # Max length
Validators.min_value(0)(value)      # Min value
Validators.max_value(100)(value)    # Max value
Validators.one_of(["A", "B"])(value) # One of options
Validators.pattern(r'^[0-9]+$')(value) # Regex pattern
Validators.matches("password_confirm")(value, data) # Match field
```

---

## 🔄 Reactivity System

### ReactiveStore

```python
from pyvibe import ReactiveStore

store = ReactiveStore("my-app")
store.state = {"count": 0, "user": {"name": "Andi"}}

# Auto-persists to localStorage
store.state["count"] = 1  # Auto-saved
store.save()
store.load()
store.clear()
```

### ReactiveDict

```python
from pyvibe import ReactiveDict, watch

state = ReactiveDict(count=0, name="Andi")

# Listen to changes
state.on_change("count", lambda new, old: print(f"Changed: {old} → {new}"))
state["count"] = 1  # Triggers callback

# Watch
unwatch = watch(state, "count", lambda new, old: print(f"{old} → {new}"))
state["count"] = 2  # Prints: 1 → 2
unwatch()  # Stop watching

# Undo
state.undo()
```

### Computed

```python
from pyvibe import computed

count = ReactiveDict(value=10)
double = computed(lambda: count["value"] * 2)
print(double.value)  # 20

count["value"] = 15
double.invalidate()
print(double.value)  # 30
```

---

## 🪝 Hooks System

```python
from pyvibe import *

# Counter
counter = use_counter(0)
counter["increment"]()  # count = 1
counter["decrement"]()  # count = 0
counter["reset"]()      # count = 0

# Toggle
toggle = use_toggle(False)
toggle["toggle"]()  # True
toggle["on"]()      # True
toggle["off"]()     # False

# List
lst = use_list([1, 2, 3])
lst["add"](4)        # [1, 2, 3, 4]
lst["remove"](0)     # [2, 3, 4]
lst["clear"]()       # []

# Memoize
expensive = use_memo(lambda: calculate(), [dep1, dep2])

# Debounce
debounced = use_debounce(search, delay=300)

# Throttle
throttled = use_throttle(on_scroll, limit=200)

# Effect
effect = use_effect(lambda: print("Mounted"))

# Interval
stop = use_interval(lambda: print("tick"), 1000)
stop()  # Stop

# Previous value
prev = use_previous(current_value)

# Local Storage
value = use_local_storage("key", default_value)
```

---

## 🔍 SEO Helpers

### Meta Tags

```python
from pyvibe import SEO

seo = SEO(
    title="My Page | MySite",
    description="This is a description",
    image="https://example.com/og.png",
    url="https://example.com/page",
    keywords=["python", "web"],
    author="PyVibe Team",
    structured_data={
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "My Article",
    }
)

html = seo.render()      # All meta tags
og_html = seo.render_og() # OG tags only
```

### Sitemap

```python
from pyvibe import SitemapGenerator

sitemap = SitemapGenerator("https://example.com")
sitemap.add("/", priority=1.0, changefreq="daily")
sitemap.add("/about", priority=0.8)
sitemap.save("sitemap.xml")
```

### Robots.txt

```python
from pyvibe import RobotsGenerator

robots = RobotsGenerator(sitemap_url="https://example.com/sitemap.xml")
robots.allow("/", "*")
robots.disallow("/admin", "*")
robots.save("robots.txt")
```

---

## 📝 Logging System

```python
from pyvibe import setup_logging, get_logger

# Setup
setup_logging(level="DEBUG", file="app.log")

# Get logger
logger = get_logger("my-module")
logger.info("Server started")
logger.error("Something went wrong", data={"code": 500})
logger.warning("Deprecated feature")
logger.critical("System failure")
```

---

## ⚡ Performance Monitoring

```python
from pyvibe import timer, monitor, benchmark, get_timer

# Timer context manager
with timer("my-operation"):
    do_something()

# Monitor decorator
@monitor
def slow_function():
    time.sleep(1)

@monitor(threshold_ms=50)
def fast_function():
    pass

# Benchmark
result = benchmark(my_function, iterations=1000)
print(result["avg_ms"])

# Get timer stats
t = get_timer()
print(t.get_slowest(top=5))
```

---

## 🔐 Security

```python
from pyvibe import Security, csrf_protect, rate_limit

# Security manager
security = Security()
token = security.generate_csrf_token()
security.validate_csrf_token(token)

# Rate limiting
@rate_limit(max_requests=100, window=60)
def api_endpoint():
    return {"data": "hello"}

# Input sanitization
clean = security.sanitize_input(user_input)
valid_email = security.validate_email("test@example.com")
```

---

## 🗄️ Database

```python
from pyvibe import Database, Model

# SQLite database
db = Database("myapp.db")

# Create table
db.create_table("users", {
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "nama": "TEXT NOT NULL",
    "email": "TEXT UNIQUE NOT NULL",
})

# CRUD operations
db.insert("users", {"nama": "Andi", "email": "andi@test.com"})
users = db.query("SELECT * FROM users")
user = db.query_one("SELECT * FROM users WHERE id = ?", (1,))
db.update("users", {"nama": "Budi"}, where="id = 1")
db.delete("users", where="id = 1")

# ORM-like Model
class User(Model):
    table = "users"
    columns = ["id", "nama", "email"]

User.set_db(db)
user = User.create(nama="Andi", email="andi@test.com")
users = User.all()
user = User.find(1)
```

---

## 🔌 Plugin System

```python
from pyvibe import Plugin, PluginManager

class MyPlugin(Plugin):
    name = "My Plugin"
    version = "1.0.0"

    def setup(self, app):
        @app.route("/api/data")
        def api_data():
            return {"data": "hello"}

# Register plugin
manager = PluginManager()
manager.register(MyPlugin())
manager.setup_all(app)
```

---

## 🧪 Testing

```python
from pyvibe import Client, TestCase

class TestApp(TestCase):
    def setup(self):
        self.app = App("Test")
        self.client = Client(self.app)

        @self.app.route("/")
        def home():
            return tampil(judul("Hello"))

    def test_home(self):
        response = self.client.get("/")
        self.assert_status(response, 200)
        self.assert_contains(response, "Hello")

    def test_component(self):
        html = self.client.render(judul("Test"))
        self.assert_contains(html, "<h1")
```

---

## 🚀 Deployment

### Vercel

```python
from pyvibe import Vercel

vercel = Vercel()
vercel.generate_config()
```

### Netlify

```python
from pyvibe import Netlify

netlify = Netlify()
netlify.generate_config()
```

### GitHub Pages

```python
from pyvibe import GitHubPages

gh = GitHubPages()
gh.generate_workflow()
```

### Docker

```python
from pyvibe import Docker

docker = Docker()
docker.generate_dockerfile()
docker.generate_compose()
```

---

## 🌐 Internationalization

```python
from pyvibe import i18n_t as t, set_locale, add_translations

# Set locale
set_locale("id")

# Translate
print(t("hello"))      # "Halo!"
print(t("welcome"))    # "Selamat Datang"

# Add custom translations
add_translations("id", {"custom": "Kustom"})
```

---

## 📦 CLI Commands

```bash
# Create project
pyvibe create my-website
pyvibe create my-website --template dashboard

# List templates
pyvibe templates

# Start dev server
pyvibe dev

# Build for production
pyvibe build
pyvibe build --output dist

# List components
pyvibe components

# Show version
pyvibe version
```

### Available Templates

| Template | Description |
|----------|-------------|
| `minimal` | Simple starter |
| `landing-page` | Landing page |
| `dashboard` | Admin dashboard |
| `portfolio` | Developer portfolio |
| `blog` | Tech blog |
| `ecommerce` | E-commerce store |
| `admin` | Admin panel |
| `saas` | SaaS landing page |
| `saas-dashboard` | SaaS dashboard |
| `restaurant` | Restaurant website |

---

## 📊 Examples

### Hello World

```python
from pyvibe import *

app = App("Hello World")
app.tampil(judul("Halo, Dunia! 🌍").tengah())
app.jalan()
```

### Landing Page

```python
from pyvibe import *

app = App("Landing Page")

@app.route("/")
def beranda():
    return tampil(
        navbar(judul("🚀 MyBrand"), tombol("Mulai", warna="biru")),
        bagian(
            judul("Bikin Website Gak Pake Ribet").besar().tengah(),
            paragraf("PyVibe bikin coding jadi gampang.").tengah(),
            tombol("Coba Gratis", warna="ungu"),
            bg="gradient-ungu",
            padding="96px 0",
        ),
        bagian(
            grid(
                kartu(teks("⚡").besar(), judul("Cepat")),
                kartu(teks("🎨").besar(), judul("Indah")),
                kartu(teks("🔒").besar(), judul("Aman")),
                kolom=3,
            ),
            padding="96px 0",
        ),
        footer(kontainer(paragraf("© 2026 MyBrand").tengah())),
    )

app.jalan()
```

### Dashboard with Charts

```python
from pyvibe import *

app = App("Dashboard")

@app.route("/")
def dashboard():
    return tampil(
        baris(
            sidebar("📊 Dashboard", "👥 Users", "⚙️ Settings"),
            kolom(10,
                judul("Dashboard 📊").besar(),
                stat_grid([
                    {"label": "Users", "value": "1,234", "icon": "👥", "trend": "+12%", "up": True},
                    {"label": "Revenue", "value": "Rp 45M", "icon": "💰", "trend": "+8%", "up": True},
                ], columns=4),
                chart_bar([
                    {"label": "Jan", "value": 45},
                    {"label": "Feb", "value": 52},
                    {"label": "Mar", "value": 48},
                ]),
            ),
        ),
    )

app.jalan()
```

---

## 📁 Project Structure

```
pyvibe/
├── core/              # App, Component, Renderer, State, Router
├── components/        # 82+ UI components
│   ├── basic.py       # Typography, media, decorative
│   ├── input.py       # Form inputs, buttons
│   ├── layout.py      # Cards, grids, sections
│   ├── navigation.py  # Navbar, sidebar, footer
│   ├── feedback.py    # Alerts, loaders, badges
│   ├── data.py        # Tables, charts, lists
│   ├── advanced.py    # Carousel, accordion, modal
│   ├── extras.py      # Stepper, timeline, rating
│   ├── modern.py      # Pagination, toast, switch
│   ├── charts.py      # Bar, line, pie, doughnut
│   ├── advanced_ui.py # Calendar, kanban, video
│   └── ...            # More components
├── style/             # Themes, animations, responsive
├── forms/             # Form builder, validators
├── forms_advanced.py  # Multi-step, conditional, auto-save
├── reactivity.py      # Reactive state, computed, watch
├── navigation.py      # SEO, sitemap, params
├── hooks.py           # 12 composable hooks
├── logging.py         # Multi-handler logging
├── performance.py     # Timer, monitor, profiler
├── lazy.py            # Lazy loading, code splitting, suspense
├── websocket.py       # WebSocket client, manager, channels
├── ssr.py             # Server-Side Rendering & streaming
├── pwa.py             # PWA manifest, service worker, offline
├── image_optimizer.py # Lazy images, responsive, blur placeholder
├── design_tokens.py   # CSS variables, Tailwind config, SCSS
├── error_boundary.py  # Error boundaries & fallback UI
├── bundler.py         # HTML/CSS/JS minification & optimization
├── webcomponents.py   # Web Components export
├── graphql.py         # GraphQL client & query builder
├── ai.py              # AI/LLM integration & code generation
├── context.py         # Context/Provider pattern
├── easy.py            # Super simple API (one-liners)
├── security/          # CSRF, XSS, rate limiting
├── middleware/         # CORS, logger, auth, cache
├── cache/             # In-memory, file-based cache
├── database/          # SQLite ORM
├── auth/              # Authentication system
├── i18n/              # Internationalization
├── events/            # Event emitter
├── errors/            # Error handling (Indonesian)
├── plugins/           # Plugin system
├── deploy/            # Vercel, Netlify, GitHub Pages
├── testing/           # Test utilities
├── cli/               # Command line tools
├── dev/               # Dev server with WebSocket
└── parser/            # Natural Language parser
```

---

## 🧪 Testing

```bash
# Run all tests
python tests/test_charts.py          # 42 tests
python tests/test_advanced_ui.py     # 70 tests
python tests/test_hooks.py           # 48 tests
python tests/test_navigation.py      # 56 tests
python tests/test_logging_performance.py  # 61 tests
python tests/test_reactivity.py      # 47 tests
python tests/test_lazy.py            # 72 tests

# Total: 396 tests passing ✅
```

---

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

## 📊 Comparison with Other Frameworks

| Feature | PyVibe v0.5.0 | React | Vue | Angular | Svelte |
|---------|:---:|:---:|:---:|:---:|:---:|
| **Components** | 82+ | Manual | Manual | Manual | Manual |
| **Charts** | 6 types | Manual | Manual | Manual | Manual |
| **Forms** | Multi-step | Manual | Manual | ✅ | Manual |
| **Themes** | 9 built-in | Manual | Manual | Manual | Manual |
| **Animations** | 22+ presets | Manual | Manual | ✅ | ✅ |
| **SSR/Streaming** | ✅ | ✅ RSC | ✅ Nuxt | ✅ | ✅ SvelteKit |
| **PWA** | ✅ | Manual | ✅ | ✅ | ✅ |
| **Lazy Loading** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Code Splitting** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **WebSocket Client** | ✅ auto-reconnect | Manual | Manual | ✅ | ✅ |
| **GraphQL** | ✅ builder | Manual | Manual | Manual | Manual |
| **Design Tokens** | ✅ | Manual | Manual | ✅ | Manual |
| **Error Boundaries** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Image Optimization** | ✅ lazy + blur | Manual | Manual | ✅ | Manual |
| **Web Components** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Context/Provider** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **SEO** | ✅ built-in | Manual | Manual | Manual | Manual |
| **Reactivity** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Hooks** | 12 hooks | ✅ | ✅ | ✅ | ✅ |
| **AI Integration** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Bundler** | ✅ minify+purge | ✅ | ✅ | ✅ | ✅ |
| **Logging** | ✅ | Manual | Manual | ✅ | Manual |
| **Performance** | ✅ monitor | Manual | Manual | Manual | Manual |
| **Hot Reload** | ✅ WebSocket | ✅ | ✅ | ✅ | ✅ |
| **Indonesian** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Zero Config** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Learning Curve** | ⭐ Easy | 🔴 Steep | 🔶 Medium | 🔶 Medium | 🟡 Easy |

---

*Made with ❤️ in Indonesia 🇮🇩*

*Last updated: August 24, 2026 | PyVibe v0.5.0 | 82+ Components | 20+ Modules | 396 Tests*
