import bpy
from math import pi, atan2, asin
import numpy as np

# ImportHelper is a helper class, defines filename and invoke() function which calls the file selector.
from bpy.props import StringProperty
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper

from .Animation0xC80x17 import Animation0xC80x17

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
            currentAnimationFrame = animation.AnimationFrames[currentAnimationFrameIndex]

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
            
            movement = [0, 0, 0]
            movement[0] = currentAnimationFrame.properties['Offset'].z * 0.001
            movement[1] = currentAnimationFrame.properties['Offset'].y * 0.001
            movement[2] = currentAnimationFrame.properties['Offset'].x * 0.001
            movement = [0, 0, 0]

            offset_bone.location[0] = currentAnimationFrame.properties['JumpStrength'].z * 0.001
            offset_bone.location[1] = currentAnimationFrame.properties['JumpStrength'].y * 0.001 - 1.15
            offset_bone.location[2] = currentAnimationFrame.properties['JumpStrength'].x * 0.001
            
            offset_bone.location[0] += movement[0]
            offset_bone.location[1] += movement[1]
            offset_bone.location[2] += movement[2]
            
            base_bone.rotation_euler.x = currentAnimationFrame.properties['Mesh'].z
            base_bone.rotation_euler.y = 0 #currentAnimationFrame.properties['Mesh'].y #temporary
            base_bone.rotation_euler.z = currentAnimationFrame.properties['Mesh'].x

            """
            upper_body_bone.rotation_euler.x = currentAnimationFrame.properties['Mesh'].z
            upper_body_bone.rotation_euler.y = currentAnimationFrame.properties['Mesh'].y
            upper_body_bone.rotation_euler.z = currentAnimationFrame.properties['Mesh'].x * -1
            """
            
            upper_body_bone.rotation_euler.x = currentAnimationFrame.properties['UpperBody'].x
            upper_body_bone.rotation_euler.y = currentAnimationFrame.properties['UpperBody'].y
            upper_body_bone.rotation_euler.z = currentAnimationFrame.properties['UpperBody'].z - (pi / 2)

            lower_body_bone.rotation_euler.x = currentAnimationFrame.properties['LowerBody'].x
            lower_body_bone.rotation_euler.y = currentAnimationFrame.properties['LowerBody'].y
            lower_body_bone.rotation_euler.z = currentAnimationFrame.properties['LowerBody'].z + (pi / 2)

            neck_bone.rotation_euler.x = currentAnimationFrame.properties['Neck'].x
            neck_bone.rotation_euler.y = currentAnimationFrame.properties['Neck'].y
            neck_bone.rotation_euler.z = currentAnimationFrame.properties['Neck'].z

            head_bone.rotation_euler.x = currentAnimationFrame.properties['Head'].x - (pi / 2)
            head_bone.rotation_euler.y = currentAnimationFrame.properties['Head'].z - (pi / 2)
            head_bone.rotation_euler.z = currentAnimationFrame.properties['Head'].y * -1

            # --------------------------------------------------------
            
            right_inner_shoulder.rotation_euler.x = 0
            right_inner_shoulder.rotation_euler.y = 0
            right_inner_shoulder.rotation_euler.z = 0

            right_outer_shoulder.rotation_euler.x = currentAnimationFrame.properties['RightOuterShoulder'].x + pi / 2
            right_outer_shoulder.rotation_euler.y = currentAnimationFrame.properties['RightOuterShoulder'].z
            right_outer_shoulder.rotation_euler.z = currentAnimationFrame.properties['RightOuterShoulder'].y


            right_elbow.rotation_euler.x = currentAnimationFrame.properties['RightElbow'].x
            right_elbow.rotation_euler.y = currentAnimationFrame.properties['RightElbow'].y
            right_elbow.rotation_euler.z = currentAnimationFrame.properties['RightElbow'].z

            right_hand.rotation_euler.x = currentAnimationFrame.properties['RightHand'].x - (pi / 2)
            right_hand.rotation_euler.y = currentAnimationFrame.properties['RightHand'].z
            right_hand.rotation_euler.z = currentAnimationFrame.properties['RightHand'].y * -1
            # --------------------------------------------------------
            
            left_inner_shoulder.rotation_euler.x = 0
            left_inner_shoulder.rotation_euler.y = 0
            left_inner_shoulder.rotation_euler.z = 0

            left_outer_shoulder.rotation_euler.x = currentAnimationFrame.properties['LeftOuterShoulder'].x + pi / 2
            left_outer_shoulder.rotation_euler.y = currentAnimationFrame.properties['LeftOuterShoulder'].z
            left_outer_shoulder.rotation_euler.z = currentAnimationFrame.properties['LeftOuterShoulder'].y

            left_elbow.rotation_euler.x = currentAnimationFrame.properties['LeftElbow'].x
            left_elbow.rotation_euler.y = currentAnimationFrame.properties['LeftElbow'].y
            left_elbow.rotation_euler.z = currentAnimationFrame.properties['LeftElbow'].z

            left_hand.rotation_euler.x = currentAnimationFrame.properties['LeftHand'].x - (pi / 2)
            left_hand.rotation_euler.y = currentAnimationFrame.properties['LeftHand'].z
            left_hand.rotation_euler.z = currentAnimationFrame.properties['LeftHand'].y * -1

            right_hip.rotation_euler.x = currentAnimationFrame.properties['RightHip'].x
            right_hip.rotation_euler.y = currentAnimationFrame.properties['RightHip'].y
            right_hip.rotation_euler.z = currentAnimationFrame.properties['RightHip'].z

            # right_knee.rotation_euler.x = currentAnimationFrame.properties['RightKnee'].x
            # right_knee.rotation_euler.y = currentAnimationFrame.properties['RightKnee'].y shouldn't set because it doesn't bent in Tekken
            right_knee.rotation_euler.z = currentAnimationFrame.properties['RightKnee'].z

            right_foot.rotation_euler.x = currentAnimationFrame.properties['RightFoot'].x
            right_foot.rotation_euler.y = currentAnimationFrame.properties['RightFoot'].y
            right_foot.rotation_euler.z = currentAnimationFrame.properties['RightFoot'].z

            left_hip.rotation_euler.x = currentAnimationFrame.properties['LeftHip'].x
            left_hip.rotation_euler.y = currentAnimationFrame.properties['LeftHip'].y
            left_hip.rotation_euler.z = currentAnimationFrame.properties['LeftHip'].z

            left_knee.rotation_euler.z = currentAnimationFrame.properties['LeftKnee'].z

            left_foot.rotation_euler.x = currentAnimationFrame.properties['LeftFoot'].x
            left_foot.rotation_euler.y = currentAnimationFrame.properties['LeftFoot'].y
            left_foot.rotation_euler.z = currentAnimationFrame.properties['LeftFoot'].z

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