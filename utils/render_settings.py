import bpy
import pickle
from pathlib import Path


def save_render_settings(context: bpy.types.Context,
                         filepath: Path) -> dict[str, dict]:
    """Save the current render settings to a file.

    Args:
            context (bpy.types.Context): The Blender context.
            filepath (Path): The path to the file where settings are saved.

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
            'use_max_b_frames': (
                context.scene.render.ffmpeg.use_max_b_frames
            ),
            'video_bitrate': context.scene.render.ffmpeg.video_bitrate,
            'maxrate': context.scene.render.ffmpeg.maxrate,
            'minrate': context.scene.render.ffmpeg.minrate,
            'buffersize': context.scene.render.ffmpeg.buffersize,
            'packetsize': context.scene.render.ffmpeg.packetsize,
            'muxrate': context.scene.render.ffmpeg.muxrate,
        }
    }
    with open(filepath, "wb") as f:
        pickle.dump(render_settings, f)  # Save .pkl file
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


def restore_render_settings(context: bpy.types.Context,
                            render_settings: dict[str,
                                                  dict] | None = None,
                            pickle_file: Path = None):
    """Restore the render settings from a saved file.

    Args:
            context (bpy.types.Context): The Blender context.
            render_settings (dict[str, dict]): The saved render settings.
            pickle_file (Path): The path to the saved settings file.
    """
    if render_settings is None:
        render_settings = {}

    if pickle_file and pickle_file.exists():
        with open(pickle_file, "rb") as f:
            render_settings = pickle.load(f)

    context.scene.render.filepath = render_settings.get(
        'filepath', context.scene.render.filepath)
    image_settings = render_settings.get('image_settings', {})
    ffmpeg_settings = render_settings.get('ffmpeg', {})

    context.scene.render.image_settings.file_format = image_settings.get(
        'file_format', 'PNG'
    )
    context.scene.render.image_settings.color_mode = image_settings.get(
        'color_mode', 'RGBA'
    )

    context.scene.render.ffmpeg.format = ffmpeg_settings.get(
        'format', 'MPEG4')
    context.scene.render.ffmpeg.codec = ffmpeg_settings.get(
        'codec', 'H264')
    context.scene.render.ffmpeg.gopsize = ffmpeg_settings.get(
        'gopsize', 15)
    context.scene.render.ffmpeg.use_max_b_frames = ffmpeg_settings.get(
        'use_max_b_frames', False)
    context.scene.render.ffmpeg.video_bitrate = ffmpeg_settings.get(
        'video_bitrate', 6000)
    context.scene.render.ffmpeg.maxrate = ffmpeg_settings.get(
        'maxrate', 9000)
    context.scene.render.ffmpeg.minrate = ffmpeg_settings.get(
        'minrate', 0)
    context.scene.render.ffmpeg.buffersize = ffmpeg_settings.get(
        'buffersize', 224 * 8)
    context.scene.render.ffmpeg.packetsize = ffmpeg_settings.get(
        'packetsize', 2048)
    context.scene.render.ffmpeg.muxrate = (
        ffmpeg_settings.get('muxrate', 10080000)
    )
