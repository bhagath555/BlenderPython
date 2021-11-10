# the livelinking of scripts
# Add addon information.
bl_info = {
    "name" : "Script-LiveLink [BD3D]",
    "author" : "BD3D",
    "description" : "LiveLink for script",
    "blender" : (2, 80, 0),
    "location" : "Operator",
    "warning" : "",
    "category" : "Generic"
}

#pep8compliant..ect..
# Import required modules.
import bpy, os,functools
from bpy.types import Menu, Panel, Operator, PropertyGroup, Operator, AddonPreferences, PropertyGroup
from bpy.props import StringProperty, IntProperty, BoolProperty, FloatProperty, EnumProperty, PointerProperty
C = bpy.context

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

def execute_check(G_path,G_name): #TIMER
    if bpy.context.scene[G_name+" check"] == False:
        print(G_name + ' checking aborted')
        return None
    if bpy.context.scene[G_name] != os.path.getmtime(G_path):
        F = open(G_path)
        will_exec = False
        if "EXECUTE" in F.readline():#EXECEXEC
            will_exec = True#EXEC
        F.close()#i just lose the first line so i need to restart
        F = open(G_path)
        bpy.data.texts[G_name].clear()         #clear all text
        bpy.data.texts[G_name].write(F.read()) #paste text from G_path
        if will_exec == True:#EXEC
            #exec(bpy.data.texts[G_name].as_string()) #wont work on addon reg... i tried a lot of other exec method, i think we need bpy.ops.text.run_script()
            exec(compile(open(G_path).read(), G_path, 'exec'))
        F.close()
        bpy.context.scene[G_name] = os.path.getmtime(G_path)
    #print('check')
    return 0.5

## Define opertors
class SCR_OT_link(bpy.types.Operator):
    bl_idname = "scr.link"
    bl_label = ""
    bl_description = ""
    index : bpy.props.IntProperty() 
    def execute(self, context):
        index = self.index
        G = bpy.context.scene.SCR_OT_group # Extracting property group information.
        if index == 1:
            G_path = G.path_01
            G_targ = G.target_01
        elif index ==2:
            G_path = G.path_02
            G_targ = G.target_02
        elif index ==3:
            G_path = G.path_03
            G_targ = G.target_03

        G_name = os.path.basename(G_path)
        G_targ.name = G_name
        bpy.context.scene[G_name]          = os.path.getmtime(G_path) 
        # is used to get the time of last modification of the specified path
        bpy.context.scene[G_name+" check"] = True
        print("starting timer")
        ## bpy.app.timers.register - excutes the provided functions after menetioned time delay.
        bpy.app.timers.register(functools.partial(execute_check,G_path,G_name), first_interval=0.5)
        return {'FINISHED'}
    
    
class SCR_OT_stop_link(bpy.types.Operator):
    bl_idname = "scr.stop_link"
    bl_label = ""
    bl_description = ""
    
    index : bpy.props.IntProperty() 
    def execute(self, context):
        index = self.index
        G = bpy.context.scene.SCR_OT_group
        if index == 1:
            G_path = G.path_01
        elif index ==2:
            G_path = G.path_02
        elif index ==3:
            G_path = G.path_03

        G_name = os.path.basename(G_path) # Collecting file name
        bpy.context.scene[G_name+" check"] = False # Unlinking
        return {'FINISHED'}

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

## Define property group
class SCR_OT_group(bpy.types.PropertyGroup): #not needed, could do with one storage 
    path_01   : StringProperty(name=" ",subtype='FILE_PATH',default=r"‪") ## This allows the entiring file path.
    target_01 : PointerProperty(type=bpy.types.Text) ## Pointer type is string type.
    
    path_02   : StringProperty(name=" ",subtype='FILE_PATH',default=r"‪")
    target_02 : PointerProperty(type=bpy.types.Text)
    
    path_03   : StringProperty(name=" ",subtype='FILE_PATH',default=r"‪")
    target_03 : PointerProperty(type=bpy.types.Text)


## Defibe panel
class SCR_PT_panel(Panel):
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Text"
    bl_label = "Live-Link"

    def draw(self, context):
        layout = self.layout

        row = layout.column(align=True)
        row.prop(bpy.context.scene.SCR_OT_group, "path_01",text="")
        row.prop(bpy.context.scene.SCR_OT_group, "target_01",text="")
        rowrow = row.row(align=True)
        # SCR_OT_link.bl_idname convention is used instead of writing opertor command.
        rowrow.operator(SCR_OT_link.bl_idname, text="Start Live-Link",icon="PASTEDOWN").index       = 1
        rowrow.operator(SCR_OT_stop_link.bl_idname, text="Stop Live-Link",icon="PANEL_CLOSE").index = 1

        layout.separator()

        row = layout.column(align=True)
        row.prop(bpy.context.scene.SCR_OT_group, "path_02",text="")
        row.prop(bpy.context.scene.SCR_OT_group, "target_02",text="")
        rowrow = row.row(align=True)
        rowrow.operator(SCR_OT_link.bl_idname, text="Start Live-Link",icon="PASTEDOWN").index       = 2
        rowrow.operator(SCR_OT_stop_link.bl_idname, text="Stop Live-Link",icon="PANEL_CLOSE").index = 2

        layout.separator()

        row = layout.column(align=True)
        row.prop(bpy.context.scene.SCR_OT_group, "path_03",text="")
        row.prop(bpy.context.scene.SCR_OT_group, "target_03",text="")
        rowrow = row.row(align=True)
        rowrow.operator(SCR_OT_link.bl_idname, text="Start Live-Link",icon="PASTEDOWN").index       = 3
        rowrow.operator(SCR_OT_stop_link.bl_idname, text="Stop Live-Link",icon="PANEL_CLOSE").index = 3

        layout.separator()

        text = layout.box().column(align=True)
        text.label(text='if "EXECUTE" is in the first line of your script', icon='INFO')
        text.label(text='it will Run the script after the Sync')


#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
# Collect all the opertors, panels, property groups for registering.
sc_classes = {
    SCR_OT_group,
    SCR_PT_panel,
    SCR_OT_link,
    SCR_OT_stop_link,
}

def register():
    for cls in sc_classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.SCR_OT_group = bpy.props.PointerProperty(type=SCR_OT_group)

def unregister():
    for cls in sc_classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.C_Slots_settings

if __name__ == "__main__":
    register()