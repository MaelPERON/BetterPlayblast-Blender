import bpy
import pickle
from pathlib import Path

def save_render_settings(context: bpy.types.Context, filepath: Path) -> dict[str, dict]:
	"""Save the current render settings to a file.

	Args:
		context (bpy.types.Context): The Blender context.
		filepath (Path): The path to the file where the settings will be saved.

	Returns:
		dict[str, dict]: The saved render settings.
	"""

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
	with open(filepath, "wb") as f: pickle.dump(render_settings, f) # Save .pkl file
	return render_settings

def override_render_settings(context: bpy.types.Context):
	"""Override the render settings for the playblast.

	Args:
		context (bpy.types.Context): The Blender context.
	"""
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

def restore_render_settings(context: bpy.types.Context, render_settings: dict[str, dict] = {}, pickle_file: Path = None):
	"""Restore the render settings from a saved file.

	Args:
		context (bpy.types.Context): The Blender context.
		render_settings (dict[str, dict]): The saved render settings.
		pickle_file (Path): The path to the saved settings file.
	"""
	if pickle_file and pickle_file.exists():
		with open(pickle_file, "rb") as f:
			render_settings = pickle.load(f)

	context.scene.render.filepath = render_settings.get('filepath', context.scene.render.filepath)
	context.scene.render.image_settings.file_format = render_settings['image_settings'].get('file_format', 'PNG')
	context.scene.render.image_settings.color_mode = render_settings['image_settings'].get('color_mode', 'RGBA')

	context.scene.render.ffmpeg.format = render_settings['ffmpeg'].get('format', 'MPEG4')
	context.scene.render.ffmpeg.codec = render_settings['ffmpeg'].get('codec', 'H264')
	context.scene.render.ffmpeg.gopsize = render_settings['ffmpeg'].get('gopsize', 15)
	context.scene.render.ffmpeg.use_max_b_frames = render_settings['ffmpeg'].get('use_max_b_frames', False)
	context.scene.render.ffmpeg.video_bitrate = render_settings['ffmpeg'].get('video_bitrate', 6000)
	context.scene.render.ffmpeg.maxrate = render_settings['ffmpeg'].get('maxrate', 9000)
	context.scene.render.ffmpeg.minrate = render_settings['ffmpeg'].get('minrate', 0)
	context.scene.render.ffmpeg.buffersize = render_settings['ffmpeg'].get('buffersize', 224 * 8)
	context.scene.render.ffmpeg.packetsize = render_settings['ffmpeg'].get('packetsize', 2048)
	context.scene.render.ffmpeg.muxrate = render_settings['ffmpeg'].get('muxrate', 10080000)