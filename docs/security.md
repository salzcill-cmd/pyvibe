# 🛡️ Security

> Panduan lengkap fitur keamanan di PyVibe: CSRF, XSS, Rate Limiting, dan lainnya.

---

## 📋 Daftar Isi

1. [Overview](#overview)
2. [CSRF Protection](#csrf-protection)
3. [XSS Protection](#xss-protection)
4. [Rate Limiting](#rate-limiting)
5. [Input Sanitization](#input-sanitization)
6. [Security Headers](#security-headers)
7. [Password Hashing](#password-hashing)

---

## Overview

PyVibe built-in security features yang penting untuk production apps:

| Feature | Status | Description |
|---------|--------|-------------|
| CSRF Protection | ✅ | Form submission protection |
| XSS Protection | ✅ | Cross-site scripting prevention |
| Rate Limiting | ✅ | API abuse prevention |
| Input Sanitization | ✅ | Malicious input filtering |
| Security Headers | ✅ | HTTP security headers |
| Password Hashing | ✅ | Secure password storage |

---

## CSRF Protection

### Basic Usage

```python
from pyvibe import *
from pyvibe.security import Security

app = App("My Website")
security = Security(app)

@app.route("/form")
def form():
    # Generate CSRF token
    token = security.generate_csrf_token()
    
    return tampil(
        judul("Contact Form"),
        
        # Include CSRF token in form
        input_teks("Nama"),
        input_email("Email"),
        textarea("Pesan"),
        
        tombol("Submit", warna="biru"),
        
        # Hidden CSRF token
        Component(tag="input", type="hidden", name="csrf_token", value=token),
    )

@app.route("/submit", methods=["POST"])
def submit():
    # Validate CSRF token
    token = request.form.get("csrf_token")
    if not security.validate_csrf_token(token):
        return tampil(alert("Invalid CSRF token!", warna="merah"))
    
    # Process form...
    return tampil(alert("Form submitted!", warna="hijau"))
```

### CSRF Decorator

```python
from pyvibe.security import csrf_protect

@app.route("/submit", methods=["POST"])
@csrf_protect
def submit():
    # CSRF automatically validated
    return tampil(alert("Success!"))
```

---

## XSS Protection

### Basic Usage

```python
from pyvibe.security import Security

security = Security()

# Sanitize user input
user_input = '<script>alert("XSS")</script>'
safe_input = security.sanitize_input(user_input)
print(safe_input)
# Output: &lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt;

# Sanitize HTML
html = '<img src=x onerror=alert(1)>'
safe_html = security.sanitize_html(html)
# All dangerous characters escaped
```

### Auto-Sanitization

```python
from pyvibe import *
from pyvibe.security import sanitize

# Sanitize data recursively
data = {
    "name": "<script>alert(1)</script>",
    "bio": "Normal text",
    "nested": {
        "field": "<img onerror=alert(1)>"
    }
}

safe_data = sanitize(data)
# All strings sanitized, structure preserved
```

---

## Rate Limiting

### Basic Usage

```python
from pyvibe import *
from pyvibe.security import Security

security = Security()
state = State(request_count=0)

@app.route("/api/data")
def api_data():
    # Check rate limit (100 requests per minute)
    client_ip = "127.0.0.1"  # In real app, get from request
    
    if not security.check_rate_limit(client_ip, max_requests=100, window=60):
        return tampil(alert("Terlalu banyak permintaan! Coba lagi nanti.", warna="merah"))
    
    # Process request...
    return tampil(judul("Data loaded"))
```

### Rate Limit Decorator

```python
from pyvibe.security import rate_limit

@app.route("/api/data")
@rate_limit(max_requests=100, window=60)
def api_data():
    # Rate limit automatically checked
    return tampil(judul("Data"))
```

### Custom Rate Limits

```python
# Different limits for different routes
@app.route("/api/public")
@rate_limit(max_requests=100, window=60)  # 100/minute
def public_api():
    return tampil(judul("Public"))

@app.route("/api/private")
@rate_limit(max_requests=10, window=60)  # 10/minute
def private_api():
    return tampil(judul("Private"))

@app.route("/api/upload")
@rate_limit(max_requests=5, window=60)   # 5/minute
def upload_api():
    return tampil(judul("Upload"))
```

---

## Input Sanitization

### Sanitize Function

```python
from pyvibe.security import sanitize, escape_html, strip_tags

# Sanitize all types
text = "<script>alert(1)</script>"
safe = sanitize(text)  # Escaped HTML

# Escape HTML entities
html = 'He said "Hello" & "Goodbye"'
escaped = escape_html(html)  # &amp;quot;Hello&amp;quot; &amp;amp; &amp;quot;Goodbye&amp;quot;

# Strip HTML tags
html = "<p>Hello <b>World</b></p>"
clean = strip_tags(html)  # "Hello World"
```

### Sanitize in Forms

```python
from pyvibe import *
from pyvibe.security import sanitize

@app.route("/submit", methods=["POST"])
def submit():
    # Get and sanitize form data
    nama = sanitize(request.form.get("nama", ""))
    email = sanitize(request.form.get("email", ""))
    pesan = sanitize(request.form.get("pesan", ""))
    
    # Process sanitized data...
    return tampil(alert("Data saved!", warna="hijau"))
```

---

## Security Headers

### Get Security Headers

```python
from pyvibe.security import Security

security = Security()

# Get recommended security headers
headers = security.get_security_headers()
print(headers)
# {
#     "X-Content-Type-Options": "nosniff",
#     "X-Frame-Options": "DENY",
#     "X-XSS-Protection": "1; mode=block",
#     "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
#     "Content-Security-Policy": "default-src 'self'",
#     "Referrer-Policy": "strict-origin-when-cross-origin",
#     "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
# }
```

### Apply Security Headers

```python
from pyvibe.security import Security

security = Security()

@app.after_request
def add_security_headers(response):
    headers = security.get_security_headers()
    for key, value in headers.items():
        response.headers[key] = value
    return response
```

---

## Password Hashing

### Hash Password

```python
from pyvibe.security import Security

security = Security()

# Generate password hash
password = "my_secure_password123"
hashed = security.hash_api_key(password)  # Uses SHA-256

# In production, use bcrypt or argon2:
# import bcrypt
# hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

### API Key Management

```python
from pyvibe.security import Security

security = Security()

# Generate API key
api_key = security.generate_api_key()
print(f"API Key: {api_key}")

# Hash for storage
hashed_key = security.hash_api_key(api_key)
print(f"Hashed: {hashed_key}")

# Verify API key
is_valid = security.verify_api_key(api_key, hashed_key)
print(f"Valid: {is_valid}")  # True
```

---

## IP Blocking

### Block/Unblock IPs

```python
from pyvibe.security import Security

security = Security()

# Block suspicious IP
security.block_ip("192.168.1.100")

# Check if IP is blocked
if security.is_ip_blocked("192.168.1.100"):
    return tampil(alert("Access denied!", warna="merah"))

# Unblock IP
security.unblock_ip("192.168.1.100")
```

---

## Email/URL Validation

### Validate Email

```python
from pyvibe.security import Security

security = Security()

# Validate email format
emails = [
    "valid@example.com",
    "invalid-email",
    "user@domain.co.id",
]

for email in emails:
    is_valid = security.validate_email(email)
    print(f"{email}: {'✅ Valid' if is_valid else '❌ Invalid'}")
```

### Validate URL

```python
from pyvibe.security import Security

security = Security()

# Validate URL format
urls = [
    "https://example.com",
    "http://localhost:3000",
    "not-a-url",
]

for url in urls:
    is_valid = security.validate_url(url)
    print(f"{url}: {'✅ Valid' if is_valid else '❌ Invalid'}")
```

---

## Complete Security Example

```python
from pyvibe import *
from pyvibe.security import Security, csrf_protect, rate_limit, sanitize

app = App("Secure Website")
security = Security()

@app.route("/")
def beranda():
    token = security.generate_csrf_token()
    return tampil(
        judul("Secure Form"),
        
        input_teks("Name"),
        input_email("Email"),
        textarea("Message"),
        
        Component(tag="input", type="hidden", name="csrf_token", value=token),
        tombol("Submit", warna="biru"),
    )

@app.route("/submit", methods=["POST"])
@csrf_protect
@rate_limit(max_requests=10, window=60)
def submit():
    # Sanitize input
    nama = sanitize(request.form.get("nama", ""))
    email = sanitize(request.form.get("email", ""))
    
    # Validate email
    if not security.validate_email(email):
        return tampil(alert("Email tidak valid!", warna="merah"))
    
    # Process...
    return tampil(alert("Terima kasih!", warna="hijau"))

# Add security headers
@app.after_request
def security_headers(response):
    for key, value in security.get_security_headers().items():
        response.headers[key] = value
    return response

app.jalan()
```

---

## 💡 Security Best Practices

### 1. Always Sanitize User Input
```python
# ✅ Good
nama = sanitize(request.form.get("nama", ""))

# ❌ Bad
nama = request.form.get("nama", "")  # Raw input!
```

### 2. Validate Email/URL
```python
# ✅ Good
if not security.validate_email(email):
    return error("Invalid email")

# ❌ Bad
# No validation!
```

### 3. Use CSRF Protection for Forms
```python
# ✅ Good
@app.route("/form")
@csrf_protect
def form():
    return tampil(...)

# ❌ Bad
@app.route("/form")  # No CSRF!
def form():
    return tampil(...)
```

### 4. Rate Limit API Endpoints
```python
# ✅ Good
@app.route("/api/data")
@rate_limit(max_requests=100, window=60)
def api_data():
    return data

# ❌ Bad
@app.route("/api/data")  # No rate limit!
def api_data():
    return data
```

### 5. Use HTTPS in Production
```python
# ✅ Good: force HTTPS
app = App("My Website", force_https=True)

# ❌ Bad: HTTP allowed
app = App("My Website")  # HTTP allowed
```

---

## 📚 Selanjutnya

- [State Management](./state.md) — Reactive state
- [Deployment](./deployment.md) — Deploy securely

---

Made with ❤️ in Indonesia 🇮🇩
