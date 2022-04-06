import bpy
import struct
from math import pi, ceil

from bpy.props import StringProperty
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper

from .Animation0xC80x17 import Animation0xC80x17
from . TekkenAnimHelper import TekkenAnimation, getAnimFrameFromBones

def get_keyframes(obj):
    keyframes = []
    anim = obj.animation_data
    if anim is not None and anim.action is not None:
        for fcu in anim.action.fcurves:
            for keyframe in fcu.keyframe_points:
                x, y = keyframe.co
                if x not in keyframes:
                    keyframes.append((ceil(x)))
    return keyframes
    
def getSourceArmature(context):
    armature = context.object
    
    if armature.type != 'ARMATURE':
        return None
        
    if "BODY_SCALE__group" not in armature.pose.bones:
        return None
        
    return armature
    
class AnimationExporter(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "animation_reader.export_animation"  # important since its how bpy.ops.animation_reader.read_animation is constructed
    bl_label = "Export Animation"

    # ImportHelper mixin class uses this
    filename_ext = ".bin"

    filter_glob: StringProperty(
        default = "*.bin",
        options = {'HIDDEN'},
    )

    def execute(self, context):
        sce = bpy.context.scene
        armature = getSourceArmature(bpy.context)
        
        if armature == None:
            self.report({'ERROR'}, "No valid armature selected")
            return {'FINISHED'}
        
        #animLength = sce.frame_end
        animLength = get_keyframes(armature)[-1]

        frames = []
        for f in range(sce.frame_start, animLength+1):
            sce.frame_set(f)
            frames.append(getAnimFrameFromBones(armature))
        
        newAnimation = TekkenAnimation()
        newAnimation.setLength(animLength)
        newAnimation.recalculateSize()
        
        for f in range(animLength):
            for fieldId, fieldValue in enumerate(frames[f]):
                newAnimation.setField(fieldValue, f, fieldId)
            
        with open(self.filepath, "wb") as f:
            f.write(bytes(newAnimation.data))
            
        self.report({'INFO'}, "Animation successfuly exported")
        return {'FINISHED'}