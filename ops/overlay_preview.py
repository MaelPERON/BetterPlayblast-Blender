"""BetterPlayblast Viewport Overlay Preview — real-time camera-view draw handler

- Reads positions & appearance from addon prefs (same source as the actual render)
- Scales font size and bar height proportionally to the camera frame
- Loads Courier New to match the HTML template typography
- Draws small icon proxy rectangles when show_icons is on, matching the Feather
  icons that appear in the final custom overlay render
"""

import os
import bpy
import blf
import gpu
from gpu_extras.batch import batch_for_shader
from bpy_extras.view3d_utils import location_3d_to_region_2d

_handle  = None
_font_id = None   # cached BLF font id for Courier New (loaded once)

# Placeholders that have a corresponding Feather icon in the final render
_ICON_PLACEHOLDER_KEYS = {
    "file_name", "file_version", "file_path",
    "camera_name", "camera_focal",
    "fps", "resolution", "width", "height",
    "frame_range", "frame_current", "frame_start", "frame_end", "frame_total",
    "datetime", "date", "time",
    "user", "hostname", "scene_name",
    "comment", "marker", "sequencer_strip",
    "memory_usage", "render_time", "thread_count",
}


# ─── helpers ──────────────────────────────────────────────────────────────────

def _get_qs(context):
    scene = getattr(context, 'scene', None)
    if scene is None:
        return None
    return getattr(scene, 'bp_quick_settings', None)


def _get_prefs(context):
    try:
        addon_id = __package__.rsplit('.', 1)[0] if __package__ else ""
        addon = context.preferences.addons.get(addon_id)
        return addon.preferences if addon else None
    except Exception:
        return None


def _has_icon(text: str) -> bool:
    """Return True if text contains any placeholder that maps to a Feather icon."""
    for key in _ICON_PLACEHOLDER_KEYS:
        if "{" + key + "}" in text:
            return True
    return False


