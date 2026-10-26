"""BetterPlayblast Main UI Panel"""

import os
import bpy
from . import pop_panel_decorator
from ..addon import packages_installed
from ..ops.install import BP_PackageInstaller
from ..ops.playblast import BP_OT_playblast
from ..playblast_utils import get_qs, find_latest_playblast_file, find_latest_version_number


class BP_MainPanel(bpy.types.Panel):
    bl_label = "Playblast"
    bl_idname = "PLAYBLAST_PT_BetterPlayblast"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'

    def draw(self, context: bpy.types.Context):
        layout = self.layout

        if not packages_installed():
            return self.draw_install(context, layout)

        qs = get_qs(context)

        # ─── Latest Playblast preview ─────────────────────────────────────────
        latest = find_latest_playblast_file(context)
        box = layout.box()
        box.scale_y = 0.65
        if latest and os.path.exists(latest):
            box.label(text=os.path.basename(latest), icon='FILE_MOVIE')
        else:
            box.label(text="No playblast yet", icon='FILE_MOVIE')

        layout.separator(factor=0.3)

        # ─── Main buttons ─────────────────────────────────────────────────────
        col = layout.column(align=True)
        col.scale_y = 1.5
        col.operator(BP_OT_playblast.bl_idname, text="Playblast")

        row_sub = col.row(align=True)
        row_sub.scale_y = 1.0
        row_sub.operator("bp.replay",      text="Replay",      icon='PLAY')
        row_sub.operator("bp.open_folder", text="Open Folder", icon='FILE_FOLDER')

        layout.separator(factor=0.4)

        # ─── Quick Settings toggle + Preferences button ───────────────────────
        row = layout.row(align=True)
        row.prop(qs, "qs_expanded", text="Quick Settings", icon='SETTINGS', toggle=True)
        row.operator("bp.open_preferences", text="", icon='PREFERENCES')

        if qs.qs_expanded:
            layout.separator(factor=0.2)
            self._draw_qs(layout, context, qs)

    # ─────────────────────────────────────────────────────────────────────────
    def _draw_qs(self, layout, context, qs):

        # 1. VERSION
        box = layout.box()
        row = box.row(align=True)
        row.prop(qs, "vs_expanded",
                 icon='TRIA_DOWN' if qs.vs_expanded else 'TRIA_RIGHT',
                 icon_only=True, emboss=False)
        row.label(text="Version", icon='LINENUMBERS_ON')

        if qs.vs_expanded:
            sub = box.column(align=True)
            sub.prop(qs, "version_enabled", text="Auto Increment", toggle=True)
            if qs.version_enabled:
                latest_ver = find_latest_version_number(context)
                sub.label(text=f"Next: v{latest_ver + 1:04d}", icon='AUTO')
            else:
                r = sub.row(align=True)
                r.operator("bp.version_dec", text="-")
                r.prop(qs, "version_number", text="")
                r.operator("bp.version_inc", text="+")

        # 2. SHADING
        box2 = layout.box()
        row2 = box2.row(align=True)
        row2.prop(qs, "res_expanded",
                  icon='TRIA_DOWN' if qs.res_expanded else 'TRIA_RIGHT',
                  icon_only=True, emboss=False)
        row2.prop(qs, "shading_override_enabled", text="")
        row2.label(text="Shading")

        if qs.res_expanded:
            sub2 = box2.column()
            sub2.enabled = qs.shading_override_enabled
            sh_row = sub2.row(align=True)
            for sh_id, sh_icon in [
                ('WIREFRAME', 'SHADING_WIRE'),
                ('SOLID',     'SHADING_SOLID'),
                ('MATERIAL',  'SHADING_TEXTURE'),
                ('RENDERED',  'SHADING_RENDERED'),
            ]:
                op = sh_row.operator("bp.set_shading", text="", icon=sh_icon,
                                     depress=(qs.viewport_shading == sh_id))
                op.shading = sh_id

        # 2.5. AUDIO
        box_audio = layout.box()
        row_audio = box_audio.row(align=True)
        row_audio.prop(qs, "au_expanded",
                       icon='TRIA_DOWN' if qs.au_expanded else 'TRIA_RIGHT',
                       icon_only=True, emboss=False)
        row_audio.prop(qs, "include_audio_enabled", text="")
        row_audio.label(text="Audio", icon='SOUND')

        if qs.au_expanded:
            sub_audio = box_audio.column()
            sub_audio.enabled = qs.include_audio_enabled
            sub_audio.prop(qs, "include_audio_codec", text="")

        # 3. SCENE OVERLAYS
        box3 = layout.box()
        row3 = box3.row(align=True)
        row3.prop(qs, "ro_expanded",
                  icon='TRIA_DOWN' if qs.ro_expanded else 'TRIA_RIGHT',
                  icon_only=True, emboss=False)
        row3.label(text="Scene Overlays")

        if qs.ro_expanded:
            sub3 = box3.column()
            sub3.prop(qs, "overlays_mode", text="")

        # 4. BURN-IN DATA
        box4 = layout.box()
        row4 = box4.row(align=True)
        row4.prop(qs, "bi_expanded",
                  icon='TRIA_DOWN' if qs.bi_expanded else 'TRIA_RIGHT',
                  icon_only=True, emboss=False)
        row4.label(text="Burn-In Data", icon='FONT_DATA')

        if qs.bi_expanded:
            sub4 = box4.column(align=False)

            # Preview toggle
            sub4.prop(qs, "overlay_preview_enabled", text="Preview in Viewport")

            sub4.separator(factor=0.3)

            # Show Icons toggle
            sub4.prop(qs, "overlay_show_icons", text="Show Icons", icon='HIDE_OFF' if qs.overlay_show_icons else 'HIDE_ON')


    def draw_install(self, context, layout):
        box = layout.box()
        row = box.row()
        row.alert = True
        col = row.column()
        col.scale_x = 5
        col.label(text="Missing packages!", icon='ERROR')
        col = row.column()
        col.operator("wm.url_open", text="?").url = "https://github.com/mael-peron/BetterPlayblast"
        row = box.row()
        row.operator(BP_PackageInstaller.bl_idname, text=BP_PackageInstaller.bl_label, icon='PACKAGE')


@pop_panel_decorator(BP_MainPanel.bl_idname, icon="logo_operator")
def pop_panel():
    pass


def register():
    bpy.types.VIEW3D_MT_editor_menus.append(pop_panel)


def unregister():
    bpy.types.VIEW3D_MT_editor_menus.remove(pop_panel)
