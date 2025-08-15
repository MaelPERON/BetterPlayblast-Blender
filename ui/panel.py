import bpy

from . import pop_panel_decorator

class BP_MainPanel(bpy.types.Panel):
    bl_label = "Better Playblast"
    bl_idname = "PLAYBLAST_PT_BetterPlayblast"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'

    def draw(self, context):
        layout = self.layout

@pop_panel_decorator(BP_MainPanel.bl_idname, icon="logo")
def pop_panel(): pass


def register():
    bpy.types.VIEW3D_MT_editor_menus.append(pop_panel)

def unregister():
    bpy.types.VIEW3D_MT_editor_menus.remove(pop_panel)