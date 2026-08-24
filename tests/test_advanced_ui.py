"""
PyVibe Advanced UI — Unit Tests

Tests for: calendar_component, kanban, video_player, timeline_enhanced,
           infinite_scroll, notification_center, theme_toggle, search_command
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyvibe.components.advanced_ui import (
    calendar_component, kanban, video_player,
    timeline_enhanced, infinite_scroll, notification_center,
    theme_toggle, search_command,
)
from pyvibe.core.component import Component

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
print("🎨 PyVibe Advanced UI — Unit Tests")
print("=" * 70)

# ==================== Calendar Component ====================
print("\n--- calendar_component ---")

result = calendar_component()
html = result.render()
test("calendar_component returns Component", isinstance(result, Component))
test("calendar_component renders HTML", "<div" in html)
test("calendar_component has card class", "pv-card" in html)
test("calendar_component shows month name", "Agustus" in html or "2026" in html)

result_with_events = calendar_component(
    year=2026, month=8,
    events=[{"day": 15, "title": "Meeting", "color": "#7C3AED"}]
)
html_e = result_with_events.render()
test("calendar_component with events", "<div" in html_e)
test("calendar_component event color", "#7C3AED" in html_e)

result_no_header = calendar_component(show_header=False)
html_nh = result_no_header.render()
test("calendar_component no header", "<div" in html_nh)

result_specific = calendar_component(year=2024, month=2)
html_s = result_specific.render()
test("calendar_component specific month", "Februari" in html_s or "2024" in html_s)

# ==================== Kanban ====================
print("\n--- kanban ---")

kanban_data = [
    {
        "title": "To Do",
        "color": "#EF4444",
        "items": [
            {"title": "Task 1", "description": "Description 1", "assignee": "Andi"},
            {"title": "Task 2", "tags": ["urgent"]},
        ]
    },
    {
        "title": "In Progress",
        "color": "#EAB308",
        "items": [
            {"title": "Task 3", "description": "Description 3", "priority": "high"},
        ]
    },
    {
        "title": "Done",
        "color": "#22C55E",
        "items": []
    }
]

result = kanban(kanban_data)
html = result.render()
test("kanban returns Component", isinstance(result, Component))
test("kanban renders HTML", "<div" in html)
test("kanban has flex layout", "pv-flex" in html)
test("kanban shows column titles", "To Do" in html)
test("kanban shows task titles", "Task 1" in html)
test("kanban shows assignee", "Andi" in html)
test("kanban shows item count", "2" in html)
test("kanban shows add button", "Add Task" in html)

result_empty = kanban([{"title": "Empty", "items": []}])
html_em = result_empty.render()
test("kanban empty column", "0" in html_em)

result_with_tags = kanban([{"title": "Col", "items": [{"title": "T", "tags": ["bug", "urgent"]}]}])
html_t = result_with_tags.render()
test("kanban with tags", "bug" in html_t)

# ==================== Video Player ====================
print("\n--- video_player ---")

result = video_player("test.mp4")
html = result.render()
test("video_player returns Component", isinstance(result, Component))
test("video_player renders HTML", "<div" in html)
test("video_player has video tag", "<video" in html)
test("video_player has src", "test.mp4" in html)

result_poster = video_player("test.mp4", poster="thumb.jpg")
html_p = result_poster.render()
test("video_player with poster", "thumb.jpg" in html_p)

result_controls = video_player("test.mp4", controls=False)
html_c = result_controls.render()
test("video_player no controls", "<video" in html_c)

result_youtube = video_player("https://youtube.com/watch?v=abc123")
html_y = result_youtube.render()
test("video_player youtube", "youtube.com" in html_y or "iframe" in html_y)

result_loop = video_player("test.mp4", loop=True, muted=True)
html_l = result_loop.render()
test("video_player loop", "loop" in html_l)
test("video_player muted", "muted" in html_l)

# ==================== Timeline Enhanced ====================
print("\n--- timeline_enhanced ---")

timeline_data = [
    {"date": "24 Agustus", "title": "Project Started", "description": "Memulai development", "icon": "🚀", "color": "#7C3AED"},
    {"date": "25 Agustus", "title": "Alpha Release", "description": "Release versi alpha", "icon": "📦", "color": "#22C55E"},
    {"date": "26 Agustus", "title": "Beta Release", "icon": "🎉", "color": "#F97316"},
]

result = timeline_enhanced(timeline_data)
html = result.render()
test("timeline_enhanced returns Component", isinstance(result, Component))
test("timeline_enhanced renders HTML", "<div" in html)
test("timeline_enhanced has vertical layout", "pv-relative" in html or "pv-pl" in html)
test("timeline_enhanced shows dates", "24 Agustus" in html)
test("timeline_enhanced shows titles", "Project Started" in html)
test("timeline_enhanced shows descriptions", "Memulai development" in html)
test("timeline_enhanced shows icons", "🚀" in html)

result_horizontal = timeline_enhanced(timeline_data, orientation="horizontal")
html_h = result_horizontal.render()
test("timeline_enhanced horizontal", "pv-flex" in html_h)

result_empty = timeline_enhanced([])
html_e = result_empty.render()
test("timeline_enhanced empty", "<div" in html_e)

result_single = timeline_enhanced([{"title": "Only Item", "icon": "📌"}])
html_s = result_single.render()
test("timeline_enhanced single item", "Only Item" in html_s)

# ==================== Infinite Scroll ====================
print("\n--- infinite_scroll ---")

result = infinite_scroll()
html = result.render()
test("infinite_scroll returns Component", isinstance(result, Component))
test("infinite_scroll renders HTML", "<div" in html)
test("infinite_scroll has spinner", "pv-spinner" in html)
test("infinite_scroll has data attribute", "data-infinite-scroll" in html)

result_custom = infinite_scroll(loader_text="Loading more...", end_text="No more")
html_c = result_custom.render()
test("infinite_scroll custom text", "Loading more..." in html_c)
test("infinite_scroll end text", "No more" in html_c)

# ==================== Notification Center ====================
print("\n--- notification_center ---")

notifications = [
    {"title": "New message", "description": "You have a new message", "time": "2 min ago", "read": False, "icon": "📩"},
    {"title": "Order shipped", "description": "Your order is on the way", "time": "1 hour ago", "read": True, "icon": "📦"},
    {"title": "System update", "description": "New version available", "time": "3 hours ago", "read": False, "icon": "🔄"},
]

result = notification_center(notifications)
html = result.render()
test("notification_center returns Component", isinstance(result, Component))
test("notification_center renders HTML", "<div" in html)
test("notification_center has bell icon", "🔔" in html)
test("notification_center shows unread count", "2" in html)
test("notification_center shows titles", "New message" in html)
test("notification_center shows descriptions", "You have a new message" in html)
test("notification_center shows time", "2 min ago" in html)
test("notification_center has mark all button", "Tandai semua dibaca" in html)
test("notification_center has view all link", "Lihat semua notifikasi" in html)

result_empty = notification_center([])
html_e = result_empty.render()
test("notification_center empty", "0" in html_e)

result_one = notification_center([{"title": "Solo", "read": True}])
html_o = result_one.render()
test("notification_center single notification", "Solo" in html_o)

# ==================== Theme Toggle ====================
print("\n--- theme_toggle ---")

result = theme_toggle()
html = result.render()
test("theme_toggle returns Component", isinstance(result, Component))
test("theme_toggle renders HTML", "<button" in html)
test("theme_toggle has onclick", "onclick" in html)
test("theme_toggle has dark mode class", "pv-dark-mode" in html)

result_custom = theme_toggle(light_icon="🌞", dark_icon="🌑")
html_c = result_custom.render()
test("theme_toggle custom icons", "🌞" in html_c)

# ==================== Search Command ====================
print("\n--- search_command ---")

result = search_command()
html = result.render()
test("search_command returns Component", isinstance(result, Component))
test("search_command renders HTML", "<div" in html)
test("search_command has search icon", "🔍" in html)
test("search_command has shortcut", "⌘K" in html)
test("search_command has onclick", "onclick" in html)

result_custom = search_command(placeholder="Find anything...", shortcut="Ctrl+K")
html_c = result_custom.render()
test("search_command custom placeholder", "Find anything..." in html_c)
test("search_command custom shortcut", "Ctrl+K" in html_c)

# ==================== Component Builder Methods ====================
print("\n--- Component Builder Methods ---")

result = calendar_component()
result.bulat("16px")
test("calendar bulat", "16px" in result.render())

result = kanban([{"title": "T", "items": []}])
result.padding("24px")
test("kanban padding", "24px" in result.render())

result = video_player("test.mp4")
result.bulat("8px")
test("video_player bulat", "8px" in result.render())

result = timeline_enhanced([{"title": "T"}])
result.gap("16px")
test("timeline_enhanced gap", "16px" in result.render())

# ==================== Summary ====================
print("\n" + "=" * 70)
print(f"Results: {passed}/{total} tests passed")
if failed == 0:
    print("🎉 ALL ADVANCED UI TESTS PASSED!")
else:
    print(f"⚠️ {failed} tests failed")
print("=" * 70)

sys.exit(0 if failed == 0 else 1)
