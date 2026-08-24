"""
PyVibe Cache — caching system.

Usage:
    from pyvibe.cache import Cache

    cache = Cache()

    # Basic operations
    cache.set("user:1", {"name": "Andi"}, ttl=300)
    user = cache.get("user:1")

    # With decorators
    @cache.memoize(ttl=600)
    def expensive_query():
        return db.query("SELECT * FROM users")

    # Cache tags
    cache.set("user:1", user, tags=["users"])
    cache.set("user:2", user, tags=["users"])
    cache.flush_tags(["users"])  # Clears all user cache
"""

from __future__ import annotations
import json
import os
import time
import hashlib
from typing import Any, Callable, Dict, List, Optional, Union
from functools import wraps
from collections import defaultdict


class CacheItem:
    """Cache item with metadata."""

    def __init__(self, value: Any, ttl: int = 300):
        self.value = value
        self.ttl = ttl
        self.created_at = time.time()
        self.access_count = 0
        self.tags: List[str] = []

    @property
    def is_expired(self) -> bool:
        return time.time() - self.created_at > self.ttl

    @property
    def age(self) -> float:
        return time.time() - self.created_at


class Cache:
    """
    In-memory cache with TTL support.

    Usage:
        cache = Cache()
        cache.set("key", "value", ttl=60)
        value = cache.get("key")
    """

    def __init__(self, default_ttl: int = 300, max_size: int = 10000):
        self._store: Dict[str, CacheItem] = {}
        self._tags: Dict[str, List[str]] = defaultdict(list)
        self.default_ttl = default_ttl
        self.max_size = max_size
        self.hits = 0
        self.misses = 0

    def get(self, key: str, default: Any = None) -> Any:
        """Get value from cache."""
        if key in self._store:
            item = self._store[key]
            if item.is_expired:
                self.delete(key)
                self.misses += 1
                return default
            item.access_count += 1
            self.hits += 1
            return item.value
        self.misses += 1
        return default

    def set(self, key: str, value: Any, ttl: Optional[int] = None, tags: Optional[List[str]] = None):
        """Set value in cache."""
        # Check max size
        if len(self._store) >= self.max_size and key not in self._store:
            self._evict()

        ttl = ttl or self.default_ttl
        item = CacheItem(value, ttl)
        if tags:
            item.tags = tags
            for tag in tags:
                self._tags[tag].append(key)

        self._store[key] = item

    def delete(self, key: str) -> bool:
        """Delete value from cache."""
        if key in self._store:
            item = self._store.pop(key)
            for tag in item.tags:
                if key in self._tags[tag]:
                    self._tags[tag].remove(key)
            return True
        return False

    def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        if key in self._store:
            if self._store[key].is_expired:
                self.delete(key)
                return False
            return True
        return False

    def flush(self):
        """Clear all cache."""
        self._store.clear()
        self._tags.clear()
        self.hits = 0
        self.misses = 0

    def flush_tags(self, tags: List[str]):
        """Clear cache by tags."""
        keys_to_delete = set()
        for tag in tags:
            keys_to_delete.update(self._tags.get(tag, []))
        for key in keys_to_delete:
            self.delete(key)

    def _evict(self):
        """Evict oldest items when cache is full."""
        if not self._store:
            return
        # Find item with oldest access time
        oldest_key = min(
            self._store.keys(),
            key=lambda k: self._store[k].access_count
        )
        self.delete(oldest_key)

    def size(self) -> int:
        """Get cache size."""
        return len(self._store)

    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total = self.hits + self.misses
        return {
            "size": self.size(),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{(self.hits / total * 100):.1f}%" if total > 0 else "0%",
        }

    def memoize(self, ttl: Optional[int] = None, key_prefix: str = ""):
        """Decorator to memoize function results."""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key
                key_parts = [key_prefix or func.__name__]
                key_parts.extend([str(a) for a in args])
                key_parts.extend([f"{k}={v}" for k, v in sorted(kwargs.items())])
                cache_key = hashlib.md5(":".join(key_parts).encode()).hexdigest()

                # Check cache
                result = self.get(cache_key)
                if result is not None:
                    return result

                # Execute function and cache result
                result = func(*args, **kwargs)
                self.set(cache_key, result, ttl=ttl)
                return result
            return wrapper
        return decorator

    def remember(self, key: str, ttl: Optional[int] = None, callback: Callable = None) -> Any:
        """Get value or compute and cache it."""
        value = self.get(key)
        if value is not None:
            return value

        if callback:
            value = callback()
            self.set(key, value, ttl=ttl)
            return value

        return None


class FileCache(Cache):
    """File-based cache."""

    def __init__(self, cache_dir: str = ".cache", **kwargs):
        super().__init__(**kwargs)
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def _get_path(self, key: str) -> str:
        safe_key = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{safe_key}.json")

    def get(self, key: str, default: Any = None) -> Any:
        path = self._get_path(key)
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                if data["expires_at"] > time.time():
                    return data["value"]
                else:
                    os.remove(path)
            except:
                pass
        return default

    def set(self, key: str, value: Any, ttl: Optional[int] = None, **kwargs):
        ttl = ttl or self.default_ttl
        path = self._get_path(key)
        data = {
            "value": value,
            "expires_at": time.time() + ttl,
            "created_at": time.time(),
        }
        with open(path, "w") as f:
            json.dump(data, f)

    def delete(self, key: str) -> bool:
        path = self._get_path(key)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False

    def flush(self):
        for filename in os.listdir(self.cache_dir):
            if filename.endswith(".json"):
                os.remove(os.path.join(self.cache_dir, filename))
