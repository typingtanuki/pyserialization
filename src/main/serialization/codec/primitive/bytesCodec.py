from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.object.noneCodec import NoneCodec
from src.main.serialization.codec.utils.byteIo import ByteIo


class BytesCodec(Codec[bytes]):
    """Codec for 'byte' type"""

    byte_bytes: bytes
    """The byte used to mark byte type"""

    def __init__(self, reserved_byte: bytes):
        super().__init__()

        self.byte_bytes = reserved_byte

    def read(self, io: ByteIo) -> bytes or None:
        marker: bytes = io.read()
        if marker == NoneCodec.NONE_VALUE:
            return None

        if marker == self.byte_bytes:
            return io.read()

        raise TypeError("Could not deserialize as a byte.")

    def write(self, io: ByteIo, value: bytes) -> None:
        if value is None:
            io.write(NoneCodec.NONE_VALUE)
            return

        io.write(self.byte_bytes)
        io.write(value)

    def reserved_bytes(self) -> [bytes]:
        return [self.byte_bytes]

    def writes(self, typez: type) -> bool:
        return False
