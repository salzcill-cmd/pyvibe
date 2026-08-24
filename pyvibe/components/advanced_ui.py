"""
Advanced UI Components — calendar, kanban, video player, timeline, and more.
"""

from __future__ import annotations
import calendar as cal_module
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Union
from pyvibe.core.component import Component


# ==================== Calendar ====================

def calendar_component(
    year: Optional[int] = None,
    month: Optional[int] = None,
    events: Optional[List[Dict[str, Any]]] = None,
    highlighted_days: Optional[List[int]] = None,
    show_header: bool = True,
    **kwargs,
) -> Component:
    """
    Calendar component.
    
    Usage:
        calendar_component(year=2026, month=8, events=[
            {"day": 15, "title": "Meeting", "color": "#7C3AED"},
        ])
    """
    now = datetime.now()
    year = year or now.year
    month = month or now.month
    events = events or []
    highlighted_days = highlighted_days or []
    
    month_names = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
                   "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    day_names = ["Min", "Sen", "Sel", "Rab", "Kam", "Jum", "Sab"]
    
    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-card", "pv-card-hover"])
    comp.style.max_width = "350px"
    
    # Header
    if show_header:
        header = Component(tag="div")
        header.class_names.extend(["pv-flex", "pv-items-center", "pv-justify-between", "pv-mb-16", "pv-pb-12"])
        header.style.border_bottom = "1px solid #E5E7EB"
        
        prev_btn = Component(tag="button", content="‹")
        prev_btn.class_names.extend(["pv-btn", "pv-btn-ghost", "pv-btn-sm"])
        
        title = Component(tag="div", content=f"{month_names[month - 1]} {year}")
        title.class_names.extend(["pv-text-bold", "pv-text-lg"])
        
        next_btn = Component(tag="button", content="›")
        next_btn.class_names.extend(["pv-btn", "pv-btn-ghost", "pv-btn-sm"])
        
        header.children = [prev_btn, title, next_btn]
        comp.children.append(header)
    
    # Day names
    day_row = Component(tag="div")
    day_row.class_names.extend(["pv-grid", "pv-gap-4", "pv-mb-8"])
    day_row.style.grid_template_columns = "repeat(7, 1fr)"
    
    for day in day_names:
        day_cell = Component(tag="div", content=day)
        day_cell.class_names.extend(["pv-text-center", "pv-text-xs", "pv-text-gray", "pv-text-bold", "pv-py-8"])
        day_row.children.append(day_cell)
    
    comp.children.append(day_row)
    
    # Days grid
    days_grid = Component(tag="div")
    days_grid.class_names.extend(["pv-grid", "pv-gap-4"])
    days_grid.style.grid_template_columns = "repeat(7, 1fr)"
    
    # Get calendar data
    cal = cal_module.monthcalendar(year, month)
    
    for week in cal:
        for day in week:
            day_cell = Component(tag="div")
            
            if day == 0:
                day_cell.content = ""
            else:
                day_cell.content = str(day)
                day_cell.class_names.extend(["pv-text-center", "pv-py-8", "pv-rounded", "pv-cursor-pointer", "pv-text-sm"])
                day_cell.style.transition = "background 0.2s"
                day_cell.attrs["onmouseenter"] = "this.style.background='#F3F4F6'"
                day_cell.attrs["onmouseleave"] = "this.style.background='transparent'"
                
                # Today
                if day == now.day and month == now.month and year == now.year:
                    day_cell.class_names.extend(["pv-bg-primary", "pv-text-white", "pv-text-bold"])
                
                # Highlighted
                elif day in highlighted_days:
                    day_cell.class_names.append("pv-bg-gray")
                
                # Events
                event_for_day = [e for e in events if e.get("day") == day]
                if event_for_day:
                    day_cell.style.border_bottom = f"3px solid {event_for_day[0].get('color', '#7C3AED')}"
            
            days_grid.children.append(day_cell)
    
    comp.children.append(days_grid)
    
    return comp


# ==================== Kanban Board ====================

