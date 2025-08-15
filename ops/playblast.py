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

		# H264 in mp4
		og_filepath = Path(render_settings.get('filepath', 'playblast.mp4'))
		video_filepath = temp_folder / f"{og_filepath.stem}.mp4"
		json_filepath = temp_folder / f"{og_filepath.stem}.json"

		# Overriding render settings
		context.scene.render.filepath = str(video_filepath)
		is_ntsc = (context.scene.render.fps != 25)

		context.scene.render.image_settings.file_format = "FFMPEG"
		context.scene.render.image_settings.color_mode = "RGB"
		context.scene.render.ffmpeg.format = "MPEG4"
		context.scene.render.ffmpeg.codec = "H264"

		if is_ntsc:
			context.scene.render.ffmpeg.gopsize = 18
		else:
			context.scene.render.ffmpeg.gopsize = 15
		context.scene.render.ffmpeg.use_max_b_frames = False

		context.scene.render.ffmpeg.video_bitrate = 6000
		context.scene.render.ffmpeg.maxrate = 9000
		context.scene.render.ffmpeg.minrate = 0
		context.scene.render.ffmpeg.buffersize = 224 * 8
		context.scene.render.ffmpeg.packetsize = 2048
		context.scene.render.ffmpeg.muxrate = 10080000

		return {'FINISHED'}