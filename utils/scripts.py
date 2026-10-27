import sys
import importlib
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Script:
    path: str
    name: str = None
    module = None

    def __post_init__(self):
        self.path = Path(self.path)
        if not self.path.is_file():
            raise FileNotFoundError(f"The script file '{self.path}' does not exist or is not a file.")

        if not self.name:
            self.name = self.path.stem

        spec = importlib.util.spec_from_file_location(self.name, str(self.path))
        self.module = importlib.util.module_from_spec(spec)
        sys.modules[self.name] = self.module
        spec.loader.exec_module(self.module)

    def run(self, function_name: str, *args, **kwargs):
        """
        Run a function from the loaded script.

        Args:
            function_name (str): The name of the function to run.
            *args: Positional arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.

        Returns:
            The result of the function call, or None if the function is not found or not callable.
        """
        if foobar := getattr(self.module, function_name, None):
            if callable(foobar):
                return foobar(*args, **kwargs)
        else:
            raise AttributeError(f"No function named '{function_name}' found in the module '{self.name}'.")