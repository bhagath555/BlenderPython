import bpy


def color_ramp_material(name = '', minvalue= '', maxvalue= ''):

   """This function create a material and assign that material to
      active object 
      

   """
   axis = bpy.data.materials.new(name= "Axis_mat") 
   #Enabling Use Nodes
   axis.use_nodes = True
   pbsdf_node = axis.node_tree.nodes.get('Principled BSDF')
   pbsdf_node.select = False
   axis_output = axis.node_tree.nodes.get('Material Output')
   axis_output.select = False

   #Adding Color Ramp Node
   colorramp_node = axis.node_tree.nodes.new('ShaderNodeValToRGB')
   #Set location of node
   colorramp_node.location = (-350,0)
   #Setting the Default Color
   colorramp_node.color_ramp.elements.new(0.5)
   colorramp_node.color_ramp.elements[0].color = (0, 0, 1, 1)
   colorramp_node.color_ramp.elements[1].color = (0, 1, 0, 1)
   colorramp_node.color_ramp.elements[2].color = (1, 0, 0, 1)
   colorramp_node.select = False

   #Adding Range Map Node
   maprange_node = axis.node_tree.nodes.new('ShaderNodeMapRange')
   #Set location of node
   maprange_node.location = (-600,0)
   maprange_node.inputs[1].default_value = minvalue
   maprange_node.inputs[2].default_value = maxvalue
   maprange_node.inputs[3].default_value = 0
   maprange_node.inputs[4].default_value = 1
   maprange_node.select = False


   #Adding Separate XYZ Node
   seperateXYZ_node = axis.node_tree.nodes.new('ShaderNodeSeparateXYZ')
   #Set location of node
   seperateXYZ_node.location = (-900,0)
   seperateXYZ_node.select = False


   #Adding Geometry Node
   geometry_node = axis.node_tree.nodes.new('ShaderNodeNewGeometry')
   #Set location of node
   geometry_node.location = (-1200,0)
   geometry_node.select = False



   #Creating Links between the Nodes
   axis.node_tree.links.new(colorramp_node.outputs[0], pbsdf_node.inputs[0])
   axis.node_tree.links.new(maprange_node.outputs[0], colorramp_node.inputs[0])
   axis.node_tree.links.new(seperateXYZ_node.outputs[2], maprange_node.inputs[0])
   axis.node_tree.links.new(geometry_node.outputs[0], seperateXYZ_node.inputs[0])

   bpy.context.object.active_material = name


