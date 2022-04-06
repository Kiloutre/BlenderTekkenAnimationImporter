import bpy
from math import pi, atan2, asin
import numpy as np

# ImportHelper is a helper class, defines filename and invoke() function which calls the file selector.
from bpy.props import StringProperty
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper

from .Animation0xC80x17 import Animation0xC80x17

def quaternion_rotation_matrix(Q):
    # Extract the values from Q
    q0 = Q[0]
    q1 = Q[1]
    q2 = Q[2]
    q3 = Q[3]
     
    # First row of the rotation matrix
    r00 = 2 * (q0 * q0 + q1 * q1) - 1
    r01 = 2 * (q1 * q2 - q0 * q3)
    r02 = 2 * (q1 * q3 + q0 * q2)
     
    # Second row of the rotation matrix
    r10 = 2 * (q1 * q2 + q0 * q3)
    r11 = 2 * (q0 * q0 + q2 * q2) - 1
    r12 = 2 * (q2 * q3 - q0 * q1)
     
    # Third row of the rotation matrix
    r20 = 2 * (q1 * q3 - q0 * q2)
    r21 = 2 * (q2 * q3 + q0 * q1)
    r22 = 2 * (q0 * q0 + q3 * q3) - 1
     
    # 3x3 rotation matrix
    rot_matrix = np.array([[r00, r01, r02],
                           [r10, r11, r12],
                           [r20, r21, r22]])
                            
    return rot_matrix
    
def get_quaternion_from_euler(roll, pitch, yaw):
  qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
  qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
  qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
  qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
  return [qx, qy, qz, qw]
  
def quaternionToMatrix(quaternion):
    te = [0] * 9

    x = quaternion[0]
    y = quaternion[1]
    z = quaternion[2]
    w = quaternion[3]

    x2 = x + x
    y2 = y + y
    z2 = z + z

    xx = x * x2
    xy = x * y2
    xz = x * z2
    yy = y * y2
    yz = y * z2
    zz = z * z2
    wx = w * x2
    wy = w * y2
    wz = w * z2

    te[ 0 ] = ( 1 - ( yy + zz ) )
    te[ 1 ] = ( xy + wz )
    te[ 2 ] = ( xz - wy )

    te[ 3 ] = ( xy - wz )
    te[ 4 ] = ( 1 - ( xx + zz ) )
    te[ 5 ] = ( yz + wx )

    te[ 6 ] = ( xz + wy )
    te[ 7 ] = ( yz - wx )
    te[ 8 ] = ( 1 - ( xx + yy ) )

    return te
    #return [[te[i] for i in range(x, 9, 3)] for x in range(3)]
    
def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)
   
def getRotationFromMatrix(te):
    m11 = te[ 0 ]
    m12 = te[ 3 ]
    m13 = te[ 6 ]
    
    m21 = te[ 1 ]
    m22 = te[ 4 ]
    m23 = te[ 7 ]
    
    m31 = te[ 2 ]
    m32 = te[ 5 ]
    m33 = te[ 8 ]
    

    y = asin( clamp( m13, - 1, 1 ) )

    if abs( m13 ) < 0.9999999:
        x = atan2( - m23, m33 )
        z = atan2( - m12, m11 )
    else:
        x = atan2( m32, m22 )
        z = 0
        
    return x, y, z
    
def worldRotationToEuler(x, y, z):
    quaternion = get_quaternion_from_euler(x, y, z)
    matrix = quaternionToMatrix(quaternion)
    return getRotationFromMatrix(matrix)

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
            
            #three angles at the same time fuck shit up
            #MAUVAIS
            
            xval = currentAnimationFrame.properties['RightInnerShoulder'].x
            zval = currentAnimationFrame.properties['RightInnerShoulder'].y - (pi / 2)
            yval = currentAnimationFrame.properties['RightInnerShoulder'].z - (pi / 2)
            #print(xval)
            #print(zval)
            #print(yval)
            
            x, y, z = worldRotationToEuler(xval, zval, yval)
            #print(x, y, z)
            
            right_inner_shoulder.rotation_euler.x = -z
            right_inner_shoulder.rotation_euler.y = y
            right_inner_shoulder.rotation_euler.z = x
            right_inner_shoulder.bone.select = True

            #three angles at the same time fuck shit up
            right_outer_shoulder.rotation_euler.x = 0#currentAnimationFrame.properties['RightOuterShoulder'].x + pi / 2
            right_outer_shoulder.rotation_euler.y = 0#currentAnimationFrame.properties['RightOuterShoulder'].z
            right_outer_shoulder.rotation_euler.z = 0#currentAnimationFrame.properties['RightOuterShoulder'].y


            # --------------------------------------------------------
            #BON
            right_elbow.rotation_euler.x = currentAnimationFrame.properties['RightElbow'].x
            right_elbow.rotation_euler.y = currentAnimationFrame.properties['RightElbow'].y
            right_elbow.rotation_euler.z = currentAnimationFrame.properties['RightElbow'].z

            right_hand.rotation_euler.x = currentAnimationFrame.properties['RightHand'].x - (pi / 2)
            right_hand.rotation_euler.y = currentAnimationFrame.properties['RightHand'].z
            right_hand.rotation_euler.z = currentAnimationFrame.properties['RightHand'].y * -1
            # --------------------------------------------------------
            #MAUVAIS
            
            #three angles at the same time fuck shit up
            left_inner_shoulder.rotation_euler.x = 0
            left_inner_shoulder.rotation_euler.y = 0
            left_inner_shoulder.rotation_euler.z = 0

            #three angles at the same time fuck shit up
            left_outer_shoulder.rotation_euler.x = 0#currentAnimationFrame.properties['LeftOuterShoulder'].x + pi / 2
            left_outer_shoulder.rotation_euler.y = 0#currentAnimationFrame.properties['LeftOuterShoulder'].z
            left_outer_shoulder.rotation_euler.z = 0#currentAnimationFrame.properties['LeftOuterShoulder'].y
            
            # --------------------------------------------------------

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