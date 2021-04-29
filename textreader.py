import bpy

# ImportHelper is a helper class, defines filename and invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class TextReader(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "text_reader.read_text"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Read Text File"

    # ImportHelper mixin class uses this
    filename_ext = ".txt"

    filter_glob: StringProperty(
        default="*.txt",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling the execute method.
    use_setting: BoolProperty(
        name="Example Boolean",
        description="Example Tooltip",
        default=True,
    )

    type: EnumProperty(
        name="Example Enum",
        description="Choose between two items",
        items=(
            ('OPT_A', "First Option", "Description one"),
            ('OPT_B', "Second Option", "Description two"),
        ),
        default='OPT_A',
    )

    def execute(self, context):
        operation_status = self.read_text_file(context, self.filepath, self.use_setting)
        return operation_status

    def read_text_file(self, context, filepath, use_some_setting):
        print("started read_text_file method.")
        f = open(filepath, 'r', encoding='utf-8')
        data = f.read()
        f.close()

        # would normally load the data here
        print(data)

        operation_status = {'FINISHED'}
        return operation_status