import bpy

# from . import animationReader
from . import AnimationExporter


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(AnimationExporter.AnimationExporter.bl_idname, text= "Export Tekken 7 Animation")

def register():
    bpy.utils.register_class(AnimationExporter.AnimationExporter)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(AnimationExporter.AnimationExporter)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
