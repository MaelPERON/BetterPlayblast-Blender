"""BetterPlayblast Playblast Operator - Renders playblasts using ONLY addon settings"""

import bpy
import os
import json
import tempfile
from pathlib import Path
from functools import partial

from ..utils.scripts import Script
from ..utils.pyppeteer import pyppeteer_import
from ..utils.capture_data import data_init_capture, data_frame_capture
from ..utils.time import get_now
from ..utils.handlers import remove_function_from_handler
from ..BetterPlayblast.install import all_installed
from ..BetterPlayblast.metadata import MetadataList as MList
from ..playblast_utils import (
    resolve_output_folder, get_playblast_filename,
    get_version_string, get_ext, find_latest_version_number, get_qs,
)


def get_addon_preferences():
    """Get addon preferences safely"""
    try:
        # __package__ here is e.g. "bl_ext.user_default.betterplayblast.ops"
        # Strip the subpackage name to get the root addon ID
        addon_id = __package__.rsplit('.', 1)[0] if __package__ else ""
        addon = bpy.context.preferences.addons.get(addon_id)
        if addon:
            return addon.preferences
        return None
    except Exception:
        return None


def get_playblast_class():
    """Check if BetterPlayblast dependencies are installed"""
    if all_installed(refresh=True, save_cache=False):
        from ..BetterPlayblast.playblast import Playblast
        return Playblast
    return None





def setup_render_settings_for_playblast(context, video_filepath):
    """Apply addon preferences to scene render settings before rendering.

    Uses Blender's native FFmpeg parameters from the Render Output panel.
    Reads the current format/codec settings that Blender already has configured.

    Writes directly into the same Blender properties that the Output panel uses:
      scene.render.image_settings.file_format
      scene.render.ffmpeg.format       (Container)
      scene.render.ffmpeg.codec        (Video Codec)
      scene.render.ffmpeg.audio_codec  (Audio Codec)
      scene.render.ffmpeg.gopsize      (Keyframe Interval)
      scene.render.ffmpeg.video_bitrate (kbps)
    """
    scene = context.scene
    prefs = get_addon_preferences()
    qs    = scene.bp_quick_settings if hasattr(scene, 'bp_quick_settings') else None

    # ── Output filepath ────────────────────────────────────────────────────────
    scene.render.filepath = str(video_filepath)

    # ── Video format — write exactly what Blender's Output panel uses ─────────
    # scene.render.image_settings.file_format : 'FFMPEG' | 'AVI_JPEG' | 'AVI_RAW'
    if scene.render.image_settings.media_type:
        scene.render.image_settings.media_type = 'VIDEO'
    scene.render.image_settings.file_format = prefs.file_format

    if prefs.file_format == 'FFMPEG':
        ffmpeg = scene.render.ffmpeg

        # Apply container and codec from addon preferences
        ffmpeg.format = prefs.container  # e.g., 'MPEG4', 'QUICKTIME', 'MKV'
        ffmpeg.codec = prefs.video_codec  # e.g., 'H264', 'QTRLE'

        # Apply audio codec — check quick settings override first
        if qs and qs.include_audio_enabled:
            ffmpeg.audio_codec = qs.include_audio_codec  # e.g., 'NO_AUDIO', 'AAC', 'MP3'
        else:
            ffmpeg.audio_codec = prefs.audio_codec  # e.g., 'NONE', 'AAC', 'MP3'

        # scene.render.ffmpeg.gopsize : keyframe interval
        ffmpeg.gopsize = prefs.keyframe_interval

        # scene.render.ffmpeg.video_bitrate : in kbps — prefs stores Mbps
        ffmpeg.video_bitrate    = prefs.video_bitrate * 1000
        ffmpeg.maxrate          = prefs.video_bitrate * 1000
        ffmpeg.minrate          = 0
        ffmpeg.use_max_b_frames = False

    # ── Resolution ────────────────────────────────────────────────────────────
    if qs and qs.resolution_override_enabled:
        scene.render.resolution_percentage = qs.resolution_percentage
    else:
        scene.render.resolution_percentage = prefs.resolution_percentage

    # ── Frame rate ────────────────────────────────────────────────────────────
    scene.render.fps = prefs.frame_rate

    # ── Frame range ───────────────────────────────────────────────────────────
    if qs and qs.frame_range_override_enabled:
        scene.frame_start = qs.frame_start
        scene.frame_end   = qs.frame_end

    # ── Viewport shading ──────────────────────────────────────────────────────
    if qs and qs.shading_override_enabled:
        target_shading = qs.viewport_shading
    else:
        target_shading = prefs.viewport_shading if prefs.use_viewport_shading else 'SOLID'

    return target_shading