def kanban(
    columns: List[Dict[str, Any]],
    **kwargs,
) -> Component:
    """
    Kanban board component.
    
    Usage:
        kanban([
            {"title": "To Do", "color": "#EF4444", "items": [
                {"title": "Task 1", "description": "Description", "assignee": "Andi"},
                {"title": "Task 2", "description": "Description"},
            ]},
            {"title": "In Progress", "color": "#EAB308", "items": [...]},
            {"title": "Done", "color": "#22C55E", "items": [...]},
        ])
    """
    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-flex", "pv-gap-16", "pv-overflow-auto"])
    comp.style.min_height = "400px"
    
    for col in columns:
        column = Component(tag="div")
        column.class_names.extend(["pv-bg-gray", "pv-rounded-lg", "pv-p-16", "pv-min-w-250"])
        column.style.min_width = "250px"
        column.style.flex = "1"
        
        # Column header
        header = Component(tag="div")
        header.class_names.extend(["pv-flex", "pv-items-center", "pv-justify-between", "pv-mb-16"])
        
        title_row = Component(tag="div")
        title_row.class_names.extend(["pv-flex", "pv-items-center", "pv-gap-8"])
        
        dot = Component(tag="div")
        dot.style.width = "10px"
        dot.style.height = "10px"
        dot.style.border_radius = "50%"
        dot.style.background = col.get("color", "#7C3AED")
        
        title = Component(tag="div", content=col.get("title", ""))
        title.class_names.extend(["pv-text-bold", "pv-text-sm"])
        
        title_row.children = [dot, title]
        
        count = Component(tag="div", content=str(len(col.get("items", []))))
        count.class_names.extend(["pv-badge", "pv-badge-gray"])
        
        header.children = [title_row, count]
        column.children.append(header)
        
        # Items
        items_container = Component(tag="div")
        items_container.class_names.extend(["pv-flex", "pv-flex-col", "pv-gap-8"])
        
        for item in col.get("items", []):
            card = Component(tag="div")
            card.class_names.extend(["pv-bg-white", "pv-rounded-lg", "pv-p-12", "pv-shadow-sm", "pv-cursor-pointer"])
            card.style.transition = "box-shadow 0.2s, transform 0.2s"
            card.attrs["onmouseenter"] = "this.style.boxShadow='0 4px 6px rgba(0,0,0,0.1)';this.style.transform='translateY(-2px)'"
            card.attrs["onmouseleave"] = "this.style.boxShadow='0 1px 3px rgba(0,0,0,0.1)';this.style.transform='translateY(0)'"
            
            title = Component(tag="div", content=item.get("title", ""))
            title.class_names.extend(["pv-text-sm", "pv-text-bold", "pv-mb-4"])
            card.children.append(title)
            
            if item.get("description"):
                desc = Component(tag="div", content=item["description"])
                desc.class_names.extend(["pv-text-xs", "pv-text-gray", "pv-mb-8"])
                card.children.append(desc)
            
            if item.get("tags"):
                tags_row = Component(tag="div")
                tags_row.class_names.extend(["pv-flex", "pv-gap-4", "pv-mb-8"])
                for tag in item["tags"]:
                    tag_el = Component(tag="span", content=tag)
                    tag_el.class_names.extend(["pv-badge", "pv-badge-primary", "pv-text-xs"])
                    tags_row.children.append(tag_el)
                card.children.append(tags_row)
            
            if item.get("assignee"):
                footer = Component(tag="div")
                footer.class_names.extend(["pv-flex", "pv-items-center", "pv-justify-between"])
                
                assignee = Component(tag="span", content=item["assignee"])
                assignee.class_names.extend(["pv-text-xs", "pv-text-gray"])
                
                if item.get("priority"):
                    priority_colors = {"high": "#EF4444", "medium": "#EAB308", "low": "#22C55E"}
                    priority = Component(tag="span", content=item["priority"])
                    priority.style.color = priority_colors.get(item["priority"], "#6B7280")
                    priority.class_names.extend(["pv-text-xs", "pv-text-bold"])
                    footer.children.append(priority)
                
                footer.children.insert(0, assignee)
                card.children.append(footer)
            
            items_container.children.append(card)
        
        # Add button
        add_btn = Component(tag="button", content="+ Add Task")
        add_btn.class_names.extend(["pv-btn", "pv-btn-ghost", "pv-btn-sm", "pv-text-gray", "pv-mt-8"])
        add_btn.style.justify_content = "flex-start"
        add_btn.style.width = "100%"
        items_container.children.append(add_btn)
        
        column.children.append(items_container)
        comp.children.append(column)
    
    return comp


# ==================== Video Player ====================

