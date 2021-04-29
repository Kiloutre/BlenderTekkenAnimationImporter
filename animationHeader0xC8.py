
class animationHeader0xC8():
    AnimationSignatureByte1 = 0xC8
    AnimationSignatureByte2 = 1
    AnimationVectorsPerFrame = 23
    AnimationLength = 0
    DeviationDescriptorMask = 0
    JumpStrengthDescriptorMask = 0
    UnknownDescriptorMask = 0
    MeshDescriptorMask = 0
    UpperBodyDescriptorMask = 0
    LowerBodyDescriptorMask = 0
    SpineFlexureDescriptorMask = 0
    NeckDescriptorMask = 0
    HeadDescriptorMask = 0
    RightInnerShoulderDescriptorMask = 0
    RightOuterShoulderDescriptorMask = 0
    RightElbowDescriptorMask = 0
    RightHandDescriptorMask = 0
    LeftInnerShoulderDescriptorMask = 0
    LeftOuterShoulderDescriptorMask = 0
    LeftElbowDescriptorMask = 0
    LeftHandDescriptorMask = 0
    RightHipDescriptorMask = 0
    RightKneeDescriptorMask = 0
    RightFootDescriptorMask = 0
    LeftHipDescriptorMask = 0
    LeftKneeDescriptorMask = 0
    LeftFootDescriptorMask = 0

    def __init__(self, headerTuple):
        if(len(headerTuple) != 27):
            raise ValueError("headerTuple argument must have 27 values in it, and it doesn't.")
        if(headerTuple[0] != 0xC8):
            raise ValueError("AnimationSignatureByte1 must be equal to 0xC8 and it isn't.")
        if(headerTuple[1] != 1):
            raise ValueError("AnimationSignatureByte2 must be equal to 1 and it isn't.")

        self.AnimationSignatureByte1 = headerTuple[0]
        self.AnimationSignatureByte2 = headerTuple[1]
        self.AnimationVectorsPerFrame = headerTuple[2]
        self.AnimationLength = headerTuple[3]
        self.DeviationDescriptorMask = headerTuple[4]
        self.JumpStrengthDescriptorMask = headerTuple[5]
        self.UnknownDescriptorMask = headerTuple[6]
        self.MeshDescriptorMask = headerTuple[7]
        self.UpperBodyDescriptorMask = headerTuple[8]
        self.LowerBodyDescriptorMask = headerTuple[9]
        self.SpineFlexureDescriptorMask = headerTuple[10]
        self.NeckDescriptorMask = headerTuple[11]
        self.HeadDescriptorMask = headerTuple[12]
        self.RightInnerShoulderDescriptorMask = headerTuple[13]
        self.RightOuterShoulderDescriptorMask = headerTuple[14]
        self.RightElbowDescriptorMask = headerTuple[15]
        self.RightHandDescriptorMask = headerTuple[16]
        self.LeftInnerShoulderDescriptorMask = headerTuple[17]
        self.LeftOuterShoulderDescriptorMask = headerTuple[18]
        self.LeftElbowDescriptorMask = headerTuple[19]
        self.LeftHandDescriptorMask = headerTuple[20]
        self.RightHipDescriptorMask = headerTuple[21]
        self.RightKneeDescriptorMask = headerTuple[22]
        self.RightFootDescriptorMask = headerTuple[23]
        self.LeftHipDescriptorMask = headerTuple[24]
        self.LeftKneeDescriptorMask = headerTuple[25]
        self.LeftFootDescriptorMask = headerTuple[26]
