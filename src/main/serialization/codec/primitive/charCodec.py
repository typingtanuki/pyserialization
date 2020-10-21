from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.object.noneCodec import NoneCodec

from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import *


class CharCodec(Codec[str]):
    """
    Codec for char (string of length 1)

    Used for decoding serialized data from other types
    """

    size_1: bytes
    """Marker for a single-byte character"""
    size_2: bytes
    """Marker for a double-byte character"""
    size_3: bytes
    """Marker for a triple-byte character"""

    def __init__(self, reserved_byte: bytes):
        super().__init__()

        self.size_1 = reserved_byte
        self.size_2 = to_byte(from_byte(reserved_byte) + 1)
        self.size_3 = to_byte(from_byte(reserved_byte) + 2)

    def read(self, io: ByteIo) -> str or None:
        marker: bytes = io.read()
        if marker == NoneCodec.NONE_VALUE:
            return None

        if marker == self.size_1:
            return io.read().decode("utf-8")[0]
        if marker == self.size_2:
            return io.read2().decode("utf-8")[0]
        if marker == self.size_3:
            return io.read3().decode("utf-8")[0]

        raise TypeError("Could not deserialize as a character.")

    def write(self, io: ByteIo, value: str) -> None:
        if value is None:
            io.write(NoneCodec.NONE_VALUE)
            return

        b: bytes = value.encode("utf-8")
        if len(b) == 1:
            io.write(self.size_1)
        if len(b) == 2:
            io.write(self.size_2)
        if len(b) == 3:
            io.write(self.size_3)
        io.write(b)

    def reserved_bytes(self) -> [bytes]:
        return [self.size_1, self.size_2, self.size_3]

    def writes(self, typez: type) -> bool:
        if typez is str:
            return True
        return False
