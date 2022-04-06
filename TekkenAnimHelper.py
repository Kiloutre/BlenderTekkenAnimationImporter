import pathlib
import struct
import bpy
import numpy as np
from math import pi, asin, atan2

def quaternionToRotationMatrix(Q):
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

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)
   
def getRotationFromMatrix(te, mode = 0):
    m11 = te[ 0 ][0]
    m12 = te[ 0 ][1]
    m13 = te[ 0 ][2]
    
    m21 = te[ 1 ][0]
    m22 = te[ 1 ][1]
    m23 = te[ 1 ][2]
    
    m31 = te[ 2 ][0]
    m32 = te[ 2 ][1]
    m33 = te[ 2 ][2]

    if mode == 0: #XYZ
        y = asin( clamp( m13, - 1, 1 ) )
        if abs( m13 ) < 0.9999999:
            x = atan2( - m23, m33 )
            z = atan2( - m12, m11 )
        else:
            x = atan2( m32, m22 )
            z = 0
            
    elif mode == 1: #YXZ
        x = asin( - clamp( m23, - 1, 1 ) )
        if abs( m23 ) < 0.9999999:
            y = atan2( m13, m33 )
            z = atan2( m21, m22 )
        else:
            y = atan2( - m31, m11 )
            z = 0
            
    elif mode == 2: #ZXY
        x = asin( clamp( m32, - 1, 1 ) )
        if abs( m32 ) < 0.9999999:
            y = atan2( - m31, m33 )
            z = atan2( - m12, m22 )
        else:
            y = 0
            z = atan2( m21, m11 )
            
    elif mode == 3: #ZYX
        y = asin( -  clamp( m31, - 1, 1 ) )
        if abs( m31 ) < 0.9999999:
            x = atan2( m32, m33 )
            z = atan2( m21, m11 )
        else:
            x = 0
            z = atan2( - m12, m22 )
            
    elif mode == 4: #YZX
        z = asin( clamp( m21, - 1, 1 ) )
        if abs( m21 ) < 0.9999999:
            x = atan2( - m23, m22 )
            y = atan2( - m31, m11 )
        else:
            x = 0
            y = atan2( m13, m33 )
            
    elif mode == 5: #XZY
        z = asin( - clamp( m12, - 1, 1 ) )
        if abs( m12 ) < 0.9999999:
            x = atan2( m32, m22 )
            y = atan2( m13, m11 )
        else:
            x = atan2( - m23, m33 )
            y = 0
        
    return x, y, z

# --------

def getAnimTemplate():
    filename = pathlib.Path(__file__).parent.resolve().__str__() + "\\source_anim.bin"
    data = None
    with open(filename, "rb") as f:
        data = list(f.read())
    return data

animTemplate = getAnimTemplate()
    
class TekkenAnimation:
    AnimC8OffsetTable = {
        0x17: 0x64,
        0x19: 0x6C,
        0x1B: 0x74,
        0x1d: 0x7c,
        0x1f: 0x80,
        0x21: 0x8c,
        0x23: 0x94,
        0x31: 0xcc 
    }

    def __init__(self, data=None):
        if data == None:
            data = animTemplate
            pass
            
        self.data = data
        self.type = self.byte(0)
        self.type2 = self.byte(2)
        self.length = self.getLength()
        self.offset = self.getOffset()
        self.frame_size = self.getFramesize()
        self.field_count = int(self.frame_size / 4)
        self.recalculateSize() #Crop or add missing bytes if needed
        
    def setLength(self, length):
        self.length = length
        self.writeInt(length,4)
        
    def recalculateSize(self):
        pastSize = len(self.data)
        self.size = self.calculateSize()
        if self.size > pastSize:
            self.data += [0] * (self.size - pastSize)
        elif self.size < pastSize:
            self.data = self.data[:self.size]

    def calculateSize(self):
        return self.getOffset() + (self.getFramesize() * self.length)
        
    def getOffset(self):
        return TekkenAnimation.AnimC8OffsetTable[self.type2]
        
    def getFramesize(self):
        return self.type2 * 0xC
        
    def getLength(self):
        return self.int(4)
    
    def bToInt(self, offset, length):
        return int.from_bytes(bytes(self.data[offset:offset+length]), 'little')
    
    def int(self, offset):
        return self.bToInt(offset, 4)
    
    def short(self, offset):
        return self.bToInt(offset, 2)
        
    def byte(self, offset):
        return self.bToInt(offset, 1)
        
    def float(self, offset):
        return struct.unpack('f', bytes(self.data[offset:offset + 4]))[0]
            
    def writeInt(self, value, offset):
        for i in range(4):
            byteValue = (value >> (i * 8)) & 0xFF
            self.data[offset + i] = byteValue
            
    def writeFloat(self, value, offset):
        byteData = struct.pack('f', value)
        for i in range(4):
            self.data[offset + i] = int(byteData[i])
        
    def getFieldOffset(self, frame, fieldId):
        if fieldId > self.field_count:
            raise
        return self.offset + (frame * self.frame_size) + (4 * fieldId)
        
    def getField(self, frame, fieldId):
        if fieldId > self.field_count:
            raise
        return self.float(self.getFieldOffset(frame, fieldId))
                
    def setField(self, value, frame, fieldId):
        if fieldId > self.field_count:
            raise
        self.writeFloat(value, self.offset + (frame * self.frame_size) + (4 * fieldId))
             
