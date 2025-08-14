import bpy
class BP_MainPanel(bpy.types.Panel):
    bl_label = "Better Playblast"
    bl_idname = "PLAYBLAST_PT_BetterPlayblast"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'

    def draw(self, context):
        layout = self.layout

def pop_menu(self: bpy.types.Menu, context: bpy.types.Context):
    layout = self.layout
    if context.area.show_menus:
        layout.popover(BP_MainPanel.bl_idname, text="Better Playblast")
