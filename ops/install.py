import bpy
import sys
from pathlib import Path
from subprocess import run

from ..addon import packages_installed
from ..BetterPlayblast.install import missing_packages

PYTHON = sys.executable
SITE_PACKAGES = Path(PYTHON).parent.parent / "lib" / "site-packages"

class InstallMissingPackages(bpy.types.Operator):
	bl_idname = "bp.install_missing_packages"
	bl_label = "Install Missing Packages"
	bl_description = "Install the required packages for Better Playblast.\n*This may cause blender to freeze.*\n(Open the console first to see the installation progress)"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context) -> set[str]:
		packages = missing_packages()
		args = [PYTHON, '-m', 'pip', 'install', '--target', str(SITE_PACKAGES), *packages]
		print(f"Running command: {' '.join(args)}")
		run(args)
		self.report({'INFO'}, f"Installed packages: {packages}")
		return {'FINISHED'}
	
	@classmethod
	def poll(cls, context):
		return not packages_installed()