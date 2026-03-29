import venv
import site
import os
import subprocess
from pathlib import Path


def get_venv_path() -> Path:
    venv_path: Path = Path(site.USER_BASE) / "BetterPlayblast-venv"
    return venv_path


def venv_create() -> Path:
    venv_path = get_venv_path()
    if not venv_path.exists():
        builder = venv.EnvBuilder(with_pip=True)
        builder.create(venv_path)

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

