# 🛤️ Routing & Navigation

> Panduan lengkap routing, navigation, dan multi-page website di PyVibe.

---

## 📋 Daftar Isi

1. [Basic Routing](#basic-routing)
2. [Route Parameters](#route-parameters)
3. [Navigation Components](#navigation-components)
4. [Client-Side Routing](#client-side-routing)
5. [Multi-Page Website](#multi-page-website)

---

## Basic Routing

### Register Route

```python
from pyvibe import *

app = App("My Website")

@app.route("/")
def beranda():
    return tampil(
        judul("Beranda"),
        paragraf("Selamat datang di website saya!"),
    )

@app.route("/tentang")
def tentang():
    return tampil(
        judul("Tentang Kami"),
        paragraf("Kami adalah perusahaan teknologi."),
    )

@app.route("/kontak")
def kontak():
    return tampil(
        judul("Kontak"),
        paragraf("Hubungi kami di email@contoh.com"),
    )

app.jalan()
```

### Route dengan Method

```python
# GET only (default)
@app.route("/products")
def products():
    return tampil(judul("Products"))

# Multiple methods
@app.route("/api/data", methods=["GET", "POST"])
def data():
    return tampil(judul("Data"))
```

---

## Route Parameters

### Dynamic Routes

```python
@app.route("/user/<nama>")
def user_profile(nama):
    return tampil(
        judul(f"Profil: {nama}"),
        paragraf(f"Ini halaman profil {nama}."),
    )

@app.route("/product/<int:id>")
def product_detail(id):
    return tampil(
        judul(f"Product #{id}"),
        paragraf(f"Detail produk {id}."),
    )
```

### Multiple Parameters

```python
@app.route("/blog/<tahun>/<bulan>/<slug>")
def blog_post(tahun, bulan, slug):
    return tampil(
        judul(f"Blog Post: {slug}"),
        paragraf(f"Dipublish: {tahun}-{bulan}"),
    )
```

---

## Navigation Components

### Navbar

```python
@app.route("/")
def beranda():
    return tampil(
        navbar(
            # Logo
            judul("🚀 My App"),
            
            # Menu links
            baris(
                tautan("Beranda", url="/"),
                tautan("Produk", url="/produk"),
                tautan("Tentang", url="/tentang"),
                tautan("Kontak", url="/kontak"),
            ).gap(4),
            
            # Action button
            tombol("Login", warna="biru"),
        ),
        
        # Page content
        bagian(
            judul("Selamat Datang!"),
            padding="96px 0",
        ),
    )
```

### Sidebar Navigation

```python
@app.route("/dashboard")
def dashboard():
    return tampil(
        baris(
            # Sidebar
            sidebar(
                "Menu",
                "📊 Dashboard",
                "👥 Users",
                "📦 Products",
                "⚙️ Settings",
                judul="My App",
            ),
            
            # Main content
            kolom(10,
                judul("Dashboard"),
                paragraf("Selamat datang di dashboard!"),
            ),
        ),
    )
```

### Breadcrumb

```python
@app.route("/products/<id>")
def product_detail(id):
    return tampil(
        breadcrumb(["Home", "Products", f"Product #{id}"]),
        judul(f"Product #{id}"),
    )
```

### Tabs

```python
@app.route("/settings")
def settings():
    return tampil(
        tabs(["Profile", "Security", "Notifications"]),
        judul("Settings"),
    )
```

### Footer

```python
@app.route("/")
def beranda():
    return tampil(
        # ... content ...
        
        footer(
            kontainer(
                baris(
                    kolom(4,
                        judul("My App"),
                        paragraf("Description here."),
                    ),
                    kolom(2,
                        judul("Product"),
                        tautan("Features"),
                        tautan("Pricing"),
                    ),
                    kolom(2,
                        judul("Company"),
                        tautan("About"),
                        tautan("Blog"),
                    ),
                ),
                spasi(24),
                paragraf("© 2026 My App").tengah(),
            ),
        ),
    )
```

---

## Client-Side Routing

PyVibe support client-side routing untuk SPA (Single Page Application):

### Hash-Based Routing

```python
# Routes use hash (#) for client-side navigation
@app.route("/")
def beranda():
    return tampil(
        navbar(
            tautan("Home", url="#/"),
            tautan("About", url="#/tentang"),
            tautan("Contact", url="#/kontak"),
        ),
        
        # Router view
        router_view(),
    )
```

### Programmatic Navigation

```python
# JavaScript navigation
tombol("Go to About", onclick="window.location.hash='#/tentang'")
```

---

## Multi-Page Website

### Complete Example

```python
from pyvibe import *

app = App("Multi-Page Website")

# ==================== PAGES ====================

@app.route("/")
def beranda():
    return tampil(
        navbar(
            judul("🚀 MyApp"),
            baris(
                tautan("Beranda", url="/"),
                tautan("Produk", url="/produk"),
                tautan("Blog", url="/blog"),
                tautan("Kontak", url="/kontak"),
            ),
            tombol("Mulai", warna="biru"),
        ),
        
        # Hero
        bagian(
            kontainer(
                judul("Selamat Datang!").besar().tengah(),
                paragraf("Website keren pakai PyVibe.").tengah(),
                tombol("Mulai Sekarang", warna="biru"),
                max_width="800px",
            ),
            padding="96px 0",
            bg="gradient-biru",
        ),
        
        # Features
        bagian(
            kontainer(
                judul("Fitur").tengah(),
                grid(
                    kartu(
                        judul_kartu("⚡ Cepat"),
                        paragraf("Loading super cepat."),
                    ),
                    kartu(
                        judul_kartu("🎨 Cantik"),
                        paragraf("Desain modern & responsive."),
                    ),
                    kartu(
                        judul_kartu("🔒 Aman"),
                        paragraf("Security built-in."),
                    ),
                    kolom=3,
                    gap=24,
                ),
                max_width="1000px",
            ),
            padding="96px 0",
        ),
        
        footer(
            paragraf("© 2026 MyApp").tengah(),
        ),
    )


@app.route("/produk")
def produk():
    return tampil(
        navbar(
            judul("🚀 MyApp"),
            baris(
                tautan("Beranda", url="/"),
                tautan("Produk", url="/produk"),
                tautan("Blog", url="/blog"),
                tautan("Kontak", url="/kontak"),
            ),
            tombol("Mulai", warna="biru"),
        ),
        
        bagian(
            kontainer(
                judul("Produk Kami").besar().tengah(),
                spasi(48),
                grid(
                    kartu(
                        badge("Baru!", warna="hijau"),
                        judul("Produk A"),
                        paragraf("Deskripsi produk A."),
                        tombol("Lihat Detail", warna="biru"),
                        padding="24px",
                    ),
                    kartu(
                        badge("Populer", warna="ungu"),
                        judul("Produk B"),
                        paragraf("Deskripsi produk B."),
                        tombol("Lihat Detail", warna="biru"),
                        padding="24px",
                    ),
                    kartu(
                        judul("Produk C"),
                        paragraf("Deskripsi produk C."),
                        tombol("Lihat Detail", warna="biru"),
                        padding="24px",
                    ),
                    kolom=3,
                    gap=24,
                ),
                max_width="1200px",
            ),
            padding="96px 0",
        ),
        
        footer(
            paragraf("© 2026 MyApp").tengah(),
        ),
    )


@app.route("/kontak")
def kontak():
    return tampil(
        navbar(
            judul("🚀 MyApp"),
            baris(
                tautan("Beranda", url="/"),
                tautan("Produk", url="/produk"),
                tautan("Blog", url="/blog"),
                tautan("Kontak", url="/kontak"),
            ),
            tombol("Mulai", warna="biru"),
        ),
        
        bagian(
            kontainer(
                judul("Kontak Kami").besar().tengah(),
                spasi(32),
                baris(
                    kolom(6,
                        input_teks("Nama"),
                        spasi(8),
                        input_email("Email"),
                        spasi(8),
                        textarea("Pesan"),
                        spasi(16),
                        tombol("Kirim Pesan", warna="biru"),
                    ),
                    kolom(6,
                        kartu(
                            judul_kartu("Informasi Kontak"),
                            paragraf("📍 Jakarta, Indonesia"),
                            paragraf("📧 hello@myapp.com"),
                            paragraf("📱 +62 812-3456-7890"),
                            padding="24px",
                        ),
                    ),
                ).gap(8),
                max_width="1000px",
            ),
            padding="96px 0",
        ),
        
        footer(
            paragraf("© 2026 MyApp").tengah(),
        ),
    )


app.jalan()
```

---

## 💡 Tips Routing

### 1. Organize Routes by Feature
```python
# ✅ Good: organized by feature
@app.route("/")
def beranda(): ...

@app.route("/produk")
def produk(): ...

@app.route("/kontak")
def kontak(): ...

# ❌ Avoid: random routes
@app.route("/page1")
def page1(): ...

@app.route("/abc")
def abc(): ...
```

### 2. Reuse Navbar Component
```python
def get_navbar():
    return navbar(
        judul("MyApp"),
        baris(
            tautan("Home", url="/"),
            tautan("About", url="/tentang"),
        ),
        tombol("Login"),
    )

@app.route("/")
def beranda():
    return tampil(
        get_navbar(),
        judul("Home"),
    )

@app.route("/tentang")
def tentang():
    return tampil(
        get_navbar(),
        judul("About"),
    )
```

### 3. Use Container for Layout
```python
@app.route("/")
def beranda():
    return tampil(
        navbar(...),
        kontainer(
            judul("Content"),
            max_width="1200px",
            padding="0 24px",
        ),
    )
```

---

## 📚 Selanjutnya

- [State Management](./state.md) — Reactive state
- [Components Reference](./components.md) — All components

---

Made with ❤️ in Indonesia 🇮🇩
