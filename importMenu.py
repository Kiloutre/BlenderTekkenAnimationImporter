import bpy
import os


# from . import animationReader
from . import AnimationImporter


# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(AnimationImporter.AnimationImporter.bl_idname, text= "Import Tekken 7 Animation")

def register():
    bpy.utils.register_class(AnimationImporter.AnimationImporter)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(AnimationImporter.AnimationImporter)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
