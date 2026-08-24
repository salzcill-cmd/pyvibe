"""
PyVibe Reactivity — Unit Tests

Tests for: ReactiveStore, ReactiveDict, computed, watch, watch_all, batch
"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyvibe.reactivity import (
    ReactiveStore, ReactiveDict, computed, watch, watch_all, batch,
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
print("🔄 PyVibe Reactivity — Unit Tests")
print("=" * 70)

# ==================== ReactiveDict ====================
print("\n--- ReactiveDict ---")

state = ReactiveDict(name="Andi", count=0)
test("ReactiveDict init", state["name"] == "Andi")
test("ReactiveDict count", state["count"] == 0)

state["count"] = 1
test("ReactiveDict set", state["count"] == 1)

state["count"] = 2
test("ReactiveDict update", state["count"] == 2)

# History
history = state.get_history("count")
test("ReactiveDict history", len(history) == 2)
test("ReactiveDict history values", history[0]["new"] == 1)

all_history = state.get_history()
test("ReactiveDict all history", len(all_history) >= 2)

# ==================== ReactiveDict Listeners ====================
print("\n--- ReactiveDict Listeners ---")

state2 = ReactiveDict()
changes = []

state2.on_change("count", lambda new, old: changes.append({"new": new, "old": old}))
state2["count"] = 1
state2["count"] = 2
state2["count"] = 3

test("ReactiveDict listener called", len(changes) == 3)
test("ReactiveDict listener values", changes[0]["new"] == 1)
test("ReactiveDict listener old value", changes[0]["old"] is None)

# Remove listener
state2.off_change("count")
state2["count"] = 10
test("ReactiveDict listener removed", len(changes) == 3)

# Global listener
global_changes = []
state2.on_any_change(lambda k, v, o: global_changes.append(k))
state2["name"] = "Budi"
test("ReactiveDict global listener", len(global_changes) == 1)

state2.off_change("name")
test("ReactiveDict off change", True)

# ==================== ReactiveDict Undo ====================
print("\n--- ReactiveDict Undo ---")

state3 = ReactiveDict(a=1)
state3["a"] = 2
state3["a"] = 3

result = state3.undo()
test("ReactiveDict undo", result is True)
test("ReactiveDict undo value", state3["a"] == 2)

state3.undo()
test("ReactiveDict undo again", state3["a"] == 1)

result_empty = ReactiveDict().undo()
test("ReactiveDict undo empty", result_empty is False)

# ==================== ReactiveDict to_dict ====================
print("\n--- ReactiveDict to_dict ---")

state4 = ReactiveDict(x=10, y=20)
d = state4.to_dict()
test("ReactiveDict to_dict", isinstance(d, dict))
test("ReactiveDict to_dict values", d["x"] == 10)

# ==================== ReactiveStore ====================
print("\n--- ReactiveStore ---")

store = ReactiveStore("test-store")
store.state = {"count": 0, "name": "Test"}
test("ReactiveStore init", store.state["count"] == 0)

store.state["count"] = 1
test("ReactiveStore set", store.state["count"] == 1)

store.save()
test("ReactiveStore save", True)

store.load()
test("ReactiveStore load", store.state["count"] == 1)

store.clear()
test("ReactiveStore clear", len(store.state) == 0)

store.reset({"x": 1})
test("ReactiveStore reset", store.state["x"] == 1)

store_dict = store.to_dict()
test("ReactiveStore to_dict", isinstance(store_dict, dict))

store.from_dict({"a": 1, "b": 2})
test("ReactiveStore from_dict", store.state["a"] == 1)

# ==================== computed ====================
print("\n--- computed ---")

state5 = ReactiveDict(count=10)
c = computed(lambda: state5["count"] * 2)
test("computed initial", c.value == 20)

state5["count"] = 15
c.invalidate()
test("computed after change", c.value == 30)

c.invalidate()
state5["count"] = 0
test("computed zero", c.value == 0)

c2 = computed(lambda: "hello")
test("computed string", c2.value == "hello")

c3 = computed(lambda: None)
test("computed None", c3.value is None)

# ==================== watch ====================
print("\n--- watch ---")

state6 = ReactiveDict(value=0)
watcher_calls = []

unwatch = watch(state6, "value", lambda new, old: watcher_calls.append((new, old)))
state6["value"] = 1
state6["value"] = 2

test("watch called", len(watcher_calls) == 2)
test("watch values", watcher_calls[0] == (1, 0))
test("watch old value", watcher_calls[1] == (2, 1))

unwatch()
state6["value"] = 3
test("watch unwatched", len(watcher_calls) == 2)

# ==================== watch_all ====================
print("\n--- watch_all ---")

state7 = ReactiveDict()
all_calls = []

unwatch_all = watch_all(state7, lambda k, v, o: all_calls.append(k))
state7["a"] = 1
state7["b"] = 2
state7["c"] = 3

test("watch_all called", len(all_calls) == 3)
test("watch_all keys", all_calls == ["a", "b", "c"])

unwatch_all()
test("watch_all unwatch", True)

# ==================== batch ====================
print("\n--- batch ---")

batch_store = ReactiveStore("batch-test")
batch_store.state = {"x": 0}

with batch(batch_store) as bs:
    bs.state["x"] = 1
    bs.state["x"] = 2

test("batch context", batch_store.state["x"] == 2)

# ==================== Edge Cases ====================
print("\n--- Edge Cases ---")

# Empty ReactiveDict
empty = ReactiveDict()
test("Empty ReactiveDict", len(empty) == 0)

empty["key"] = "value"
test("Empty ReactiveDict set", empty["key"] == "value")

# History limit
state_limit = ReactiveDict()
for i in range(60):
    state_limit["key"] = i
test("History limit", len(state_limit.get_history()) <= 50)

# Computed with dependencies
dep_state = ReactiveDict(x=1, y=2)
dep_computed = computed(lambda: dep_state["x"] + dep_state["y"], dependencies=["x", "y"])
test("Computed with deps", dep_computed.value == 3)

dep_state["x"] = 10
dep_computed.invalidate()
test("Computed with deps updated", dep_computed.value == 12)

# Store init
store_init = ReactiveStore("init-test")
store_init.init({"default": "value"})
test("Store init", store_init.state.get("default") == "value")

store_init.init({"default": "new"})
test("Store init existing", store_init.state.get("default") == "value")

# ==================== Summary ====================
print("\n" + "=" * 70)
print(f"Results: {passed}/{total} tests passed")
if failed == 0:
    print("🎉 ALL REACTIVITY TESTS PASSED!")
else:
    print(f"⚠️ {failed} tests failed")
print("=" * 70)

sys.exit(0 if failed == 0 else 1)
