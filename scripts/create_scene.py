import bpy

bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 0, 10), rotation=(0, -0, 0), scale=(1, 1, 1))

bpy.context.object.data.type = 'ORTHO'

bpy.context.object.data.ortho_scale = 32

bpy.ops.mesh.primitive_plane_add(size=32, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
bpy.context.object.name = 'Grid'
 
bpy.ops.mesh.primitive_plane_add(size=32, enter_editmode=False, align='WORLD', location=(0, 0, 0.25), scale=(1, 1, 1))
bpy.context.object.name = 'Axis'
