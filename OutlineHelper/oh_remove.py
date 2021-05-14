import bpy

from bpy.props import *
from bpy.types import (Panel,Menu,Operator,PropertyGroup)

class OH_OT_Remove_Operator(bpy.types.Operator):
    bl_idname = "object.oh_remove"
    bl_label = "Remove Outline"
    bl_description = "Remove the outline from selected objects."
    bl_options = { "REGISTER", "UNDO"}

    @classmethod    
    def poll(cls, context):
        return (bpy.context.object.mode != "EDIT")

    def execute(self, context):

        sel = bpy.context.selected_objects

        for obj in sel:
            if obj.type in ["MESH", "CURVE"]:
                bpy.context.view_layer.objects.active = obj

                matindex = obj.data.materials.find('OH_Outline_Material')
                if matindex != -1:
                    obj.data.materials.pop(index=matindex)

                exists = False

                for mod in bpy.context.object.modifiers:
                    if mod.name == "OH_OUTLINE":
                        exists = True

                if exists:
                    mod = bpy.context.object.modifiers["OH_OUTLINE"]
                    obj.modifiers.remove(mod)

                for vg in obj.vertex_groups:
                    if vg.name == "OH_Outline_VertexGroup":
                        obj.vertex_groups.remove(vg)
                        

        return {"FINISHED"}