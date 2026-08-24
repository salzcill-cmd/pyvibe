"""
PyVibe Logging & Performance — Unit Tests

Tests for: Logger, get_logger, setup_logging, LogLevel,
           timer, monitor, benchmark, get_timer, get_memory_usage
"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyvibe.logging import (
    Logger, get_logger, setup_logging, LogLevel,
    ConsoleHandler, FileHandler, TextFormatter, ColoredFormatter,
)
from pyvibe.performance import (
    monitor, timer, benchmark, get_timer, Timer,
    get_memory_usage, CacheStats,
)

passed = 0
failed = 0
total = 0


def test(name, condition, expected="", got=""):
    global passed, failed, total
    total += 1
    if condition:
        passed += 1
        print(f"  ✅ {name}")
    else:
        failed += 1
        print(f"  ❌ {name}")
        if expected or got:
            print(f"     Expected: {expected}")
            print(f"     Got: {got}")


print("=" * 70)
print("📝 PyVibe Logging & Performance — Unit Tests")
print("=" * 70)

# ==================== LogLevel ====================
print("\n--- LogLevel ---")

test("LogLevel.DEBUG", LogLevel.DEBUG == 10)
test("LogLevel.INFO", LogLevel.INFO == 20)
test("LogLevel.WARNING", LogLevel.WARNING == 30)
test("LogLevel.ERROR", LogLevel.ERROR == 40)
test("LogLevel.CRITICAL", LogLevel.CRITICAL == 50)
test("LogLevel.NAMES", 10 in LogLevel.NAMES)
test("LogLevel.COLORS", 10 in LogLevel.COLORS)

# ==================== Logger ====================
print("\n--- Logger ---")

logger = Logger("test-module")
test("Logger created", logger is not None)
test("Logger name", logger.name == "test-module")
test("Logger has handlers", isinstance(logger.handlers, list))

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")

test("Logger history length", len(logger.get_history()) == 5)

# Filter by level
error_logs = logger.get_history(level=LogLevel.ERROR)
test("Logger filter by level", len(error_logs) == 2)

logger.clear_history()
test("Logger clear history", len(logger.get_history()) == 0)

# ==================== Logger Handlers ====================
print("\n--- Logger Handlers ---")

logger2 = Logger("handler-test")
logger2.set_level(LogLevel.WARNING)

console_handler = ConsoleHandler(colored=True)
test("ConsoleHandler created", console_handler is not None)

logger2.add_handler(console_handler)
test("Logger add handler", len(logger2.handlers) == 1)

logger2.remove_handler(console_handler)
test("Logger remove handler", len(logger2.handlers) == 0)

# ==================== Logger Formatters ====================
print("\n--- Logger Formatters ---")

text_fmt = TextFormatter()
test("TextFormatter created", text_fmt is not None)

from pyvibe.logging import LogRecord
record = LogRecord(level=20, message="Test", module="test")
formatted = text_fmt.format(record)
test("TextFormatter format", "Test" in formatted)
test("TextFormatter has level", "INFO" in formatted)

colored_fmt = ColoredFormatter()
colored = colored_fmt.format(record)
test("ColoredFormatter format", "Test" in colored)

# ==================== get_logger ====================
print("\n--- get_logger ---")

logger_a = get_logger("module-a")
logger_b = get_logger("module-b")
logger_a2 = get_logger("module-a")

test("get_logger creates logger", logger_a is not None)
test("get_logger different modules", logger_a is not logger_b)
test("get_logger same module", logger_a is logger_a2)

# ==================== Timer ====================
print("\n--- Timer ---")

timer = Timer()
test("Timer created", timer is not None)

timer.start("test-op")
time.sleep(0.01)
duration = timer.stop("test-op")
test("Timer start/stop", duration > 0)
test("Timer records", len(timer.get_records()) == 1)

# Context manager
with timer.measure("context-op"):
    time.sleep(0.01)
test("Timer context manager", len(timer.get_records()) == 2)

# Stats
stats = timer.get_stats("test-op")
test("Timer stats count", stats["count"] == 1)
test("Timer stats avg_ms", "avg_ms" in stats)
test("Timer stats min_ms", "min_ms" in stats)
test("Timer stats max_ms", "max_ms" in stats)

# Slowest
slowest = timer.get_slowest(top=5)
test("Timer slowest", len(slowest) >= 1)

timer.clear()
test("Timer clear", len(timer.get_records()) == 0)

# ==================== monitor decorator ====================
print("\n--- monitor ---")

@monitor
def slow_func():
    time.sleep(0.01)
    return "done"

result = slow_func()
test("monitor returns result", result == "done")

@monitor(threshold_ms=50)
def fast_func():
    return "fast"

result2 = fast_func()
test("monitor fast function", result2 == "fast")

# ==================== benchmark ====================
print("\n--- benchmark ---")

def simple_func():
    return sum(range(100))

result = benchmark(simple_func, iterations=50)
test("benchmark returns dict", isinstance(result, dict))
test("benchmark has function name", result["function"] == "simple_func")
test("benchmark has iterations", result["iterations"] == 50)
test("benchmark has total_ms", "total_ms" in result)
test("benchmark has avg_ms", "avg_ms" in result)
test("benchmark has min_ms", "min_ms" in result)
test("benchmark has max_ms", "max_ms" in result)
test("benchmark has median_ms", "median_ms" in result)

# ==================== get_timer ====================
print("\n--- get_timer ---")

gt = get_timer()
test("get_timer returns Timer", isinstance(gt, Timer))

# ==================== get_memory_usage ====================
print("\n--- get_memory_usage ---")

mem = get_memory_usage()
test("get_memory_usage returns dict", isinstance(mem, dict))
test("get_memory_usage has rss_mb", "rss_mb" in mem)

# ==================== CacheStats ====================
print("\n--- CacheStats ---")

stats = CacheStats()
test("CacheStats initial hits", stats.hits == 0)
test("CacheStats initial misses", stats.misses == 0)
test("CacheStats initial total", stats.total == 0)
test("CacheStats initial hit_rate", stats.hit_rate == 0)

stats.record_hit()
stats.record_hit()
stats.record_miss()
test("CacheStats after ops hits", stats.hits == 2)
test("CacheStats after ops misses", stats.misses == 1)
test("CacheStats after ops total", stats.total == 3)
test("CacheStats hit_rate calc", abs(stats.hit_rate - 66.67) < 1)

stats_dict = stats.to_dict()
test("CacheStats to_dict", isinstance(stats_dict, dict))
test("CacheStats to_dict keys", "hit_rate" in stats_dict)

# ==================== setup_logging ====================
print("\n--- setup_logging ---")

setup_logging(level="DEBUG")
test("setup_logging DEBUG", True)

setup_logging(level="WARNING")
test("setup_logging WARNING", True)

# ==================== Edge Cases ====================
print("\n--- Edge Cases ---")

empty_logger = Logger("empty")
empty_logger.info("msg")
test("Logger single message", len(empty_logger.get_history()) == 1)

empty_logger.clear_history()
test("Logger clear single", len(empty_logger.get_history()) == 0)

timer2 = Timer()
timer2.start("op1")
timer2.stop("nonexistent")
test("Timer stop nonexistent", True)

# ==================== Summary ====================
print("\n" + "=" * 70)
print(f"Results: {passed}/{total} tests passed")
if failed == 0:
    print("🎉 ALL LOGGING & PERFORMANCE TESTS PASSED!")
else:
    print(f"⚠️ {failed} tests failed")
print("=" * 70)

sys.exit(0 if failed == 0 else 1)
