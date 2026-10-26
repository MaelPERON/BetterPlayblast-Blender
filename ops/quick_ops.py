"""Quick Settings Operators - Version management, Replay, Open Folder, Preferences, Import/Export"""

import os
import json
import bpy
from ..playblast_utils import get_qs, get_prefs, find_latest_playblast_file, resolve_output_folder, play_file


class BP_OT_set_shading(bpy.types.Operator):
    bl_idname = "bp.set_shading"
    bl_label = "Set Shading"
    bl_description = "Set viewport shading for the playblast"
    shading: bpy.props.StringProperty()

    def execute(self, context):
        get_qs(context).viewport_shading = self.shading
        return {'FINISHED'}


class BP_OT_version_increment(bpy.types.Operator):
    bl_idname = "bp.version_inc"
    bl_label = "+1"
    bl_description = "Increment version by 1"

    def execute(self, context):
        qs = get_qs(context)
        qs.version_number = min(9999, qs.version_number + 1)
        return {'FINISHED'}


class BP_OT_version_decrement(bpy.types.Operator):
    bl_idname = "bp.version_dec"
    bl_label = "-1"
    bl_description = "Decrement version by 1"

    def execute(self, context):
        qs = get_qs(context)
        qs.version_number = max(1, qs.version_number - 1)
        return {'FINISHED'}


class BP_OT_replay(bpy.types.Operator):
    bl_idname = "bp.replay"
    bl_label = "Replay"
    bl_description = "Play the latest playblast file"

    def execute(self, context):
        if not bpy.data.is_saved:
            self.report({'WARNING'}, "Please save your .blend file first")
            return {'CANCELLED'}

        path = find_latest_playblast_file(context)
        if not path or not os.path.exists(path):
            self.report({'WARNING'}, "No playblast file found")
            return {'CANCELLED'}

        ok = play_file(path)
        if not ok:
            self.report({'WARNING'}, f"Could not play: {path}")
        return {'FINISHED'}


class BP_OT_open_folder(bpy.types.Operator):
    bl_idname = "bp.open_folder"
    bl_label = "Open Folder"
    bl_description = "Open the playblast output folder"

    def execute(self, context):
        folder = resolve_output_folder(context)
        # Ensure folder exists
        os.makedirs(folder, exist_ok=True)
        
        try:
            # Try Blender's built-in path opener first (most reliable)
            bpy.ops.wm.path_open(filepath=folder)
        except Exception:
            # Fallback to system-specific methods
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(folder)
                else:  # macOS / Linux
                    import subprocess
                    import platform
                    if platform.system() == "Darwin":
                        subprocess.Popen(["open", folder])
                    else:
                        subprocess.Popen(["xdg-open", folder])
            except Exception as e:
                self.report({'ERROR'}, f"Could not open folder: {e}")
                return {'CANCELLED'}
        
        return {'FINISHED'}


class BP_OT_open_preferences(bpy.types.Operator):
    bl_idname = "bp.open_preferences"
    bl_label = "Preferences"
    bl_description = "Open addon preferences"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
        context.preferences.active_section = 'ADDONS'
        try:
            bpy.data.window_managers["WinMan"].addon_search = "Betterplayblast"
        except Exception:
            pass
        return {'FINISHED'}


_EXPORT_PROPS = [
    'output_folder_mode', 'project_subfolder_enabled', 'project_subfolder_name',
    'system_folder_path', 'playblast_name_mode', 'include_version_number',
    'custom_playblast_name', 'video_codec', 'video_bitrate',
    'use_viewport_shading', 'viewport_shading', 'resolution_percentage',
    'frame_rate', 'burnin_enabled', 'burnin_include_frame_number',
    'burnin_include_timecode', 'burnin_include_filename',
]


class BP_OT_export_settings(bpy.types.Operator):
    bl_idname = "bp.export_settings"
    bl_label = "Export Settings"
    bl_description = "Export addon settings to a JSON file"

    filepath: bpy.props.StringProperty(subtype='FILE_PATH')
    filter_glob: bpy.props.StringProperty(default="*.json", options={'HIDDEN'})
    filename: bpy.props.StringProperty(default="betterplayblast_settings.json")

    def invoke(self, context, event):
        self.filepath = "betterplayblast_settings.json"
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        prefs = get_prefs(context)
        if not prefs:
            self.report({'ERROR'}, "Addon preferences not found")
            return {'CANCELLED'}

        data = {k: getattr(prefs, k) for k in _EXPORT_PROPS if hasattr(prefs, k)}
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            self.report({'INFO'}, f"Settings exported to {os.path.basename(self.filepath)}")
        except Exception as e:
            self.report({'ERROR'}, f"Export failed: {e}")
            return {'CANCELLED'}
        return {'FINISHED'}


class BP_OT_import_settings(bpy.types.Operator):
    bl_idname = "bp.import_settings"
    bl_label = "Import Settings"
    bl_description = "Import addon settings from a JSON file"

    filepath: bpy.props.StringProperty(subtype='FILE_PATH')
    filter_glob: bpy.props.StringProperty(default="*.json", options={'HIDDEN'})

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        prefs = get_prefs(context)
        if not prefs:
            self.report({'ERROR'}, "Addon preferences not found")
            return {'CANCELLED'}

        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for key, val in data.items():
                if key in _EXPORT_PROPS and hasattr(prefs, key):
                    try:
                        setattr(prefs, key, val)
                    except Exception:
                        pass
            self.report({'INFO'}, "Settings imported successfully")
        except Exception as e:
            self.report({'ERROR'}, f"Import failed: {e}")
            return {'CANCELLED'}
        return {'FINISHED'}

