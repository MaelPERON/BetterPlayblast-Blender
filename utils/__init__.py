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
