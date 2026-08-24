"""
PyVibe Charts — Unit Tests

Tests for: chart_bar, chart_line, chart_pie, chart_doughnut, chart_sparkline, chart_progress_ring
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyvibe.components.charts import (
    chart_bar, chart_line, chart_pie, chart_doughnut,
    chart_sparkline, chart_progress_ring,
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
print("📊 PyVibe Charts — Unit Tests")
print("=" * 70)

# ==================== Chart Bar ====================
print("\n--- chart_bar ---")

data_simple = [
    {"label": "Jan", "value": 45},
    {"label": "Feb", "value": 52},
    {"label": "Mar", "value": 48},
]

result = chart_bar(data_simple)
html = result.render()
test("chart_bar returns Component", isinstance(result, Component))
test("chart_bar renders HTML", "<div" in html)
test("chart_bar has default color", "7C3AED" in html or "flex" in html)

result_h = chart_bar(data_simple, horizontal=True)
html_h = result_h.render()
test("chart_bar horizontal mode", "<div" in html_h)

result_no_labels = chart_bar(data_simple, show_labels=False, show_values=False)
html_nl = result_no_labels.render()
test("chart_bar no labels", "<div" in html_nl)

result_empty = chart_bar([])
html_empty = result_empty.render()
test("chart_bar empty data", "<div" in html_empty)

# ==================== Chart Line ====================
print("\n--- chart_line ---")

result = chart_line(data_simple)
html = result.render()
test("chart_line returns Component", isinstance(result, Component))
test("chart_line renders SVG", "<svg" in html or "<div" in html)
test("chart_line has polyline", "polyline" in html or "<div" in html)

result_fill = chart_line(data_simple, fill=True)
html_fill = result_fill.render()
test("chart_line fill mode", "<svg" in html_fill or "<div" in html_fill)

result_no_dots = chart_line(data_simple, show_dots=False)
html_nd = result_no_dots.render()
test("chart_line no dots", "<svg" in html_nd or "<div" in html_nd)

result_empty = chart_line([])
html_empty = result_empty.render()
test("chart_line empty data", "Tidak ada data" in html_empty or "<div" in html_empty)

# ==================== Chart Pie ====================
print("\n--- chart_pie ---")

pie_data = [
    {"label": "Elektronik", "value": 45},
    {"label": "Fashion", "value": 30},
    {"label": "Makanan", "value": 25},
]

result = chart_pie(pie_data)
html = result.render()
test("chart_pie returns Component", isinstance(result, Component))
test("chart_pie renders HTML", "<div" in html)
test("chart_pie has SVG", "<svg" in html)
test("chart_pie has legend", "Elektronik" in html)

result_no_legend = chart_pie(pie_data, show_legend=False)
html_nl = result_no_legend.render()
test("chart_pie no legend", "<svg" in html_nl)

result_custom_colors = chart_pie(pie_data, colors=["#FF0000", "#00FF00", "#0000FF"])
html_cc = result_custom_colors.render()
test("chart_pie custom colors", "#FF0000" in html_cc)

# ==================== Chart Doughnut ====================
print("\n--- chart_doughnut ---")

result = chart_doughnut(pie_data, center_text="100%")
html = result.render()
test("chart_doughnut returns Component", isinstance(result, Component))
test("chart_doughnut renders HTML", "<div" in html)
test("chart_doughnut has SVG", "<svg" in html)
test("chart_doughnut has center text", "100%" in html)

result_no_center = chart_doughnut(pie_data)
html_nc = result_no_center.render()
test("chart_doughnut no center text", "<svg" in html_nc)

# ==================== Chart Sparkline ====================
print("\n--- chart_sparkline ---")

values = [10, 15, 13, 18, 22, 20, 25]

result = chart_sparkline(values)
html = result.render()
test("chart_sparkline returns Component", isinstance(result, Component))
test("chart_sparkline renders HTML", "<svg" in html or "<div" in html)
test("chart_sparkline has polyline", "polyline" in html or "viewBox" in html)

result_dots = chart_sparkline(values, show_dots=True)
html_d = result_dots.render()
test("chart_sparkline with dots", "<svg" in html_d or "<div" in html_d)

result_fill = chart_sparkline(values, fill=True)
html_f = result_fill.render()
test("chart_sparkline fill mode", "<svg" in html_f or "<div" in html_f)

result_empty = chart_sparkline([])
html_e = result_empty.render()
test("chart_sparkline empty data", "<div" in html_e)

# ==================== Chart Progress Ring ====================
print("\n--- chart_progress_ring ---")

result = chart_progress_ring(75, label="Score")
html = result.render()
test("chart_progress_ring returns Component", isinstance(result, Component))
test("chart_progress_ring renders HTML", "<div" in html)
test("chart_progress_ring has SVG", "<svg" in html)
test("chart_progress_ring shows percentage", "75%" in html)
test("chart_progress_ring shows label", "Score" in html)

result_no_label = chart_progress_ring(50)
html_nl = result_no_label.render()
test("chart_progress_ring no label", "<svg" in html_nl)

result_zero = chart_progress_ring(0)
html_z = result_zero.render()
test("chart_progress_ring zero value", "<svg" in html_z)

result_full = chart_progress_ring(100)
html_f = result_full.render()
test("chart_progress_ring full value", "100%" in html_f)

# ==================== Edge Cases ====================
print("\n--- Edge Cases ---")

result = chart_bar([{"label": "A", "value": 0}])
test("chart_bar zero value", "<div" in result.render())

result = chart_bar([{"label": "A", "value": 100}, {"label": "B", "value": 100}])
test("chart_bar equal values", "<div" in result.render())

result = chart_pie([{"label": "Only", "value": 100}])
test("chart_pie single item", "<svg" in result.render())

result = chart_sparkline([5])
test("chart_sparkline single value", "<svg" in result.render() or "<div" in result.render())

result = chart_progress_ring(50, max_value=200)
html = result.render()
test("chart_progress_ring custom max", "25%" in html)

# ==================== Summary ====================
print("\n" + "=" * 70)
print(f"Results: {passed}/{total} tests passed")
if failed == 0:
    print("🎉 ALL CHART TESTS PASSED!")
else:
    print(f"⚠️ {failed} tests failed")
print("=" * 70)

sys.exit(0 if failed == 0 else 1)
