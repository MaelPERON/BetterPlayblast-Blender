# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from . import auto_load
from .quick_settings import BP_QuickSettings
import bpy
from bpy.props import PointerProperty

bl_info = {
    "name": "Betterplayblast",
    "author": "Mael Peron, Corentin Bileau",
    "description": "Blender addon integrating BetterPlayblast (+ Easy Playblast features)",
    "blender": (4, 2, 0),
    "version": (2, 0, 7),
    "location": "3D View > Header",
    "warning": "",
    "category": "Generic",
}

auto_load.init()


def register():
    auto_load.register()
    # BP_QuickSettings is auto-registered by auto_load, just add the scene property
    bpy.types.Scene.bp_quick_settings = PointerProperty(type=BP_QuickSettings)


def unregister():
    auto_load.unregister()
    del bpy.types.Scene.bp_quick_settings
