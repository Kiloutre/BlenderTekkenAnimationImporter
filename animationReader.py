import bpy

# ImportHelper is a helper class, defines filename and invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class AnimationReader(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "animation_reader.read_animation"  # important since its how bpy.ops.animation_reader.read_animation is constructed
    bl_label = "Import Some Data"

    # ImportHelper mixin class uses this
    filename_ext = ".bin"

    filter_glob: StringProperty(
        default = "*.bin",
        options = {'HIDDEN'},
    )

    def execute(self, context):
        operation_status = self.read_animation_file(context, self.filepath)
        return operation_status

    def read_animation_file(self, context, filepath = None):
        print("started read_file method")

        with open(filepath, 'rb') as animationFile:
            binaryData = animationFile.read()

        # would normally load the binaryData here
        print(len(binaryData))

        operation_status = {'FINISHED'}
        return operation_status
