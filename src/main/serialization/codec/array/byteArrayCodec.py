from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.object.noneCodec import NoneCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import from_byte, to_byte


class ByteArrayCodec(Codec[bytes]):
    """Codec for bytes type"""

    reserved_byte: bytes

    def __init__(self, reserved_byte: bytes):
        super().__init__()

        self.reserved_byte = reserved_byte

    def read(self, io: ByteIo) -> bytes or None:
        read: int = from_byte(io.peek())

        if read == from_byte(NoneCodec.NONE_VALUE):
            return None

        size: bytes or None = io.read_size(self.reserved_byte)

        if size == 0:
            return bytes()
        return io.read(size)

    def write(self, io: ByteIo, array: bytes) -> None:
        if array is None:
            io.write(NoneCodec.NONE_VALUE)
            return

        io.write_size(len(array), self.reserved_byte)
        io.write(array)

    def reserved_bytes(self) -> [bytes]:
        reserved_int: int = from_byte(self.reserved_byte)

        return [to_byte(reserved_int),
                to_byte(reserved_int + 1),
                to_byte(reserved_int + 2),
                to_byte(reserved_int + 3)]

    def writes(self, typez: type) -> bool:
        if typez is bytes:
            return True
        return False
