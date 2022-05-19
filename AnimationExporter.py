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
    
    keepEndPos : bpy.props.EnumProperty(
            name="Keep end position",
            description="Choose if the character will reset to its original position when the animation ends",
            items=(
                ("OPT_0", "Keep end pos", "Character stays where they are at the animation's end"),
                ("OPT_1", "Reset end pos", "Character goes back original position"),
            ),
            default='OPT_0',
            )

    def execute(self, context):
        sce = bpy.context.scene
        armature = getSourceArmature(bpy.context)
        
        if armature == None:
            self.report({'ERROR'}, "No valid armature selected")
            return {'FINISHED'}
        
        try:
            animLength = get_keyframes(armature)[-1]
        except:
            self.report({'ERROR'}, "No keyframe for animation")
            return {'FINISHED'}

        frames = []
        keepEndPos = self.keepEndPos == 'OPT_0'
        
        for f in range(sce.frame_start, animLength+1):
            sce.frame_set(f)
            frames.append(getAnimFrameFromBones(armature, keepEndPos))
        
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

    type : bpy.props.EnumProperty(
            name="Target character",
            description="Choose the character the animation will play on",
            items=(
                ("OPT_0", "Paul", "Paul"),
                ("OPT_1", "Law", "Law"),
                ("OPT_2", "King", "King"),
                ("OPT_3", "Yoshimitsu", "Yoshimitsu"),
                ("OPT_4", "Hwoarang", "Hwoarang"),
                ("OPT_5", "Xiaoyu", "Xiaoyu"),
                ("OPT_6", "Jin", "Jin"),
                ("OPT_7", "Bryan", "Bryan"),
                ("OPT_8", "Heihachi", "Heihachi"),
                ("OPT_9", "Kazuya", "Kazuya"),
                ("OPT_10", "Steve", "Steve"),
                ("OPT_11", "Jack-7", "Jack-7"),
                ("OPT_12", "Asuka", "Asuka"),
                ("OPT_13", "Devil Jin", "Devil Jin"),
                ("OPT_14", "Feng", "Feng"),
                ("OPT_15", "Lili", "Lili"),
                ("OPT_16", "Dragunov", "Dragunov"),
                ("OPT_17", "Leo", "Leo"),
                ("OPT_18", "Lars", "Lars"),
                ("OPT_19", "Alisa", "Alisa"),
                ("OPT_20", "Claudio", "Claudio"),
                ("OPT_21", "Katarina", "Katarina"),
                ("OPT_22", "Lucky Chloe", "Lucky Chloe"),
                ("OPT_23", "Shaheen", "Shaheen"),
                ("OPT_24", "Josie", "Josie"),
                ("OPT_25", "Gigas", "Gigas"),
                ("OPT_26", "Kazumi", "Kazumi"),
                ("OPT_27", "Devil Kazumi", "Devil Kazumi"),
                ("OPT_28", "Nina", "Nina"),
                ("OPT_29", "Master Raven", "Master Raven"),
                ("OPT_30", "Lee", "Lee"),
                ("OPT_31", "Bob", "Bob"),
                ("OPT_32", "Akuma", "Akuma"),
                ("OPT_33", "Kuma", "Kuma"),
                ("OPT_34", "Panda", "Panda"),
                ("OPT_35", "Eddy", "Eddy"),
                ("OPT_36", "Elisa", "Elisa"),
                ("OPT_37", "Miguel", "Miguel"),
                ("OPT_38", "Soldier", "Soldier"),
                ("OPT_39", "Child Kazuya", "Child Kazuya"),
                ("OPT_40", "Jack-5", "Jack-5"),
                ("OPT_41", "Young Heihachi", "Young Heihachi"),
                ("OPT_42", "Dummy", "Dummy"),
                ("OPT_43", "Geese", "Geese"),
                ("OPT_44", "Noctis", "Noctis"),
                ("OPT_45", "Anna", "Anna"),
                ("OPT_46", "Lei", "Lei"),
                ("OPT_47", "Marduk", "Marduk"),
                ("OPT_48", "Armor King", "Armor King"),
                ("OPT_49", "Julia", "Julia"),
                ("OPT_50", "Negan", "Negan"),
                ("OPT_51", "Zafina", "Zafina"),
                ("OPT_52", "Ganryu", "Ganryu"),
                ("OPT_53", "Leroy", "Leroy"),
                ("OPT_54", "Fahkumram", "Fahkumram"),
                ("OPT_55", "Kunimitsu", "Kunimitsu"),
                ("OPT_56", "Lidia", "Lidia"),
            ),
            default='OPT_0',
            )
    
    
    def execute(self, context):
        sce = bpy.context.scene
        armature = getSourceArmature(bpy.context)
        
        if armature == None:
            self.report({'ERROR'}, "No valid armature selected")
            return {'FINISHED'}
        
        try:
            animLength = get_keyframes(armature)[-1]
        except:
            self.report({'ERROR'}, "No keyframe for animation")
            return {'FINISHED'}

        characterId = int(self.type[4:])
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
        
        try:
            animLength = get_keyframes(armature)[-1]
        except:
            self.report({'ERROR'}, "No keyframe for animation")
            return {'FINISHED'}

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
        
        try:
            animLength = get_keyframes(armature)[-1]
        except:
            self.report({'ERROR'}, "No keyframe for animation")
            return {'FINISHED'}

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