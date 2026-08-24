# ❓ FAQ & Troubleshooting

> Pertanyaan umum dan solusi untuk masalah yang sering terjadi di PyVibe.

---

## 📋 Daftar Isi

1. [Pertanyaan Umum](#pertanyaan-umum)
2. [Installation Issues](#installation-issues)
3. [Runtime Errors](#runtime-errors)
4. [Styling Issues](#styling-issues)
5. [Deployment Issues](#deployment-issues)
6. [Performance Tips](#performance-tips)

---

## Pertanyaan Umum

### ❓ Apa itu PyVibe?

PyVibe adalah framework Python untuk membuat website frontend yang:
- Pakai Bahasa Indonesia
- Zero config, langsung jalan
- 58+ komponen responsive
- Natural Language syntax
- Built-in security features

### ❓ PyVibe bedanya sama React/Vue?

| Aspek | PyVibe | React/Vue |
|-------|--------|-----------|
| Bahasa | Python 🐍 | JavaScript 📜 |
| Learning curve | ⭐ Easy | 🔶 Medium |
| Setup | Zero config | Ribet |
| Backend | Built-in | Manual |
| Bahasa error | Indonesia 🇮🇩 | English 🇬🇧 |

### ❓ PyVibe bisa buat backend?

Saat ini PyVibe fokus ke **frontend**. Untuk backend, lo bisa pakai:
- **FastAPI** + PyVibe
- **Flask** + PyVibe
- **Django** + PyVibe

### ❓ PyVibe support browser apa?

Semua modern browser:
- ✅ Chrome/Edge (terbaru)
- ✅ Firefox (terbaru)
- ✅ Safari (terbaru)
- ✅ Mobile browsers

### ❓ PyVibe gratis?

Ya! PyVibe open source dan gratis selamanya. License: MIT.

---

## Installation Issues

### ❌ "ModuleNotFoundError: No module named 'pyvibe'"

**Solusi:**
```bash
# Install PyVibe
pip install pyvibe

# Atau upgrade
pip install --upgrade pyvibe

# Pastikan pakai pip yang benar
python -m pip install pyvibe
```

### ❌ "pip not found"

**Solusi:**
```bash
# Pakai python -m pip
python -m pip install pyvibe

# Atau install pip dulu
python -m ensurepip --upgrade
```

### ❌ "Permission denied"

**Solusi:**
```bash
# Pakai --user flag
pip install --user pyvibe

# Atau pakai virtual environment
python -m venv myenv
source myenv/bin/activate  # Linux/Mac
myenv\Scripts\activate     # Windows
pip install pyvibe
```

### ❌ "Version conflict"

**Solusi:**
```bash
# Force reinstall
pip install --force-reinstall pyvibe

# Atau pakai --no-deps
pip install --no-deps pyvibe
```

---

## Runtime Errors

### ❌ "Address already in use" / "Port 3000 sudah digunakan"

**Solusi:**
```python
# Ganti port
app.jalan(port=8000)

# Atau cari process yang pakai port
# Linux/Mac:
lsof -i :3000
kill -9 <PID>

# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### ❌ "App' object has no attribute 'route'"

**Solusi:**
```python
# ✅ Correct
app = App("My Website")

@app.route("/")
def beranda():
    return tampil(judul("Hello"))

# ❌ Wrong
app = App("My Website")
app.route("/")  # Missing decorator!
```

### ❌ "tampil() takes 0 positional arguments but 1 was given"

**Solusi:**
```python
# ✅ Correct: return tampil(...)
@app.route("/")
def beranda():
    return tampil(judul("Hello"))

# ❌ Wrong: print tampil(...)
@app.route("/")
def beranda():
    print(judul("Hello"))  # Don't print!
```

### ❌ "Component object is not iterable"

**Solusi:**
```python
# ✅ Correct: unpack with *
return tampil(*nl('tampilin judul "Hello"'))

# ❌ Wrong: pass list directly
return tampil(nl('tampilin judul "Hello"'))
```

### ❌ "TypeError: judul() got multiple values for argument"

**Solusi:**
```python
# ✅ Correct
judul("Hello").besar().tengah()

# ❌ Wrong: duplicate parameter
judul("Hello", size="lg", besar=True)
```

---

## Styling Issues

### ❌ "Website gak responsive"

**Solusi:**
```python
# ✅ Use grid with responsive columns
grid(kartu1, kartu2, kartu3, kolom=3)

# ✅ Use container
kontainer(content, max_width="1200px")

# ❌ Avoid fixed widths
Component(tag="div", style="width: 800px")
```

### ❌ "CSS gak keliatan"

**Solusi:**
```python
# ✅ Check if you're returning from route
@app.route("/")
def beranda():
    return tampil(judul("Hello"))  # Must return!

# ✅ Check container
kontainer(
    judul("Hello"),
    padding="24px",
)
```

### ❌ "Dark mode gak jalan"

**Solusi:**
```python
# ✅ Enable dark mode in App init
app = App("My Website", theme="gelap")

# ✅ Check CSS variables
:root {
    --pv-bg-primary: #ffffff;
}

[data-theme="dark"] {
    --pv-bg-primary: #111827;
}
```

### ❌ "Animation gak work"

**Solusi:**
```python
# ✅ Check animation name
judul("Hello").animate("fade-in")  # ✅
judul("Hello").animate("fadein")   # ❌ Wrong name

# Available animations:
# fade-in, slide-up, bounce, pulse, spin
```

---

## Deployment Issues

### ❌ "Build folder kosong"

**Solusi:**
```bash
# ✅ Make sure routes are defined
@app.route("/")
def beranda():
    return tampil(judul("Hello"))

# Then build
pyvibe build

# Check output
ls -la dist/
```

### ❌ "404 on refresh (SPA)"

**Solusi:**
```nginx
# Nginx: add redirect rule
location / {
    try_files $uri $uri/ /index.html;
}
```

```javascript
// Netlify: _redirects file
/* /index.html 200
```

### ❌ "CSS/JS not loading on deploy"

**Solusi:**
```python
# ✅ Use relative paths
app = App("My Website", base_url="/")

# ✅ Check file paths in output
# dist/index.html should reference:
# ./css/style.css (not /css/style.css)
```

### ❌ "CORS error on API calls"

**Solusi:**
```python
from pyvibe.middleware import CorsMiddleware

# Add CORS middleware
app.add_middleware(CorsMiddleware(origins=["*"]))
```

---

## Performance Tips

### 💡 Optimize Loading Speed

```python
# 1. Minimize components
tampil(
    judul("Hello"),  # ✅ Simple
)

# 2. Avoid complex nested structures
tampil(
    grid(
        kartu(paragraf("1")),
        kartu(paragraf("2")),
        kartu(paragraf("3")),
    ),  # ✅ Simple grid
)

# 3. Use lazy loading for images
gambar("photo.jpg", loading="lazy")
```

### 💡 Optimize Bundle Size

```bash
# Build with minification
pyvibe build --minify

# Check output size
du -sh dist/
```

### 💡 Optimize Images

```bash
# Compress images before deploy
# Use tools like:
# - TinyPNG (https://tinypng.com)
# - Squoosh (https://squoosh.app)
# - ImageOptim (Mac)
```

---

## 🔧 Debug Mode

### Enable Debug

```python
app = App("My Website", debug=True)

# Or via environment variable
import os
debug = os.environ.get("DEBUG", "False").lower() == "true"
app = App("My Website", debug=debug)
```

### Debug Output

```python
# Print component tree
print(app.render())

# Print specific component
print(judul("Hello").render())

# Print full page
html = app.tampil(judul("Hello"), paragraf("World"))
print(html)
```

---

## 📚 Still Stuck?

If you can't find your issue:

1. **Check GitHub Issues:** github.com/pyvibe/pyvibe/issues
2. **Join Discord:** discord.gg/pyvibe
3. **Search Stack Overflow:** tag `pyvibe`
4. **Email Support:** support@pyvibe.dev

---

Made with ❤️ in Indonesia 🇮🇩
