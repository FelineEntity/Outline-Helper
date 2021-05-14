import bpy
from bpy.props import *
from bpy.types import (Panel,Menu,Operator,PropertyGroup)

class OH_PT_SidePanel(bpy.types.Panel):
    bl_idname = "OH_PT_SidePanel"
    bl_label = "Outline Helper"
    bl_category = "Outline Helper"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def draw(self, context):
        layout = self.layout

        col = layout.column()

        row = col.row()
        row.operator("object.oh_outline", icon = "ADD", text = "Add/Set Outline")
        row = col.row()
        row.operator("object.oh_adjust", icon = "ARROW_LEFTRIGHT", text = "Adjust Outline")
        row = col.row()
        row.operator("object.oh_remove", icon = "PANEL_CLOSE", text = "Remove Outline")
