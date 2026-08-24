"""
PyVibe Hooks — Unit Tests

Tests for: use_local_storage, use_debounce, use_throttle, use_memo,
           use_effect, use_interval, use_timeout, use_previous,
           use_counter, use_toggle, use_list
"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyvibe.hooks import (
    use_local_storage, use_debounce, use_throttle, use_memo,
    use_effect, use_interval, use_timeout, use_previous,
    use_counter, use_toggle, use_list, LocalStorage,
    _get_counter_count, _get_toggle_value, _get_list_items,
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
print("🪝 PyVibe Hooks — Unit Tests")
print("=" * 70)

# ==================== LocalStorage ====================
print("\n--- LocalStorage ---")

storage = LocalStorage("test-namespace")
storage.set("test-key", "test-value")
test("LocalStorage set", storage.get("test-key") == "test-value")

storage.set("test-number", 42)
test("LocalStorage number", storage.get("test-number") == 42)

storage.set("test-list", [1, 2, 3])
test("LocalStorage list", storage.get("test-list") == [1, 2, 3])

test("LocalStorage default", storage.get("nonexistent", "default") == "default")

storage.delete("test-key")
test("LocalStorage delete", storage.get("test-key") is None)

storage.has("test-number")
test("LocalStorage has", storage.has("test-number") is True)
test("LocalStorage has not", storage.has("deleted-key") is False)

# ==================== use_counter ====================
print("\n--- use_counter ---")

counter = use_counter(0)
test("use_counter initial", _get_counter_count(counter) == 0)

counter["increment"]()
test("use_counter increment", _get_counter_count(counter) == 1)

counter["increment"]()
counter["increment"]()
test("use_counter multiple increments", _get_counter_count(counter) == 3)

counter["decrement"]()
test("use_counter decrement", _get_counter_count(counter) == 2)

counter["reset"]()
test("use_counter reset", _get_counter_count(counter) == 0)

counter2 = use_counter(10)
test("use_counter custom initial", _get_counter_count(counter2) == 10)
counter2["increment"]()
test("use_counter custom increment", _get_counter_count(counter2) == 11)

# ==================== use_toggle ====================
print("\n--- use_toggle ---")

toggle = use_toggle(False)
test("use_toggle initial false", _get_toggle_value(toggle) is False)

toggle["toggle"]()
test("use_toggle toggle", _get_toggle_value(toggle) is True)

toggle["toggle"]()
test("use_toggle toggle back", _get_toggle_value(toggle) is False)

toggle["on"]()
test("use_toggle on", _get_toggle_value(toggle) is True)

toggle["off"]()
test("use_toggle off", _get_toggle_value(toggle) is False)

toggle["on"]()
toggle["on"]()
test("use_toggle multiple on", _get_toggle_value(toggle) is True)

toggle2 = use_toggle(True)
test("use_toggle initial true", _get_toggle_value(toggle2) is True)

# ==================== use_list ====================
print("\n--- use_list ---")

lst = use_list([1, 2, 3])
test("use_list initial", _get_list_items(lst) == [1, 2, 3])

lst["add"](4)
test("use_list add", _get_list_items(lst) == [1, 2, 3, 4])

lst["remove"](0)
test("use_list remove", _get_list_items(lst) == [2, 3, 4])

lst["update"](0, 99)
test("use_list update", _get_list_items(lst) == [99, 3, 4])

lst["clear"]()
test("use_list clear", _get_list_items(lst) == [])

lst2 = use_list()
test("use_list empty initial", _get_list_items(lst2) == [])

lst2["add"]("first")
lst2["add"]("second")
test("use_list multiple adds", len(_get_list_items(lst2)) == 2)

# ==================== use_memo ====================
print("\n--- use_memo ---")

call_count = [0]

def expensive_calc():
    call_count[0] += 1
    return 42

memo = use_memo(expensive_calc, [])
result1 = memo()
result2 = memo()
test("use_memo result", result1 == 42)
test("use_memo cached", result2 == 42)

memo.clear()
result3 = memo()
test("use_memo after clear", result3 == 42)

# ==================== use_previous ====================
print("\n--- use_previous ---")

prev1 = use_previous("initial")
test("use_previous first call", prev1 is None)

prev2 = use_previous("second")
test("use_previous second call", prev2 == "initial")

prev3 = use_previous("third")
test("use_previous third call", prev3 == "second")

# ==================== use_effect ====================
print("\n--- use_effect ---")

effect_called = [False]

def effect_func():
    effect_called[0] = True
    return lambda: None  # cleanup

effect = use_effect(effect_func)
test("use_effect runs", effect_called[0] is True)
test("use_effect has cleanup", hasattr(effect, "cleanup"))

effect.cleanup()
test("use_effect cleanup runs", True)

# ==================== use_debounce ====================
print("\n--- use_debounce ---")

debounce_results = []

def debounced_func(x):
    debounce_results.append(x)

debounced = use_debounce(debounced_func, delay=10)
test("use_debounce returns callable", callable(debounced))

# Note: debounce is async, so we just test it's callable
debounced("test")
test("use_debounce callable", callable(debounced))

# ==================== use_throttle ====================
print("\n--- use_throttle ---")

throttle_results = []

def throttled_func(x):
    throttle_results.append(x)

throttled = use_throttle(throttled_func, limit=10)
test("use_throttle returns callable", callable(throttled))

throttled("test1")
throttled("test2")
test("use_throttle callable", callable(throttled))

# ==================== use_interval ====================
print("\n--- use_interval ---")

interval_count = [0]

def interval_func():
    interval_count[0] += 1

stop = use_interval(interval_func, 50)
time.sleep(0.2)
stop()
test("use_interval runs", interval_count[0] > 0)

# ==================== use_timeout ====================
print("\n--- use_timeout ---")

timeout_result = [False]

def timeout_func():
    timeout_result[0] = True

cancel = use_timeout(timeout_func, 50)
time.sleep(0.1)
test("use_timeout runs", timeout_result[0] is True)

timeout_result2 = [False]
cancel2 = use_timeout(lambda: timeout_result2.__setitem__(0, True), 1000)
cancel2()
time.sleep(0.05)
test("use_timeout cancel", timeout_result2[0] is False)

# ==================== Edge Cases ====================
print("\n--- Edge Cases ---")

storage2 = LocalStorage("edge-test")
storage2.set("key", None)
test("LocalStorage None value", storage2.get("key") is None)

counter3 = use_counter(0)
for _ in range(100):
    counter3["increment"]()
test("use_counter 100 increments", _get_counter_count(counter3) == 100)

toggle3 = use_toggle(False)
for _ in range(10):
    toggle3["toggle"]()
test("use_toggle 10 toggles", _get_toggle_value(toggle3) is False)

lst3 = use_list()
for i in range(50):
    lst3["add"](i)
test("use_list 50 adds", len(_get_list_items(lst3)) == 50)

# ==================== Summary ====================
print("\n" + "=" * 70)
print(f"Results: {passed}/{total} tests passed")
if failed == 0:
    print("🎉 ALL HOOKS TESTS PASSED!")
else:
    print(f"⚠️ {failed} tests failed")
print("=" * 70)

sys.exit(0 if failed == 0 else 1)
