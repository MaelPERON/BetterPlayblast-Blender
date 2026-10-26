"""Overlay Configuration and Positioning System

Supports customizable overlay positioning with placeholder templates for metadata.
Each position (top-left, top-center, etc.) can have custom text with placeholders.
"""

# ═════════════════════════════════════════════════════════════════════════════
# AVAILABLE PLACEHOLDERS FOR OVERLAY TEXT
# ═════════════════════════════════════════════════════════════════════════════

AVAILABLE_PLACEHOLDERS = {
    # File Information
    "{file_name}": "Blend file name (e.g., 'scene.blend')",
    "{file_path}": "Full blend file path",
    "{file_version}": "Playblast version number (e.g., '0001')",
    
    # Date & Time
    "{datetime}": "Current date and time (e.g., '2026-04-30 16:42')",
    "{date}": "Current date only (e.g., '2026-04-30')",
    "{time}": "Current time only (e.g., '16:42:15')",
    
    # Scene & Camera
    "{scene_name}": "Active scene name",
    "{camera_name}": "Active camera name",
    "{camera_focal}": "Camera focal length in mm",
    
    # Resolution & Frame Rate
    "{width}": "Render width in pixels",
    "{height}": "Render height in pixels",
    "{resolution}": "Resolution as WIDTHxHEIGHT (e.g., '1920x1080')",
    "{fps}": "Frames per second",
    
    # Frame Information
    "{frame_current}": "Current frame number",
    "{frame_start}": "Sequence start frame",
    "{frame_end}": "Sequence end frame",
    "{frame_range}": "Frame range (e.g., '1-120')",
    "{frame_total}": "Total number of frames",
    
    # System Information
    "{user}": "System username",
    "{hostname}": "Computer hostname",
    "{memory_usage}": "Memory used during render",
    "{render_time}": "Time taken to render",
    "{thread_count}": "Number of CPU threads used",
    
    # Metadata
    "{comment}": "User comment/note",
    "{marker}": "Current marker name (if on a marker)",
    "{sequencer_strip}": "Active sequencer strip name",
}

# ═════════════════════════════════════════════════════════════════════════════
# QUICK TEMPLATES - Fast preset configurations
# ═════════════════════════════════════════════════════════════════════════════

QUICK_TEMPLATES = {
    "minimal": {
        "top_left": "{file_name} v{file_version}",
        "top_center": "",
        "top_right": "{datetime}",
        "bottom_left": "",
        "bottom_center": "",
        "bottom_right": "{resolution} | {fps}fps",
    },
    
    "standard": {
        "top_left": "{file_name} | v{file_version}",
        "top_center": "{camera_name}",
        "top_right": "{datetime}",
        "bottom_left": "{user} @ {hostname}",
        "bottom_center": "",
        "bottom_right": "{resolution} | {fps}fps | {frame_range}",
    },
    
    "production": {
        "top_left": "{file_name} v{file_version}",
        "top_center": "{scene_name} | {camera_name} {camera_focal}mm",
        "top_right": "{datetime}",
        "bottom_left": "{user} @ {hostname}",
        "bottom_center": "{frame_current}/{frame_total}",
        "bottom_right": "{width}x{height} | {fps}fps | {render_time}",
    },
    
    "tech_specs": {
        "top_left": "{file_name}",
        "top_center": "{resolution} | {fps}fps | {frame_range}",
        "top_right": "{datetime}",
        "bottom_left": "Camera: {camera_name} {camera_focal}mm",
        "bottom_center": "Frame {frame_current}/{frame_total}",
        "bottom_right": "Threads: {thread_count} | Memory: {memory_usage}",
    },
    
    "minimal_bottom": {
        "top_left": "",
        "top_center": "",
        "top_right": "",
        "bottom_left": "{file_name} v{file_version}",
        "bottom_center": "{frame_current}/{frame_total} | {datetime}",
        "bottom_right": "{resolution} | {fps}fps",
    },
}

# ═════════════════════════════════════════════════════════════════════════════
# POSITION NAMES & LAYOUT
# ═════════════════════════════════════════════════════════════════════════════

OVERLAY_POSITIONS = {
    "top_left": "Top Left",
    "top_center": "Top Center",
    "top_right": "Top Right",
    "bottom_left": "Bottom Left",
    "bottom_center": "Bottom Center",
    "bottom_right": "Bottom Right",
}

# ═════════════════════════════════════════════════════════════════════════════
# DEFAULT CONFIGURATION
# ═════════════════════════════════════════════════════════════════════════════

DEFAULT_OVERLAY_CONFIG = {
    "custom_enabled": False,  # Use custom layout instead of default
    "template_preset": "standard",  # Active template
    "top_left": "{file_name} | v{file_version}",
    "top_center": "{camera_name}",
    "top_right": "{datetime}",
    "bottom_left": "{user}",
    "bottom_center": "",
    "bottom_right": "{resolution} | {fps}fps",
}


def get_placeholder_help() -> str:
    """Generate help text for available placeholders"""
    help_text = "📋 AVAILABLE PLACEHOLDERS:\n"
    help_text += "=" * 50 + "\n\n"
    
    current_category = ""
    for placeholder, description in sorted(AVAILABLE_PLACEHOLDERS.items()):
        # Extract category from description
        category = description.split()[0] if description else ""
        if category != current_category:
            current_category = category
            help_text += f"\n{category.upper()}:\n"
        
        help_text += f"  {placeholder:<20} - {description}\n"
    
    return help_text


def validate_placeholder(placeholder: str) -> bool:
    """Check if a placeholder is valid"""
    # Remove {} and check against available
    clean = placeholder.strip("{}")
    return f"{{{clean}}}" in AVAILABLE_PLACEHOLDERS or placeholder in AVAILABLE_PLACEHOLDERS
