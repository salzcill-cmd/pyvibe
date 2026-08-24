"""
PyVibe Performance — monitoring and profiling utilities.

Usage:
    from pyvibe.performance import monitor, timer, profile

    # Monitor function
    @monitor
    def slow_function():
        time.sleep(1)

    # Timer
    with timer("my-operation"):
        do_something()

    # Profile
    result = profile(my_function, args=(arg1, arg2))
"""

from __future__ import annotations
import time
import os
import json
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from functools import wraps
from collections import defaultdict
from contextlib import contextmanager


# ==================== Timer ====================

@dataclass
class TimingRecord:
    """Timing record."""
    name: str
    duration: float
    timestamp: float
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "duration_ms": round(self.duration * 1000, 2),
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }


class Timer:
    """Performance timer."""

    def __init__(self):
        self.records: List[TimingRecord] = []
        self._active: Dict[str, float] = {}

    def start(self, name: str) -> None:
        """Start timing."""
        self._active[name] = time.time()

    def stop(self, name: str, metadata: Optional[Dict] = None) -> float:
        """Stop timing and record."""
        if name in self._active:
            duration = time.time() - self._active.pop(name)
            record = TimingRecord(
                name=name,
                duration=duration,
                timestamp=time.time(),
                metadata=metadata or {},
            )
            self.records.append(record)
            return duration
        return 0.0

    @contextmanager
    def measure(self, name: str, metadata: Optional[Dict] = None):
        """Context manager for timing."""
        self.start(name)
        try:
            yield
        finally:
            self.stop(name, metadata)

    def get_records(self, name: Optional[str] = None) -> List[TimingRecord]:
        """Get timing records."""
        if name:
            return [r for r in self.records if r.name == name]
        return list(self.records)

    def get_stats(self, name: str) -> Dict[str, Any]:
        """Get statistics for a timer."""
        records = [r for r in self.records if r.name == name]
        if not records:
            return {}
        
        durations = [r.duration * 1000 for r in records]
        return {
            "name": name,
            "count": len(durations),
            "total_ms": round(sum(durations), 2),
            "avg_ms": round(sum(durations) / len(durations), 2),
            "min_ms": round(min(durations), 2),
            "max_ms": round(max(durations), 2),
        }

    def get_slowest(self, top: int = 10) -> List[Dict]:
        """Get slowest operations."""
        stats = defaultdict(list)
        for record in self.records:
            stats[record.name].append(record.duration * 1000)
        
        result = []
        for name, durations in stats.items():
            result.append({
                "name": name,
                "avg_ms": round(sum(durations) / len(durations), 2),
                "count": len(durations),
            })
        
        return sorted(result, key=lambda x: x["avg_ms"], reverse=True)[:top]

    def clear(self) -> None:
        """Clear all records."""
        self.records.clear()
        self._active.clear()

    def to_dict(self) -> Dict:
        """Export all data."""
        return {
            "records": [r.to_dict() for r in self.records],
            "stats": {name: self.get_stats(name) for name in set(r.name for r in self.records)},
        }

    def save(self, filepath: str = "performance.json") -> None:
        """Save to file."""
        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=2)


# Global timer
_timer = Timer()


@contextmanager
def timer(name: str, metadata: Optional[Dict] = None):
    """
    Time a code block.
    
    Usage:
        with timer("my-operation"):
            do_something()
    """
    _timer.start(name)
    try:
        yield
    finally:
        _timer.stop(name, metadata)


# ==================== Monitor Decorator ====================

def monitor(func: Callable = None, *, threshold_ms: float = 100) -> Callable:
    """
    Monitor function performance.
    
    Usage:
        @monitor
        def slow_function():
            time.sleep(1)
        
        @monitor(threshold_ms=50)
        def fast_function():
            pass
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = f(*args, **kwargs)
            duration = (time.time() - start) * 1000
            
            if duration > threshold_ms:
                _timer.records.append(TimingRecord(
                    name=f.__name__,
                    duration=duration / 1000,
                    timestamp=time.time(),
                    metadata={"slow": True, "threshold_ms": threshold_ms},
                ))
            
            return result
        
        wrapper._monitor = True
        return wrapper
    
    if func is not None:
        return decorator(func)
    return decorator


# ==================== Profiler ====================

def profile(func: Callable, *args, **kwargs) -> Dict[str, Any]:
    """
    Profile function execution.
    
    Usage:
        result = profile(my_function, arg1, arg2)
    """
    import cProfile
    import pstats
    import io

    profiler = cProfile.Profile()
    profiler.enable()
    
    start_time = time.time()
    result = func(*args, **kwargs)
    duration = time.time() - start_time
    
    profiler.disable()
    
    # Get stats
    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats("cumulative")
    stats.print_stats(10)
    
    return {
        "result": result,
        "duration_ms": round(duration * 1000, 2),
        "stats": stream.getvalue(),
    }


# ==================== Memory Monitor ====================

def get_memory_usage() -> Dict[str, Any]:
    """Get current memory usage."""
    try:
        import psutil
        process = psutil.Process(os.getpid())
        mem_info = process.memory_info()
        return {
            "rss_mb": round(mem_info.rss / 1024 / 1024, 2),
            "vms_mb": round(mem_info.vms / 1024 / 1024, 2),
        }
    except ImportError:
        return {"rss_mb": 0, "vms_mb": 0, "note": "psutil not installed"}


# ==================== Cache Stats ====================

class CacheStats:
    """Cache performance statistics."""

    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.total = 0

    def record_hit(self) -> None:
        self.hits += 1
        self.total += 1

    def record_miss(self) -> None:
        self.misses += 1
        self.total += 1

    @property
    def hit_rate(self) -> float:
        return (self.hits / self.total * 100) if self.total > 0 else 0

    def to_dict(self) -> Dict:
        return {
            "hits": self.hits,
            "misses": self.misses,
            "total": self.total,
            "hit_rate": f"{self.hit_rate:.1f}%",
        }


# ==================== Benchmark ====================

def benchmark(func: Callable, iterations: int = 100, *args, **kwargs) -> Dict[str, Any]:
    """
    Benchmark function.
    
    Usage:
        result = benchmark(my_function, iterations=1000)
    """
    durations = []
    
    for _ in range(iterations):
        start = time.time()
        func(*args, **kwargs)
        duration = (time.time() - start) * 1000
        durations.append(duration)
    
    return {
        "function": func.__name__,
        "iterations": iterations,
        "total_ms": round(sum(durations), 2),
        "avg_ms": round(sum(durations) / len(durations), 2),
        "min_ms": round(min(durations), 2),
        "max_ms": round(max(durations), 2),
        "median_ms": round(sorted(durations)[len(durations) // 2], 2),
    }


# ==================== Get Timer ====================

def get_timer() -> Timer:
    """Get global timer instance."""
    return _timer
