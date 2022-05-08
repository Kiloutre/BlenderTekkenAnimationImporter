import bpy

# from . import animationReader
from . AnimationExporter import AnimationExporter, FaceAnimationExporter, LeftHandAnimationExporter, RightHandAnimationExporter


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(AnimationExporter.bl_idname, text= "Export Tekken 7 Animation")
    self.layout.operator(FaceAnimationExporter.bl_idname, text= "Export Tekken 7 Face Animation")
    self.layout.operator(LeftHandAnimationExporter.bl_idname, text= "Export Tekken 7 Left-Hand Animation")
    self.layout.operator(RightHandAnimationExporter.bl_idname, text= "Export Tekken 7 Right-Hand Animation")

def register():
    bpy.utils.register_class(AnimationExporter)
    bpy.utils.register_class(FaceAnimationExporter)
    bpy.utils.register_class(LeftHandAnimationExporter)
    bpy.utils.register_class(RightHandAnimationExporter)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(AnimationExporter)
    bpy.utils.unregister_class(FaceAnimationExporter)
    bpy.utils.unregister_class(LeftHandAnimationExporter)
    bpy.utils.unregister_class(RightHandAnimationExporter)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
