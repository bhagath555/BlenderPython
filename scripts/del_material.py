import bpy

from bpy.types import Panel, Operator


class del_material_op(Operator):
    bl_idname = "del.unsuedmats"
    bl_label = "Deletes unused materials from the blend file."

    """
        This operator deletes all the unused materials from the scene.
    """

    def execute(self, context):
        """
        Body of the operator.
        """
        for material in bpy.data.materials:
            if not material.users:
                bpy.data.materials.remove(material)

        return {'FINISHED'}


class Mographs_PT(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "MoGraphs"
    bl_label = "Del materials"

    def draw(self, context):
      layout = self.layout
      row = layout.row()
      row.label(text="Unused mats:", icon = "MATERIAL")
      row.operator(del_material_op.bl_idname, text="Del")  
    
def register():
    bpy.utils.register_class(del_material_op)
    bpy.utils.register_class(Mographs_PT)


def unregister():
    bpy.utils.unregister_class(del_material_op)
    bpy.utils.unregister_class(Mographs_PT)

if __name__ == "__main__":
    register()