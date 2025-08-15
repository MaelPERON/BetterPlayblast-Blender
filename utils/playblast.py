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