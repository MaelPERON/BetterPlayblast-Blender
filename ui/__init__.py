import bpy

from ..icons import get_icon

def pop_panel_decorator(idname, text: str = None, icon: str = None):
	def decorator(func):
		def wrapper(self: bpy.types.Menu, context: bpy.types.Context):
			layout = self.layout
			if context.area.show_menus:
				args = {
					"panel": idname,
					"text": ""
				}
				if text: args["text"] = text
				if icon: args["icon_value"] = get_icon(icon)
				layout.popover(**args)
			return func()
		return wrapper
	return decorator

def spawn_error(layout: bpy.types.UILayout, message: str):
	row = layout.row(align=True)
	row.alert = True
	row.label(text=message, icon="ERROR")