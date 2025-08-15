from datetime import datetime

def get_current_time(days: bool = True) -> str:
	"""Get the current time as a formatted string.

	Returns:
		str: The current time formatted as YYYY-MM-DD HH:MM:SS.
	"""
	format = "%Y-%m-%d %H:%M:%S" if days else "%H:%M:%S"
	return datetime.now().strftime(format)