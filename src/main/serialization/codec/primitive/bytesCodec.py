from io import BufferedWriter, BufferedReader

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.object.noneCodec import NoneCodec


class BytesCodec(Codec[bytes]):
    """Codec for 'byte' type"""

    byte_bytes: bytes
    """The byte used to mark byte type"""

    def __init__(self, reserved_byte: bytes):
        super().__init__()

        self.byte_bytes = reserved_byte

    def read(self, wrapper: BufferedReader) -> bytes or None:
        marker: bytes = wrapper.read(1)
        if marker == NoneCodec.NONE_VALUE:
            return None

        if marker == self.byte_bytes:
            return wrapper.read(1)

        raise TypeError("Could not deserialize as a byte.")

    def write(self, wrapper: BufferedWriter, value: bytes) -> None:
        if value is None:
            wrapper.write(NoneCodec.NONE_VALUE)
            return

        wrapper.write(self.byte_bytes)
        wrapper.write(value)

    def reserved_bytes(self) -> [bytes]:
        return [self.byte_bytes]

    def writes(self, typez: type) -> bool:
        if typez is bytes:
            return True
        return False
