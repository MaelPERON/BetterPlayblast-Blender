import bpy
import os
import json
from pathlib import Path
from functools import partial
from ..utils.render_settings import *
from ..utils.capture_data import *
from ..utils.time import get_now
from ..utils.handlers import remove_function_from_handler
from ..BetterPlayblast.install import all_installed
from ..BetterPlayblast.metadata import MetadataList as MList

Playblast = None
if all_installed(refresh=True,save_cache=False):
	from ..BetterPlayblast.playblast import Playblast


class BP_Playblast(bpy.types.Operator):
	bl_idname = "bl.playblast"
	bl_label = "Better Playblast"
	bl_description = "Create a playblast with Better Playblast"
	bl_options = {'REGISTER'}

	preview_process: bpy.props.BoolProperty(name="Preview Process", description="Display the video overlay preview when building it.", default=False) # type: ignore

	@classmethod
	def poll(cls, context: bpy.types.Context):
		return Playblast is not None

	def execute(self, context: bpy.types.Context):
		if Playblast is None:
			self.report({'ERROR'}, "Better Playblast is not installed or not available.")
			return {'CANCELLED'}

		# Configure path local_app_data
		local_app_data = Path(os.getenv('LOCALAPPDATA', '')) # not compatible with non-Windows OS
		if not local_app_data.exists():
			self.report({'ERROR'}, "Local App Data path does not exist.")
			return {'CANCELLED'}

		temp_folder = local_app_data / "BetterPlayblast" / "temp"
		if not temp_folder.exists():
			temp_folder.mkdir(parents=True, exist_ok=True)

		# Save all current render settings
		settings_path = temp_folder / "render_settings.pkl"
		render_settings = save_render_settings(context, settings_path)

		# H264 in mp4
		og_filepath = Path(render_settings.get('filepath', 'C:/tmp/playblast.mp4'))
		video_filepath = temp_folder / f"{og_filepath.stem}.mp4"
		json_filepath = temp_folder / f"{og_filepath.stem}.json"

		# Overriding render settings
		context.scene.render.filepath = str(video_filepath)
		override_render_settings(context)

		# Capturing the data
		## Initial data capture
		data = data_init_capture(context)
		## Frame dependent capture
		handler = bpy.app.handlers.frame_change_post
		remove_function_from_handler(data_frame_capture, handler)
		handler.append(partial(data_frame_capture, data, get_now()))

		# Write video file
		bpy.ops.render.opengl(animation=True)
		remove_function_from_handler(data_frame_capture, handler)
		# Write JSON file
		with open(json_filepath, 'w') as f:
			json.dump(data, f, indent=4)

		# Restoring render settings
		restore_render_settings(context, render_settings=render_settings)

		pb = Playblast(video_filepath, json_filepath, metadatas=[MList.DATE, MList.FILE])
		rendered_video = pb.render(preview=self.preview_process)

		og_filepath.parent.mkdir(parents=True, exist_ok=True)
		if og_filepath.exists():
			og_filepath.unlink()
		rendered_video.replace(og_filepath)

		return {'FINISHED'}