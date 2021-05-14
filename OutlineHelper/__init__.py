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

bl_info = {
    "name" : "Outline Helper",
    "author" : "Feline Entity",
    "description" : "Helps managing inverted hull outlines in Eevee and Cycles.",
    "blender" : (2, 81, 0),
    "version" : (1, 1, 0),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}

import bpy

from . oh_outline import OH_OT_Outline_Operator
from . oh_sidepanel import OH_PT_SidePanel
from . oh_remove import OH_OT_Remove_Operator
from . oh_adjust import OH_OT_Adjust_Operator

classes = (OH_OT_Outline_Operator, OH_PT_SidePanel, OH_OT_Remove_Operator, OH_OT_Adjust_Operator)

register, unregister = bpy.utils.register_classes_factory(classes)