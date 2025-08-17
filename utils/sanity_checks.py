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

		return (self.check_function(value, *args, **kwargs), self.error_message)
	

sanity_file_saved = SanityCheck(lambda file: file != "", "Blend file not saved")