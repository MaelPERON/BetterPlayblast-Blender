import bpy
import sys

from ..addon import VenvLibraries, packages_installed
from ..utils import pyppeteer_download
from ..utils.venv import VenvManager
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
