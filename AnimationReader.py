import bpy

# ImportHelper is a helper class, defines filename and invoke() function which calls the file selector.
import struct

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator

from . import AnimationHeader0xC8


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
        operation_status = self.__read_animation_file(context, self.filepath)
        return operation_status

    def __read_animation_file(self, context, filepath = None):
        print("started read_file method")

        with open(filepath, 'rb') as animationFile:
            binaryData = animationFile.read()

        self.__get_animation(binaryData)

        operation_status = {'FINISHED'}
        return operation_status

    def __get_animation(self, binaryData):
        # "< 2B H 24I" stands for little endian, 2 unsigned bytes, unsigned short, 24 unsigned 4-byte integers
        struct_packer = struct.Struct("< 2B H 24I")
        animation_header_tuple = struct_packer.unpack_from(binaryData)
        animation_header = AnimationHeader0xC8.AnimationHeader0xC8(animation_header_tuple)

        print(animation_header_tuple)
        print(animation_header)
