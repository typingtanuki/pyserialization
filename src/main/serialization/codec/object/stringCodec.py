import struct

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.object.noneCodec import NoneCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import *


class StringCodec(Codec[str]):
    """
    Codec for strings
    """

    size_1: bytes
    """Marker for a single-byte short"""
    size_2: bytes
    """Marker for a double-byte short"""

    def __init__(self, reserved_byte: bytes):
        super().__init__()

        self.size_1 = reserved_byte
        self.size_2 = to_byte(from_byte(reserved_byte) + 1)

    def read(self, io: ByteIo) -> int or None:
        marker: bytes = io.read()
        if marker == NoneCodec.NONE_VALUE:
            return None

        read: bytes
        if marker == self.size_1:
            read: bytes = io.read(1, 2)
        elif marker == self.size_2:
            read: bytes = io.read(2, 2)
        else:
            raise TypeError("Could not deserialize as a short.")
        return struct.unpack(">h", read)[0]

    def write(self, io: ByteIo, value: int) -> None:
        if value is None:
            io.write(NoneCodec.NONE_VALUE)
            return

        b: bytes = struct.pack(">h", value)
        buffer_len: int = len(b)
        found: bool = False

        for i in range(0, len(b)):
            if not found and b[i] == 0:
                buffer_len = buffer_len - 1
            else:
                found = True

        if buffer_len == 2:
            io.write(self.size_2)
            io.write2(value)
        elif buffer_len == 1:
            io.write(self.size_1)
            io.write1(value)

    def reserved_bytes(self) -> [bytes]:
        return [self.size_1, self.size_2]

    def writes(self, typez: type) -> bool:
        # For interoperability only
        return False
