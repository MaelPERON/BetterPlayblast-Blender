import bpy
import os
import pickle
from pathlib import Path
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
		render_settings = {
			'filepath': context.scene.render.filepath,
			'image_settings': {
				'file_format': context.scene.render.image_settings.file_format,
				'color_mode': context.scene.render.image_settings.color_mode,
			},
			'ffmpeg': {
				'format': context.scene.render.ffmpeg.format,
				'codec': context.scene.render.ffmpeg.codec,
				'gopsize': context.scene.render.ffmpeg.gopsize,
				'use_max_b_frames': context.scene.render.ffmpeg.use_max_b_frames,
				'video_bitrate': context.scene.render.ffmpeg.video_bitrate,
				'maxrate': context.scene.render.ffmpeg.maxrate,
				'minrate': context.scene.render.ffmpeg.minrate,
				'buffersize': context.scene.render.ffmpeg.buffersize,
				'packetsize': context.scene.render.ffmpeg.packetsize,
				'muxrate': context.scene.render.ffmpeg.muxrate,
			}
		}
		with open(settings_path, "wb") as f: pickle.dump(render_settings, f) # Save .pkl file
		return {'FINISHED'}