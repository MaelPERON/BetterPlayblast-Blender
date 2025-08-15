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

		# In case they're already installed (encourager the user to restart -> better UX)
		if len(packages) == 0:
			self.report({'WARNING'}, "All required packages are already installed. Restart Blender to apply changes.")
			return {'CANCELLED'}

		# Install missing packages (targeting the blender app site-packages)
		args = [PYTHON, '-m', 'pip', 'install', '--target', str(SITE_PACKAGES), *packages]
		print(f"Running command: {' '.join(args)}")
		run(args)
		
		# User Feedback
		self.report({'INFO'}, f"Installed packages: {packages}. Restart Blender to apply changes.")
		return {'FINISHED'}
	
	@classmethod
	def poll(cls, context):
		return not packages_installed()