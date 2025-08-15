from pathlib import Path
import bpy.utils.previews as previews

preview_collections = {}

def get_icon(name: str) -> int:
	"""Get the icon ID for a given icon name."""
	if "main" not in preview_collections:
		return 0
	icon = preview_collections["main"].get(name, None)
	if not icon:
		print(f"Icon '{name}' not found.")
	return getattr(icon, "icon_id", 0)

def register():
	preview_collection = previews.new()
	preview_collections["main"] = preview_collection

	icon_folder = Path(__file__).parent / "icons"
	icons = [f for f in icon_folder.iterdir() if f.is_file() and f.suffix in {'.png', '.jpg', '.jpeg', '.svg'}]
	for icon in icons:
		preview_collection.load(icon.stem, str(icon), 'IMAGE')

def unregister():
	for collection in preview_collections.values():
		previews.remove(collection)
	preview_collections.clear()