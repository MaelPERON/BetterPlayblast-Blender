from re import sub
import bpy
import os
from pathlib import Path

from .ui import spawn_error, spawn_warning
from .utils.sanity_checks import *

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

	pb_folder_force: bpy.props.BoolProperty( # type: ignore
		name="Force Playblast Folder Creation",
		description="When folder doesn't exist, create it.\nWarning: This may create unwanted folders.",
		default=False
	)

	pb_filename: bpy.props.EnumProperty( # type: ignore
		name="Playblast Filename",
		description="Choose the filename for playblasts",
		items=[
			("FILE_NAME", "Blender Filename", "Use the Blender filename"),
			("CUSTOM", "Custom Filename", "Use a custom filename"),
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

	pb_path_preview: bpy.props.StringProperty( # type: ignore
		name="Playblast Path Preview",
		description="Preview of the playblast output path",
		default=""
	)

	def draw(self, context: bpy.types.Context):
		layout = self.layout
		# Pre-checks
		saved = sanity_file_saved.check(bpy.data.filepath)
		scene = bpy.context.scene
		render = scene.render

		
		# region PLAYBLAST SETTINGS
		box = layout.box()
		box.label(text="Playblast Settings", icon="TOOL_SETTINGS")
		box.separator()


		# region PLAYBLAST FOLDER
		col = box.column(align=True)
		row = col.row().split(align=True, factor=0.6)
		row.prop(self, "pb_folder")
		sub_row = row.row(align=True)
		sub_row.enabled = self.pb_folder != "RENDER"
		match self.pb_folder:
			case "RELATIVE":
				sub_row.prop(self, "pb_folder_relative", text="")
				filepath = bpy.data.filepath

			case "RENDER":
				filepath = Path(context.scene.render.filepath)
				self.pb_folder_render = str(filepath) if filepath.parent.exists() else ""
				sub_row.prop(self, "pb_folder_render", text="")
			case "CUSTOM":
				sub_row.prop(self, "pb_folder_custom", text="")

		folder = self.get_folder()
		if not saved:
			spawn_error(col, "Blend file not saved")
		elif folder is None:
			spawn_error(col, "Folder path is empty")
		
		# endregion

		# region PLAYBLAST FILENAME
		col = box.column(align=True)
		row = col.row().split(align=True, factor=0.6)
		row.prop(self, "pb_filename")

		sub_row = row.row(align=True)
		sub_row.enabled = self.pb_filename == "CUSTOM"

		self.pb_filename_blender = bpy.path.basename(bpy.data.filepath)
		self.pb_filename_render = bpy.path.basename(context.scene.render.filepath)
		match self.pb_filename:
			case "FILE_NAME":
				sub_row.prop(self, "pb_filename_blender", text="")
			case "RENDER":
				sub_row.prop(self, "pb_filename_render", text="")
			case "CUSTOM":
				sub_row.prop(self, "pb_filename_custom", text="")

		filename = self.get_filename()
		if not saved:
			spawn_error(col, "Blend file not saved")
		elif filename is None:
			spawn_error(col, "Filename is empty")
		else:
			valid, msg = sanity_file_stem.check_and_report(filename)
			if not valid:
				spawn_error(col, msg)

		# endregion

		# region FILE OUTPUT PATH
		if self.pb_folder == "RENDER" or self.pb_filename == "RENDER":
			scene = bpy.context.scene
			col.separator()
			row = col.row(align=True).split(factor=0.2)
			row.label(text="Render Output Path:")
			row.prop(scene.render, "filepath", text="")

		# endregion

		# region PLAYBLAST FOLDER FORCE
		col = box.column(align=True)
		row = col.row().split(align=True, factor=0.6)
		row.prop(self, "pb_folder_force")
		if not folder:
			row.enabled = False

		# endregion

		# region PLAYBLAST PATH PREVIEW
		preview_path = self.get_path()
		if preview_path:
			col.separator_spacer()
			row = col.row(align=True)
			row.emboss = "NONE"
			self.pb_path_preview = str(preview_path.resolve())
			row.prop(self, "pb_path_preview", text="Playblast Destination Preview", icon="FOLDER_REDIRECT")

		# endregion

		# endregion PLAYBLAST SETTINGS

		# region VIDEO SETTINGS
		box = layout.box()
		box.label(text="Video Settings", icon="FILE_MOVIE")
		spawn_warning(box, "Video Codec not supported for the moment. Default to .MPEG-4")
		box.separator()
		col = box.column(align=True)

		# region VIDEO / AUDIO Codecs
		video = col.row(align=True)
		video.enabled = False
		video.prop(render.ffmpeg, "format", text="Video Format")
		sub_row = video.row(align=True)
		sub_row.alert = True
		
		col.prop(render.ffmpeg, "audio_codec", text="Audio Codec")

		# endregion

		# region ADVANCED
		col.separator()
		advanced = col.row().split()
		# region VIDEO
		video = advanced.column(align=True)
		video.label(text="Video Settings")
		video.separator()
		video.prop(render.ffmpeg, "gopsize", text="GOP Size")
		video.prop(render.ffmpeg, "video_bitrate", text="Video Bitrate")
		video.prop(render.ffmpeg, "maxrate", text="Max Rate")
		video.prop(render.ffmpeg, "minrate", text="Min Rate")
		video.prop(render.ffmpeg, "buffersize", text="Buffer Size")
		video.prop(render.ffmpeg, "packetsize", text="Packet Size")
		video.prop(render.ffmpeg, "muxrate", text="Mux Rate")
		# endregion
		# region AUDIO
		if ffmpeg.audio_codec != "NONE":
			audio = advanced.column(align=True)
			audio.label(text="Audio Settings")
			audio.separator()

			if ffmpeg.audio_codec != 'NONE':
				audio.prop(ffmpeg, "audio_channels")
				audio.prop(ffmpeg, "audio_mixrate", text="Sample Rate")
				audio.prop(ffmpeg, "audio_bitrate")
				audio.prop(ffmpeg, "audio_volume", slider=True)
		# endregion
		# endregion ADVANCED

		# endregion VIDEO SETTINGS

	def get_filename(self) -> str | None:
		match self.pb_filename:
			case "FILE_NAME":
				filepath = bpy.data.filepath
				return bpy.path.basename(filepath) if filepath else None
			case "RENDER":
				scene = bpy.context.scene
				return bpy.path.basename(scene.render.filepath) or None
			case "CUSTOM":
				return self.pb_filename_custom
			case _:
				return None
			
	def get_folder(self) -> str | None:
		match self.pb_folder:
			case "RELATIVE":
				filepath = bpy.data.filepath or None
				if not filepath: return None
				return Path(filepath).parent / self.pb_folder_relative
			case "RENDER":
				scene = bpy.context.scene
				filepath = scene.render.filepath or None
				if not filepath: return None
				return str(Path(filepath).parent)
			case "CUSTOM":
				return self.pb_folder_custom
			case _:
				return None
			
	def get_path(self) -> Path | None:
		folder = self.get_folder()
		filename = self.get_filename()
		if not folder or not filename:
			return None
		return Path(folder) / filename