def _load_monospace_font():
    """Load Courier New (or closest monospace) via BLF. Returns font_id."""
    candidates = [
        r"C:\Windows\Fonts\cour.ttf",
        "/Library/Fonts/Courier New.ttf",
        "/System/Library/Fonts/Courier New.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]
    for path in candidates:
        if os.path.isfile(path):
            try:
                fid = blf.load(path)
                if fid >= 0:
                    return fid
            except Exception:
                pass
    return 0


def _resolve_preview_text(text: str, context: bpy.types.Context) -> str:
    """Resolve {placeholder} tokens using current scene state (no rendering)."""
    import socket
    from datetime import datetime

    scene = context.scene
    cam = scene.camera
    cam_data = cam.data if cam else None
    qs = _get_qs(context)
    render = scene.render
    res_x = int(render.resolution_x * render.resolution_percentage / 100)
    res_y = int(render.resolution_y * render.resolution_percentage / 100)
    fps = round(render.fps / render.fps_base)

    repl = {
        "{file_name}":       os.path.splitext(os.path.basename(bpy.data.filepath))[0] if bpy.data.filepath else "untitled",
        "{file_version}":    f"{qs.version_number:04d}" if qs else "0001",
        "{file_path}":       bpy.data.filepath or "",
        "{datetime}":        datetime.now().strftime("%Y-%m-%d %H:%M"),
        "{date}":            datetime.now().strftime("%Y-%m-%d"),
        "{time}":            datetime.now().strftime("%H:%M:%S"),
        "{scene_name}":      scene.name,
        "{camera_name}":     cam.name if cam else "",
        "{camera_focal}":    f"{cam_data.lens:.0f}" if cam_data else "",
        "{resolution}":      f"{res_x}x{res_y}",
        "{width}":           str(res_x),
        "{height}":          str(res_y),
        "{fps}":             str(fps),
        "{frame_current}":   str(scene.frame_current),
        "{frame_start}":     str(scene.frame_start),
        "{frame_end}":       str(scene.frame_end),
        "{frame_range}":     f"{scene.frame_start}-{scene.frame_end}",
        "{frame_total}":     str(scene.frame_end - scene.frame_start + 1),
        "{user}":            os.getenv("USERNAME") or os.getenv("USER") or "",
        "{hostname}":        socket.gethostname(),
        "{comment}":         getattr(qs, 'overlay_comment_text', '') if qs else "",
        "{memory_usage}":    "",
        "{render_time}":     "",
        "{thread_count}":    "",
        "{marker}":          "",
        "{sequencer_strip}": "",
    }
    for k, v in repl.items():
        text = text.replace(k, v)
    return text


def _camera_frame_rect(region, rv3d, scene):
    """Return (x0, y0, x1, y1) of the camera frame in viewport pixel coordinates."""
    cam = scene.camera
    if cam is not None:
        frame_local = cam.data.view_frame(scene=scene)
        frame_world = [cam.matrix_world @ v for v in frame_local]
        frame_2d = [location_3d_to_region_2d(region, rv3d, v) for v in frame_world]
        if all(v is not None for v in frame_2d):
            xs = [v.x for v in frame_2d]
            ys = [v.y for v in frame_2d]
            return min(xs), min(ys), max(xs), max(ys)

    render = scene.render
    cam_w = render.resolution_x * (render.pixel_aspect_x or 1.0)
    cam_h = render.resolution_y * (render.pixel_aspect_y or 1.0)
    vw, vh = float(region.width), float(region.height)
    if cam_h == 0 or vh == 0:
        return 0.0, 0.0, vw, vh
    cam_aspect = cam_w / cam_h
    view_aspect = vw / vh
    if cam_aspect >= view_aspect:
        fw, fh = vw, vw / cam_aspect
    else:
        fh, fw = vh, vh * cam_aspect
    x0 = (vw - fw) / 2.0
    y0 = (vh - fh) / 2.0
    return x0, y0, x0 + fw, y0 + fh


def _draw_rect(x1, y1, x2, y2, color):
    """Draw a filled alpha-blended rectangle in screen space."""
    vertices = [(x1, y1), (x2, y1), (x1, y2), (x2, y2)]
    indices = [(0, 1, 2), (1, 3, 2)]
    shader = gpu.shader.from_builtin('UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)
    gpu.state.blend_set('ALPHA')
    shader.bind()
    shader.uniform_float("color", color)
    batch.draw(shader)
    gpu.state.blend_set('NONE')


def _draw_text_row(font_id, left, center, right, x0, x1, y, margin, font_size, color,
                   icon_left=False, icon_center=False, icon_right=False):
    """Draw left/center/right text with optional icon proxy rectangles."""
    # Icon proxy: a filled square the size of the font cap-height
    icon_sz  = font_size * 0.75
    icon_gap = font_size * 0.30
    icon_adv = icon_sz + icon_gap  # horizontal space consumed by icon + gap
    # Vertical placement: align icon with text cap-height
    icon_y0  = y + font_size * 0.08
    icon_y1  = y + font_size * 0.83

    blf.size(font_id, font_size)
    blf.color(font_id, *color)

    if left:
        x = x0 + margin
        if icon_left:
            _draw_rect(x, icon_y0, x + icon_sz, icon_y1, color)
            x += icon_adv
        blf.position(font_id, x, y, 0)
        blf.draw(font_id, left)

    if center:
        w, _ = blf.dimensions(font_id, center)
        total_w = w + (icon_adv if icon_center else 0)
        cx = (x0 + x1) / 2.0 - total_w / 2.0
        if icon_center:
            _draw_rect(cx, icon_y0, cx + icon_sz, icon_y1, color)
            cx += icon_adv
        blf.position(font_id, cx, y, 0)
        blf.draw(font_id, center)

    if right:
        w, _ = blf.dimensions(font_id, right)
        total_w = w + (icon_adv if icon_right else 0)
        rx = x1 - margin - total_w
        if icon_right:
            _draw_rect(rx, icon_y0, rx + icon_sz, icon_y1, color)
            rx += icon_adv
        blf.position(font_id, rx, y, 0)
        blf.draw(font_id, right)


# ─── main draw callback ────────────────────────────────────────────────────────

def draw_overlay_callback():
    """Called on every 3D viewport redraw (POST_PIXEL). Draws the overlay preview."""
    context = bpy.context

    try:
        if not hasattr(context, 'scene') or context.scene is None:
            return
        space = getattr(context, 'space_data', None)
        if space is None or getattr(space, 'type', None) != 'VIEW_3D':
            return
        rv3d = getattr(space, 'region_3d', None)
        if rv3d is None or rv3d.view_perspective != 'CAMERA':
            return

        qs = _get_qs(context)
        if not qs or not qs.overlay_preview_enabled:
            return

        prefs  = _get_prefs(context)
        scene  = context.scene
        render = scene.render
        region = context.region

        # ── Appearance (prefs = source of truth) ──────────────────────────────
        font_size_base = getattr(prefs, 'overlay_font_size', 24) if prefs else getattr(qs, 'overlay_font_size', 24)
        margin_base    = float(getattr(prefs, 'overlay_margin', 10) if prefs else getattr(qs, 'overlay_margin', 10))
        if prefs:
            r, g, b          = prefs.overlay_text_color
            bg_r, bg_g, bg_b = prefs.overlay_bg_color
            opacity          = float(getattr(prefs, 'overlay_opacity', 0.75))
        else:
            r, g, b          = qs.overlay_text_color
            bg_r, bg_g, bg_b = qs.overlay_bg_color
            opacity          = float(getattr(qs, 'overlay_opacity', 0.75))
        text_color = (r, g, b, 1.0)
        bg_color   = (bg_r, bg_g, bg_b, opacity)

        show_icons = getattr(qs, 'overlay_show_icons', True)

        # ── Camera frame in viewport pixels ───────────────────────────────────
        x0, y0, x1, y1 = _camera_frame_rect(region, rv3d, scene)
        cam_w = x1 - x0
        cam_h = y1 - y0
        if cam_w <= 0 or cam_h <= 0:
            return

        # ── Proportional scaling relative to render resolution ────────────────
        # Final render: overlay height = 36*2 px at render_h → each bar = 36 px
        render_w = render.resolution_x * render.resolution_percentage / 100
        render_h = render.resolution_y * render.resolution_percentage / 100
        scale    = (cam_w / render_w) if render_w > 0 else 1.0

        font_size = max(6, round(font_size_base * scale))
        margin    = max(1.0, margin_base * scale)
        bar_h     = (36.0 / render_h * cam_h) if render_h > 0 else float(font_size + 10)

        # ── Text content + icon detection ─────────────────────────────────────
        src = prefs if prefs else qs

        if qs.overlay_custom_enabled:
            tl = _resolve_preview_text(src.overlay_top_left,      context)
            tc = _resolve_preview_text(src.overlay_top_center,    context)
            tr = _resolve_preview_text(src.overlay_top_right,     context)
            bl = _resolve_preview_text(src.overlay_bottom_left,   context)
            bc = _resolve_preview_text(src.overlay_bottom_center, context)
            br = _resolve_preview_text(src.overlay_bottom_right,  context)

            # Icon proxies: check template strings (before resolution) for known placeholders
            icon_tl = show_icons and _has_icon(src.overlay_top_left)
            icon_tc = show_icons and _has_icon(src.overlay_top_center)
            icon_tr = show_icons and _has_icon(src.overlay_top_right)
            icon_bl = show_icons and _has_icon(src.overlay_bottom_left)
            icon_bc = show_icons and _has_icon(src.overlay_bottom_center)
            icon_br = show_icons and _has_icon(src.overlay_bottom_right)
        else:
            # Default layout: approximate enabled metadata fields
            icon_tl = icon_tc = icon_tr = icon_bl = icon_bc = icon_br = False
            res  = lambda ph: _resolve_preview_text(ph, context)
            meta = lambda key: getattr(prefs, key, True) if prefs else True

            tl_parts = []
            if meta('meta_file'):   tl_parts.append(res("{file_name} v{file_version}"))
            if meta('meta_scene'):  tl_parts.append(res("{scene_name}"))
            tl = " | ".join(p for p in tl_parts if p)

            tc = res("{frame_current}/{frame_total}")

            tr_parts = []
            if meta('meta_resolution'):  tr_parts.append(res("{resolution}"))
            if meta('meta_fps'):         tr_parts.append(res("{fps}fps"))
            if meta('meta_frame_range'): tr_parts.append(res("{frame_range}"))
            tr = " | ".join(p for p in tr_parts if p)

            bl_parts = []
            if meta('meta_camera'): bl_parts.append(res("{camera_name}"))
            if meta('meta_lens'):   bl_parts.append(res("{camera_focal}mm"))
            bl = " | ".join(p for p in bl_parts if p)

            bc = res("{comment}") if meta('meta_comment') else ""

            br_parts = []
            if meta('meta_user'): br_parts.append(res("{user}"))
            if meta('meta_date'): br_parts.append(res("{datetime}"))
            br = " | ".join(p for p in br_parts if p)

        # ── Draw background bars ───────────────────────────────────────────────
        _draw_rect(x0, y1 - bar_h, x1, y1, bg_color)   # top bar
        _draw_rect(x0, y0, x1, y0 + bar_h, bg_color)   # bottom bar

        # ── Draw text + icon proxies ───────────────────────────────────────────
        global _font_id
        if _font_id is None:
            _font_id = _load_monospace_font()
        font_id = _font_id

        text_y_top    = y1 - bar_h + (bar_h - font_size) * 0.5
        text_y_bottom = y0         + (bar_h - font_size) * 0.5

        _draw_text_row(font_id, tl, tc, tr, x0, x1, text_y_top,    margin, font_size, text_color,
                       icon_tl, icon_tc, icon_tr)
        _draw_text_row(font_id, bl, bc, br, x0, x1, text_y_bottom, margin, font_size, text_color,
                       icon_bl, icon_bc, icon_br)

    except Exception:
        pass  # never crash Blender from a draw callback


# ─── register / unregister ────────────────────────────────────────────────────

def register():
    global _handle, _font_id
    _font_id = None  # reset so Courier New is loaded on first draw
    _handle = bpy.types.SpaceView3D.draw_handler_add(
        draw_overlay_callback, (), 'WINDOW', 'POST_PIXEL'
    )


def unregister():
    global _handle
    if _handle is not None:
        bpy.types.SpaceView3D.draw_handler_remove(_handle, 'WINDOW')
        _handle = None
