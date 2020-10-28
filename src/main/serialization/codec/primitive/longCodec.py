import struct

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.object.noneCodec import NoneCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import *


class LongCodec(Codec[int]):
    """
    Codec for long

    Used for decoding serialized data from other languages
    """

    size_1: bytes
    """Marker for a single-byte long"""
    size_2: bytes
    """Marker for a double-byte long"""
    size_3: bytes
    """Marker for a triple-byte long"""
    size_4: bytes
    """Marker for a 4 bytes long"""
    size_5: bytes
    """Marker for a 5 bytes long"""
    size_6: bytes
    """Marker for a 6 bytes long"""
    size_7: bytes
    """Marker for a 7 bytes long"""
    size_8: bytes
    """Marker for a 8 bytes long"""

    def __init__(self, reserved_byte: bytes):
        super().__init__()

        self.size_1 = reserved_byte
        self.size_2 = to_byte(from_byte(reserved_byte) + 1)
        self.size_3 = to_byte(from_byte(reserved_byte) + 2)
        self.size_4 = to_byte(from_byte(reserved_byte) + 3)
        self.size_5 = to_byte(from_byte(reserved_byte) + 4)
        self.size_6 = to_byte(from_byte(reserved_byte) + 5)
        self.size_7 = to_byte(from_byte(reserved_byte) + 6)
        self.size_8 = to_byte(from_byte(reserved_byte) + 7)

    def read(self, io: ByteIo) -> int or None:
        marker: bytes = io.read()
        if marker == NoneCodec.NONE_VALUE:
            return None

        read: bytes
        if marker == self.size_1:
            read: bytes = io.read(1, 8)
        elif marker == self.size_2:
            read: bytes = io.read(2, 8)
        elif marker == self.size_3:
            read: bytes = io.read(3, 8)
        elif marker == self.size_4:
            read: bytes = io.read(4, 8)
        elif marker == self.size_5:
            read: bytes = io.read(5, 8)
        elif marker == self.size_6:
            read: bytes = io.read(6, 8)
        elif marker == self.size_7:
            read: bytes = io.read(7, 8)
        elif marker == self.size_8:
            read: bytes = io.read(8, 8)
        else:
            raise TypeError("Could not deserialize as a long.")
        return struct.unpack(">q", read)[0]

    def write(self, io: ByteIo, value: int) -> None:
        if value is None:
            io.write(NoneCodec.NONE_VALUE)
            return

        b: bytes = struct.pack(">q", value)
        buffer_len: int = len(b)
        found: bool = False

        for i in range(0, len(b)):
            if not found and b[i] == 0:
                buffer_len = buffer_len - 1
            else:
                found = True

        if buffer_len == 8:
            io.write(self.size_8)
            io.write8(value)
        elif buffer_len == 7:
            io.write(self.size_7)
            io.write7(value)
        elif buffer_len == 6:
            io.write(self.size_6)
            io.write6(value)
        elif buffer_len == 5:
            io.write(self.size_5)
            io.write5(value)
        elif buffer_len == 4:
            io.write(self.size_4)
            io.write4(value)
        elif buffer_len == 3:
            io.write(self.size_3)
            io.write3(value)
        elif buffer_len == 2:
            io.write(self.size_2)
            io.write2(value)
        elif buffer_len <= 1:
            io.write(self.size_1)
            io.write1(value)
        else:
            raise TypeError(f"Could not serialize long {value}")

    def reserved_bytes(self) -> [bytes]:
        return [self.size_1,
                self.size_2,
                self.size_3,
                self.size_4,
                self.size_5,
                self.size_6,
                self.size_7,
                self.size_8]

    def writes(self, typez: type) -> bool:
        if typez is int:
            return True
        return False
