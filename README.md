# 🐍 PyVibe

> **Build frontend websites in Python as easy as chatting.**
> *"Gak perlu ribet, yang penting gacor."*

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/Version-0.3.0-7C3AED?style=flat-square)](https://pypi.org/project/pyvibe)
[![Tests](https://img.shields.io/badge/Tests-324%20passing-22C55E?style=flat-square)](#testing)

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
| CSS ribet | Built-in design system dengan 9 themes |
| Charts ribet | 6 chart types tanpa dependency |
| Forms ribet | Built-in validation dengan 12+ validators |
| SEO ribet | Built-in meta tags, sitemap, OG tags |

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
├── core/           # App, Component, Renderer, State, Router
├── components/     # 82+ UI components
│   ├── basic.py    # Typography, media, decorative
│   ├── input.py    # Form inputs, buttons
│   ├── layout.py   # Cards, grids, sections
│   ├── navigation.py # Navbar, sidebar, footer
│   ├── feedback.py # Alerts, loaders, badges
│   ├── data.py     # Tables, charts, lists
│   ├── advanced.py # Carousel, accordion, modal
│   ├── extras.py   # Stepper, timeline, rating
│   ├── modern.py   # Pagination, toast, switch
│   ├── charts.py   # Bar, line, pie, doughnut
│   └── advanced_ui.py # Calendar, kanban, video
├── style/          # Themes, animations, responsive
├── forms/          # Form builder, validators
├── reactivity.py   # Reactive state, computed, watch
├── navigation.py   # SEO, sitemap, params
├── hooks.py        # 12 composable hooks
├── logging.py      # Multi-handler logging
├── performance.py  # Timer, monitor, profiler
├── security/       # CSRF, XSS, rate limiting
├── middleware/      # CORS, logger, auth, cache
├── cache/          # In-memory, file-based cache
├── database/       # SQLite ORM
├── auth/           # Authentication system
├── i18n/           # Internationalization
├── events/         # Event emitter
├── errors/         # Error handling (Indonesian)
├── plugins/        # Plugin system
├── deploy/         # Vercel, Netlify, GitHub Pages
├── testing/        # Test utilities
├── cli/            # Command line tools
├── dev/            # Dev server with WebSocket
└── parser/         # Natural Language parser
```

---

## 🧪 Testing

```bash
# Run all tests
python tests/test_charts.py
python tests/test_advanced_ui.py
python tests/test_hooks.py
python tests/test_navigation.py
python tests/test_logging_performance.py
python tests/test_reactivity.py

# Total: 324 tests passing ✅
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

| Feature | PyVibe v0.3.0 | React | Vue | Django | Flask |
|---------|:---:|:---:|:---:|:---:|:---:|
| **Components** | 82+ | Manual | Manual | Manual | Manual |
| **Charts** | 6 types | Manual | Manual | Manual | Manual |
| **Forms** | Built-in | Manual | Manual | Manual | Manual |
| **Themes** | 9 built-in | Manual | Manual | Manual | Manual |
| **Animations** | 22 presets | Manual | Manual | Manual | Manual |
| **SEO** | Built-in | Manual | Manual | ⚠️ | Manual |
| **Reactivity** | Built-in | ✅ | ✅ | ❌ | ❌ |
| **Hooks** | 12 hooks | ✅ | ✅ | ❌ | ❌ |
| **Logging** | Built-in | Manual | Manual | ✅ | Manual |
| **Performance** | Built-in | Manual | Manual | Manual | Manual |
| **Hot Reload** | ✅ WebSocket | ✅ | ✅ | ⚠️ | ⚠️ |
| **Indonesian** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Zero Config** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Learning Curve** | ⭐ Easy | 🔴 Steep | 🔶 Medium | 🔶 Medium | 🟡 Easy |

---

*Made with ❤️ in Indonesia 🇮🇩*

*Last updated: August 24, 2026*
