import bpy
import sys
from textwrap import wrap
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
    bl_options = {'REGISTER'}

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
        self._show_restart_popup(context)
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return not packages_installed()

    def draw(self, context):
        layout = self.layout
        layout.label(
            text="BetterPlayblast requires additional packages.",
            icon='INFO',
        )

        # Listing the missing packages.
        venv = (VenvManager()
                if get_venv_path().exists()
                else None)

        subheader, subbody = layout.panel(
            idname=f"{self.bl_idname}_packages",
            default_closed=True,
        )
        subheader.label(text="Required Packages", icon='PACKAGE')
        for package in PACKAGES.keys():
            if subbody is None:
                continue
            row = subbody.row(align=True)
            if venv is not None and venv.has_library(package):
                row.label(text=package, icon="SORTTIME")
            else:
                row.label(text=package, icon='DOT')

        # Warning about the installation process.
        warning_box = layout.box()
        warning_box.scale_x = 2
        header = warning_box.row()
        header.alert = True
        header.label(text="Before you install", icon='ERROR')
        warning_column = warning_box.column(align=True)

        messages = [
            "The installation process may take a while.",
            "Blender may become unresponsive during installation.",
            "It's recommended to open the console to see the progress.",
            "After installation, restart Blender to apply changes."
        ]

        for message in messages:
            wrapped_lines = wrap(message, width=70)
            for line_index, line in enumerate(wrapped_lines):
                row = warning_column.row(align=True)
                row.label(text="", icon='DOT' if line_index == 0 else 'BLANK1')
                row.label(text=line)

    def _show_restart_popup(self, context):
        def draw_popup(self, context):
            layout: bpy.types.UILayout = self.layout

            layout.label(text="Installation complete!"
                         "Please restart Blender to apply changes.")

        bpy.context.window_manager.popup_menu(
            draw_popup,
            title="Restart Required",
            icon='INFO',
        )

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400, confirm_text="Install")
