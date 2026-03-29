import bpy
import sys
from pathlib import Path
from subprocess import CalledProcessError, run

from ..addon import packages_installed
from ..utils import pyppeteer_import, pyppeteer_download, get_python_executable
from ..BetterPlayblast.install import missing_packages

PYTHON = sys.executable
SITE_PACKAGES = bpy.utils.user_resource('SCRIPTS', path="modules")

class BP_PackageInstaller(bpy.types.Operator):
	bl_idname = "bp.install_missing_packages"
	bl_label = "Install Missing Packages"
	bl_description = "Install the required packages for Better Playblast.\n*This may cause blender to freeze.*\n(Open the console first to see the installation progress)"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context) -> set[str]:
		packages = missing_packages(save_cache=False)

		# In case they're already installed (encourager the user to restart -> better UX)
		if len(packages) != 0:
			# Check if python 3.11 is available
			python_path = get_python_executable("311")
			if not python_path:
				self.report({'ERROR'}, "Python 3.11 is not available.")
				return {'CANCELLED'}

			# Install missing packages (targeting the user site-packages)
			packages.append("psutil")
			args = [python_path, '-m', 'pip', 'install', '--user', *packages]
			print(f"Running command: {' '.join(args)}")
			proc = run(args)
			try:
				proc.check_returncode()
			except CalledProcessError as e:
				self.report({'ERROR'}, str(e))
				self.report({'ERROR'}, f"Failed to install packages.")
				return {'CANCELLED'}
		else:
			self.report({'WARNING'}, "All required packages are already installed. Restart Blender to apply changes.")

		pyppeteer_install = pyppeteer_download()
		if not pyppeteer_install:
			self.report({'ERROR'}, f"Failed to install pyppeteer.")
			return {'CANCELLED'}

		# User Feedback
		self.report({'INFO'}, f"Installed packages: {packages}. Restart Blender to apply changes.")
		return {'FINISHED'}
	
	@classmethod
	def poll(cls, context):
		return not packages_installed()