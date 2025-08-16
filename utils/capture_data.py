import bpy
import os
from . import time
from datetime import datetime

def data_init_capture(context: bpy.types.Context) -> dict:
	"""Initialize data capture for the playblast.

	Args:
		context (bpy.types.Context): The Blender context.

	Returns:
		dict: The initialized data capture.
	"""
	scene = context.scene
	date = time.get_current_time(days=True)
	frame_start, frame_end, frame_step = scene.frame_start, scene.frame_end, scene.frame_step
	fps = scene.render.fps
	width = scene.render.resolution_x
	height = scene.render.resolution_y
	scale = scene.render.resolution_percentage / 100
	step_suffix = f":{frame_step}" if frame_step > 1 else ""
	
	data = {
		"frames": [],
		"frame_range": f"{frame_start}:{frame_end}{step_suffix}",
		"fps": fps,
		"hostname": os.uname().nodename if hasattr(os, "uname") else os.environ.get("COMPUTERNAME", ""),
		"user": os.environ.get("USERNAME", ""),
		"scene": scene.name,
		"filename": bpy.path.basename(bpy.data.filepath),
		"note": scene.render.stamp_note_text if scene.render.use_stamp_note else "",
		"resolution": f"{int(scene.render.resolution_x*scale)}x{int(scene.render.resolution_y*scale)}",
		"date": date,
		"software": "blender",
		"icon": "blender"
	}
	return data

def data_frame_capture(data: dict, last_check_time: datetime, scene: bpy.types.Scene, depsgraph: bpy.types.Depsgraph) -> dict:
	"""Capture data for the current frame.

	Args:
		data (dict): The data dictionary to update.
		last_check_time (datetime): The last time the data was checked.
		scene (bpy.types.Scene): The current Blender scene.
		depsgraph (bpy.types.Depsgraph): The current Blender dependency graph.

	Returns:
		dict: The updated data dictionary.
	"""

	""" MEMORY USAGE """
	process = psutil.Process()
	mem_info = process.memory_info()
	num_threads = process.num_threads()
	memory_mb = mem_info.rss / (1024 * 1024)

	return data