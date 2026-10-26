"""Playblast utility functions"""

import os
import re
import shutil
import tempfile
import bpy


def get_addon_id():
    """Get the addon module ID"""
    # __package__ for a root-level file is already the full addon ID
    # e.g. "bl_ext.user_default.betterplayblast"
    return __package__


def get_prefs(context):
    """Get addon preferences safely"""
    try:
        addon_id = get_addon_id()
        return context.preferences.addons[addon_id].preferences
    except KeyError:
        # Preferences not available, return None
        return None


def get_qs(context):
    """Get Quick Settings from current scene"""
    return context.scene.bp_quick_settings


def resolve_output_folder(context):
    """Resolve the output folder for playblasts"""
    blend_path = bpy.data.filepath

    if not blend_path:
        return tempfile.gettempdir()

    blend_dir = os.path.dirname(os.path.abspath(blend_path))
    
    # Try to get preferences, but handle gracefully if not available
    prefs = get_prefs(context)

    # If prefs not available, default to parent/videos (VIDEOS mode default behavior)
    if not prefs:
        parent = os.path.dirname(blend_dir)
        videos_folder = os.path.join(parent, "videos")
        os.makedirs(videos_folder, exist_ok=True)
        return videos_folder

    # Use preferences to determine output folder
    output_mode = getattr(prefs, 'output_folder_mode', 'VIDEOS')
    
    if output_mode == "VIDEOS":
        # Go up one level from workVersions to get the parent, then enter videos
        # D:\tsec_production\production\assets\props\Rifle\modeling\workVersions
        # → D:\tsec_production\production\assets\props\Rifle\modeling\videos
        parent = os.path.dirname(blend_dir)
        videos_folder = os.path.join(parent, "videos")
        # Ensure folder exists
        try:
            os.makedirs(videos_folder, exist_ok=True)
        except Exception:
            pass
        return videos_folder

    elif output_mode == "PROJECT":
        # Save in project folder (where .blend is)
        project_subfolder_enabled = getattr(prefs, 'project_subfolder_enabled', False)
        project_subfolder_name = getattr(prefs, 'project_subfolder_name', 'videos')
        if project_subfolder_enabled:
            subfolder = project_subfolder_name or "videos"
            folder = os.path.join(blend_dir, subfolder)
        else:
            folder = blend_dir
        try:
            os.makedirs(folder, exist_ok=True)
        except Exception:
            pass
        return folder

    elif output_mode == "SYSTEM":
        # Use custom system folder
        system_folder_path = getattr(prefs, 'system_folder_path', '')
        if system_folder_path and os.path.isdir(system_folder_path):
            return system_folder_path
        # Fallback if path doesn't exist
        return blend_dir

    # Default fallback
    return blend_dir


def get_base_name(context):
    """Get the base name for playblast files"""
    prefs = get_prefs(context)
    blend_path = bpy.data.filepath

    if not prefs:
        # Default: use blend filename without extension
        if blend_path:
            raw = os.path.splitext(os.path.basename(blend_path))[0]
            return re.sub(r'\.\d{4}$', '', raw)
        return "playblast"

    if prefs.playblast_name_mode == "FILENAME":
        # Use .blend filename, remove .0001 suffix and extension
        if blend_path:
            raw = os.path.splitext(os.path.basename(blend_path))[0]
            # Remove version suffix like .0001
            return re.sub(r'\.\d{4}$', '', raw)
        return "playblast"

    elif prefs.playblast_name_mode == "CUSTOM":
        # Use custom name
        return prefs.custom_playblast_name or "playblast"

    return "playblast"


def get_ext(context):
    """Get the file extension for playblasts"""
    return ".mp4"


def get_version_string(context):
    """Get version string for playblasts"""
    prefs = get_prefs(context)
    qs = get_qs(context)
    
    # Check quick settings first
    if qs and qs.version_enabled:
        return f".{qs.version_number:04d}"
    
    # Check preferences
    if not prefs:
        return ""
    
    if prefs.include_version_number:
        latest = find_latest_version_number(context)
        return f".{latest + 1:04d}"
    
    return ""


def get_output_filepath(context):
    """Get the complete output filepath for playblast"""
    folder = resolve_output_folder(context)
    base = get_base_name(context)
    ver = get_version_string(context)
    ext = get_ext(context)
    
    # Ensure folder exists
    os.makedirs(folder, exist_ok=True)
    
    return os.path.join(folder, f"{base}{ver}{ext}")


def get_playblast_filename(context):
    """Get playblast filename without version number (base_name + extension)
    
    Returns: Tuple (base_name, filename_with_ext)
    
    This is used for initial render filename (before version numbering).
    """
    base = get_base_name(context)
    ext = get_ext(context)
    return base, base + ext


def find_latest_playblast_file(context):
    """Find the latest playblast file in the output folder"""
    folder = resolve_output_folder(context)
    base = get_base_name(context)
    ext = get_ext(context)

    if not os.path.isdir(folder):
        return None

    # Pattern 1: with version numbers (e.g., characters_Leo_modeling_main.0001.mp4)
    pattern_ver = re.compile(rf"^{re.escape(base)}\.(\d{{4}}){re.escape(ext)}$")
    # Pattern 2: without version (e.g., characters_Leo_modeling_main.mp4)
    pattern_plain = re.compile(rf"^{re.escape(base)}{re.escape(ext)}$")

    best_ver = -1
    best_path = None

    for fname in os.listdir(folder):
        fpath = os.path.join(folder, fname)
        if not os.path.isfile(fpath):
            continue
            
        m = pattern_ver.match(fname)
        if m:
            v = int(m.group(1))
            if v > best_ver:
                best_ver = v
                best_path = fpath
        elif pattern_plain.match(fname) and best_ver == -1:
            best_path = fpath

    return best_path


def find_latest_version_number(context):
    """Find the latest version number of playblasts"""
    folder = resolve_output_folder(context)
    base = get_base_name(context)
    ext = get_ext(context)

    if not os.path.isdir(folder):
        return 0

    pattern = re.compile(rf"^{re.escape(base)}\.(\d{{4}}){re.escape(ext)}$")
    max_ver = 0
    for fname in os.listdir(folder):
        m = pattern.match(fname)
        if m:
            max_ver = max(max_ver, int(m.group(1)))
    return max_ver


def play_file(filepath):
    """Play a file using the system default player"""
    try:
        import subprocess
        import platform

        if platform.system() == "Darwin":
            subprocess.Popen(["open", filepath])
        elif platform.system() == "Windows":
            os.startfile(filepath)
        else:
            subprocess.Popen(["xdg-open", filepath])
        return True
    except Exception as e:
        print(f"Could not play file: {e}")
        return False
