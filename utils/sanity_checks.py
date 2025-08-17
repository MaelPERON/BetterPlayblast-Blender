from pathlib import Path

class SanityCheck:
	def __init__(self, check_function: callable = None, error_message: str = None):
		self.check_function = check_function
		self.error_message = error_message or "Invalid value"

	def check(self, value, *args, **kwargs) -> bool:
		if not self.check_function:
			return None

		return self.check_function(value, *args, **kwargs)

	def check_and_report(self, value, *args, **kwargs):
		if not self.check_function:
			return True, None

		message = self.error_message
		for key, value in kwargs.items():
			message = message.replace(f"${{{key}}}", str(value))

		return (self.check_function(value, *args, **kwargs), message)


sanity_file_saved = SanityCheck(lambda file: file != "", "Blend file not saved")
sanity_file_exists = SanityCheck(lambda file: (Path(file) if not isinstance(file, Path) else file).resolve().exists(), f"Path not valid")