def __get_visual_rotations__(armature, bones):
    poses = {}
    for prefix in ["L_", "R_"]: # set default values
        for bone in ["UpLeg", "Leg", "Foot", "Hand", "ForeArm", "Arm", "Shoulder"]:
            b = prefix + bone
            #rot_source = bones[b].rotation_euler
            rot_source = getEulerVisualRotation(b, armature.name)
            poses[b] = { 'x': rot_source.x, 'y': rot_source.y, 'z': rot_source.z}
    return poses
    
    
def getEulerVisualRotation(boneName, armatureName):
    bone        = bpy.data.armatures[armatureName].bones[boneName]
    bone_ml     = bone.matrix_local
    bone_pose   = bpy.data.objects[armatureName].pose.bones[boneName]
    bone_pose_m = bone_pose.matrix
    #
    if bone.parent:
        #
        parent        = bone.parent
        parent_ml     = parent.matrix_local
        parent_pose   = bone_pose.parent
        parent_pose_m = parent_pose.matrix
        #
        object_diff = parent_ml.inverted() @ bone_ml
        pose_diff   = parent_pose_m.inverted() @ bone_pose_m
        local_diff  = object_diff.inverted() @ pose_diff
        #
    else:
        local_diff = bone_ml.inverted() @ bone_pose_m
    #
    return local_diff.to_quaternion().to_euler(bone_pose.rotation_mode)
    
def convertArmToTekkenXYZ(x, y, z):
    x, y, z = -x, -z, y
    
    orig_quat = get_quaternion_from_euler(pi / 2, 0, pi / 2)
    orig_mat = quaternionToRotationMatrix(orig_quat)
    orig_mat = np.linalg.inv(orig_mat)

    quat = get_quaternion_from_euler(x, y, z)
    mat = quaternionToRotationMatrix(quat)

    mat = np.matmul(mat, orig_mat)
    
    x, y, z = getRotationFromMatrix(mat, mode=3)
    
    return x, -y, -z
             