def video_player(
    src: str,
    poster: str = "",
    autoplay: bool = False,
    controls: bool = True,
    loop: bool = False,
    muted: bool = False,
    width: str = "100%",
    height: str = "auto",
    **kwargs,
) -> Component:
    """
    Enhanced video player.
    
    Usage:
        video_player("video.mp4", poster="thumb.jpg")
        video_player("https://youtube.com/watch?v=xxx", autoplay=True)
    """
    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-video-player", "pv-rounded-lg", "pv-overflow-hidden", "pv-shadow-md"])
    comp.style.position = "relative"
    comp.style.width = width
    
    # Check if YouTube
    is_youtube = "youtube.com" in src or "youtu.be" in src
    
    if is_youtube:
        # Extract video ID
        import re
        match = re.search(r'(?:v=|youtu\.be/)([^&]+)', src)
        video_id = match.group(1) if match else ""
        
        iframe = Component(tag="iframe")
        iframe.attrs["src"] = f"https://www.youtube.com/embed/{video_id}"
        iframe.attrs["frameborder"] = "0"
        iframe.attrs["allowfullscreen"] = "true"
        iframe.attrs["allow"] = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        iframe.style.width = "100%"
        iframe.style.aspect_ratio = "16/9"
        comp.children.append(iframe)
    else:
        video = Component(tag="video")
        video.attrs["src"] = src
        if poster:
            video.attrs["poster"] = poster
        if autoplay:
            video.attrs["autoplay"] = "autoplay"
        if controls:
            video.attrs["controls"] = "controls"
        if loop:
            video.attrs["loop"] = "loop"
        if muted:
            video.attrs["muted"] = "muted"
        video.style.width = "100%"
        video.style.display = "block"
        comp.children.append(video)
    
    return comp


# ==================== Timeline Enhanced ====================

def timeline_enhanced(
    items: List[Dict[str, Any]],
    orientation: str = "vertical",
    **kwargs,
) -> Component:
    """
    Enhanced timeline with rich content.
    
    Usage:
        timeline_enhanced([
            {
                "date": "24 Agustus 2026",
                "title": "Project Started",
                "description": "Memulai development PyVibe v0.2.0",
                "icon": "🚀",
                "color": "#7C3AED",
            },
            {
                "date": "25 Agustus 2026",
                "title": "Alpha Release",
                "description": "Release versi alpha pertama",
                "icon": "📦",
                "color": "#22C55E",
            },
        ])
    """
    comp = Component(tag="div", **kwargs)
    
    if orientation == "horizontal":
        comp.class_names.extend(["pv-flex", "pv-overflow-auto", "pv-gap-0", "pv-py-16"])
        
        for i, item in enumerate(items):
            entry = Component(tag="div")
            entry.style.min_width = "200px"
            entry.style.padding = "0 16px"
            entry.style.position = "relative"
            
            # Connector line
            if i < len(items) - 1:
                line = Component(tag="div")
                line.style.position = "absolute"
                line.style.top = "20px"
                line.style.right = "-50%"
                line.style.width = "100%"
                line.style.height = "2px"
                line.style.background = "#E5E7EB"
                line.style.z_index = "0"
                entry.children.append(line)
            
            # Icon
            icon = Component(tag="div", content=item.get("icon", "•"))
            icon.style.width = "40px"
            icon.style.height = "40px"
            icon.style.border_radius = "50%"
            icon.style.background = item.get("color", "#7C3AED")
            icon.style.display = "flex"
            icon.style.align_items = "center"
            icon.style.justify_content = "center"
            icon.style.margin = "0 auto 12px"
            icon.style.position = "relative"
            icon.style.z_index = "1"
            entry.children.append(icon)
            
            # Content
            if item.get("date"):
                date = Component(tag="div", content=item["date"])
                date.class_names.extend(["pv-text-xs", "pv-text-gray", "pv-text-center", "pv-mb-4"])
                entry.children.append(date)
            
            if item.get("title"):
                title = Component(tag="div", content=item["title"])
                title.class_names.extend(["pv-text-sm", "pv-text-bold", "pv-text-center", "pv-mb-4"])
                entry.children.append(title)
            
            if item.get("description"):
                desc = Component(tag="div", content=item["description"])
                desc.class_names.extend(["pv-text-xs", "pv-text-gray", "pv-text-center"])
                entry.children.append(desc)
            
            comp.children.append(entry)
    else:
        # Vertical
        comp.class_names.extend(["pv-relative", "pv-pl-32"])
        
        for i, item in enumerate(items):
            entry = Component(tag="div")
            entry.class_names.extend(["pv-relative", "pv-mb-32"])
            
            # Connector line
            if i < len(items) - 1:
                line = Component(tag="div")
                line.class_names.extend(["pv-absolute"])
                line.style.width = "2px"
                line.style.height = "calc(100% + 8px)"
                line.style.background = "#E5E7EB"
                line.style.left = "-20px"
                line.style.top = "32px"
                entry.children.append(line)
            
            # Icon
            icon = Component(tag="div", content=item.get("icon", "•"))
            icon.class_names.extend(["pv-absolute", "pv-rounded-full"])
            icon.style.width = "40px"
            icon.style.height = "40px"
            icon.style.background = item.get("color", "#7C3AED")
            icon.style.display = "flex"
            icon.style.align_items = "center"
            icon.style.justify_content = "center"
            icon.style.left = "-38px"
            icon.style.top = "0"
            icon.style.z_index = "1"
            icon.style.font_size = "1.2rem"
            entry.children.append(icon)
            
            # Content
            if item.get("date"):
                date = Component(tag="div", content=item["date"])
                date.class_names.extend(["pv-text-xs", "pv-text-gray", "pv-mb-4"])
                entry.children.append(date)
            
            if item.get("title"):
                title = Component(tag="h4", content=item["title"])
                title.class_names.extend(["pv-mb-4", "pv-text-bold"])
                entry.children.append(title)
            
            if item.get("description"):
                desc = Component(tag="p", content=item["description"])
                desc.class_names.extend(["pv-text-sm", "pv-text-gray"])
                entry.children.append(desc)
            
            comp.children.append(entry)
    
    return comp


