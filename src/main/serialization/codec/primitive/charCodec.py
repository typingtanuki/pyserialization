from io import BufferedWriter, BufferedReader

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.object.noneCodec import NoneCodec
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

    def read(self, wrapper: BufferedReader) -> str or None:
        marker: bytes = wrapper.read(1)
        if marker == NoneCodec.NONE_VALUE:
            return None

        if marker == self.size_1:
            return wrapper.read(1).decode("utf-8")[0]
        if marker == self.size_2:
            return wrapper.read(2).decode("utf-8")[0]
        if marker == self.size_3:
            return wrapper.read(3).decode("utf-8")[0]

        raise TypeError("Could not deserialize as a character.")

    def write(self, wrapper: BufferedWriter, value: str) -> None:
        if value is None:
            wrapper.write(NoneCodec.NONE_VALUE)
            return

        b: bytes = value.encode("utf-8")
        if len(b) == 1:
            wrapper.write(self.size_1)
        if len(b) == 2:
            wrapper.write(self.size_2)
        if len(b) == 3:
            wrapper.write(self.size_3)
        wrapper.write(b)

    def reserved_bytes(self) -> [bytes]:
        return [self.size_1, self.size_2, self.size_3]

    def writes(self, typez: type) -> bool:
        if typez is str:
            return True
        return False
