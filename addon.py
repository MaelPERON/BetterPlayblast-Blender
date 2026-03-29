import sys
import os
from .utils.venv import VenvManager, get_venv_path
from .utils.pyppeteer import chromium_is_installed
from .BetterPlayblast.install import all_installed


def packages_installed() -> bool:
    # Set the Chromium revision to use
    os.environ["PYPPETEER_CHROMIUM_REVISION"] = "1230501"

    if not get_venv_path().exists():
        return False

    if not all_installed(refresh=True):
        return False

    if not chromium_is_installed():
        return False

    return True


def register():
    if get_venv_path().exists():
        venv = VenvManager()
        if venv.site not in sys.path:
            print(f"Adding {venv.site} to sys.path")
            sys.path.insert(0, str(get_venv_path() / "Lib" / "site-packages"))

    print("BetterPlayblast-Blender: addon reloaded")
