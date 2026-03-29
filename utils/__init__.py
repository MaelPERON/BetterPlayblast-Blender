from importlib import reload, import_module


def pyppeteer_import(downloader: bool = False):
    try:
        if downloader:
            module = import_module("pyppeteer.chromium_downloader")
        else:
            module = import_module("pyppeteer")
        reload(module)
        return module
    except ImportError:
        return None


def pyppeteer_is_installed() -> bool:
    return pyppeteer_import() is not None


def chromium_is_installed() -> bool:
    downloader = pyppeteer_import(downloader=True)
    if not downloader:
        return False

    return downloader.check_chromium()


def pyppeteer_download():
    downloader = pyppeteer_import(downloader=True)
    if not downloader:
        return None

    if not downloader.check_chromium():  # Check if Chromium is downloaded
        downloader.download_chromium()
    else:
        print("Chromium is already downloaded.")


def psutil_import():
    try:
        module = import_module("psutil")
        reload(module)
        return module
    except ImportError:
        return None