class BP_OT_playblast(bpy.types.Operator):
    """Main Playblast Operator - renders using ONLY addon settings"""
    bl_idname = "bp.playblast"
    bl_label = "Playblast"
    bl_description = "Render playblast with BetterPlayblast"
    bl_options = {'REGISTER'}

    _timer = None
    _rendering = False

    comment: bpy.props.StringProperty(name="Comment", default="")  # type: ignore

    @classmethod
    def poll(cls, context):
        return get_playblast_class() is not None and bpy.data.filepath

    def invoke(self, context, event):
        prefs = get_addon_preferences()
        if prefs and prefs.comment_dialog_enabled:
            return context.window_manager.invoke_props_dialog(self, width=420)
        return self.execute(context)

    def draw(self, context):
        self.layout.prop(self, "comment", text="Comment")

    def run_pre_script(self, context, comment):
        prefs = get_addon_preferences()
        if prefs and prefs.pre_script_path:
            try:
                pre_script = Script(prefs.pre_script_path)
                pre_script.run("before_playblast", context, comment)
            except Exception as e:
                self.report({'ERROR'}, f"Pre-script execution failed: {str(e)}")

    def run_post_script(self, context, final_path, comment):
        prefs = get_addon_preferences()
        if prefs and prefs.post_script_path:
            try:
                post_script = Script(prefs.post_script_path)
                post_script.run("after_playblast", context, str(final_path), comment)
            except Exception as e:
                self.report({'ERROR'}, f"Post-script execution failed: {str(e)}")

    def execute(self, context):
        prefs = get_addon_preferences()
        if not prefs:
            self.report({'ERROR'}, "Cannot access addon preferences!")
            return {'CANCELLED'}

        Playblast = get_playblast_class()
        if not Playblast:
            self.report({'ERROR'}, "Better Playblast dependencies not installed!")
            return {'CANCELLED'}

        if not bpy.data.is_saved:
            self.report({'ERROR'}, "Please save your .blend file first!")
            return {'CANCELLED'}

        self.run_pre_script(context, self.comment)
        try:
            # Create temporary folder for rendering
            temp_folder = Path(tempfile.gettempdir()) / "BetterPlayblast"
            temp_folder.mkdir(parents=True, exist_ok=True)

            # Auto-increment version if enabled
            qs = get_qs(context)
            if qs and qs.version_enabled:
                qs.version_number = find_latest_version_number(context) + 1

            # Get output settings
            output_folder = Path(resolve_output_folder(context))
            output_folder.mkdir(parents=True, exist_ok=True)
            base_name, _ = get_playblast_filename(context)
            ver      = get_version_string(context)   # e.g. ".0017" or ""
            ext      = get_ext(context)              # e.g. ".mp4"
            filename = base_name + ver + ext         # e.g. "props_Rifle_modeling_main.0017.mp4"

            # Final output path
            final_path = output_folder / filename

            # Temporary render path
            temp_video_path = temp_folder / f"_temp_{filename}"
            temp_json_path  = temp_folder / f"_temp_{base_name}.json"

            # Save current render settings to restore later
            scene = context.scene
            r = scene.render
            saved_settings = {
                'filepath':              r.filepath,
                'resolution_percentage': r.resolution_percentage,
                'frame_start':           scene.frame_start,
                'frame_end':             scene.frame_end,
                'fps':                   r.fps,
                'file_format':           r.image_settings.file_format,
                'color_mode':            r.image_settings.color_mode,
                'ffmpeg_format':         r.ffmpeg.format,
                'ffmpeg_codec':          r.ffmpeg.codec,
                'ffmpeg_audio_codec':    r.ffmpeg.audio_codec,
                'ffmpeg_gopsize':        r.ffmpeg.gopsize,
                'ffmpeg_video_bitrate':  r.ffmpeg.video_bitrate,
                'ffmpeg_maxrate':        r.ffmpeg.maxrate,
                'ffmpeg_minrate':        r.ffmpeg.minrate,
                'ffmpeg_use_max_b_frames': r.ffmpeg.use_max_b_frames,
            }

            # Save viewport shading if needed
            for area in context.screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        if space.type == 'VIEW_3D':
                            saved_settings['shading_type'] = space.shading.type
                            break

            # Setup render with addon settings only
            target_shading = setup_render_settings_for_playblast(context, temp_video_path)

            # Set viewport shading (if using viewport shading mode)
            is_opengl = target_shading != 'RENDERED'
            if is_opengl:
                for area in context.screen.areas:
                    if area.type == 'VIEW_3D':
                        for space in area.spaces:
                            if space.type == 'VIEW_3D':
                                # Map our shading enum to Blender's shading types
                                shading_map = {
                                    'WIREFRAME': 'WIREFRAME',
                                    'SOLID': 'SOLID',
                                    'MATERIAL': 'MATERIAL',
                                    'RENDERED': 'RENDERED'
                                }
                                space.shading.type = shading_map.get(target_shading, 'SOLID')
                                break

            # Save and apply overlay settings
            saved_overlays = {}
            overlay_space = None
            for area in context.screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        if space.type == 'VIEW_3D':
                            overlay_space = space
                            break
                    break

            if overlay_space and qs and qs.overlays_mode != 'NONE':
                ov = overlay_space.overlay
                saved_overlays = {
                    'show_overlays': ov.show_overlays,
                    'show_bones': ov.show_bones,
                    'show_extras': ov.show_extras,
                    'show_floor': ov.show_floor,
                    'show_axis_x': ov.show_axis_x,
                    'show_axis_y': ov.show_axis_y,
                    'show_axis_z': ov.show_axis_z,
                    'show_text': ov.show_text,
                    'show_cursor': ov.show_cursor,
                    'show_annotation': ov.show_annotation,
                    'show_relationship_lines': ov.show_relationship_lines,
                    'show_outline_selected': ov.show_outline_selected,
                    'show_motion_paths': ov.show_motion_paths,
                    'show_object_origins': ov.show_object_origins,
                    'show_wireframes': ov.show_wireframes,
                    'show_face_orientation': ov.show_face_orientation,
                    'show_stats': ov.show_stats,
                }
                mode = qs.overlays_mode
                if mode == 'ALL':
                    ov.show_overlays = False
                elif mode == 'BONES':
                    ov.show_bones = False
                elif mode == 'ALL_EXCEPT_BG':
                    ov.show_bones = False
                    ov.show_extras = False
                    ov.show_floor = False
                    ov.show_axis_x = False
                    ov.show_axis_y = False
                    ov.show_axis_z = False
                    ov.show_text = False
                    ov.show_cursor = False
                    ov.show_annotation = False
                    ov.show_relationship_lines = False
                    ov.show_outline_selected = False
                    ov.show_motion_paths = False
                    ov.show_object_origins = False
                    ov.show_wireframes = False
                    ov.show_face_orientation = False
                    ov.show_stats = False

            # Initialize capture data
            data = data_init_capture(context)
            data["file_version"] = f"{qs.version_number:04d}" if qs else "0001"

            # Inject comment — stored in data["note"] so {comment} placeholder resolves it
            comment = getattr(self, 'comment', '')
            if comment:
                data["note"] = comment

            # Setup frame capture handler
            handler = bpy.app.handlers.frame_change_post
            remove_function_from_handler(data_frame_capture, handler)
            handler.append(partial(data_frame_capture, data, get_now()))

            # Render using OpenGL
            if is_opengl:
                bpy.ops.render.opengl(animation=True)
            else:
                bpy.ops.render.render(animation=True)

            # Clean up handler
            remove_function_from_handler(data_frame_capture, handler)

            # Restore overlay settings
            if overlay_space and saved_overlays:
                ov = overlay_space.overlay
                for key, val in saved_overlays.items():
                    setattr(ov, key, val)

            # Add encoding settings to metadata
            data['encoding'] = {
                'format': context.scene.render.image_settings.file_format,
                'container': context.scene.render.ffmpeg.format if context.scene.render.image_settings.file_format == 'FFMPEG' else 'N/A',
                'codec': context.scene.render.ffmpeg.codec if context.scene.render.image_settings.file_format == 'FFMPEG' else 'N/A',
                'audio_codec': context.scene.render.ffmpeg.audio_codec if context.scene.render.image_settings.file_format == 'FFMPEG' else 'N/A',
                'bitrate_kbps': context.scene.render.ffmpeg.video_bitrate if context.scene.render.image_settings.file_format == 'FFMPEG' else 0,
                'gopsize': context.scene.render.ffmpeg.gopsize if context.scene.render.image_settings.file_format == 'FFMPEG' else 0,
            }

            # Save metadata JSON
            with open(temp_json_path, 'w') as f:
                json.dump(data, f, indent=4)

            # Apply burn-in and process
            pyppeteer_import()
            _META_MAP = [
                ("meta_file",        MList.FILE),
                ("meta_frame_range", MList.FRAME_RANGE),
                ("meta_scene",       MList.SCENE),
                ("meta_resolution",  MList.RESOLUTION),
                ("meta_fps",         MList.FPS),
                ("meta_camera",      MList.CAMERA),
                ("meta_lens",        MList.LENS),
                ("meta_marker",      MList.MARKER),
                ("meta_strip",       MList.STRIP),
                ("meta_user",        MList.USER),
                ("meta_hostname",    MList.HOSTNAME),
                ("meta_date",        MList.DATE),
                ("meta_memory",      MList.MEMORY),
                ("meta_render_time", MList.RENDER_TIME),
                ("meta_threads",     MList.THREADS),
                ("meta_comment",     MList.COMMENT),
                ("meta_icon",        MList.ICON),
            ]
            if prefs and prefs.burnin_enabled:
                metadatas = [m for pref_key, m in _META_MAP if getattr(prefs, pref_key, True)]
            else:
                metadatas = []

            # Build overlay options (use default HTML layout)
            overlay_opts = {}

            # show_icons applies to the default HTML layout
            if qs:
                overlay_opts["show_icons"] = getattr(qs, "overlay_show_icons", True)

            # TEMPORARILY DISABLED: Custom text mode (coming in future version)
            # Always use default HTML overlay mode
            # Default HTML mode: ensure COMMENT metadata is included when a comment is set
            if data.get("note") and MList.COMMENT not in metadatas:
                metadatas.append(MList.COMMENT)

            import shutil
            if prefs.burnin_enabled and (metadatas or (qs and qs.overlay_custom_enabled)):
                pb = Playblast(temp_video_path, temp_json_path, metadatas=metadatas,
                               options={"overlay": overlay_opts})
                rendered_video = pb.render(preview=False)
                if rendered_video.exists():
                    if final_path.exists():
                        final_path.unlink()
                    shutil.move(str(rendered_video), str(final_path))
            else:
                if final_path.exists():
                    final_path.unlink()
                shutil.move(str(temp_video_path), str(final_path))

            # Update Quick Settings with latest playblast name
            if hasattr(scene, 'bp_quick_settings'):
                scene.bp_quick_settings.last_playblast_name = final_path.name

            # Open video player in Blender's native video player
            if final_path.exists():
                scene.render.filepath = str(final_path)
                try:
                    bpy.ops.render.play_rendered_anim()
                except Exception:
                    self.report({'WARNING'}, "Could not open video player")

            # Restore render settings
            try:
                r = scene.render
                r.filepath                       = saved_settings['filepath']
                r.resolution_percentage          = saved_settings['resolution_percentage']
                scene.frame_start                = saved_settings['frame_start']
                scene.frame_end                  = saved_settings['frame_end']
                r.fps                            = saved_settings['fps']
                r.image_settings.file_format     = saved_settings['file_format']
                r.image_settings.color_mode      = saved_settings['color_mode']
                r.ffmpeg.format                  = saved_settings['ffmpeg_format']
                r.ffmpeg.codec                   = saved_settings['ffmpeg_codec']
                r.ffmpeg.audio_codec             = saved_settings['ffmpeg_audio_codec']
                r.ffmpeg.gopsize                 = saved_settings['ffmpeg_gopsize']
                r.ffmpeg.video_bitrate           = saved_settings['ffmpeg_video_bitrate']
                r.ffmpeg.maxrate                 = saved_settings['ffmpeg_maxrate']
                r.ffmpeg.minrate                 = saved_settings['ffmpeg_minrate']
                r.ffmpeg.use_max_b_frames        = saved_settings['ffmpeg_use_max_b_frames']
            except TypeError as e:
                self.report({'WARNING'}, f"Could not restore render settings: {str(e)}")

            # Restore viewport shading
            if 'shading_type' in saved_settings:
                for area in context.screen.areas:
                    if area.type == 'VIEW_3D':
                        for space in area.spaces:
                            if space.type == 'VIEW_3D':
                                space.shading.type = saved_settings['shading_type']
                                break

            self.run_post_script(context, final_path, comment=self.comment)
            self.report({'INFO'}, f"Playblast saved: {final_path.name}")

            # Reset comment for next playblast
            self.comment = ""

            return {'FINISHED'}

        except Exception as e:
            import traceback
            self.report({'ERROR'}, f"Playblast failed: {str(e)}")
            traceback.print_exc()
            return {'CANCELLED'}
