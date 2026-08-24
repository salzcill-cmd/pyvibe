# 🚀 Deployment

> Panduan lengkap deploy PyVibe website ke berbagai platform: Vercel, Netlify, GitHub Pages, Docker.

---

## 📋 Daftar Isi

1. [Build Static Files](#build-static-files)
2. [Vercel](#vercel)
3. [Netlify](#netlify)
4. [GitHub Pages](#github-pages)
5. [Docker](#docker)
6. [Custom Server](#custom-server)

---

## Build Static Files

Sebelum deploy, build project lo ke static files:

```bash
# Build ke folder dist/
pyvibe build

# Build ke custom folder
pyvibe build --output my-dist
```

### Output Structure

```
dist/
├── index.html          # Beranda
├── about.html          # Halaman /about
├── contact.html        # Halaman /contact
├── css/
│   └── style.css       # Auto-generated CSS
├── js/
│   └── app.js          # Auto-generated JS
└── images/             # Static images (jika ada)
```

---

## Vercel

### Step-by-Step Deploy

1. **Install Vercel CLI**
```bash
npm i -g vercel
```

2. **Login to Vercel**
```bash
vercel login
```

3. **Build Project**
```bash
pyvibe build
```

4. **Deploy**
```bash
vercel --prod
```

5. **Follow Prompts**
- Set up and deploy? `Y`
- Which scope? Select your account
- Link to existing project? `N`
- Project name? `my-pyvibe-app`
- Directory where code is located? `./dist`

### Vercel Configuration

Create `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "dist/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

### Custom Domain

```bash
# Add custom domain
vercel domains add mydomain.com
```

---

## Netlify

### Step-by-Step Deploy

1. **Install Netlify CLI**
```bash
npm install -g netlify-cli
```

2. **Login to Netlify**
```bash
netlify login
```

3. **Build Project**
```bash
pyvibe build
```

4. **Deploy**
```bash
netlify deploy --dir=dist --prod
```

### Netlify Configuration

Create `netlify.toml`:
```toml
[build]
  publish = "dist"
  command = "pyvibe build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Form Handling

Netlify support form handling. Add to your form:
```python
form_tag = Component(tag="form", attrs={
    "method": "POST",
    "data-netlify": "true",
    "name": "contact"
})

input_teks("Name", name="name")
input_email("Email", name="email")
textarea("Message", name="message")
tombol("Submit", warna="biru")
```

---

## GitHub Pages

### Step-by-Step Deploy

1. **Build Project**
```bash
pyvibe build
```

2. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/repo.git
git push -u origin main
```

3. **Enable GitHub Pages**
- Go to Repository → Settings → Pages
- Source: Deploy from a branch
- Branch: `main` / `/dist`
- Save

4. **Access Your Site**
```
https://username.github.io/repo-name/
```

### GitHub Actions Auto-Deploy

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy PyVibe

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install pyvibe
    
    - name: Build
      run: |
        pyvibe build
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./dist
```

---

## Docker

### Basic Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install PyVibe
RUN pip install pyvibe

# Copy project
COPY . .

# Build
RUN pyvibe build

# Expose port
EXPOSE 3000

# Serve static files
CMD ["python", "-m", "http.server", "3000", "--directory", "dist"]
```

### Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - .:/app
    command: python -m http.server 3000 --directory dist
```

### Build and Run

```bash
# Build image
docker build -t my-pyvibe-app .

# Run container
docker run -p 3000:3000 my-pyvibe-app

# Or with docker-compose
docker-compose up
```

### Production Dockerfile

```dockerfile
# Build stage
FROM python:3.9-slim as builder
WORKDIR /app
COPY . .
RUN pip install pyvibe && pyvibe build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## Custom Server

### Python HTTP Server

```bash
# Simple HTTP server
cd dist
python -m http.server 3000

# With binding
python -m http.server 3000 --bind 0.0.0.0
```

### Production Server (Gunicorn)

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 4 app:app
```

### Nginx Configuration

Create `/etc/nginx/sites-available/my-pyvibe-app`:
```nginx
server {
    listen 80;
    server_name mydomain.com;
    root /var/www/my-pyvibe-app/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /static {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

### Apache Configuration

Create `.htaccess`:
```apache
RewriteEngine On
RewriteBase /

# Redirect to HTTPS
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Serve index.html for all routes
RewriteRule ^ index.html [L]

# Cache static files
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType text/css "access plus 1 year"
    ExpiresByType application/javascript "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
</IfModule>
```

---

## Environment Variables

### Using Environment Variables

```python
import os

# Get environment variables
api_key = os.environ.get("API_KEY", "default_value")
debug = os.environ.get("DEBUG", "False").lower() == "true"

app = App(
    "My Website",
    debug=debug,
    api_key=api_key,
)
```

### .env File

Create `.env`:
```
DEBUG=True
API_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
```

Load in Python:
```python
from dotenv import load_dotenv
load_dotenv()

import os
api_key = os.environ.get("API_KEY")
```

---

## Performance Optimization

### 1. Enable Compression

```nginx
# Nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml;
gzip_min_length 256;
```

### 2. Cache Headers

```nginx
# Static files
location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### 3. Minify Output

```python
# Build with minification
app.build_minified=True
```

---

## 💡 Deployment Checklist

- [ ] Build project: `pyvibe build`
- [ ] Test locally: `cd dist && python -m http.server 3000`
- [ ] Check all routes work
- [ ] Check responsive design
- [ ] Check images load
- [ ] Check CSS/JS loads
- [ ] Enable HTTPS
- [ ] Set up custom domain (optional)
- [ ] Configure redirects
- [ ] Set up analytics (optional)

---

## 📚 Selanjutnya

- [Security Guide](./security.md) — Security features
- [FAQ & Troubleshooting](./faq.md) — Common issues

---

Made with ❤️ in Indonesia 🇮🇩
