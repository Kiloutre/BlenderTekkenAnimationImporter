
class AnimationHeader0xC8():
    AnimationSignatureByte1 = 0xC8
    AnimationSignatureByte2 = 1
    AnimationVectorsPerFrame = 23
    AnimationLength = 0
    DeviationDescriptorMask = 11
    JumpStrengthDescriptorMask = 11
    UnknownDescriptorMask = 5
    MeshDescriptorMask = 7
    UpperBodyDescriptorMask = 7
    LowerBodyDescriptorMask = 7
    SpineFlexureDescriptorMask = 11
    NeckDescriptorMask = 7
    HeadDescriptorMask = 7
    RightInnerShoulderDescriptorMask = 7
    RightOuterShoulderDescriptorMask = 7
    RightElbowDescriptorMask = 6
    RightHandDescriptorMask = 7
    LeftInnerShoulderDescriptorMask = 7
    LeftOuterShoulderDescriptorMask = 7
    LeftElbowDescriptorMask = 6
    LeftHandDescriptorMask = 7
    RightHipDescriptorMask = 7
    RightKneeDescriptorMask = 6
    RightFootDescriptorMask = 7
    LeftHipDescriptorMask = 7
    LeftKneeDescriptorMask = 6
    LeftFootDescriptorMask = 7

    def __init__(self, header_tuple):
        self.__check_if_header_tuple_is_valid(header_tuple)

        self.__initialize_animation_header(header_tuple)

    def __check_if_header_tuple_is_valid(self, header_tuple):
        if (len(header_tuple) != 27):
            raise ValueError(f"headerTuple argument must have 27 values in it,"
                             f"and this tuple has: {len(header_tuple)}.")

        if (header_tuple[0] != 0xC8):
            raise ValueError(f"AnimationSignatureByte1 must be equal to 0xC8"
                             f"and in this animation first signature byte is equal to {header_tuple[0]}.")

        if (header_tuple[1] != 1):
            raise ValueError(f"AnimationSignatureByte2 must be equal to 1"
                             f"and in this animation second signature byte is equal to {header_tuple[1]}.")

        if (header_tuple[2] != 23):
            raise ValueError(f"This plugin only works with animations that animate 23 bones on the character."
                             f"This animation has {header_tuple[2]} bones.")

    def __initialize_animation_header(self, header_tuple):
        self.AnimationSignatureByte1 = header_tuple[0]
        self.AnimationSignatureByte2 = header_tuple[1]
        self.AnimationVectorsPerFrame = header_tuple[2]
        self.AnimationLength = header_tuple[3]
        self.DeviationDescriptorMask = header_tuple[4]
        self.JumpStrengthDescriptorMask = header_tuple[5]
        self.UnknownDescriptorMask = header_tuple[6]
        self.MeshDescriptorMask = header_tuple[7]
        self.UpperBodyDescriptorMask = header_tuple[8]
        self.LowerBodyDescriptorMask = header_tuple[9]
        self.SpineFlexureDescriptorMask = header_tuple[10]
        self.NeckDescriptorMask = header_tuple[11]
        self.HeadDescriptorMask = header_tuple[12]
        self.RightInnerShoulderDescriptorMask = header_tuple[13]
        self.RightOuterShoulderDescriptorMask = header_tuple[14]
        self.RightElbowDescriptorMask = header_tuple[15]
        self.RightHandDescriptorMask = header_tuple[16]
        self.LeftInnerShoulderDescriptorMask = header_tuple[17]
        self.LeftOuterShoulderDescriptorMask = header_tuple[18]
        self.LeftElbowDescriptorMask = header_tuple[19]
        self.LeftHandDescriptorMask = header_tuple[20]
        self.RightHipDescriptorMask = header_tuple[21]
        self.RightKneeDescriptorMask = header_tuple[22]
        self.RightFootDescriptorMask = header_tuple[23]
        self.LeftHipDescriptorMask = header_tuple[24]
        self.LeftKneeDescriptorMask = header_tuple[25]
        self.LeftFootDescriptorMask = header_tuple[26]

    def __repr__(self):
        return \
            f"AnimationSignatureByte1: {self.AnimationSignatureByte1}\n" \
            f"AnimationSignatureByte2: {self.AnimationSignatureByte2}\n" \
            f"AnimationVectorsPerFrame: {self.AnimationVectorsPerFrame}\n" \
            f"AnimationLength: {self.AnimationLength}\n" \
            f"DeviationDescriptorMask: {self.DeviationDescriptorMask}\n" \
            f"JumpStrengthDescriptorMask: {self.JumpStrengthDescriptorMask}\n" \
            f"UnknownDescriptorMask: {self.UnknownDescriptorMask}\n" \
            f"MeshDescriptorMask: {self.MeshDescriptorMask}\n" \
            f"UpperBodyDescriptorMask: {self.UpperBodyDescriptorMask}\n" \
            f"LowerBodyDescriptorMask: {self.LowerBodyDescriptorMask}\n" \
            f"SpineFlexureDescriptorMask: {self.SpineFlexureDescriptorMask}\n" \
            f"NeckDescriptorMask: {self.NeckDescriptorMask}\n" \
            f"HeadDescriptorMask: {self.HeadDescriptorMask}\n" \
            f"RightInnerShoulderDescriptorMask: {self.RightInnerShoulderDescriptorMask}\n" \
            f"RightOuterShoulderDescriptorMask: {self.RightOuterShoulderDescriptorMask}\n" \
            f"RightElbowDescriptorMask: {self.RightElbowDescriptorMask}\n" \
            f"RightHandDescriptorMask: {self.RightHandDescriptorMask}\n" \
            f"LeftInnerShoulderDescriptorMask: {self.LeftInnerShoulderDescriptorMask}\n" \
            f"LeftOuterShoulderDescriptorMask: {self.LeftOuterShoulderDescriptorMask}\n" \
            f"LeftElbowDescriptorMask: {self.LeftElbowDescriptorMask}\n" \
            f"LeftHandDescriptorMask: {self.LeftHandDescriptorMask}\n" \
            f"RightHipDescriptorMask: {self.RightHipDescriptorMask}\n" \
            f"RightKneeDescriptorMask: {self.RightKneeDescriptorMask}\n" \
            f"RightFootDescriptorMask: {self.RightFootDescriptorMask}\n" \
            f"LeftHipDescriptorMask: {self.LeftHipDescriptorMask}\n" \
            f"LeftKneeDescriptorMask: {self.LeftKneeDescriptorMask}\n" \
            f"LeftFootDescriptorMask: {self.LeftFootDescriptorMask}\n"