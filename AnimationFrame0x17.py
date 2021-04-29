import mathutils


class AnimationFrame0x17():
    Offset = mathutils.Euler([0.0, 0.0, 0.0])
    JumpStrength = mathutils.Euler([0.0, 0.0, 0.0])
    Unknown = mathutils.Euler([0.0, 0.0, 0.0])
    Mesh = mathutils.Euler([0.0, 0.0, 0.0])
    UpperBody = mathutils.Euler([0.0, 0.0, 0.0])
    LowerBody = mathutils.Euler([0.0, 0.0, 0.0])
    SpineFlexure = mathutils.Euler([0.0, 0.0, 0.0])
    Neck = mathutils.Euler([0.0, 0.0, 0.0])
    Head = mathutils.Euler([0.0, 0.0, 0.0])
    RightInnerShoulder = mathutils.Euler([0.0, 0.0, 0.0])
    RightOuterShoulder = mathutils.Euler([0.0, 0.0, 0.0])
    RightElbow = mathutils.Euler([0.0, 0.0, 0.0])
    RightHand = mathutils.Euler([0.0, 0.0, 0.0])
    LeftInnerShoulder = mathutils.Euler([0.0, 0.0, 0.0])
    LeftOuterShoulder = mathutils.Euler([0.0, 0.0, 0.0])
    LeftElbow = mathutils.Euler([0.0, 0.0, 0.0])
    LeftHand = mathutils.Euler([0.0, 0.0, 0.0])
    RightHip = mathutils.Euler([0.0, 0.0, 0.0])
    RightKnee = mathutils.Euler([0.0, 0.0, 0.0])
    RightFoot = mathutils.Euler([0.0, 0.0, 0.0])
    LeftHip = mathutils.Euler([0.0, 0.0, 0.0])
    LeftKnee = mathutils.Euler([0.0, 0.0, 0.0])
    LeftFoot = mathutils.Euler([0.0, 0.0, 0.0])

    def __init__(self, animation_frame_tuple):
        self.__check_if_animation_frame_is_valid(animation_frame_tuple)
        self.__initialize_animation_frame(animation_frame_tuple)

    def __check_if_animation_frame_is_valid(self, animation_frame_tuple):
        if (len(animation_frame_tuple) != 23 * 3):
            raise ValueError(f"animationFrameTuple argument must have 23 values in it, "
                             f"and this tuple has: {len(animation_frame_tuple)}.")

        for index in range(len(animation_frame_tuple)):
            current_variable = animation_frame_tuple[index]

            if type(current_variable) is not float:
                raise ValueError(f"Variables in animation_frame_tuple should all be floats. "
                                 f"Variable at index {index} in animation_frame_tuple is not a float.")

    def __initialize_animation_frame(self, animation_frame_tuple):
        tup = animation_frame_tuple

        self.Offset = self.__get_euler_from_tuple(animation_frame_tuple, 0)
        self.JumpStrength = self.__get_euler_from_tuple(animation_frame_tuple, 3)
        self.Unknown = self.__get_euler_from_tuple(animation_frame_tuple, 6)
        self.Mesh = self.__get_euler_from_tuple(animation_frame_tuple, 9)
        self.UpperBody = self.__get_euler_from_tuple(animation_frame_tuple, 12)
        self.LowerBody = self.__get_euler_from_tuple(animation_frame_tuple, 15)
        self.SpineFlexure = self.__get_euler_from_tuple(animation_frame_tuple, 18)
        self.Neck = self.__get_euler_from_tuple(animation_frame_tuple, 21)
        self.Head = self.__get_euler_from_tuple(animation_frame_tuple, 24)
        self.RightInnerShoulder = self.__get_euler_from_tuple(animation_frame_tuple, 27)
        self.RightOuterShoulder = self.__get_euler_from_tuple(animation_frame_tuple, 30)
        self.RightElbow = self.__get_euler_from_tuple(animation_frame_tuple, 33)
        self.RightHand = self.__get_euler_from_tuple(animation_frame_tuple, 36)
        self.LeftInnerShoulder = self.__get_euler_from_tuple(animation_frame_tuple, 39)
        self.LeftOuterShoulder = self.__get_euler_from_tuple(animation_frame_tuple, 42)
        self.LeftElbow = self.__get_euler_from_tuple(animation_frame_tuple, 45)
        self.LeftHand = self.__get_euler_from_tuple(animation_frame_tuple, 48)
        self.RightHip = self.__get_euler_from_tuple(animation_frame_tuple, 51)
        self.RightKnee = self.__get_euler_from_tuple(animation_frame_tuple, 54)
        self.RightFoot = self.__get_euler_from_tuple(animation_frame_tuple, 57)
        self.LeftHip = self.__get_euler_from_tuple(animation_frame_tuple, 60)
        self.LeftKnee = self.__get_euler_from_tuple(animation_frame_tuple, 63)
        self.LeftFoot = self.__get_euler_from_tuple(animation_frame_tuple, 66)

    @staticmethod
    def __get_euler_from_tuple(tuple, tuple_start_index):
        euler = mathutils.Euler([tuple[tuple_start_index], tuple[tuple_start_index+1], tuple[tuple_start_index+2]])
        return euler
