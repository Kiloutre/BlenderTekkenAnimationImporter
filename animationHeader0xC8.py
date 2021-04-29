from collections import OrderedDict


class AnimationHeader0xC8():
    properties = OrderedDict([('AnimationSignatureByte1', 0xC8),
                              ('AnimationSignatureByte2', 1),
                              ('AnimationVectorsPerFrame', 23),
                              ('AnimationLength', 0),
                              ('DeviationDescriptorMask', 11),
                              ('JumpStrengthDescriptorMask', 11),
                              ('UnknownDescriptorMask', 5),
                              ('MeshDescriptorMask', 7),
                              ('UpperBodyDescriptorMask', 7),
                              ('LowerBodyDescriptorMask', 7),
                              ('SpineFlexureDescriptorMask', 11),
                              ('NeckDescriptorMask', 7),
                              ('HeadDescriptorMask', 7),
                              ('RightInnerShoulderDescriptorMask', 7),
                              ('RightOuterShoulderDescriptorMask', 7),
                              ('RightElbowDescriptorMask', 6),
                              ('RightHandDescriptorMask', 7),
                              ('LeftInnerShoulderDescriptorMask', 7),
                              ('LeftOuterShoulderDescriptorMask', 7),
                              ('LeftElbowDescriptorMask', 6),
                              ('LeftHandDescriptorMask', 7),
                              ('RightHipDescriptorMask', 7),
                              ('RightKneeDescriptorMask', 6),
                              ('RightFootDescriptorMask', 7),
                              ('LeftHipDescriptorMask', 7),
                              ('LeftKneeDescriptorMask', 6),
                              ('LeftFootDescriptorMask', 7), ])

    def __init__(self, header_tuple):
        self.__check_if_header_tuple_is_valid(header_tuple)

        self.__initialize_animation_header(header_tuple)

    def __check_if_header_tuple_is_valid(self, header_tuple):
        if (len(header_tuple) != 27):
            raise ValueError(f"headerTuple argument must have 27 values in it, "
                             f"and this tuple has: {len(header_tuple)}.")

        if (header_tuple[0] != 0xC8):
            raise ValueError(f"AnimationSignatureByte1 must be equal to 0xC8 "
                             f"and in this animation first signature byte is equal to {header_tuple[0]}.")

        if (header_tuple[1] != 1):
            raise ValueError(f"AnimationSignatureByte2 must be equal to 1 "
                             f"and in this animation second signature byte is equal to {header_tuple[1]}.")

        if (header_tuple[2] != 23):
            raise ValueError(f"This plugin only works with animations that animate 23 bones on the character. "
                             f"This animation has {header_tuple[2]} bones.")

    def __initialize_animation_header(self, header_tuple):
        header_properties_list = list(self.properties.items())

        for index in range(len(header_properties_list)):
            key = header_properties_list[index][0]
            value = header_properties_list[index][1]
            self.properties[key] = header_tuple[index]

    def __repr__(self):
        header_properties_list = list(self.properties.items())
        animation_header_text = ""

        for index in range(len(header_properties_list)):
            key = header_properties_list[index][0]
            value = header_properties_list[index][1]
            animation_header_text += f"{key}: {value}\n"

        return animation_header_text
