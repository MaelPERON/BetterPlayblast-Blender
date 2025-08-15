from datetime import datetime

def get_current_time(days: bool = True) -> str:
	"""Get the current time as a formatted string.

	Returns:
		str: The current time formatted as YYYY-MM-DD HH:MM:SS.
	"""
	format = "%Y-%m-%d %H:%M:%S" if days else "%H:%M:%S"
	return datetime.now().strftime(format)

def get_timecode_from_frame(frame: int, fps: int = 24, start: int = 0) -> str:
	"""Get the timecode from a frame number.

	Args:
		frame (int): The frame number.
		fps (int, optional): The frames per second. Defaults to 24.
		start (int, optional): The start frame. Defaults to 0.

	Returns:
		str: The timecode formatted as HH:MM:SS.mmm.
	"""
	frame_time = (frame - start) / fps
	hours = int(frame_time // 3600)
	minutes = int((frame_time % 3600) // 60)
	seconds = int(frame_time % 60)
	milliseconds = int((frame_time - int(frame_time)) * 1000)
	return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"