import bpy

def pop_panel_decorator(idname):
	def decorator(func):
		def wrapper(self: bpy.types.Menu, context: bpy.types.Context):
			layout = self.layout
			if context.area.show_menus:
				layout.popover(idname, text="Better Playblast")
			return func()
		return wrapper
	return decorator
