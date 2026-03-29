import os
import sys
from importlib import reload, import_module
from site import getusersitepackages
from subprocess import run


def pyppeteer_import(downloader: bool = False):
    os.putenv("PYPPETEER_CHROMIUM_REVISION", "1230501")
    try:
        if downloader:
            module = import_module("pyppeteer.chromium_downloader")
        else:
            module = import_module("pyppeteer")
        reload(module)
        return module
    except ImportError:
        return None


def pyppeteer_download():
    downloader = pyppeteer_import(downloader=True)
    if not downloader:
        return None

    if not downloader.check_chromium():  # Check if Chromium is downloaded
        downloader.download_chromium()


def psutil_import():
    try:
        module = import_module("psutil")
        reload(module)
        return module
    except ImportError:
        return None


def get_user_site_packages() -> str:
    return str(getusersitepackages())


def add_user_site_packages():
    site_packages = get_user_site_packages()
    if site_packages not in sys.path:
        sys.path.append(site_packages)


def get_python_executable(version: str = "311") -> str | None:
    try:
        result = run(['where', 'python'], capture_output=True, text=True)
        if result.returncode != 0:
            return None
        result = result.stdout.strip()
        paths = result.splitlines()
        for path in paths:
            if version in path:
                return path
    except Exception as e:
        print(f"Error occurred while getting Python executable: {e}")
        return None