def getAnimFrameFromBones(armature):
    bones = armature.pose.bones
    
    visualRots = __get_visual_rotations__(armature, bones)

    offset1 = -(bones["BODY_SCALE__group"].location[2] * 1000)
    offset2 = (bones["BODY_SCALE__group"].location[1]) * 1000 + 1150
    offset3 = bones["BODY_SCALE__group"].location[0] * 1000
    
    RotX = bones["BASE"].rotation_euler.z * -1
    RotY = bones["BASE"].rotation_euler.y
    RotZ = bones["BASE"].rotation_euler.x 
    
    UpperBody1 = bones["Spine1"].rotation_euler.z * -1
    UpperBody2 = bones["Spine1"].rotation_euler.y
    UpperBody3 = bones["Spine1"].rotation_euler.x + (pi / 2)
    
    LowerBody1 = bones["Hip"].rotation_euler.z * -1
    LowerBody2 = bones["Hip"].rotation_euler.y
    LowerBody3 = bones["Hip"].rotation_euler.x - (pi / 2)
    
    Neck1 = bones["Neck"].rotation_euler.x
    Neck2 = bones["Neck"].rotation_euler.y
    Neck3 = bones["Neck"].rotation_euler.z
    
    Head1 = bones["Head"].rotation_euler.x + (pi / 2)
    Head2 = bones["Head"].rotation_euler.z * -1
    Head3 = bones["Head"].rotation_euler.y + (pi / 2)
    
    # --------- SHOULDER ------------
    
    #x, y, z = bones["R_Shoulder"].rotation_euler
    x, y, z = visualRots["R_Shoulder"]['x'], visualRots["R_Shoulder"]['y'], visualRots["R_Shoulder"]['z']
    x, y, z = convertArmToTekkenXYZ(x, y, z)
    RightInnerShoulder1 = x + pi
    RightInnerShoulder2 = y
    RightInnerShoulder3 = z
    
    # --------- ARM IK -----------
    
    """
    RightOuterShoulder1 = bones["R_Arm"].rotation_euler.x * -1 - pi / 2
    RightOuterShoulder2 = bones["R_Arm"].rotation_euler.z * -1
    RightOuterShoulder3 = bones["R_Arm"].rotation_euler.y * -1
    
    RightElbow1 = bones["R_ForeArm"].rotation_euler.x * -1
    RightElbow2 = bones["R_ForeArm"].rotation_euler.y
    RightElbow3 = bones["R_ForeArm"].rotation_euler.z * -1
    
    RightHand1 = bones["R_Hand"].rotation_euler.x + pi / 2
    RightHand2 = bones["R_Hand"].rotation_euler.z * -1
    RightHand3 = bones["R_Hand"].rotation_euler.y
    """
    
    RightOuterShoulder1 = visualRots["R_Arm"]['x'] * -1 - pi / 2
    RightOuterShoulder2 = visualRots["R_Arm"]['z'] * -1
    RightOuterShoulder3 = visualRots["R_Arm"]['y'] * -1
    
    RightElbow1 = visualRots["R_ForeArm"]['x'] * -1
    RightElbow2 = visualRots["R_ForeArm"]['y']
    RightElbow3 = visualRots["R_ForeArm"]['z'] * -1
    
    RightHand1 = visualRots["R_Hand"]['x'] + pi / 2
    RightHand2 = visualRots["R_Hand"]['z'] * -1
    RightHand3 = visualRots["R_Hand"]['y']
    
    # --------- SHOULDER ------------
    
    # x, y, z = bones["L_Shoulder"].rotation_euler
    x, y, z = visualRots["L_Shoulder"]['x'], visualRots["L_Shoulder"]['y'], visualRots["L_Shoulder"]['z']
    x, y, z = convertArmToTekkenXYZ(x, y, z)
    
    LeftInnerShoulder1 = x + pi
    LeftInnerShoulder2 = y + pi
    LeftInnerShoulder3 = z * -1
    
    # --------- ARM IK -----------
    """
    LeftOuterShoulder1 = bones["L_Arm"].rotation_euler.x - pi / 2
    LeftOuterShoulder2 = bones["L_Arm"].rotation_euler.z
    LeftOuterShoulder3 = bones["L_Arm"].rotation_euler.y * -1
    
    LeftElbow1 = bones["L_ForeArm"].rotation_euler.x
    LeftElbow2 = bones["L_ForeArm"].rotation_euler.y
    LeftElbow3 = bones["L_ForeArm"].rotation_euler.z
    
    LeftHand1 = bones["L_Hand"].rotation_euler.x * -1 + pi / 2
    LeftHand2 = bones["L_Hand"].rotation_euler.z * -1
    LeftHand3 = bones["L_Hand"].rotation_euler.y * -1
    """
    
    LeftOuterShoulder1 = visualRots["L_Arm"]['x'] - pi / 2
    LeftOuterShoulder2 = visualRots["L_Arm"]['z']
    LeftOuterShoulder3 = visualRots["L_Arm"]['x'] * -1
    
    LeftElbow1 = visualRots["L_ForeArm"]['x']
    LeftElbow2 = visualRots["L_ForeArm"]['y']
    LeftElbow3 = visualRots["L_ForeArm"]['z']
    
    LeftHand1 = visualRots["L_Hand"]['x'] * -1 + pi / 2
    LeftHand2 = visualRots["L_Hand"]['z'] * -1
    LeftHand3 = visualRots["L_Hand"]['y'] * -1

    
    #---------------- LEG IK -----------------
    
    """
    RightHip1 = -bones["R_UpLeg"].rotation_euler.z
    RightHip2 = bones["R_UpLeg"].rotation_euler.y
    RightHip3 = bones["R_UpLeg"].rotation_euler.x
    
    RightKnee1 = bones["R_Leg"].rotation_euler.z * -1
    RightKnee2 = bones["R_Leg"].rotation_euler.y
    RightKnee3 = bones["R_Leg"].rotation_euler.x

    RightFoot1 = bones["R_Foot"].rotation_euler.z * -1
    RightFoot2 = bones["R_Foot"].rotation_euler.y
    RightFoot3 = bones["R_Foot"].rotation_euler.x
    
    
    LeftHip1 = -bones["L_UpLeg"].rotation_euler.z
    LeftHip2 = bones["L_UpLeg"].rotation_euler.y
    LeftHip3 = bones["L_UpLeg"].rotation_euler.x
    
    LeftKnee1 = bones["L_Leg"].rotation_euler.z * -1
    LeftKnee2 = bones["L_Leg"].rotation_euler.y
    LeftKnee3 = bones["L_Leg"].rotation_euler.x

    LeftFoot1 = bones["L_Foot"].rotation_euler.z * -1
    LeftFoot2 = bones["L_Foot"].rotation_euler.y
    LeftFoot3 = bones["L_Foot"].rotation_euler.x
    """
    
    RightHip1 = visualRots["R_UpLeg"]['z'] * -1
    RightHip2 = visualRots["R_UpLeg"]['y']
    RightHip3 = visualRots["R_UpLeg"]['x']
    
    RightKnee1 = visualRots["R_Leg"]['z'] * -1
    RightKnee2 = visualRots["R_Leg"]['y']
    RightKnee3 = visualRots["R_Leg"]['x']

    RightFoot1 = visualRots["R_Foot"]['z'] * -1
    RightFoot2 = visualRots["R_Foot"]['y']
    RightFoot3 = visualRots["R_Foot"]['x']
    
    
    LeftHip1 = visualRots["L_UpLeg"]['z'] * -1
    LeftHip2 = visualRots["L_UpLeg"]['y']
    LeftHip3 = visualRots["L_UpLeg"]['x']
    
    LeftKnee1 = visualRots["L_Leg"]['z'] * -1
    LeftKnee2 = visualRots["L_Leg"]['y']
    LeftKnee3 = visualRots["L_Leg"]['x']

    LeftFoot1 = visualRots["L_Foot"]['z'] * -1
    LeftFoot2 = visualRots["L_Foot"]['y']
    LeftFoot3 = visualRots["L_Foot"]['x']
    
    # ------ end --------
    
    _DEF_VAL_TEST = 0 #default value for stuff we don't know or care about
    
    return [
        _DEF_VAL_TEST, #Offset = movement x
        _DEF_VAL_TEST, #Offset = height
        _DEF_VAL_TEST, #Offset = movement z
        offset1, #JumpStrength = pos x
        offset2, #JumpStrength = pos y
        offset3, #JumpStrength = pos Z
        _DEF_VAL_TEST, #Unknown = field 7
        _DEF_VAL_TEST, #Unknown = field 8
        _DEF_VAL_TEST, #Unknown = field 9
        RotX, #Mesh = rotx
        RotY, #Mesh = roty
        RotZ, #Mesh = rotz
        UpperBody1, # = spine1 x
        UpperBody2, # = spine1 x
        UpperBody3, # = spine1 z
        LowerBody1, # = hip x
        LowerBody2, # = hip y
        LowerBody3, # = hip z
        _DEF_VAL_TEST, #SpineFlexure # = spine 2
        _DEF_VAL_TEST, #SpineFlexure # = field 20
        _DEF_VAL_TEST, #SpineFlexure # = field 21
        Neck1, # = neck 22
        Neck2, # = neck 23
        Neck3, # = neck 24
        Head1, # = neck 25
        Head2, # = neck 26
        Head3, # = neck 27
        RightInnerShoulder1, #RightInnerShoulder
        RightInnerShoulder2, #RightInnerShoulder
        RightInnerShoulder3, #RightInnerShoulder
        RightOuterShoulder1, #RightOuterShoulder
        RightOuterShoulder2, #RightOuterShoulder
        RightOuterShoulder3, #RightOuterShoulder
        RightElbow1, #RightElbow
        RightElbow2, #RightElbow
        RightElbow3, #RightElbow
        RightHand1, #RightHand
        RightHand2, #RightHand
        RightHand3, #RightHand
        LeftInnerShoulder1, #LeftInnerShoulder
        LeftInnerShoulder2, #LeftInnerShoulder
        LeftInnerShoulder3, #LeftInnerShoulder
        LeftOuterShoulder1, #LeftOuterShoulder
        LeftOuterShoulder2, #LeftOuterShoulder
        LeftOuterShoulder3, #LeftOuterShoulder
        LeftElbow1, #LeftElbow
        LeftElbow2, #LeftElbow
        LeftElbow3, #LeftElbow
        LeftHand1, #LeftHand
        LeftHand2, #LeftHand
        LeftHand3, #LeftHand
        RightHip1, #RightHip
        RightHip2, #RightHip
        RightHip3, #RightHip
        RightKnee1, #RightKnee
        RightKnee2, #RightKnee
        RightKnee3, #RightKnee
        RightFoot1, #RightFoot
        RightFoot2, #RightFoot
        RightFoot3, #RightFoot
        LeftHip1, #LeftHip
        LeftHip2, #LeftHip
        LeftHip3, #LeftHip
        LeftKnee1, #LeftKnee
        LeftKnee2, #LeftKnee
        LeftKnee3, #LeftKnee
        LeftFoot1, #LeftFoot
        LeftFoot2, #LeftFoot
        LeftFoot3, #LeftFoot
    ]