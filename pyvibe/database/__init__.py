"""
PyVibe Database — SQLite integration.

Usage:
    from pyvibe.database import Database

    db = Database("myapp.db")

    # Create table
    db.create_table("users", {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "nama": "TEXT NOT NULL",
        "email": "TEXT UNIQUE NOT NULL",
        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
    })

    # Insert
    db.insert("users", {"nama": "Andi", "email": "andi@test.com"})

    # Query
    users = db.query("SELECT * FROM users")
    user = db.query_one("SELECT * FROM users WHERE id = ?", (1,))

    # Update
    db.update("users", {"nama": "Budi"}, where="id = 1")

    # Delete
    db.delete("users", where="id = 1")
"""

from __future__ import annotations
import sqlite3
import os
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime


class Database:
    """
    SQLite database wrapper.

    Usage:
        db = Database("myapp.db")
        db.create_table("users", {"id": "INTEGER PRIMARY KEY", "nama": "TEXT"})
        db.insert("users", {"nama": "Andi"})
        users = db.query("SELECT * FROM users")
    """

    def __init__(self, db_path: str = "pyvibe.db"):
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None

    def connect(self):
        """Connect to database."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        return self

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def create_table(self, table_name: str, columns: Dict[str, str]) -> bool:
        """Create table."""
        if not self.conn:
            self.connect()

        cols = ", ".join([f"{col} {dtype}" for col, dtype in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({cols})"

        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error creating table: {e}")
            return False

    def drop_table(self, table_name: str) -> bool:
        """Drop table."""
        if not self.conn:
            self.connect()

        try:
            self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error dropping table: {e}")
            return False

    def insert(self, table_name: str, data: Dict[str, Any]) -> Optional[int]:
        """Insert row and return last row id."""
        if not self.conn:
            self.connect()

        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        try:
            self.cursor.execute(query, list(data.values()))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Error inserting: {e}")
            return None

    def insert_many(self, table_name: str, rows: List[Dict[str, Any]]) -> bool:
        """Insert multiple rows."""
        if not self.conn:
            self.connect()

        if not rows:
            return True

        columns = ", ".join(rows[0].keys())
        placeholders = ", ".join(["?" for _ in rows[0]])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        try:
            self.cursor.executemany(query, [list(row.values()) for row in rows])
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error inserting many: {e}")
            return False

    def query(self, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        """Execute query and return all rows."""
        if not self.conn:
            self.connect()

        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error querying: {e}")
            return []

    def query_one(self, query: str, params: Optional[Tuple] = None) -> Optional[Dict[str, Any]]:
        """Execute query and return one row."""
        if not self.conn:
            self.connect()

        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"Error querying: {e}")
            return None

    def update(self, table_name: str, data: Dict[str, Any], where: str = "", where_params: Optional[Tuple] = None) -> bool:
        """Update rows."""
        if not self.conn:
            self.connect()

        set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
        query = f"UPDATE {table_name} SET {set_clause}"
        if where:
            query += f" WHERE {where}"

        params = list(data.values())
        if where_params:
            params.extend(list(where_params))

        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating: {e}")
            return False

    def delete(self, table_name: str, where: str = "", where_params: Optional[Tuple] = None) -> bool:
        """Delete rows."""
        if not self.conn:
            self.connect()

        query = f"DELETE FROM {table_name}"
        if where:
            query += f" WHERE {where}"

        try:
            if where_params:
                self.cursor.execute(query, list(where_params))
            else:
                self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting: {e}")
            return False

    def count(self, table_name: str, where: str = "", where_params: Optional[Tuple] = None) -> int:
        """Count rows."""
        query = f"SELECT COUNT(*) FROM {table_name}"
        if where:
            query += f" WHERE {where}"

        result = self.query_one(query, where_params)
        return result["COUNT(*)"] if result else 0

    def exists(self, table_name: str, where: str = "", where_params: Optional[Tuple] = None) -> bool:
        """Check if row exists."""
        return self.count(table_name, where, where_params) > 0

    def tables(self) -> List[str]:
        """List all tables."""
        rows = self.query("SELECT name FROM sqlite_master WHERE type='table'")
        return [row["name"] for row in rows]

    def columns(self, table_name: str) -> List[Dict[str, str]]:
        """Get table columns."""
        rows = self.query(f"PRAGMA table_info({table_name})")
        return [{"name": row["name"], "type": row["type"]} for row in rows]

    def export_to_dict(self, table_name: str) -> List[Dict[str, Any]]:
        """Export table to dictionary."""
        return self.query(f"SELECT * FROM {table_name}")

    def import_from_dict(self, table_name: str, data: List[Dict[str, Any]]) -> bool:
        """Import data from dictionary."""
        return self.insert_many(table_name, data)


# ==================== ORM-like Helpers ====================

class Model:
    """
    Simple ORM-like model.

    Usage:
        class User(Model):
            table = "users"
            columns = ["id", "nama", "email"]

        # Create
        user = User.create(nama="Andi", email="andi@test.com")

        # Find
        user = User.find(1)
        users = User.all()
        user = User.where("email", "andi@test.com").first()

        # Update
        user.update(nama="Budi")

        # Delete
        user.delete()
    """

    table: str = ""
    columns: List[str] = []
    db: Optional[Database] = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def set_db(cls, db: Database):
        """Set database connection."""
        cls.db = db

    @classmethod
    def create(cls, **kwargs) -> "Model":
        """Create new record."""
        if not cls.db:
            raise ValueError("Database not set. Call Model.set_db(db) first.")

        row_id = cls.db.insert(cls.table, kwargs)
        if row_id:
            kwargs["id"] = row_id
            return cls(**kwargs)
        return None

    @classmethod
    def find(cls, id: int) -> Optional["Model"]:
        """Find by ID."""
        if not cls.db:
            raise ValueError("Database not set.")

        row = cls.db.query_one(f"SELECT * FROM {cls.table} WHERE id = ?", (id,))
        return cls(**row) if row else None

    @classmethod
    def all(cls) -> List["Model"]:
        """Get all records."""
        if not cls.db:
            raise ValueError("Database not set.")

        rows = cls.db.query(f"SELECT * FROM {cls.table}")
        return [cls(**row) for row in rows]

    @classmethod
    def where(cls, column: str, value: Any) -> "QuerySet":
        """Filter records."""
        if not cls.db:
            raise ValueError("Database not set.")

        rows = cls.db.query(f"SELECT * FROM {cls.table} WHERE {column} = ?", (value,))
        return QuerySet([cls(**row) for row in rows])

    @classmethod
    def count(cls) -> int:
        """Count records."""
        if not cls.db:
            raise ValueError("Database not set.")

        return cls.db.count(cls.table)

    def update(self, **kwargs) -> bool:
        """Update record."""
        if not self.__class__.db:
            raise ValueError("Database not set.")

        return self.__class__.db.update(self.__class__.table, kwargs, where="id = ?", where_params=(self.id,))

    def delete(self) -> bool:
        """Delete record."""
        if not self.__class__.db:
            raise ValueError("Database not set.")

        return self.__class__.db.delete(self.__class__.table, where="id = ?", where_params=(self.id,))

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}


class QuerySet:
    """Query set for chaining filters."""

    def __init__(self, results: List[Model]):
        self.results = results

    def first(self) -> Optional[Model]:
        return self.results[0] if self.results else None

    def last(self) -> Optional[Model]:
        return self.results[-1] if self.results else None

    def all(self) -> List[Model]:
        return self.results

    def count(self) -> int:
        return len(self.results)

    def exists(self) -> bool:
        return len(self.results) > 0
