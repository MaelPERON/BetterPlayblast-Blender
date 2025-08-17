from re import sub
import bpy
import os
from pathlib import Path

class BP_Preferences(bpy.types.AddonPreferences):
	bl_idname = __package__ or "BetterPlayblast-Blender"
	
	# PLAYBLAST SETTINGS
	pb_folder: bpy.props.EnumProperty( # type: ignore
		name="Playblast Folder",
		description="Choose the folder for playblasts",
		items=[
			("RELATIVE", "Relative Folder", "Relative to the .blend file"),
			("CUSTOM", "Custom Folder", "Select a location"),
			("RENDER", "Same as Output Path", "Same Folder as the Output Path under Render Settings")
		],
		default="RENDER"
	)

	pb_folder_relative: bpy.props.StringProperty( # type: ignore
		name="Relative Folder",
		description="Set a relative folder for playblasts",
		default="./Playblast/"
	)

	pb_folder_render: bpy.props.StringProperty( # type: ignore
		name="Render Folder",
		description="Set the render folder for playblasts",
		default=""
	)

	pb_folder_custom: bpy.props.StringProperty( # type: ignore
		name="Custom Folder",
		description="Set a custom folder for playblasts",
		default="",
		subtype='DIR_PATH'
	)

	pb_filename: bpy.props.EnumProperty( # type: ignore
		name="Playblast Filename",
		description="Choose the filename for playblasts",
		items=[
			("FILE_NAME", "Blender Filename", "Use the Blender filename"),
			("CUSTOM", "Custom", "Use a custom filename"),
			("RENDER", "Same as Output Path", "Use the same name as the output file")
		],
		default="RENDER"
	)

	pb_filename_blender: bpy.props.StringProperty( # type: ignore
		name="Blender Filename",
		description="Blender filename",
		default=""
	)

	pb_filename_render: bpy.props.StringProperty( # type: ignore
		name="Render Filename",
		description="Set the render filename for playblasts",
		default=""
	)

	pb_filename_custom: bpy.props.StringProperty( # type: ignore
		name="Custom Filename",
		description="Set a custom filename for playblasts",
		default=""
	)

	def draw(self, context: bpy.types.Context):
		layout = self.layout

		box = layout.box()
		box.label(text="Playblast Settings", icon="TOOL_SETTINGS")
		box.separator()

		# Playblast Folder
		col = box.column(align=True)
		row = col.row(align=True)
		row.prop(self, "pb_folder")
		sub_row = row.row(align=True)
		sub_row.enabled = self.pb_folder != "RENDER"
		match self.pb_folder:
			case "RELATIVE":
				sub_row.prop(self, "pb_folder_relative", text="")
			case "RENDER":
				self.pb_folder_render = str(filepath) if (filepath := Path(context.scene.render.filepath).parent).exists() else ""
				sub_row.prop(self, "pb_folder_render", text="")
			case "CUSTOM":
				sub_row.prop(self, "pb_folder_custom", text="")

		# Playblast Filename
		col = box.column(align=True)
		row = col.row(align=True)
		row.prop(self, "pb_filename")

		sub_row = row.row(align=True)
		sub_row.enabled = self.pb_filename == "CUSTOM"

		self.pb_filename_blender = bpy.path.basename(bpy.data.filepath) or "playblast"
		self.pb_filename_render = bpy.path.basename(context.scene.render.filepath) or "playblast"
		match self.pb_filename:
			case "FILE_NAME":
				sub_row.prop(self, "pb_filename_blender", text="")
			case "RENDER":
				sub_row.prop(self, "pb_filename_render", text="")
			case "CUSTOM":
				row.prop(self, "pb_filename_custom", text="")