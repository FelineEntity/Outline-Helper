import bpy

from bpy.props import *
from bpy.types import (Panel,Menu,Operator,PropertyGroup)

class OH_OT_Outline_Operator(bpy.types.Operator):
    bl_idname = "object.oh_outline"
    bl_label = "Set Outline"
    bl_description = "Add or adjust geometry outline of selected objects"
    bl_options = { "REGISTER" , "UNDO" }

    #Operator Properties
    outline_thickness : FloatProperty(
        name = "Outline Thickness",
        description = "Thickness of the applied outline",
        default = 0.1,
        min = 0,
        max = 1000000
    )

    apply_scale : BoolProperty(
        name = "Apply Scale",
        description = "Applies scale of objects to make outlines uniform",
        default = False
    )

    @classmethod    
    def poll(cls, context):
        return (bpy.context.object.mode != "EDIT")

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        box = layout.box()

        col = box.column()

        col.label(text="Outline Thickness")
        colrow = col.row(align=True)
        colrow.prop(self, "outline_thickness", expand = True, text = "")
        colrow = col.row(align=True)
        colrow.prop(self, "apply_scale", expand = True, text = "Apply Scale")


    def invoke(self, context, event):
        #print("INVOKE OUTLINE")

        sel = bpy.context.selected_objects
        if bpy.context.view_layer.objects.active is not None:
            for mod in bpy.context.view_layer.objects.active.modifiers:
                if mod.name == "OH_OUTLINE":
                    self.outline_thickness = -(bpy.context.view_layer.objects.active.modifiers["OH_OUTLINE"].thickness)

        mat = bpy.data.materials.get("OH_Outline_Material")

        if mat is None:
            mat = bpy.data.materials.new(name="OH_Outline_Material")
            mat.use_nodes = True
            mat.use_backface_culling = True
            mat.use_backface_culling_shadow = True
            nodes = mat.node_tree.nodes
            nodes.clear()
            links = mat.node_tree.links
            #Create Eevee Path
            node_color = nodes.new(type="ShaderNodeRGB")
            node_color.outputs[0].default_value = (0,0,0,1)
            node_color.location= -700,-100
            node_output = nodes.new(type="ShaderNodeOutputMaterial")
            node_output.location = 100,-100
            node_output.target = "EEVEE"
            link = links.new(node_color.outputs[0], node_output.inputs[0])
            #Create Cycles Path
            node_geometry = nodes.new(type="ShaderNodeNewGeometry")
            node_geometry.location = -700,400
            node_transparency = nodes.new(type="ShaderNodeBsdfTransparent")
            node_transparency.location = -700,100
            node_lightpath = nodes.new(type="ShaderNodeLightPath")
            node_lightpath.location = -500,500
            node_mix_1 = nodes.new(type="ShaderNodeMixShader")
            node_mix_1.location = -500,100
            node_mix_2 = nodes.new(type="ShaderNodeMixShader")
            node_mix_2.location = -300,100
            node_mix_3 = nodes.new(type="ShaderNodeMixShader")
            node_mix_3.location = -100,100
            node_output_cycles = nodes.new(type="ShaderNodeOutputMaterial")
            node_output_cycles.location = 100,100
            node_output_cycles.target = "CYCLES"

            #Mix1
            links.new(node_geometry.outputs[6],node_mix_1.inputs[0])
            links.new(node_color.outputs[0], node_mix_1.inputs[1])
            links.new(node_transparency.outputs[0],node_mix_1.inputs[2])
            #Mix2
            links.new(node_lightpath.outputs[0],node_mix_2.inputs[0])
            links.new(node_transparency.outputs[0], node_mix_2.inputs[1])
            links.new(node_mix_1.outputs[0],node_mix_2.inputs[2])
            #Mix3
            links.new(node_lightpath.outputs[3],node_mix_3.inputs[0])
            links.new(node_mix_2.outputs[0], node_mix_3.inputs[1])
            links.new(node_mix_1.outputs[0],node_mix_3.inputs[2])

            links.new(node_mix_3.outputs[0],node_output_cycles.inputs[0])
        
            bpy.ops.ed.undo_push()

        return self.execute(context)
        
        
    def execute(self, context):

        sel = bpy.context.selected_objects

        for obj in sel:
            if obj.type in ["MESH", "CURVE"]:
                bpy.context.view_layer.objects.active = obj

                if self.apply_scale:
                    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True,properties=False)

                #Material

                mat_missing = True

                for slot in obj.data.materials:
                    if slot is not None:
                        if slot.name == "OH_Outline_Material":
                            mat_missing = False

                if mat_missing:
                    mat = bpy.data.materials.get("OH_Outline_Material")
                    bpy.context.object.data.materials.append(mat)


                #Vertex Group if MESH

                if obj.type == "MESH":
                    vg_missing = True
                    vg_outline = None

                    for vg in obj.vertex_groups:
                        if vg.name == "OH_Outline_VertexGroup":
                            vg_missing = False
                            vg_outline = vg

                    if vg_missing:
                        vg_outline = obj.vertex_groups.new(name="OH_Outline_VertexGroup")
                        for vert in obj.data.vertices:
                            vg_outline.add([vert.index],1.0,"ADD")


                #Modifier

                exists = False

                for mod in bpy.context.object.modifiers:
                    if mod.name == "OH_OUTLINE":
                        exists = True

                if exists:
                    mod = bpy.context.object.modifiers["OH_OUTLINE"]
                    mod.thickness = -(self.outline_thickness)
                else: 
                    obj.modifiers.new("OH_OUTLINE","SOLIDIFY")
                    mod = obj.modifiers["OH_OUTLINE"]
                    mod.use_flip_normals = True
                    mod.use_rim = False
                    if obj.type == "MESH":
                        mod.vertex_group = "OH_Outline_VertexGroup"
                    mod.thickness = -(self.outline_thickness)
                    mod.material_offset = 999

        return {"FINISHED"}
