from typing import List

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.object.noneCodec import NoneCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import from_byte, to_byte, int_from_byte


class ShortArrayCodec(Codec[List[int]]):
    """Codec for short list type"""

    reserved_byte: bytes

    def __init__(self, reserved_byte: bytes):
        super().__init__()

        self.reserved_byte = reserved_byte

    def read(self, io: ByteIo) -> List[int] or None:
        read: int = from_byte(io.peek())

        if read == from_byte(NoneCodec.NONE_VALUE):
            return None

        size: bytes or None = io.read_size(self.reserved_byte)

        out: List[int] = []
        for i in range(0, size):
            out.append(int_from_byte(io.read(2)))

        return out

    def write(self, io: ByteIo, array: List[int]) -> None:
        if array is None:
            io.write(NoneCodec.NONE_VALUE)
            return

        io.write_size(len(array), self.reserved_byte)

        for element in array:
            io.write1(element >> 8)
            io.write1(element)

    def reserved_bytes(self) -> [bytes]:
        reserved_int: int = from_byte(self.reserved_byte)

        return [to_byte(reserved_int),
                to_byte(reserved_int + 1),
                to_byte(reserved_int + 2),
                to_byte(reserved_int + 3)]

    def writes(self, typez: type) -> bool:
        return False
