import bpy
import os
from pathlib import Path
from ..utils.playblast import *
from ..BetterPlayblast.install import all_installed

Playblast = None
if all_installed(refresh=True,save_cache=False):
	from ..BetterPlayblast.playblast import Playblast


class BP_Playblast(bpy.types.Operator):
	bl_idname = "bl.playblast"
	bl_label = "Better Playblast"
	bl_description = "Create a playblast with Better Playblast"
	bl_options = {'REGISTER'}

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
		og_filepath = Path(render_settings.get('filepath', 'playblast.mp4'))
		video_filepath = temp_folder / f"{og_filepath.stem}.mp4"
		json_filepath = temp_folder / f"{og_filepath.stem}.json"

		# Overriding render settings
		context.scene.render.filepath = str(video_filepath)
		override_render_settings(context)

		return {'FINISHED'}