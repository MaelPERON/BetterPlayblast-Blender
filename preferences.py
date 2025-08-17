import bpy
import os

class BP_Preferences(bpy.types.AddonPreferences):
	bl_idname = __package__ or "BetterPlayblast-Blender"
	def draw(self, context):
		layout = self.layout

		box = layout.box()
		box.label(text="Playblast Settings", icon="TOOL_SETTINGS")
		box.separator()
