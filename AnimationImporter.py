# ImportHelper is a helper class, defines filename and invoke() function which calls the file selector.
from bpy.props import StringProperty
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper

from . import Animation0xC80x17


class AnimationImporter(Operator, ImportHelper):
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
        animation_binary = self.__get_binary_data_from_animation_file(context, self.filepath)
        animation = self.__get_animation(animation_binary)
        print(animation)

        operation_status = {'FINISHED'}
        return operation_status

    def __get_binary_data_from_animation_file(self, context, filepath = None):
        with open(filepath, 'rb') as animationFile:
            binary_data = animationFile.read()
            return binary_data

    def __get_animation(self, binary_data):
        # "< 2B H 24I" stands for little endian, 2 unsigned bytes, unsigned short, 24 unsigned 4-byte integers
        animation = Animation0xC80x17.Animation0xC80x17(binary_data)

        return animation