"""BetterPlayblast Overlay UI Panel Components"""

import bpy
from ..overlay_config import QUICK_TEMPLATES, OVERLAY_POSITIONS


def _get_prefs(context):
    addon_id = __package__.rsplit('.', 1)[0] if __package__ else ""
    addon = context.preferences.addons.get(addon_id)
    return addon.preferences if addon else None


class BP_PT_overlay_customization(bpy.types.Panel):
    """Panel for overlay customization settings"""
    bl_label = "Overlay Customization"
    bl_idname = "PLAYBLAST_PT_overlay_customization"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="Overlay Customization", icon='OVERLAY')

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        qs = context.scene.bp_quick_settings
        prefs = _get_prefs(context)

        # ───────────────────────────────────────────────────────────────────────
        # VIEWPORT PREVIEW
        # ───────────────────────────────────────────────────────────────────────
        col = layout.column(align=True)
        row = col.row()
        row.prop(qs, "overlay_preview_enabled", text="Preview in Viewport")
        row.operator("bp.overlay_preview_viewport", text="Toggle", icon='PLAY')

        layout.separator(factor=0.5)

        # ───────────────────────────────────────────────────────────────────────
        # CUSTOM LAYOUT TOGGLE
        # ───────────────────────────────────────────────────────────────────────
        layout.prop(qs, "overlay_custom_enabled", text="Enable Custom Layout")

        if not qs.overlay_custom_enabled:
            layout.label(text="Default metadata overlay active", icon='INFO')
            return

        if not prefs:
            layout.label(text="Preferences unavailable", icon='ERROR')
            return

        layout.separator(factor=0.3)

        # ───────────────────────────────────────────────────────────────────────
        # TEMPLATE SELECTOR & QUICK BUTTONS
        # ───────────────────────────────────────────────────────────────────────
        box = layout.box()
        box.label(text="Quick Templates", icon='PRESET')

        row = box.row(align=True)
        row.scale_y = 1.2
        for template_name in ["minimal", "standard", "production"]:
            op = row.operator("bp.overlay_apply_template",
                            text=template_name.replace('_', ' ').title())
            op.template_name = template_name

        row = box.row(align=True)
        op = row.operator("bp.overlay_apply_template", text="Tech Specs")
        op.template_name = "tech_specs"
        op = row.operator("bp.overlay_apply_template", text="Bottom Only")
        op.template_name = "minimal_bottom"

        box.operator("bp.overlay_reset_to_default", icon='LOOP_BACK')

        layout.separator(factor=0.5)

        # ───────────────────────────────────────────────────────────────────────
        # CUSTOM POSITIONS EDITOR
        # ───────────────────────────────────────────────────────────────────────
        box = layout.box()
        box.label(text="Custom Text by Position", icon='WORKSPACE')

        # TOP ROW
        row = box.row(align=True)
        row.label(text="TOP", icon='SORT_ASC')
        row = box.row(align=False)
        row.scale_x = 0.33
        row.column().prop(prefs, "overlay_top_left", text="Left", icon='ALIGN_LEFT')
        row.column().prop(prefs, "overlay_top_center", text="Center", icon='ALIGN_CENTER')
        row.column().prop(prefs, "overlay_top_right", text="Right", icon='ALIGN_RIGHT')

        # BOTTOM ROW
        row = box.row(align=True)
        row.label(text="BOTTOM", icon='SORT_DESC')
        row = box.row(align=False)
        row.scale_x = 0.33
        row.column().prop(prefs, "overlay_bottom_left", text="Left", icon='ALIGN_LEFT')
        row.column().prop(prefs, "overlay_bottom_center", text="Center", icon='ALIGN_CENTER')
        row.column().prop(prefs, "overlay_bottom_right", text="Right", icon='ALIGN_RIGHT')

        layout.separator(factor=0.5)

        # ───────────────────────────────────────────────────────────────────────
        # APPEARANCE SETTINGS
        # ───────────────────────────────────────────────────────────────────────
        box = layout.box()
        box.label(text="Appearance", icon='SHADING')

        row = box.row()
        row.prop(prefs, "overlay_opacity")
        row.prop(prefs, "overlay_font_size", slider=True)

        box.prop(prefs, "overlay_text_color", text="Text")
        box.prop(prefs, "overlay_bg_color", text="Background")

        layout.separator(factor=0.5)

        # ───────────────────────────────────────────────────────────────────────
        # PLACEHOLDER HELP
        # ───────────────────────────────────────────────────────────────────────
        box = layout.box()
        row = box.row()
        row.label(text="Available Placeholders", icon='HELP')
        row.operator("bp.overlay_show_help", text="Help", icon='QUESTION')

        # Show common placeholders as quick reference
        col = box.column(align=True)
        col.scale_y = 0.8
        common_placeholders = [
            "{file_name}", "{file_version}",
            "{datetime}", "{date}",
            "{camera_name}", "{camera_focal}",
            "{width}x{height}", "{fps}",
            "{frame_current}/{frame_total}",
            "{user}", "{hostname}",
        ]

        for placeholder in common_placeholders:
            row = col.row(align=True)
            row.label(text=placeholder, icon='COPY_ID')
            op = row.operator("bp.overlay_copy_placeholder", text="Copy", icon='DUPLICATE')
            op.placeholder = placeholder


def draw_overlay_panel_in_properties(self, context):
    """Draw overlay customization in properties panel if needed"""
    layout = self.layout
    qs = context.scene.bp_quick_settings

    if not qs.overlay_custom_enabled:
        return

    box = layout.box()
    box.label(text="Overlay Settings", icon='OVERLAY')
    row = box.row()
    row.prop(qs, "overlay_preview_enabled")
    row.operator("bp.overlay_preview_viewport", text="", icon='PLAY')
