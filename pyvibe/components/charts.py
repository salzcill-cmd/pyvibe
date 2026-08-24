"""
Charts Components — bar, line, pie, doughnut, radar, area, sparkline charts.
Pure CSS/HTML charts, no JavaScript dependencies needed.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from pyvibe.core.component import Component


# ==================== Bar Chart ====================

def chart_bar(
    data: List[Dict[str, Any]],
    label_key: str = "label",
    value_key: str = "value",
    color: str = "#7C3AED",
    height: str = "300px",
    show_labels: bool = True,
    show_values: bool = True,
    horizontal: bool = False,
    **kwargs,
) -> Component:
    """
    Bar chart component.
    
    Usage:
        chart_bar([
            {"label": "Jan", "value": 45},
            {"label": "Feb", "value": 52},
            {"label": "Mar", "value": 48},
        ])
    """
    comp = Component(tag="div", **kwargs)
    
    if horizontal:
        comp.class_names.extend(["pv-flex", "pv-flex-col", "pv-gap-8"])
        comp.style.height = height
        
        max_val = max((item.get(value_key, 1) for item in data), default=1)
        
        for item in data:
            label = item.get(label_key, "")
            value = item.get(value_key, 0)
            percentage = (value / max_val * 100) if max_val > 0 else 0
            
            row = Component(tag="div")
            row.class_names.extend(["pv-flex", "pv-items-center", "pv-gap-12"])
            
            lbl = Component(tag="div", content=str(label))
            lbl.class_names.extend(["pv-text-sm", "pv-text-gray"])
            lbl.style.width = "80px"
            lbl.style.flex_shrink = "0"
            
            bar_container = Component(tag="div")
            bar_container.style.flex = "1"
            bar_container.style.height = "24px"
            bar_container.style.background = "#F3F4F6"
            bar_container.style.border_radius = "6px"
            bar_container.style.overflow = "hidden"
            
            bar_fill = Component(tag="div")
            bar_fill.style.width = f"{percentage}%"
            bar_fill.style.height = "100%"
            bar_fill.style.background = color
            bar_fill.style.border_radius = "6px"
            bar_fill.style.transition = "width 0.5s ease"
            
            bar_container.children.append(bar_fill)
            
            val = Component(tag="div", content=str(value))
            val.class_names.extend(["pv-text-sm", "pv-text-bold"])
            val.style.width = "50px"
            val.style.text_align = "right"
            
            row.children = [lbl, bar_container, val]
            comp.children.append(row)
    else:
        comp.style.height = height
        comp.class_names.extend(["pv-flex", "pv-items-end", "pv-gap-8", "pv-p-16"])
        comp.style.border_bottom = "1px solid #E5E7EB"
        
        max_val = max((item.get(value_key, 1) for item in data), default=1)
        bar_width = f"{100 / len(data)}%" if data else "100%"
        
        for item in data:
            label = item.get(label_key, "")
            value = item.get(value_key, 0)
            percentage = (value / max_val * 100) if max_val > 0 else 0
            
            bar_container = Component(tag="div")
            bar_container.style.flex = "1"
            bar_container.style.height = "100%"
            bar_container.style.display = "flex"
            bar_container.style.flex_direction = "column"
            bar_container.style.align_items = "center"
            bar_container.style.justify_content = "flex-end"
            bar_container.style.padding_bottom = "4px"
            
            if show_values:
                val = Component(tag="div", content=str(value))
                val.class_names.extend(["pv-text-xs", "pv-text-gray", "pv-mb-4"])
                bar_container.children.append(val)
            
            bar_fill = Component(tag="div")
            bar_fill.style.width = "70%"
            bar_fill.style.height = f"{percentage}%"
            bar_fill.style.background = color
            bar_fill.style.border_radius = "4px 4px 0 0"
            bar_fill.style.transition = "height 0.5s ease"
            
            bar_container.children.append(bar_fill)
            
            if show_labels:
                lbl = Component(tag="div", content=str(label))
                lbl.class_names.extend(["pv-text-xs", "pv-text-gray", "pv-mt-8"])
                bar_container.children.append(lbl)
            
            comp.children.append(bar_container)
    
    return comp


# ==================== Line Chart ====================

def chart_line(
    data: List[Dict[str, Any]],
    label_key: str = "label",
    value_key: str = "value",
    color: str = "#7C3AED",
    height: str = "200px",
    show_dots: bool = True,
    fill: bool = False,
    **kwargs,
) -> Component:
    """
    Line chart using SVG.
    
    Usage:
        chart_line([
            {"label": "Jan", "value": 45},
            {"label": "Feb", "value": 52},
            {"label": "Mar", "value": 48},
        ])
    """
    comp = Component(tag="div", **kwargs)
    comp.style.height = height
    comp.style.position = "relative"
    
    if not data:
        empty = Component(tag="div", content="Tidak ada data")
        empty.class_names.extend(["pv-text-center", "pv-text-gray", "pv-p-32"])
        comp.children.append(empty)
        return comp
    
    # Calculate points
    values = [item.get(value_key, 0) for item in data]
    labels = [item.get(label_key, "") for item in data]
    max_val = max(values) if values else 1
    min_val = min(values) if values else 0
    range_val = max_val - min_val if max_val != min_val else 1
    
    width = 400
    height_px = 150
    padding = 40
    
    points = []
    for i, val in enumerate(values):
        x = padding + (i / (len(values) - 1)) * (width - 2 * padding) if len(values) > 1 else width / 2
        y = height_px - padding - ((val - min_val) / range_val) * (height_px - 2 * padding)
        points.append((x, y))
    
    # Build SVG
    svg_points = " ".join(f"{x},{y}" for x, y in points)
    fill_points = svg_points + f" {points[-1][0]},{height_px - padding} {points[0][0]},{height_px - padding}"
    
    svg = f'''<svg viewBox="0 0 {width} {height_px}" style="width:100%;height:100%;">
        <defs>
            <linearGradient id="grad-{id(comp)}" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:{color};stop-opacity:0.3" />
                <stop offset="100%" style="stop-color:{color};stop-opacity:0.05" />
            </linearGradient>
        </defs>'''
    
    if fill:
        svg += f'<polygon points="{fill_points}" fill="url(#grad-{id(comp)})" />'
    
    svg += f'<polyline points="{svg_points}" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />'
    
    if show_dots:
        for x, y in points:
            svg += f'<circle cx="{x}" cy="{y}" r="4" fill="{color}" stroke="white" stroke-width="2" />'
    
    # X-axis labels
    for i, label in enumerate(labels):
        x = padding + (i / (len(labels) - 1)) * (width - 2 * padding) if len(labels) > 1 else width / 2
        svg += f'<text x="{x}" y="{height_px - 10}" text-anchor="middle" fill="#9CA3AF" font-size="10">{label}</text>'
    
    svg += '</svg>'
    
    comp.attrs["innerHTML"] = svg
    return comp


# ==================== Pie Chart ====================

def chart_pie(
    data: List[Dict[str, Any]],
    label_key: str = "label",
    value_key: str = "value",
    colors: Optional[List[str]] = None,
    size: str = "200px",
    show_legend: bool = True,
    **kwargs,
) -> Component:
    """
    Pie chart using SVG.
    
    Usage:
        chart_pie([
            {"label": "Elektronik", "value": 45},
            {"label": "Fashion", "value": 30},
            {"label": "Makanan", "value": 25},
        ])
    """
    default_colors = ["#7C3AED", "#06B6D4", "#22C55E", "#F97316", "#EC4899", "#EAB308", "#EF4444", "#3B82F6"]
    colors = colors or default_colors
    
    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-flex", "pv-items-center", "pv-gap-24"])
    
    # SVG pie
    svg_size = 160
    cx, cy, r = svg_size // 2, svg_size // 2, svg_size // 2 - 10
    
    total = sum(item.get(value_key, 0) for item in data)
    if total == 0:
        total = 1
    
    svg = f'<svg viewBox="0 0 {svg_size} {svg_size}" style="width:{size};height:{size};flex-shrink:0;">'
    
    start_angle = -90
    for i, item in enumerate(data):
        value = item.get(value_key, 0)
        percentage = value / total
        angle = percentage * 360
        
        # Calculate arc
        end_angle = start_angle + angle
        large_arc = 1 if angle > 180 else 0
        
        import math
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        x1 = cx + r * math.cos(start_rad)
        y1 = cy + r * math.sin(start_rad)
        x2 = cx + r * math.cos(end_rad)
        y2 = cy + r * math.sin(end_rad)
        
        color = colors[i % len(colors)]
        
        if percentage >= 0.99:
            # Full circle
            svg += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" />'
        else:
            svg += f'<path d="M {cx},{cy} L {x1},{y1} A {r},{r} 0 {large_arc},1 {x2},{y2} Z" fill="{color}" />'
        
        start_angle = end_angle
    
    svg += '</svg>'
    
    pie_container = Component(tag="div")
    pie_container.attrs["innerHTML"] = svg
    comp.children.append(pie_container)
    
    # Legend
    if show_legend:
        legend = Component(tag="div")
        legend.class_names.extend(["pv-flex", "pv-flex-col", "pv-gap-8"])
        
        for i, item in enumerate(data):
            label = item.get(label_key, "")
            value = item.get(value_key, 0)
            percentage = (value / total * 100) if total > 0 else 0
            color = colors[i % len(colors)]
            
            legend_item = Component(tag="div")
            legend_item.class_names.extend(["pv-flex", "pv-items-center", "pv-gap-8"])
            
            dot = Component(tag="div")
            dot.style.width = "12px"
            dot.style.height = "12px"
            dot.style.border_radius = "50%"
            dot.style.background = color
            dot.style.flex_shrink = "0"
            
            text = Component(tag="span", content=f"{label} ({percentage:.1f}%)")
            text.class_names.extend(["pv-text-sm", "pv-text-gray"])
            
            legend_item.children = [dot, text]
            legend.children.append(legend_item)
        
        comp.children.append(legend)
    
    return comp


# ==================== Doughnut Chart ====================

def chart_doughnut(
    data: List[Dict[str, Any]],
    label_key: str = "label",
    value_key: str = "value",
    colors: Optional[List[str]] = None,
    size: str = "200px",
    center_text: str = "",
    **kwargs,
) -> Component:
    """
    Doughnut chart using SVG.
    
    Usage:
        chart_doughnut([
            {"label": "Active", "value": 70},
            {"label": "Inactive", "value": 30},
        ], center_text="70%")
    """
    default_colors = ["#7C3AED", "#06B6D4", "#22C55E", "#F97316", "#EC4899", "#EAB308"]
    colors = colors or default_colors
    
    comp = Component(tag="div", **kwargs)
    comp.style.position = "relative"
    comp.style.display = "inline-block"
    
    # SVG
    svg_size = 160
    cx, cy, r = svg_size // 2, svg_size // 2, svg_size // 2 - 10
    inner_r = r * 0.6
    
    total = sum(item.get(value_key, 0) for item in data)
    if total == 0:
        total = 1
    
    svg = f'<svg viewBox="0 0 {svg_size} {svg_size}" style="width:{size};height:{size};">'
    
    # Background circle
    svg += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#F3F4F6" stroke-width="{r - inner_r}" />'
    
    # Data arcs
    circumference = 2 * 3.14159 * ((r + inner_r) / 2)
    stroke_width = r - inner_r
    current_offset = 0
    
    for i, item in enumerate(data):
        value = item.get(value_key, 0)
        percentage = value / total
        arc_length = percentage * circumference
        
        color = colors[i % len(colors)]
        
        svg += f'<circle cx="{cx}" cy="{cy}" r="{(r + inner_r) / 2}" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-dasharray="{arc_length} {circumference - arc_length}" stroke-dashoffset="-{current_offset}" transform="rotate(-90 {cx} {cy})" />'
        
        current_offset += arc_length
    
    svg += '</svg>'
    
    comp.attrs["innerHTML"] = svg
    
    # Center text
    if center_text:
        center = Component(tag="div", content=center_text)
        center.class_names.extend(["pv-absolute", "pv-text-center", "pv-text-bold"])
        center.style.top = "50%"
        center.style.left = "50%"
        center.style.transform = "translate(-50%, -50%)"
        center.style.font_size = "1.5rem"
        comp.children.append(center)
    
    return comp


# ==================== Sparkline ====================

def chart_sparkline(
    values: List[float],
    color: str = "#7C3AED",
    height: str = "40px",
    width: str = "120px",
    show_dots: bool = False,
    fill: bool = False,
    **kwargs,
) -> Component:
    """
    Sparkline chart (small inline chart).
    
    Usage:
        chart_sparkline([10, 15, 13, 18, 22, 20, 25])
    """
    comp = Component(tag="div", **kwargs)
    comp.style.display = "inline-block"
    comp.style.width = width
    comp.style.height = height
    
    if not values:
        return comp
    
    svg_w, svg_h = 100, 30
    max_val = max(values)
    min_val = min(values)
    range_val = max_val - min_val if max_val != min_val else 1
    
    points = []
    for i, val in enumerate(values):
        x = (i / (len(values) - 1)) * svg_w if len(values) > 1 else svg_w / 2
        y = svg_h - ((val - min_val) / range_val) * svg_h
        points.append((x, y))
    
    svg_points = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    fill_points = svg_points + f" {points[-1][0]},{svg_h} {points[0][0]},{svg_h}"
    
    svg = f'<svg viewBox="0 0 {svg_w} {svg_h}" preserveAspectRatio="none" style="width:100%;height:100%;">'
    
    if fill:
        svg += f'<polygon points="{fill_points}" fill="{color}" opacity="0.1" />'
    
    svg += f'<polyline points="{svg_points}" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" />'
    
    if show_dots:
        last_x, last_y = points[-1]
        svg += f'<circle cx="{last_x}" cy="{last_y}" r="3" fill="{color}" />'
    
    svg += '</svg>'
    comp.attrs["innerHTML"] = svg
    
    return comp


# ==================== Progress Ring ====================

def chart_progress_ring(
    value: float = 0,
    max_value: float = 100,
    color: str = "#7C3AED",
    size: str = "80px",
    label: str = "",
    show_percentage: bool = True,
    **kwargs,
) -> Component:
    """
    Circular progress ring.
    
    Usage:
        chart_progress_ring(value=75, label="Score")
    """
    comp = Component(tag="div", **kwargs)
    comp.style.position = "relative"
    comp.style.display = "inline-flex"
    comp.style.align_items = "center"
    comp.style.justify_content = "center"
    
    percentage = min(max(value / max_value * 100, 0), 100) if max_value > 0 else 0
    
    svg_size = 80
    r = 35
    circumference = 2 * 3.14159 * r
    offset = circumference - (percentage / 100) * circumference
    
    svg = f'''<svg viewBox="0 0 {svg_size} {svg_size}" style="width:{size};height:{size};transform:rotate(-90deg);">
        <circle cx="{svg_size//2}" cy="{svg_size//2}" r="{r}" fill="none" stroke="#F3F4F6" stroke-width="6" />
        <circle cx="{svg_size//2}" cy="{svg_size//2}" r="{r}" fill="none" stroke="{color}" stroke-width="6" 
                stroke-dasharray="{circumference}" stroke-dashoffset="{offset}" stroke-linecap="round" />
    </svg>'''
    
    comp.attrs["innerHTML"] = svg
    
    if show_percentage:
        center = Component(tag="div", content=f"{percentage:.0f}%")
        center.class_names.extend(["pv-absolute", "pv-text-bold", "pv-text-sm"])
        comp.children.append(center)
    
    if label:
        label_el = Component(tag="div", content=label)
        label_el.class_names.extend(["pv-text-xs", "pv-text-gray", "pv-mt-4", "pv-text-center"])
        comp.children.append(label_el)
    
    return comp
