from . import AnimationHeader0xC8
from . import AnimationFrame0x17

import struct


class Animation0xC80x17():
    AnimationHeader0xC8 = 0
    AnimationFrames = list()

    def __init__(self, binary_data):
        # "< 2B H 24I" stands for little endian, 2 unsigned bytes, unsigned short, 24 unsigned 4-byte integers
        struct_packer = struct.Struct("< 2B H 24I")
        animation_header_tuple = struct_packer.unpack_from(binary_data)
        self.AnimationHeader0xC8 = AnimationHeader0xC8.AnimationHeader0xC8(animation_header_tuple)

        header_size = struct_packer.size
        struct_packer = struct.Struct("< 69f")
        animation_frame_size = struct_packer.size

        for frameIndex in range(self.AnimationHeader0xC8.properties['AnimationLength']):
            animation_frame_data_offset = header_size + (animation_frame_size * frameIndex)
            animation_frame_tuple = struct_packer.unpack_from(binary_data, animation_frame_data_offset)
            animation_frame = AnimationFrame0x17.AnimationFrame0x17(animation_frame_tuple)
            self.AnimationFrames.append(animation_frame)

    def __repr__(self):
        animation_text = ""

        animation_text = f"Animation header:\n" \
                         f"{self.AnimationHeader0xC8}\n"

        animation_text += f"Animation frames:\n"

        for animation_frame_index in range(len(self.AnimationFrames)):
            animation_frame = self.AnimationFrames[animation_frame_index]

            animation_text += f"Animation frame #{animation_frame_index}:\n" \
                              f"{animation_frame}\n"

        return animation_text