import struct

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.object.noneCodec import NoneCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import *


class FloatCodec(Codec[int]):
    """
    Codec for float

    Used for decoding serialized data from other languages
    """

    size_1: bytes
    """Marker for a single-byte float"""
    size_2: bytes
    """Marker for a double-byte float"""
    size_3: bytes
    """Marker for a triple-byte float"""
    size_4: bytes
    """Marker for a 4 bytes float"""

    def __init__(self, reserved_byte: bytes):
        super().__init__()

        self.size_1 = reserved_byte
        self.size_2 = to_byte(from_byte(reserved_byte) + 1)
        self.size_3 = to_byte(from_byte(reserved_byte) + 2)
        self.size_4 = to_byte(from_byte(reserved_byte) + 3)

    def read(self, io: ByteIo) -> float or None:
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
        else:
            raise TypeError("Could not deserialize as a float.")
        return struct.unpack("d", read)[0]

    def write(self, io: ByteIo, value: float) -> None:
        if value is None:
            io.write(NoneCodec.NONE_VALUE)
            return

        packed: bytes = struct.pack("d", value)
        long: int = int_from_byte(packed)
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
        elif long < 32768:
            if long < 128:
                io.write(self.size_1)
                io.write1(long)
            else:
                io.write(self.size_2)
                io.write2(long)
        elif long < 8388608:
            io.write(self.size_3)
            io.write3(long)
        else:
            io.write(self.size_4)
            io.write4(long)

    def reserved_bytes(self) -> [bytes]:
        return [self.size_1, self.size_2, self.size_3, self.size_4]

    def writes(self, typez: type) -> bool:
        # For interoperability only
        return False
