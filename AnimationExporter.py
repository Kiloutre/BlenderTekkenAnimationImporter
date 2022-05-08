import bpy
import struct
from math import pi, ceil

from bpy.props import StringProperty
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper

from . TekkenAnimHelper import TekkenAnimation, getAnimFrameFromBones, getFaceAnimFrameFromBones, getLeftHandAnimFrameFromBones, getRightHandAnimFrameFromBones
from . characterFaces import getCharacterFacePos

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
    
class FaceAnimationExporter(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "animation_reader.export_face_animation"  # important since its how bpy.ops.animation_reader.read_animation is constructed
    bl_label = "Export Facial Animation"

    # ImportHelper mixin class uses this
    filename_ext = ".f_bin"

    filter_glob: StringProperty(
        default = "*.f_bin",
        options = {'HIDDEN'},
    )

    def execute(self, context):
        sce = bpy.context.scene
        armature = getSourceArmature(bpy.context)
        
        if armature == None:
            self.report({'ERROR'}, "No valid armature selected")
            return {'FINISHED'}
        
        animLength = get_keyframes(armature)[-1]

        characterId = 0
        face_base_pos = getCharacterFacePos(characterId)
        
        frames = []
        for f in range(sce.frame_start, animLength+1):
            sce.frame_set(f)
            frames.append(getFaceAnimFrameFromBones(armature, face_base_pos))
        
        newAnimation = TekkenAnimation(type="face")
        newAnimation.setLength(animLength)
        newAnimation.recalculateSize()
        
        for f in range(animLength):
            for fieldId, fieldValue in enumerate(frames[f]):
                newAnimation.setField(fieldValue, f, fieldId)
            
        with open(self.filepath, "wb") as f:
            f.write(bytes(newAnimation.data))
            
        self.report({'INFO'}, "Facial Animation successfuly exported")
        return {'FINISHED'}
    
class LeftHandAnimationExporter(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "animation_reader.export_lhand_animation"  # important since its how bpy.ops.animation_reader.read_animation is constructed
    bl_label = "Export Left-Hand Animation"

    # ImportHelper mixin class uses this
    filename_ext = ".h_bin"

    filter_glob: StringProperty(
        default = "*.h_bin",
        options = {'HIDDEN'},
    )

    def execute(self, context):
        sce = bpy.context.scene
        armature = getSourceArmature(bpy.context)
        
        if armature == None:
            self.report({'ERROR'}, "No valid armature selected")
            return {'FINISHED'}
        
        animLength = get_keyframes(armature)[-1]

        frames = []
        for f in range(sce.frame_start, animLength+1):
            sce.frame_set(f)
            frames.append(getLeftHandAnimFrameFromBones(armature))
        
        newAnimation = TekkenAnimation(type="hand")
        newAnimation.setLength(animLength)
        newAnimation.recalculateSize()
        
        for f in range(animLength):
            for fieldId, fieldValue in enumerate(frames[f]):
                newAnimation.setField(fieldValue, f, fieldId)
            
        with open(self.filepath, "wb") as f:
            f.write(bytes(newAnimation.data))
            
        self.report({'INFO'}, "Left-Hand Animation successfuly exported")
        return {'FINISHED'}
    
class RightHandAnimationExporter(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "animation_reader.export_rhand_animation"  # important since its how bpy.ops.animation_reader.read_animation is constructed
    bl_label = "Export Right-Hand Animation"

    # ImportHelper mixin class uses this
    filename_ext = ".h_bin"

    filter_glob: StringProperty(
        default = "*.h_bin",
        options = {'HIDDEN'},
    )

    def execute(self, context):
        sce = bpy.context.scene
        armature = getSourceArmature(bpy.context)
        
        if armature == None:
            self.report({'ERROR'}, "No valid armature selected")
            return {'FINISHED'}
        
        animLength = get_keyframes(armature)[-1]

        frames = []
        for f in range(sce.frame_start, animLength+1):
            sce.frame_set(f)
            frames.append(getRightHandAnimFrameFromBones(armature))
        
        newAnimation = TekkenAnimation(type="hand")
        newAnimation.setLength(animLength)
        newAnimation.recalculateSize()
        
        for f in range(animLength):
            for fieldId, fieldValue in enumerate(frames[f]):
                newAnimation.setField(fieldValue, f, fieldId)
            
        with open(self.filepath, "wb") as f:
            f.write(bytes(newAnimation.data))
            
        self.report({'INFO'}, "Right-Hand Animation successfuly exported")
        return {'FINISHED'}