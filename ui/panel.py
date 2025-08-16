import bpy

from . import pop_panel_decorator
from ..addon import packages_installed
from ..icons import get_icon
from ..ops.install import InstallMissingPackages
from ..ops.playblast import BP_Playblast

class BP_MainPanel(bpy.types.Panel):
    bl_label = "Better Playblast"
    bl_idname = "PLAYBLAST_PT_BetterPlayblast"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'

    def draw(self, context: bpy.types.Context):
        layout = self.layout
        if not packages_installed():
            return self.draw_install(context, layout)
        
        layout.label(text="Ready to use!", icon='FAKE_USER_ON')
        row = layout.row()
        row.operator(BP_Playblast.bl_idname, text=BP_Playblast.bl_label, icon_value=get_icon("logo_operator"))

    def draw_install(self, context: bpy.types.Context, layout: bpy.types.UILayout):
        box = layout.box()
        row = box.row()
        row.alert = True
        col = row.column()
        col.scale_x = 5
        col.label(text="Missing packages!", icon='ERROR')
        col = row.column()
        col.operator("wm.url_open", text="?").url = "https://example.com/docs" # TODO : replace with actual documentation
        row = box.row()
        row.operator(InstallMissingPackages.bl_idname, text=InstallMissingPackages.bl_label, icon='PACKAGE')

@pop_panel_decorator(BP_MainPanel.bl_idname, icon="logo")
def pop_panel(): pass


def register():
    bpy.types.VIEW3D_MT_editor_menus.append(pop_panel)

def unregister():
    bpy.types.VIEW3D_MT_editor_menus.remove(pop_panel)