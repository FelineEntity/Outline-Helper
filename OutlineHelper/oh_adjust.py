import bpy

from bpy.props import *
from bpy.types import (Panel,Menu,Operator,PropertyGroup)

class OH_OT_Adjust_Operator(bpy.types.Operator):
    bl_idname = "object.oh_adjust"
    bl_label = "Adjust Outline"
    bl_description = "Adjust geometry outline of selected objects"
    bl_options = { "REGISTER", "UNDO" }

    #Operator Properties
    outline_thickness : FloatProperty(
        name = "Outline Thickness",
        description = "Thickness of the applied outline",
        default = 0.1,
        min = 0,
        max = 1000000
    )

    vertex_thickness : FloatProperty(
        name = "Outline Thickness Vertex Weight",
        description = "Thickness of the applied outline at vertex",
        default = 1.0,
        min = 0,
        max = 1
    )

    apply_scale : BoolProperty(
        name = "Apply Scale",
        description = "Applies scale of objects to make outlines uniform",
        default = False
    )

    @classmethod    
    def poll(cls, context):
        if bpy.context.object.mode == "EDIT":
            return (bpy.context.object.type == "MESH")
            
        return True

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        box = layout.box()

        col = box.column()

        if bpy.context.object.mode != "EDIT":
            col.label(text="Outline Thickness") 
            colrow = col.row(align=True)
            colrow.prop(self, "outline_thickness", expand = True, text = "")
            colrow = col.row(align=True)
            colrow.prop(self, "apply_scale", expand = True, text = "Apply Scale")
        else:
            col.label(text="Outline Thickness Vertex Weight")
            colrow = col.row(align=True)
            colrow.prop(self, "vertex_thickness", expand = True, text = "")


    def invoke(self, context, event):
        for mod in bpy.context.view_layer.objects.active.modifiers:
            if mod.name == "OH_OUTLINE":
                self.outline_thickness = -(bpy.context.view_layer.objects.active.modifiers["OH_OUTLINE"].thickness)
            
        return self.execute(context)

    def execute(self, context):

        sel = bpy.context.selected_objects

        for obj in sel:
            if obj.type in ["MESH", "CURVE"]:
                if obj.mode != "EDIT":
                    bpy.context.view_layer.objects.active = obj

                    if self.apply_scale:
                        bpy.ops.object.transform_apply(location=False,rotation=False,scale=True,properties=False)

                    exists = False

                    for mod in bpy.context.object.modifiers:
                        if mod.name == "OH_OUTLINE":
                            exists = True

                    if exists:
                        mod = bpy.context.object.modifiers["OH_OUTLINE"]
                        mod.thickness = -(self.outline_thickness)
                else:
                    if obj.type == "MESH":
                        bpy.ops.object.mode_set(mode='OBJECT')
                        for vg in obj.vertex_groups:
                            if vg.name == "OH_Outline_VertexGroup":
                                for vert in obj.data.vertices:
                                    if vert.select:
                                        vg.add([vert.index],self.vertex_thickness,"REPLACE")
                        bpy.ops.object.mode_set(mode='EDIT')

        return {"FINISHED"}