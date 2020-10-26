from typing import List, TypeVar

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.object.noneCodec import NoneCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import from_byte, to_byte

T = TypeVar('T')


class AbstractArrayCodec(Codec[List[T]]):
    """Codec for array of primitives"""

    codec: Codec[T]
    reserved_byte: bytes

    def __init__(self,
                 reserved_byte: bytes,
                 codec: Codec[T]):
        super().__init__()

        self.reserved_byte = reserved_byte
        self.codec = codec

    def read(self, io: ByteIo) -> List[T] or None:
        read: int = from_byte(io.peek())

        if read == from_byte(NoneCodec.NONE_VALUE):
            return None

        size: bytes or None = io.read_size(self.reserved_byte)

        out: List[T] = []
        for i in range(0, size):
            out.append(self.codec.read(io))
        return out

    def write(self, io: ByteIo, array: List[T]) -> None:
        if array is None:
            io.write(NoneCodec.NONE_VALUE)
            return

        io.write_size(len(array), self.reserved_byte)
        for item in array:
            self.codec.write(io, item)

    def reserved_bytes(self) -> [bytes]:
        reserved_int: int = from_byte(self.reserved_byte)

        return [to_byte(reserved_int),
                to_byte(reserved_int + 1),
                to_byte(reserved_int + 2),
                to_byte(reserved_int + 3)]
