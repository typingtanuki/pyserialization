from typing import List

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.object.noneCodec import NoneCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import from_byte, to_byte


class CharArrayCodec(Codec[List[str]]):
    """Codec for character list type"""

    reserved_byte: bytes

    def __init__(self, reserved_byte: bytes):
        super().__init__()

        self.reserved_byte = reserved_byte

    def read(self, io: ByteIo) -> List[str] or None:
        read: int = from_byte(io.peek())

        if read == from_byte(NoneCodec.NONE_VALUE):
            return None

        size: bytes or None = io.read_size(self.reserved_byte)

        out: List[str] = []

        encoded: bytes = io.read(size)
        string: str = encoded.decode("UTF-8")
        for char in string:
            out.append(char)
        return out

    def write(self, io: ByteIo, array: List[str]) -> None:
        if array is None:
            io.write(NoneCodec.NONE_VALUE)
            return

        encoded: bytes = "".join(array).encode("UTF-8")
        io.write_size(len(encoded), self.reserved_byte)
        io.write(encoded)

    def reserved_bytes(self) -> [bytes]:
        reserved_int: int = from_byte(self.reserved_byte)

        return [to_byte(reserved_int),
                to_byte(reserved_int + 1),
                to_byte(reserved_int + 2),
                to_byte(reserved_int + 3)]

    def writes(self, typez: type) -> bool:
        return False
