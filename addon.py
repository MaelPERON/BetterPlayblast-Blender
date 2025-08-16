import bpy
from pathlib import Path

from .BetterPlayblast.install import all_installed

def packages_installed() -> bool:
	return all_installed(refresh=False)

def register():
	print("BetterPlayblast-Blender: addon reloaded")