# ==================== Infinite Scroll ====================

def infinite_scroll(
    loader_text: str = "Memuat lebih banyak...",
    end_text: str = "Semua data sudah dimuat",
    **kwargs,
) -> Component:
    """
    Infinite scroll placeholder component.
    
    Usage:
        infinite_scroll(loader_text="Loading more...")
    """
    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-text-center", "pv-p-24"])
    
    spinner = Component(tag="div")
    spinner.class_names.extend(["pv-spinner", "pv-mx-auto", "pv-mb-8"])
    
    text = Component(tag="div", content=loader_text)
    text.class_names.extend(["pv-text-sm", "pv-text-gray"])
    
    comp.children = [spinner, text]
    
    # Add data attribute for JS integration
    comp.attrs["data-infinite-scroll"] = "true"
    comp.attrs["data-end-text"] = end_text
    
    return comp


# ==================== Notification Center ====================

def notification_center(
    notifications: Optional[List[Dict[str, Any]]] = None,
    **kwargs,
) -> Component:
    """
    Notification center with badge and dropdown.
    
    Usage:
        notification_center(notifications=[
            {"title": "New message", "description": "You have a new message", "time": "2 min ago", "read": False},
            {"title": "Order shipped", "description": "Your order is on the way", "time": "1 hour ago", "read": True},
        ])
    """
    notifications = notifications or []
    unread_count = sum(1 for n in notifications if not n.get("read", True))
    
    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-relative", "pv-inline-block"])
    
    # Bell icon with badge
    bell = Component(tag="div")
    bell.class_names.extend(["pv-cursor-pointer", "pv-relative", "pv-p-8"])
    bell.attrs["onclick"] = "this.nextElementSibling.classList.toggle('active')"
    
    bell_icon = Component(tag="span", content="🔔")
    bell_icon.style.font_size = "1.25rem"
    bell.children.append(bell_icon)
    
    if unread_count > 0:
        badge = Component(tag="span", content=str(unread_count))
        badge.class_names.extend(["pv-absolute", "pv-rounded-full", "pv-bg-danger", "pv-text-white"])
        badge.style.top = "0"
        badge.style.right = "0"
        badge.style.width = "18px"
        badge.style.height = "18px"
        badge.style.font_size = "10px"
        badge.style.display = "flex"
        badge.style.align_items = "center"
        badge.style.justify_content = "center"
        bell.children.append(badge)
    
    comp.children.append(bell)
    
    # Dropdown
    dropdown = Component(tag="div")
    dropdown.class_names.extend(["pv-dropdown-menu", "pv-absolute", "pv-right-0"])
    dropdown.style.width = "320px"
    dropdown.style.max_height = "400px"
    dropdown.style.overflow = "auto"
    dropdown.style.z_index = "100"
    dropdown.style.margin_top = "8px"
    
    # Header
    header = Component(tag="div")
    header.class_names.extend(["pv-flex", "pv-items-center", "pv-justify-between", "pv-p-12", "pv-px-16", "pv-border-b"])
    
    title = Component(tag="div", content=f"Notifikasi ({unread_count})")
    title.class_names.extend(["pv-text-bold", "pv-text-sm"])
    header.children.append(title)
    
    mark_all = Component(tag="button", content="Tandai semua dibaca")
    mark_all.class_names.extend(["pv-btn", "pv-btn-ghost", "pv-btn-sm"])
    header.children.append(mark_all)
    
    dropdown.children.append(header)
    
    # Notifications
    for notif in notifications:
        item = Component(tag="div")
        item.class_names.extend(["pv-flex", "pv-gap-12", "pv-p-12", "pv-px-16", "pv-cursor-pointer"])
        if not notif.get("read", True):
            item.style.background = "#F8FAFC"
        item.attrs["onmouseenter"] = "this.style.background='#F3F4F6'"
        item.attrs["onmouseleave"] = "this.style.background='" + ("#F8FAFC" if not notif.get("read", True) else "transparent") + "'"
        
        # Icon
        icon = Component(tag="div", content=notif.get("icon", "📌"))
        icon.style.font_size = "1.25rem"
        item.children.append(icon)
        
        # Content
        content = Component(tag="div")
        content.style.flex = "1"
        
        title = Component(tag="div", content=notif.get("title", ""))
        title.class_names.extend(["pv-text-sm", "pv-text-bold"])
        if not notif.get("read", True):
            title.class_names.append("pv-text-primary")
        content.children.append(title)
        
        desc = Component(tag="div", content=notif.get("description", ""))
        desc.class_names.extend(["pv-text-xs", "pv-text-gray"])
        content.children.append(desc)
        
        time_el = Component(tag="div", content=notif.get("time", ""))
        time_el.class_names.extend(["pv-text-xs", "pv-text-gray"])
        content.children.append(time_el)
        
        item.children.append(content)
        
        if not notif.get("read", True):
            dot = Component(tag="div")
            dot.style.width = "8px"
            dot.style.height = "8px"
            dot.style.border_radius = "50%"
            dot.style.background = "#7C3AED"
            dot.style.flex_shrink = "0"
            item.children.append(dot)
        
        dropdown.children.append(item)
    
    # Footer
    footer = Component(tag="div", content="Lihat semua notifikasi")
    footer.class_names.extend(["pv-text-center", "pv-text-sm", "pv-text-primary", "pv-p-12", "pv-border-t", "pv-cursor-pointer"])
    dropdown.children.append(footer)
    
    comp.children.append(dropdown)
    
    return comp


