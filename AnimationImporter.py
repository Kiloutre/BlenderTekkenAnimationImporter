import bpy
from math import pi, atan2, asin
import numpy as np

# ImportHelper is a helper class, defines filename and invoke() function which calls the file selector.
from bpy.props import StringProperty
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper

from .Animation0xC80x17 import Animation0xC80x17
from .TekkenAnimHelper import applyRotationFromAnimdata

class AnimationImporter(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "animation_reader.read_animation"  # important since its how bpy.ops.animation_reader.read_animation is constructed
    bl_label = "Import Animation"

    # ImportHelper mixin class uses this
    filename_ext = ".bin"

    filter_glob: StringProperty(
        default = "*.bin",
        options = {'HIDDEN'},
    )

    def __init__(self):

        self.needed_bones_list = list([
            'BODY_SCALE__group',
            'Spine1',
            'Hip',
            'BASE'
        ])

    def execute(self, context):
        animation_binary_data = self.__get_binary_data_from_animation_file(context, self.filepath)
        animation = self.__get_animation(animation_binary_data)
        print(animation)

        self.insert_key_frames_for_animation(animation)

        operation_status = {'FINISHED'}
        return operation_status

    def check_if_armature_has_all_bones_needed(self, armature_name):
        armature = bpy.data.objects['armature_name']

    def insert_key_frames_for_animation(self, animation: Animation0xC80x17):
        bpy.context.scene.frame_end = len(animation.AnimationFrames)
        
        for currentAnimationFrameIndex in range(len(animation.AnimationFrames)):
            currentAnimationFrame = animation.AnimationFrames[currentAnimationFrameIndex].properties

            armature = bpy.data.objects['Armature']
            offset_bone = armature.pose.bones['BODY_SCALE__group']
            base_bone = armature.pose.bones['BASE']
            upper_body_bone = armature.pose.bones['Spine1']
            lower_body_bone = armature.pose.bones['Hip']
            neck_bone = armature.pose.bones['Neck']
            head_bone = armature.pose.bones['Head']

            right_inner_shoulder = armature.pose.bones['R_Shoulder']
            right_outer_shoulder = armature.pose.bones['R_Arm']
            right_elbow = armature.pose.bones['R_ForeArm']
            right_hand = armature.pose.bones['R_Hand']

            left_inner_shoulder = armature.pose.bones['L_Shoulder']
            left_outer_shoulder = armature.pose.bones['L_Arm']
            left_elbow = armature.pose.bones['L_ForeArm']
            left_hand = armature.pose.bones['L_Hand']

            right_hip = armature.pose.bones['R_UpLeg']
            right_knee = armature.pose.bones['R_Leg']
            right_foot = armature.pose.bones['R_Foot']

            left_hip = armature.pose.bones['L_UpLeg']
            left_knee = armature.pose.bones['L_Leg']
            left_foot = armature.pose.bones['L_Foot']
            
            applyRotationFromAnimdata(armature, [
                currentAnimationFrame['Offset'].x,
                currentAnimationFrame['Offset'].y,
                currentAnimationFrame['Offset'].z,
                currentAnimationFrame['JumpStrength'].x,
                currentAnimationFrame['JumpStrength'].y,
                currentAnimationFrame['JumpStrength'].z,
                currentAnimationFrame['Unknown'].x,
                currentAnimationFrame['Unknown'].y,
                currentAnimationFrame['Unknown'].z,
                currentAnimationFrame['Mesh'].x,
                currentAnimationFrame['Mesh'].y,
                currentAnimationFrame['Mesh'].z,
                currentAnimationFrame['UpperBody'].x,
                currentAnimationFrame['UpperBody'].y,
                currentAnimationFrame['UpperBody'].z,
                currentAnimationFrame['LowerBody'].x,
                currentAnimationFrame['LowerBody'].y,
                currentAnimationFrame['LowerBody'].z,
                currentAnimationFrame['SpineFlexure'].x,
                currentAnimationFrame['SpineFlexure'].y,
                currentAnimationFrame['SpineFlexure'].z,
                currentAnimationFrame['Neck'].x,
                currentAnimationFrame['Neck'].y,
                currentAnimationFrame['Neck'].z,
                currentAnimationFrame['Head'].x,
                currentAnimationFrame['Head'].y,
                currentAnimationFrame['Head'].z,
                currentAnimationFrame['RightInnerShoulder'].x,
                currentAnimationFrame['RightInnerShoulder'].y,
                currentAnimationFrame['RightInnerShoulder'].z,
                currentAnimationFrame['RightOuterShoulder'].x,
                currentAnimationFrame['RightOuterShoulder'].y,
                currentAnimationFrame['RightOuterShoulder'].z,
                currentAnimationFrame['RightElbow'].x,
                currentAnimationFrame['RightElbow'].y,
                currentAnimationFrame['RightElbow'].z,
                currentAnimationFrame['RightHand'].x,
                currentAnimationFrame['RightHand'].y,
                currentAnimationFrame['RightHand'].z,
                currentAnimationFrame['LeftInnerShoulder'].x,
                currentAnimationFrame['LeftInnerShoulder'].y,
                currentAnimationFrame['LeftInnerShoulder'].z,
                currentAnimationFrame['LeftOuterShoulder'].x,
                currentAnimationFrame['LeftOuterShoulder'].y,
                currentAnimationFrame['LeftOuterShoulder'].z,
                currentAnimationFrame['LeftElbow'].x,
                currentAnimationFrame['LeftElbow'].y,
                currentAnimationFrame['LeftElbow'].z,
                currentAnimationFrame['LeftHand'].x,
                currentAnimationFrame['LeftHand'].y,
                currentAnimationFrame['LeftHand'].z,
                currentAnimationFrame['RightHip'].x,
                currentAnimationFrame['RightHip'].y,
                currentAnimationFrame['RightHip'].z,
                currentAnimationFrame['RightKnee'].x,
                currentAnimationFrame['RightKnee'].y,
                currentAnimationFrame['RightKnee'].z,
                currentAnimationFrame['RightFoot'].x,
                currentAnimationFrame['RightFoot'].y,
                currentAnimationFrame['RightFoot'].z,
                currentAnimationFrame['LeftHip'].x,
                currentAnimationFrame['LeftHip'].y,
                currentAnimationFrame['LeftHip'].z,
                currentAnimationFrame['LeftKnee'].x,
                currentAnimationFrame['LeftKnee'].y,
                currentAnimationFrame['LeftKnee'].z,
                currentAnimationFrame['LeftFoot'].x,
                currentAnimationFrame['LeftFoot'].y,
                currentAnimationFrame['LeftFoot'].z,
            ])

            offset_bone.keyframe_insert(data_path = 'location', frame = currentAnimationFrameIndex + 1)
            base_bone.keyframe_insert(data_path = 'rotation_euler', frame = currentAnimationFrameIndex + 1)
            upper_body_bone.keyframe_insert(data_path = 'rotation_euler', frame = currentAnimationFrameIndex + 1)
            lower_body_bone.keyframe_insert(data_path = 'rotation_euler', frame = currentAnimationFrameIndex + 1)
            neck_bone.keyframe_insert(data_path = 'rotation_euler', frame = currentAnimationFrameIndex + 1)
            head_bone.keyframe_insert(data_path = 'rotation_euler', frame = currentAnimationFrameIndex + 1)

            right_inner_shoulder.keyframe_insert(data_path = 'rotation_euler', frame = currentAnimationFrameIndex + 1)
            right_outer_shoulder.keyframe_insert(data_path = 'rotation_euler', frame = currentAnimationFrameIndex + 1)
            right_elbow.keyframe_insert(data_path = 'rotation_euler', frame = currentAnimationFrameIndex + 1)
            right_hand.keyframe_insert(data_path = 'rotation_euler', frame = currentAnimationFrameIndex + 1)

            left_inner_shoulder.keyframe_insert(data_path = 'rotation_euler', frame = currentAnimationFrameIndex + 1)
            left_outer_shoulder.keyframe_insert(data_path = 'rotation_euler', frame = currentAnimationFrameIndex + 1)
            left_elbow.keyframe_insert(data_path = 'rotation_euler', frame = currentAnimationFrameIndex + 1)
            left_hand.keyframe_insert(data_path = 'rotation_euler', frame = currentAnimationFrameIndex + 1)

            right_hip.keyframe_insert(data_path = 'rotation_euler', frame = currentAnimationFrameIndex + 1)
            right_knee.keyframe_insert(data_path = 'rotation_euler', frame = currentAnimationFrameIndex + 1)
            right_foot.keyframe_insert(data_path = 'rotation_euler', frame = currentAnimationFrameIndex + 1)

            left_hip.keyframe_insert(data_path = 'rotation_euler', frame = currentAnimationFrameIndex + 1)
            left_knee.keyframe_insert(data_path = 'rotation_euler', frame = currentAnimationFrameIndex + 1)
            left_foot.keyframe_insert(data_path = 'rotation_euler', frame = currentAnimationFrameIndex + 1)

    def __get_binary_data_from_animation_file(self, context, filepath = None):
        with open(filepath, 'rb') as animationFile:
            binary_data = animationFile.read()
            return binary_data

    def __get_animation(self, binary_data) -> Animation0xC80x17:
        # "< 2B H 24I" stands for little endian, 2 unsigned bytes, unsigned short, 24 unsigned 4-byte integers
        animation = Animation0xC80x17(binary_data)

        return animation