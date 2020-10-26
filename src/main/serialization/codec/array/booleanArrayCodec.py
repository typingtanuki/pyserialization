from typing import List

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.object.noneCodec import NoneCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import int_from_byte, from_byte, to_byte


class BooleanArrayCodec(Codec[List[bool]]):
    """Codec for bool list type"""

    reserved_byte: bytes

    def __init__(self, reserved_byte: bytes):
        super().__init__()

        self.reserved_byte = reserved_byte

    def read(self, io: ByteIo) -> List[bool] or None:
        read: int = from_byte(io.peek())

        if read == from_byte(NoneCodec.NONE_VALUE):
            return None

        size: bytes or None = io.read_size(self.reserved_byte)

        out: List[bool] = []
        i: int = 0
        value: int = 0
        read: int = 8
        while i < size:
            if read == 8:
                value = int_from_byte(io.read(1))
                read = 0
            decoded: bool = (value & 0b10000000) != 0
            out.append(decoded)
            i += 1
            value = value << 1
            read += 1

        return out

    def write(self, io: ByteIo, array: List[bool]) -> None:
        if array is None:
            io.write(NoneCodec.NONE_VALUE)
            return

        io.write_size(len(array), self.reserved_byte)
        current_count: int = 0
        value: int = 0

        for element in array:
            bool_int: int = 0
            if element:
                bool_int = 1
            value = value << 1 | bool_int
            if current_count == 7:
                current_count = 0
                io.write1(value)
            else:
                current_count = current_count + 1
        if current_count > 0:
            io.write1(value << (8 - current_count))

    def reserved_bytes(self) -> [bytes]:
        reserved_int: int = from_byte(self.reserved_byte)

        return [to_byte(reserved_int),
                to_byte(reserved_int + 1),
                to_byte(reserved_int + 2),
                to_byte(reserved_int + 3)]

    def writes(self, typez: type) -> bool:
        return False
