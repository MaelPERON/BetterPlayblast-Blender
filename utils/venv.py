import venv
import site
import os
import subprocess
from pathlib import Path


def get_venv_path() -> Path:
    venv_path: Path = Path(site.USER_BASE) / "BetterPlayblast-venv"
    return venv_path


def venv_bin() -> Path:
    venv_path = get_venv_path()
    if os.name == "nt":
        return venv_path / "Scripts"
    else:
        return venv_path / "bin"


def venv_python_executable() -> Path:
    python_executable = venv_bin() / "python"
    if os.name == "nt":
        return python_executable.with_suffix(".exe")
    else:
        return python_executable


def parse_library_argument(library: str | list[str]) -> list[str]:
    if isinstance(library, str):
        return [library]
    elif isinstance(library, list):
        return library
    else:
        raise ValueError("Library argument must be a string or a list of strings.")  # noqa: E501


def start_pip_command(python_executable: Path, *args: str) -> list[str]:
    return subprocess.check_call([str(python_executable), "-m", "pip", *args])


class VenvManager():
    """Class to manage a virtual environment for BetterPlayblast.\n
    Ensures the virtual environment is created and provides methods to install
    and uninstall libraries within it.
    """
    def __init__(self):
        self.venv_path = get_venv_path()
        if not self.venv_path.exists():
            builder = venv.EnvBuilder(with_pip=True)
            builder.create(self.venv_path)

        self.bin = venv_bin()
        self.python_executable = venv_python_executable()
        self.site = self.venv_path / "Lib" / "site-packages"
        if not self.python_executable.exists():
            raise FileNotFoundError(f"Python executable not found at {self.python_executable}")  # noqa: E501

    def install_library(self, library: str | list[str]) -> None:
        libraries = parse_library_argument(library)
        start_pip_command(self.python_executable, "install", *libraries)

    def uninstall_library(self, library: str | list[str]) -> None:
        libraries = parse_library_argument(library)
        start_pip_command(self.python_executable, "uninstall", "-y",
                          *libraries)

    def has_library(self, library: str) -> bool:
        try:
            subprocess.check_call(
                [str(self.python_executable), "-m", "pip", "show", library],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except subprocess.CalledProcessError:
            return False


class VenvLibraries():
    """Class to manage the required libraries for BetterPlayblast within a virtual environment."""  # noqa: E501
    def __init__(self, venv_manager: VenvManager, libraries: list[str]):
        self.venv_manager = venv_manager
        self.libraries = libraries

    def missing_libraries(self) -> list[str]:
        return [lib for lib in self.libraries
                if not self.venv_manager.has_library(lib)]

    def install_missing_libraries(self) -> None:
        missing = self.missing_libraries()
        if missing:
            self.venv_manager.install_library(missing)

    def uninstall_libraries(self) -> None:
        self.venv_manager.uninstall_library(self.libraries)
