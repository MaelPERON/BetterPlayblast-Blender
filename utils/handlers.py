def remove_function_from_handler(function: callable, handler: list) -> None:
	"""Reset the handler to avoid duplicate calls."""
	if function in handler:
		handler.remove(function)