# ==================== Theme Toggle ====================

def theme_toggle(
    light_icon: str = "☀️",
    dark_icon: str = "🌙",
    **kwargs,
) -> Component:
    """
    Theme toggle button (light/dark mode).
    
    Usage:
        theme_toggle()
    """
    comp = Component(tag="button", **kwargs)
    comp.class_names.extend(["pv-btn", "pv-btn-ghost", "pv-btn-sm", "pv-rounded-full"])
    comp.style.width = "40px"
    comp.style.height = "40px"
    comp.style.display = "flex"
    comp.style.align_items = "center"
    comp.style.justify_content = "center"
    comp.style.fontSize = "1.25rem"
    comp.attrs["onclick"] = "document.documentElement.classList.toggle('pv-dark-mode');this.textContent=this.textContent.trim()==='☀️'?'🌙':'☀️'"
    
    icon = Component(tag="span", content=light_icon)
    comp.children.append(icon)
    
    return comp


# ==================== Search Command ====================

def search_command(
    placeholder: str = "Cari...",
    shortcut: str = "⌘K",
    **kwargs,
) -> Component:
    """
    Search command / palette trigger.
    
    Usage:
        search_command(placeholder="Cari command...")
    """
    comp = Component(tag="div", **kwargs)
    comp.class_names.extend(["pv-flex", "pv-items-center", "pv-gap-8", "pv-p-8", "pv-px-12", "pv-bg-gray", "pv-rounded-lg", "pv-cursor-pointer", "pv-border"])
    comp.attrs["onclick"] = "document.querySelector('[data-command-palette]').style.display='flex'"
    
    icon = Component(tag="span", content="🔍")
    icon.style.opacity = "0.5"
    
    text = Component(tag="span", content=placeholder)
    text.class_names.extend(["pv-text-sm", "pv-text-gray"])
    text.style.flex = "1"
    
    kbd = Component(tag="kbd", content=shortcut)
    kbd.class_names.extend(["pv-text-xs", "pv-text-gray", "pv-bg-white", "pv-rounded", "pv-px-8", "pv-py-4", "pv-border"])
    
    comp.children = [icon, text, kbd]
    
    return comp
