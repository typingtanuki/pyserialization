import struct

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.object.noneCodec import NoneCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import *


class DoubleCodec(Codec[int]):
    """
    Codec for float

    Used for decoding serialized data from other languages
    """

    size_1: bytes
    """Marker for a single-byte double"""
    size_2: bytes
    """Marker for a double-byte double"""
    size_3: bytes
    """Marker for a triple-byte double"""
    size_4: bytes
    """Marker for a 4 bytes double"""
    size_5: bytes
    """Marker for a 5 bytes double"""
    size_6: bytes
    """Marker for a 6 bytes double"""
    size_7: bytes
    """Marker for a 7 bytes double"""
    size_8: bytes
    """Marker for a 8 bytes double"""

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

    def read(self, io: ByteIo) -> float or None:
        marker: bytes = io.read()
        if marker == NoneCodec.NONE_VALUE:
            return None

        if marker == self.size_1:
            val: bytes = io.read(1)
            return struct.unpack("d", val)
        if marker == self.size_2:
            val: bytes = io.read(2)
            return struct.unpack("d", val)
        if marker == self.size_3:
            val: bytes = io.read(3)
            return struct.unpack("d", val)
        if marker == self.size_4:
            val: bytes = io.read(4)
            return struct.unpack("d", val)
        if marker == self.size_5:
            val: bytes = io.read(5)
            return struct.unpack("d", val)
        if marker == self.size_6:
            val: bytes = io.read(6)
            return struct.unpack("d", val)
        if marker == self.size_7:
            val: bytes = io.read(7)
            return struct.unpack("d", val)
        if marker == self.size_8:
            val: bytes = io.read(8)
            return struct.unpack("d", val)

        raise TypeError("Could not deserialize as a double.")

    def write(self, io: ByteIo, value: float) -> None:
        if value is None:
            io.write(NoneCodec.NONE_VALUE)
            return

        packed: bytes = struct.pack("d", value)
        long: int = int_from_byte(packed)
        if long < -2147483648:
            if long < -549755813888:
                if long < -140737488355328:
                    if long < -36028797018963968:
                        io.write(self.size_8)
                        io.write8(long)
                    else:
                        io.write(self.size_7)
                        io.write7(long)
                else:
                    io.write(self.size_6)
                    io.write6(long)
            else:
                io.write(self.size_5)
                io.write5(long)
        elif long < 128:
            if long < -128:
                if long < -32768:
                    if long < -8388608:
                        io.write(self.size_4)
                        io.write4(long)
                    else:
                        io.write(self.size_3)
                        io.write3(long)
                else:
                    io.write(self.size_2)
                    io.write2(long)
            else:
                io.write(self.size_1)
                io.write1(long)
        elif long < 2147483648:
            if long < 8388608:
                if long < 32768:
                    io.write(self.size_2)
                    io.write2(long)
                else:
                    io.write(self.size_3)
                    io.write3(long)
            else:
                io.write(self.size_4)
                io.write4(long)
        elif long < 140737488355328:
            if long < 549755813888:
                io.write(self.size_5)
                io.write5(long)
            else:
                io.write(self.size_6)
                io.write6(long)
        elif long < 36028797018963968:
            io.write(self.size_7)
            io.write7(long)
        else:
            io.write(self.size_8)
            io.write8(long)

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
        if typez is float:
            return True
        return False
