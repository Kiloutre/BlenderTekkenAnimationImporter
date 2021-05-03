import mathutils
from collections import OrderedDict


class AnimationFrame0x17():
    def __init__(self, animation_frame_tuple):
        self.__bones_number = 0x17

        self.properties = OrderedDict([('Offset', 0),
                              ('JumpStrength', 0),
                              ('Unknown', 0),
                              ('Mesh', 0),
                              ('UpperBody', 0),
                              ('LowerBody', 0),
                              ('SpineFlexure', 0),
                              ('Neck', 0),
                              ('Head', 0),
                              ('RightInnerShoulder', 0),
                              ('RightOuterShoulder', 0),
                              ('RightElbow', 0),
                              ('RightHand', 0),
                              ('LeftInnerShoulder', 0),
                              ('LeftOuterShoulder', 0),
                              ('LeftElbow', 0),
                              ('LeftHand', 0),
                              ('RightHip', 0),
                              ('RightKnee', 0),
                              ('RightFoot', 0),
                              ('LeftHip', 0),
                              ('LeftKnee', 0),
                              ('LeftFoot', 0)])

        self.__check_if_animation_frame_is_valid(animation_frame_tuple)
        self.__initialize_animation_frame(animation_frame_tuple)

    def __check_if_animation_frame_is_valid(self, animation_frame_tuple):
        if (len(animation_frame_tuple) != self.__bones_number * 3):
            raise ValueError(f"animationFrameTuple argument must have 23 values in it, "
                             f"and this tuple has: {len(animation_frame_tuple)}.")

        for index in range(len(animation_frame_tuple)):
            current_variable = animation_frame_tuple[index]

            if type(current_variable) is not float:
                raise ValueError(f"Variables in animation_frame_tuple should all be floats. "
                                 f"Variable at index {index} in animation_frame_tuple is not a float.")

    def __initialize_animation_frame(self, animation_frame_tuple):
        frame_properties_list = list(self.properties.items())

        for index in range(len(frame_properties_list)):
            key = frame_properties_list[index][0]
            value = frame_properties_list[index][1]
            self.properties[key] = self.__get_euler_from_tuple(animation_frame_tuple, index * 3)

    @staticmethod
    def __get_euler_from_tuple(tuple, tuple_start_index):
        euler = mathutils.Euler([tuple[tuple_start_index], tuple[tuple_start_index+1], tuple[tuple_start_index+2]])
        return euler

    def __repr__(self):
        frame_properties_list = list(self.properties.items())
        animation_frame_text = ""

        for index in range(len(frame_properties_list)):
            key = frame_properties_list[index][0]
            value = frame_properties_list[index][1]
            animation_frame_text += f"{key}: {value}\n"

        return animation_frame_text