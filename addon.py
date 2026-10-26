import sys
from .utils.venv import VenvManager, get_venv_path
from .BetterPlayblast.install import all_installed

def packages_installed() -> bool:
	return all_installed(refresh=False)

def register():
    if get_venv_path().exists():
        venv = VenvManager()
        if venv.site not in sys.path:
            print(f"Adding {venv.site} to sys.path")
            sys.path.insert(0, str(get_venv_path() / "Lib" / "site-packages"))

    print("BetterPlayblast-Blender: addon reloaded")
