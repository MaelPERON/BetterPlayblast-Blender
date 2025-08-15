import bpy

from ..addon import packages_installed, missing_packages

class InstallMissingPackages(bpy.types.Operator):
	bl_idname = "bp.install_missing_packages"
	bl_label = "Install Missing Packages"
	bl_description = "Install the required packages for Better Playblast"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context) -> set[str]:
		# TODO : Implement the installation process
		return {'FINISHED'}
	
	@classmethod
	def poll(cls, context):
		return not packages_installed()