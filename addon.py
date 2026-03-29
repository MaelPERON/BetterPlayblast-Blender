import os
from .utils.venv import VenvManager, get_venv_path
from .utils import chromium_is_installed
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
    print("BetterPlayblast-Blender: addon reloaded")
