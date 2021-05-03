from .AnimationHeader0xC8 import AnimationHeader0xC8
from .AnimationFrame0x17 import AnimationFrame0x17

import struct


class Animation0xC80x17():
    def __init__(self, binary_data):
        self.AnimationHeader0xC8 = 0
        self.AnimationFrames = list()
        # Initializing header
        # "< 2B H 24I" stands for little endian, 2 unsigned bytes, unsigned short, 24 unsigned 4-byte integers
        struct_packer = struct.Struct("< 2B H 24I")
        animation_header_tuple = struct_packer.unpack_from(binary_data)
        self.AnimationHeader0xC8 = AnimationHeader0xC8(animation_header_tuple)

        # Initializing animation frames list
        header_size = struct_packer.size
        struct_packer = struct.Struct("< 69f")
        animation_frame_size = struct_packer.size

        for frame_index in range(self.AnimationHeader0xC8.properties['AnimationLength']):
            animation_frame_data_offset = header_size + (animation_frame_size * frame_index)

            self.check_if_can_read_frame_from_binary_data(animation_frame_data_offset, animation_frame_size,
                                                          binary_data, frame_index)

            animation_frame_tuple = struct_packer.unpack_from(binary_data, animation_frame_data_offset)
            animation_frame = AnimationFrame0x17(animation_frame_tuple)
            self.AnimationFrames.append(animation_frame)

    def check_if_can_read_frame_from_binary_data(self, animation_frame_data_offset, animation_frame_size, binary_data,
                                                 frame_index):
        if (animation_frame_data_offset + animation_frame_size > len(binary_data)):
            raise ValueError(
                f"Can't read frame #{frame_index + 1}. "
                f"animation_frame_data_offset({animation_frame_data_offset})+animation_frame_size({animation_frame_size}) "
                f"is bigger than length of binary_data({len(binary_data)})"
            )

    def __repr__(self):
        animation_text = ""

        animation_text = f"Animation header:\n" \
                         f"{self.AnimationHeader0xC8}\n"

        animation_text += f"Animation frames:\n"

        for animation_frame_index in range(len(self.AnimationFrames)):
            animation_frame = self.AnimationFrames[animation_frame_index]

            animation_text += f"Animation frame #{animation_frame_index + 1}:\n" \
                              f"{animation_frame}\n"

        return animation_text
