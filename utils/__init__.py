from importlib import import_module, reload


def psutil_import():
    try:
        module = import_module("psutil")
        reload(module)
        return module
    except ImportError:
        return None
