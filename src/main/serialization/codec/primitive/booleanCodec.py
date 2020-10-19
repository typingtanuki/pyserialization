from io import BufferedWriter, BufferedReader

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.object.noneCodec import NoneCodec
from src.main.serialization.codec.utils.bytes import *


class BooleanCodec(Codec[bool]):
    """Codec for bool type"""

    true_bytes: bytes
    """Byte used to encode 'True'"""
    false_bytes: bytes
    """Byte used to encode 'False'"""

    def __init__(self, reserved_byte: bytes):
        super().__init__()

        self.true_bytes = reserved_byte
        self.false_bytes = to_byte(from_byte(reserved_byte) + 1)

    def read(self, wrapper: BufferedReader) -> bool or None:
        marker: bytes = wrapper.read(1)
        if marker == NoneCodec.NONE_VALUE:
            return None

        if marker == self.true_bytes:
            return True
        if marker == self.false_bytes:
            return False

        raise TypeError("Could not deserialize as a boolean.")

    def write(self, wrapper: BufferedWriter, value: bool) -> None:
        if value is None:
            wrapper.write(NoneCodec.NONE_VALUE)
            return

        if value:
            wrapper.write(self.true_bytes)
        else:
            wrapper.write(self.false_bytes)

    def reserved_bytes(self) -> [bytes]:
        return [self.true_bytes, self.false_bytes]

    def writes(self, typez: type) -> bool:
        if typez is bool:
            return True
        return False