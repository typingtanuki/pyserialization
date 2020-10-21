from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.object.noneCodec import NoneCodec

from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import *


class CharCodec(Codec[str]):
    """
    Codec for char (string of length 1)

    Used for decoding serialized data from other languages
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
            return chr(io.read_int())
        if marker == self.size_2:
            return chr(io.read2_int())
        if marker == self.size_3:
            return chr(io.read3_int())

        raise TypeError("Could not deserialize as a character.")

    def write(self, io: ByteIo, value: str) -> None:
        if value is None:
            io.write(NoneCodec.NONE_VALUE)
            return

        ordinal: int = ord(value);

        if ordinal >= 32768:
            io.write(self.size_3)
            io.write3(ordinal)
            return
        if ordinal >= 128:
            io.write(self.size_2)
            io.write2(ordinal)
            return

        io.write(self.size_1)
        io.write((ordinal & 0xFF).to_bytes(1, byteorder="big"))

    def reserved_bytes(self) -> [bytes]:
        return [self.size_1, self.size_2, self.size_3]

    def writes(self, typez: type) -> bool:
        if typez is str:
            return True
        return False
