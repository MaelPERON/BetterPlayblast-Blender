import venv
import site
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