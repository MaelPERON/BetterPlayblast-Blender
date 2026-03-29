import bpy
import sys

from ..addon import packages_installed
from ..utils.pyppeteer import pyppeteer_download
from ..utils.venv import VenvManager, get_venv_path
from ..BetterPlayblast.install import PACKAGES

PYTHON = sys.executable
SITE_PACKAGES = bpy.utils.user_resource('SCRIPTS', path="modules")


class BP_PackageInstaller(bpy.types.Operator):
    bl_idname = "bp.install_missing_packages"
    bl_label = "Install Missing Packages"
    bl_description = (
        "Install the required packages for Better Playblast.\n"
        "*This may cause blender to freeze.*\n"
        "(Open the console first to see the installation progress)"
    )
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context) -> set[str]:
        packages = list(PACKAGES.keys())

        # In case they're already installed (encourager the user to restart ->
        # better UX)
        if len(packages) != 0:
            venv_manager = VenvManager()
            venv_manager.install_library(packages)
            venv_manager.ensure_site()
        else:
            self.report(
                {'WARNING'},
                (
                    "All required packages are already installed. "
                    "Restart Blender to apply changes."
                ),
            )

        pyppeteer_install = pyppeteer_download()
        if not pyppeteer_install:
            self.report({'ERROR'}, "Failed to install pyppeteer.")
            return {'CANCELLED'}

        # User Feedback
        self.report(
            {'INFO'},
            (
                f"Installed packages: {packages}. "
                "Restart Blender to apply changes."
            ),
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return not packages_installed()

    def draw(self, context):
        layout = self.layout
        layout.label(text="BetterPlayblast requires additional packages to work.")  # noqa: E501

        # Listing the missing packages.
        venv = (VenvManager()
                if get_venv_path().exists()
                else None)

        subheader, subbody = layout.panel(idname=f"{self.bl_idname}_packages",
                                          default_closed=True)
        subheader.label(text="Required Packages:")
        for package in PACKAGES.keys():
            if subbody is None:
                continue
            box = subbody.box()
            if venv is not None and venv.has_library(package):
                box.label(text=package, icon="SORTTIME")
            else:
                box.label(text=package)

        # Warning about the installation process.
        warning_row = layout.row()
        warning_column = layout.column()
        warning_column.scale_x = 1.5

        warning_row.alert = True
        warning_row.label(text="Warning:", icon='WARNING_LARGE')

        messages = [
            "The installation process may take a while.",
            "Blender may become unresponsive during installation.",
            "It's recommended to open the console to see the progress.",
            "After installation, restart Blender to apply changes.",]

        for message in messages:
            row = warning_column.row(align=True)
            row.label(text="", icon='DOT')
            box = row.box()
            box.label(text=message)
            box.emboss = "NONE"

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400, confirm_text="Install")
