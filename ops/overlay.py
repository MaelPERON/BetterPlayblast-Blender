"""BetterPlayblast Overlay Preview & Management Operators"""

import bpy
from ..overlay_config import QUICK_TEMPLATES, OVERLAY_POSITIONS, get_placeholder_help


def _get_prefs():
    addon_id = __package__.rsplit('.', 1)[0] if __package__ else ""
    addon = bpy.context.preferences.addons.get(addon_id)
    return addon.preferences if addon else None


class BP_OT_overlay_preview_viewport(bpy.types.Operator):
    """Toggle overlay preview in viewport"""
    bl_idname = "bp.overlay_preview_viewport"
    bl_label = "Preview Overlay in Viewport"
    bl_description = "Show/hide overlay preview in 3D viewport camera view"

    _timer = None

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        qs = context.scene.bp_quick_settings
        qs.overlay_preview_enabled = not qs.overlay_preview_enabled

        if qs.overlay_preview_enabled:
            self.report({'INFO'}, "Overlay preview enabled")
            # Start timer for viewport updates
            wm = context.window_manager
            self._timer = wm.event_timer_add(0.5, window=context.window)
            wm.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'INFO'}, "Overlay preview disabled")
            return {'FINISHED'}

    def modal(self, context, event):
        qs = context.scene.bp_quick_settings

        if event.type == 'TIMER':
            # Redraw viewport when timer triggers
            for area in context.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()

        if not qs.overlay_preview_enabled:
            # Stop timer when disabled
            wm = context.window_manager
            if self._timer:
                wm.event_timer_remove(self._timer)
            return {'FINISHED'}

        return {'RUNNING_MODAL'}


class BP_OT_overlay_apply_template(bpy.types.Operator):
    """Apply a quick overlay template"""
    bl_idname = "bp.overlay_apply_template"
    bl_label = "Apply Template"
    bl_description = "Apply a quick template to overlay positions"

    template_name: bpy.props.StringProperty(
        name="Template",
        default="standard"
    )

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        prefs = _get_prefs()

        if self.template_name not in QUICK_TEMPLATES:
            self.report({'ERROR'}, f"Unknown template: {self.template_name}")
            return {'CANCELLED'}

        template = QUICK_TEMPLATES[self.template_name]

        # Apply template to overlay positions (in prefs = source of truth)
        if prefs:
            prefs.overlay_top_left    = template.get("top_left", "")
            prefs.overlay_top_center  = template.get("top_center", "")
            prefs.overlay_top_right   = template.get("top_right", "")
            prefs.overlay_bottom_left  = template.get("bottom_left", "")
            prefs.overlay_bottom_center= template.get("bottom_center", "")
            prefs.overlay_bottom_right = template.get("bottom_right", "")

        self.report({'INFO'}, f"Applied template: {self.template_name}")
        return {'FINISHED'}


class BP_OT_overlay_reset_to_default(bpy.types.Operator):
    """Reset overlay to default configuration"""
    bl_idname = "bp.overlay_reset_to_default"
    bl_label = "Reset to Default"
    bl_description = "Reset overlay to default settings"

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        prefs = _get_prefs()

        # Apply standard template as default (in prefs = source of truth)
        template = QUICK_TEMPLATES["standard"]
        if prefs:
            prefs.overlay_top_left     = template.get("top_left", "")
            prefs.overlay_top_center   = template.get("top_center", "")
            prefs.overlay_top_right    = template.get("top_right", "")
            prefs.overlay_bottom_left  = template.get("bottom_left", "")
            prefs.overlay_bottom_center= template.get("bottom_center", "")
            prefs.overlay_bottom_right = template.get("bottom_right", "")
            prefs.overlay_opacity      = 0.75
            prefs.overlay_text_color   = (1.0, 1.0, 1.0)
            prefs.overlay_bg_color     = (0.0, 0.0, 0.0)
            prefs.overlay_font_size    = 24

        self.report({'INFO'}, "Overlay reset to default")
        return {'FINISHED'}


class BP_OT_overlay_show_help(bpy.types.Operator):
    """Show available placeholders for overlay text"""
    bl_idname = "bp.overlay_show_help"
    bl_label = "Overlay Placeholder Help"
    bl_description = "Display list of available placeholders for overlay text"

    def execute(self, context):
        help_text = get_placeholder_help()
        print(help_text)
        self.report({'INFO'}, "See console for placeholder list")
        return {'FINISHED'}

    def invoke(self, context, event):
        # Open a popup dialog
        return context.window_manager.invoke_props_dialog(self, width=600)

    def draw(self, context):
        layout = self.layout
        help_text = get_placeholder_help()

        # Display in a scrollable text area (simulate with labels)
        lines = help_text.split('\n')
        for line in lines[:20]:  # Show first 20 lines
            layout.label(text=line)

        if len(lines) > 20:
            layout.label(text="... (see console for full list)")


class BP_OT_overlay_copy_placeholder(bpy.types.Operator):
    """Copy a placeholder to clipboard"""
    bl_idname = "bp.overlay_copy_placeholder"
    bl_label = "Copy Placeholder"

    placeholder: bpy.props.StringProperty(
        name="Placeholder",
        default=""
    )

    def execute(self, context):
        import bpy
        context.window_manager.clipboard = self.placeholder
        self.report({'INFO'}, f"Copied: {self.placeholder}")
        return {'FINISHED'}
