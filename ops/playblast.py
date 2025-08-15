import bpy
from ..BetterPlayblast.install import all_installed

Playblast = None
if all_installed(refresh=True,save_cache=False):
	from ..BetterPlayblast.playblast import Playblast


class BP_Playblast(bpy.types.Operator):
	bl_idname = "bl.playblast"
	bl_label = "Better Playblast"
	bl_description = "Create a playblast with Better Playblast"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(cls, context: bpy.types.Context):
		return Playblast is not None

	def execute(self, context: bpy.types.Context):
		if Playblast is None:
			self.report({'ERROR'}, "Better Playblast is not installed or not available.")
			return {'CANCELLED'}
		
		playblast = Playblast(context)
		playblast.execute()
		return {'FINISHED'}