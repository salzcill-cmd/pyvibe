"""
🐍 Example 4: Natural Language Syntax — nulis kode kayak ngobrol!

Ini adalah demo syntax natural language PyVibe.
Lo bisa nulis instruksi dalam bahasa Indonesia sehari-hari,
dan PyVibe akan convert jadi komponen UI yangproper.

Usage:
    python examples/04_natural_language.py
"""

from pyvibe import *

# ============================================
# CONTOH 1: Natural Language → Python Code
# ============================================

print("=" * 60)
print("🗣️  Natural Language Syntax Demo")
print("=" * 60)
print()

# Show NL → Python conversion
nl_examples = [
    'tampilin judul "Selamat Datang di PyVibe"',
    'tampilin judul "Halo Dunia" di tengah',
    'tampilin paragraf "Ini website pertama gue pakai PyVibe."',
    'tampilin tombol "Mulai Sekarang" warna ungu',
    'tampilin tombol "Pelajari Lagi" warna outline',
    'tampilin gambar "banner.jpg" bulat',
    'tampilin tautan "Klik di sini" url "/about"',
    'tampilin badge "BARU"',
    'tampilin input_teks "Nama Lengkap"',
    'tampilin input_email "Email"',
    'tampilin spasi',
    'tampilin pemisah',
]

for example in nl_examples:
    python_code = nl(example)
    print(f"🗣️  {example}")
    print(f"🐍 {python_code}")
    print()

# ============================================
# CONTOH 2: Full Page dengan Natural Language
# ============================================

print("=" * 60)
print("📄 Full Page dengan Natural Language")
print("=" * 60)
print()

# Ini contoh gimana lo bisa nulis page pake NL syntax
# dan langsung di-convert ke proper PyVibe code

page_code = """
# Bayangin lo nulis ini di file .py lo:

from pyvibe import *

app = App("Toko Gacor")

@app.route("/")
def beranda():
    return tampil(
        # Lo bisa pake NL syntax:
        navbar(logo="🛍️ Toko Gacor", menu=["Beranda", "Produk", "Kontak"]),
        
        bagian(
            judul("Selamat Datang di Toko Gacor!").besar().tengah(),
            paragraf("Belanja gampang, harga gacor!").tengah(),
            tombol("Mulai Belanja", warna="ungu", ukuran="besar"),
            padding="96px 32px",
            bg="gradient-ungu",
        ),
        
        bagian(
            judul("Produk Terlaris").tengah(),
            grid(
                kartu(
                    judul_kartu("Nike Air Max"),
                    paragraf("Rp 1.299.000"),
                    tombol("Beli", warna="ungu"),
                ),
                kartu(
                    judul_kartu("MacBook Air"),
                    paragraf("Rp 15.999.000"),
                    tombol("Beli", warna="ungu"),
                ),
                kartu(
                    judul_kartu("iPhone 15"),
                    paragraf("Rp 18.999.000"),
                    tombol("Beli", warna="ungu"),
                ),
                kolom=3,
                gap="24px",
            ),
            padding="64px 32px",
        ),
        
        footer(copyright="© 2026 Toko Gacor"),
    )

app.jalan()
"""
print(page_code)

# ============================================
# CONTOH 3: Cara Pakai NL Parser
# ============================================

print("=" * 60)
print("🔧 Cara Pakai NL Parser")
print("=" * 60)
print()

usage_code = """
from pyvibe import *

# Method 1: Convert NL ke Python code
python_code = nl('tampilin judul "Halo" di tengah')
print(python_code)  # → judul("Halo").tengah()

# Method 2: Parse NL jadi component definitions
parsed = nl_parse('tampilin judul "Halo" di tengah')
print(parsed)
# → [{'action': 'render', 'component': 'judul', 'content': 'Halo', ...}]

# Method 3: Use parser directly
parser = NaturalLanguageParser()
result = parser.parse('tampilin tombol "Klik" warna ungu')
print(result)
# → {'action': 'render', 'component': 'tombol', 'content': 'Klik', ...}

# Method 4: Convert entire file
nl_code = '''
tampilin judul "Welcome"
tampilin paragraf "This is my website"
tampilin tombol "Click me" warna ungu
'''
python_code = parser.to_python(nl_code)
print(python_code)
"""
print(usage_code)

# ============================================
# CONTOH 4: Run actual app
# ============================================

print("=" * 60)
print("🚀 Running actual app...")
print("=" * 60)
print()

# Create a simple app to demo
app = App("NL Demo")

@app.route("/")
def beranda():
    return tampil(
        navbar(logo="🗣️ NL Demo", menu=["Beranda", "Demo"]),
        bagian(
            judul("Natural Language Syntax!").besar().tengah(),
            paragraf("Tulis kode seperti lo ngobrol. PyVibe convert jadi komponen UI.").tengah(),
            padding="96px 32px",
            bg="gradient-ungu",
        ),
        bagian(
            judul("Contoh Konversi").tengah(),
            grid(
                kartu(
                    judul_kartu("🗣️ Input"),
                    paragraf('tampilin judul "Halo" di tengah'),
                ),
                kartu(
                    judul_kartu("🐍 Output"),
                    paragraf('judul("Halo").tengah()'),
                ),
                kartu(
                    judul_kartu("📱 Result"),
                    paragraf('<h1 style="text-align: center">Halo</h1>'),
                ),
                kolom=3,
                gap="24px",
            ),
            padding="64px 32px",
        ),
        footer(copyright="© 2026 PyVibe NL Demo"),
    )

# Export to see the output
app.export("output/nl_demo")
print("✅ Exported to output/nl_demo/")
print()
print("🌐 To run: python examples/04_natural_language.py")
