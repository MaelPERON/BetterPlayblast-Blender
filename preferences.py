import bpy
import os

class BP_Preferences(bpy.types.AddonPreferences):
	bl_idname = __package__ or "BetterPlayblast-Blender"
	
	# PLAYBLAST SETTINGS
	pb_folder: bpy.props.EnumProperty( # type: ignore
		name="Playblast Folder",
		description="Choose the folder for playblasts",
		items=[
			("RELATIVE", "Relative Folder", "Relative to the .blend file"),
			("CUSTOM", "Custom Folder", "Select a location"),
			("SAME", "Output Path", "Same Folder as the Output Path under Render Settings")
		],
		default="RELATIVE"
	)

	pb_folder_relative: bpy.props.StringProperty( # type: ignore
		name="Relative Folder",
		description="Set a relative folder for playblasts",
		default="./Playblast/"
	)
	pb_folder_custom: bpy.props.StringProperty( # type: ignore
		name="Custom Folder",
		description="Set a custom folder for playblasts",
		default="",
		subtype='DIR_PATH'
	)

	def draw(self, context):
		layout = self.layout

		box = layout.box()
		box.label(text="Playblast Settings", icon="TOOL_SETTINGS")
		box.separator()

		# Playblast Folder
		col = box.column(align=True)
		row = col.row(align=True)
		row.prop(self, "pb_folder")
		match self.pb_folder:
			case "RELATIVE":
				row.prop(self, "pb_folder_relative", text="")
			case "CUSTOM":
				row.prop(self, "pb_folder_custom", text="")
