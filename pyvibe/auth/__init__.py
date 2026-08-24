"""
PyVibe Auth — authentication system.

Usage:
    from pyvibe.auth import Auth, User

    # Setup
    auth = Auth(db)

    # Register
    user = auth.register("Andi", "andi@test.com", "password123")

    # Login
    user = auth.login("andi@test.com", "password123")

    # Check auth
    if auth.is_logged_in():
        user = auth.current_user()

    # Logout
    auth.logout()
"""

from __future__ import annotations
import hashlib
import secrets
import json
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from pyvibe.database import Database, Model


class User(Model):
    """User model."""
    table = "users"
    columns = ["id", "nama", "email", "password_hash", "role", "created_at"]


class Auth:
    """
    Authentication system.

    Usage:
        db = Database("auth.db")
        auth = Auth(db)

        # Register
        user = auth.register("Andi", "andi@test.com", "password123")

        # Login
        user = auth.login("andi@test.com", "password123")

        # Check
        if auth.is_logged_in():
            print(f"Welcome, {auth.current_user().nama}!")
    """

    def __init__(self, db: Database):
        self.db = db
        self._current_user: Optional[User] = None
        self._session: Dict[str, Any] = {}

        # Setup
        User.set_db(db)
        self._setup_tables()

    def _setup_tables(self):
        """Create auth tables."""
        self.db.create_table("users", {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "nama": "TEXT NOT NULL",
            "email": "TEXT UNIQUE NOT NULL",
            "password_hash": "TEXT NOT NULL",
            "role": "TEXT DEFAULT 'user'",
            "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        })

        self.db.create_table("sessions", {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "user_id": "INTEGER NOT NULL",
            "token": "TEXT UNIQUE NOT NULL",
            "expires_at": "TIMESTAMP NOT NULL",
            "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        })

    def _hash_password(self, password: str) -> str:
        """Hash password dengan SHA256 + salt."""
        salt = secrets.token_hex(16)
        hash_obj = hashlib.sha256(f"{salt}{password}".encode())
        return f"{salt}:{hash_obj.hexdigest()}"

    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password."""
        try:
            salt, hash_val = password_hash.split(":")
            hash_obj = hashlib.sha256(f"{salt}{password}".encode())
            return hash_obj.hexdigest() == hash_val
        except:
            return False

    def register(self, nama: str, email: str, password: str, role: str = "user") -> Optional[User]:
        """Register user baru."""
        # Check if email exists
        if self.db.exists("users", "email = ?", (email,)):
            print(f"Email {email} sudah terdaftar.")
            return None

        # Validate
        if len(password) < 8:
            print("Password minimal 8 karakter.")
            return None

        # Create user
        password_hash = self._hash_password(password)
        user_id = self.db.insert("users", {
            "nama": nama,
            "email": email,
            "password_hash": password_hash,
            "role": role,
        })

        if user_id:
            return User(id=user_id, nama=nama, email=email, role=role)
        return None

    def login(self, email: str, password: str) -> Optional[User]:
        """Login user."""
        row = self.db.query_one("SELECT * FROM users WHERE email = ?", (email,))
        if not row:
            print("Email tidak ditemukan.")
            return None

        if not self._verify_password(password, row["password_hash"]):
            print("Password salah.")
            return None

        user = User(**{k: v for k, v in row.items() if k != "password_hash"})
        self._current_user = user

        # Create session
        token = secrets.token_urlsafe(32)
        expires = datetime.now() + timedelta(days=7)
        self.db.insert("sessions", {
            "user_id": user.id,
            "token": token,
            "expires_at": expires.isoformat(),
        })

        self._session = {"token": token, "user_id": user.id}
        return user

    def logout(self):
        """Logout user."""
        self._current_user = None
        self._session = {}

    def is_logged_in(self) -> bool:
        """Check if user is logged in."""
        return self._current_user is not None

    def current_user(self) -> Optional[User]:
        """Get current user."""
        return self._current_user

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        row = self.db.query_one("SELECT * FROM users WHERE id = ?", (user_id,))
        if row:
            return User(**{k: v for k, v in row.items() if k != "password_hash"})
        return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        row = self.db.query_one("SELECT * FROM users WHERE email = ?", (email,))
        if row:
            return User(**{k: v for k, v in row.items() if k != "password_hash"})
        return None

    def update_password(self, user_id: int, new_password: str) -> bool:
        """Update user password."""
        if len(new_password) < 8:
            print("Password minimal 8 karakter.")
            return False

        password_hash = self._hash_password(new_password)
        return self.db.update("users", {"password_hash": password_hash}, "id = ?", (user_id,))

    def get_all_users(self) -> List[User]:
        """Get all users."""
        rows = self.db.query("SELECT * FROM users")
        return [User(**{k: v for k, v in row.items() if k != "password_hash"}) for row in rows]

    def delete_user(self, user_id: int) -> bool:
        """Delete user."""
        return self.db.delete("users", "id = ?", (user_id,))

    def require_auth(self, func):
        """Decorator untuk protected routes."""
        def wrapper(*args, **kwargs):
            if not self.is_logged_in():
                return {"error": "Unauthorized"}, 401
            return func(*args, **kwargs)
        return wrapper

    def require_role(self, role: str):
        """Decorator untuk role-based access."""
        def decorator(func):
            def wrapper(*args, **kwargs):
                if not self.is_logged_in():
                    return {"error": "Unauthorized"}, 401
                if self.current_user().role != role:
                    return {"error": "Forbidden"}, 403
                return func(*args, **kwargs)
            return wrapper
        return decorator


# ==================== Password Utilities ====================

def hash_password(password: str) -> str:
    """Hash password."""
    salt = secrets.token_hex(16)
    hash_obj = hashlib.sha256(f"{salt}{password}".encode())
    return f"{salt}:{hash_obj.hexdigest()}"


def verify_password(password: str, password_hash: str) -> bool:
    """Verify password."""
    try:
        salt, hash_val = password_hash.split(":")
        hash_obj = hashlib.sha256(f"{salt}{password}".encode())
        return hash_obj.hexdigest() == hash_val
    except:
        return False


def generate_token(length: int = 32) -> str:
    """Generate random token."""
    return secrets.token_urlsafe(length)
