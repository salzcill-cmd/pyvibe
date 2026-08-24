# 🔄 State Management

> Panduan lengkap state management, reactive data, dan data binding di PyVibe.

---

## 📋 Daftar Isi

1. [Basic State](#basic-state)
2. [Reactive State](#reactive-state)
3. [State in Components](#state-in-components)
4. [Form State](#form-state)
5. [Global State](#global-state)

---

## Basic State

### Create State

```python
from pyvibe import *

# Create state with initial values
state = State(
    count=0,
    nama="Budi",
    isLoggedIn=False,
    items=[],
)

# Access state values
print(state.count)      # 0
print(state.nama)       # "Budi"
print(state.isLoggedIn) # False
```

### Set State Values

```python
# Set single value
state.count = 1
state.nama = "Sari"

# Set multiple values
state.update(count=0, nama="Reset")
```

---

## Reactive State

PyVibe support reactive state yang otomatis update UI saat data berubah:

### Basic Reactive State

```python
from pyvibe import *

app = App("Reactive Counter")
state = State(count=0)

@app.route("/")
def beranda():
    return tampil(
        judul(f"Count: {state.count}").tengah(),
        
        baris(
            tombol("- Kurang", warna="merah", onclick="decrement()"),
            tombol("+ Tambah", warna="hijau", onclick="increment()"),
        ).gap(4).tengah(),
        
        paragraf(f"Total: {state.count}").tengah(),
    )

app.jalan()
```

### State Listeners

```python
state = State(count=0)

# Listen to state changes
@state.on("count")
def on_count_change(new_value, old_value):
    print(f"Count changed from {old_value} to {new_value}")

# Update state
state.count = 1  # Triggers listener
```

---

## State in Components

### Using State in Route Handlers

```python
from pyvibe import *

app = App("Todo App")
state = State(todos=[], filter="all")

@app.route("/")
def beranda():
    # Filter todos based on state
    filtered = state.todos
    if state.filter == "active":
        filtered = [t for t in state.todos if not t["done"]]
    elif state.filter == "completed":
        filtered = [t for t in state.todos if t["done"]]
    
    return tampil(
        judul("Todo App").tengah(),
        
        # Filter buttons
        baris(
            tombol("All", onclick="setFilter('all')"),
            tombol("Active", onclick="setFilter('active')"),
            tombol("Completed", onclick="setFilter('completed')"),
        ).tengah().gap(2),
        
        # Todo list
        *[
            baris(
                centang(todo["text"], checked=todo["done"]),
                tombol("🗑️", onclick=f"deleteTodo({i})"),
            )
            for i, todo in enumerate(filtered)
        ],
        
        # Add todo form
        baris(
            input_teks("New todo"),
            tombol("Add", onclick="addTodo()"),
        ).gap(2),
    )

app.jalan()
```

---

## Form State

### Form with State

```python
from pyvibe import *

app = App("Form Example")
state = State(
    nama="",
    email="",
    agree=False,
    submitted=False,
)

@app.route("/")
def form():
    if state.submitted:
        return tampil(
            judul("Terima Kasih!").tengah(),
            paragraf(f"Nama: {state.nama}").tengah(),
            paragraf(f"Email: {state.email}").tengah(),
            tombol("Kembali", onclick="resetForm()"),
        )
    
    return tampil(
        judul("Form Pendaftaran").tengah(),
        
        input_teks("Nama", value=state.nama, oninput="updateNama(this.value)"),
        spasi(8),
        input_email("Email", value=state.email, oninput="updateEmail(this.value)"),
        spasi(8),
        centang("Saya setuju", checked=state.agree, onchange="toggleAgree()"),
        spasi(16),
        
        tombol(
            "Daftar",
            warna="biru",
            onclick="submitForm()",
            disabled=not (state.nama and state.email and state.agree),
        ),
    )

app.jalan()
```

### Form Validation State

```python
from pyvibe import *
from pyvibe.forms.validation import FormValidator, required, email, min_length

app = App("Form Validation")
state = State(
    form={},
    errors={},
    submitted=False,
)

validator = FormValidator({
    "nama": [required(), min_length(3)],
    "email": [required(), email()],
})

@app.route("/")
def form():
    return tampil(
        judul("Registration Form").tengah(),
        
        input_teks(
            "Nama",
            value=state.form.get("nama", ""),
            error=state.errors.get("nama"),
        ),
        spasi(8),
        
        input_email(
            "Email",
            value=state.form.get("email", ""),
            error=state.errors.get("email"),
        ),
        spasi(16),
        
        tombol("Register", warna="biru", onclick="validateAndSubmit()"),
    )

app.jalan()
```

---

## Global State

### Shared State Across Routes

```python
from pyvibe import *

app = App("Global State Demo")

# Global state accessible from all routes
state = State(
    user=None,
    theme="light",
    notifications=0,
)

@app.route("/")
def beranda():
    if state.user:
        return tampil(
            navbar(
                judul(f"Hello, {state.user['nama']}!"),
                paragraf(f"Notifications: {state.notifications}"),
                tombol("Logout", onclick="logout()"),
            ),
            judul("Dashboard"),
        )
    
    return tampil(
        judul("Please Login").tengah(),
        tombol("Login", warna="biru", onclick="login()"),
    )

@app.route("/profile")
def profile():
    if not state.user:
        return tampil(judul("Unauthorized").tengah())
    
    return tampil(
        navbar(judul("Profile")),
        judul(f"Profile: {state.user['nama']}"),
        paragraf(f"Email: {state.user['email']}"),
    )

app.jalan()
```

### State with API

```python
from pyvibe import *
from pyvibe.fetch import Fetch

app = App("API State Demo")
state = State(users=[], loading=False, error=None)

api = Fetch("https://jsonplaceholder.typicode.com")

@app.route("/")
def users():
    return tampil(
        judul("Users").tengah(),
        
        # Loading state
        *([loader()] if state.loading else []),
        
        # Error state
        *([alert(state.error, warna="merah")] if state.error else []),
        
        # Users list
        *[
            kartu(
                judul(user["name"]),
                paragraf(user["email"]),
                padding="16px",
            )
            for user in state.users
        ],
        
        tombol("Load Users", warna="biru", onclick="loadUsers()"),
    )

app.jalan()
```

---

## 💡 Tips State Management

### 1. Keep State Minimal
```python
# ✅ Good: minimal state
state = State(count=0, items=[])

# ❌ Avoid: too much state
state = State(
    count=0, items=[], user=None, theme="light",
    modal_open=False, loading=False, error=None,
    # ... too many!
)
```

### 2. Use Descriptive Names
```python
# ✅ Good: descriptive names
state = State(
    todo_list=[],
    filter_status="all",
    is_logged_in=False,
)

# ❌ Avoid: vague names
state = State(data=[], f="", ok=False)
```

### 3. Derive State When Possible
```python
# ✅ Good: derive from existing state
completed_count = sum(1 for t in state.todos if t["done"])

# ❌ Avoid: duplicate state
state.completed_count = 5  # Redundant!
```

---

## 📚 Selanjutnya

- [Routing Guide](./routing.md) — Multi-page routing
- [Security Guide](./security.md) — Security features

---

Made with ❤️ in Indonesia 🇮🇩
