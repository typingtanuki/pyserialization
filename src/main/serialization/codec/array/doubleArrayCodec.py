from typing import List

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.object.noneCodec import NoneCodec
from src.main.serialization.codec.primitive.doubleCodec import DoubleCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import from_byte, to_byte


class DoubleArrayCodec(Codec[List[float]]):
    """Codec for double list type"""

    double_codec: DoubleCodec = DoubleCodec(to_byte(0))
    reserved_byte: bytes

    def __init__(self, reserved_byte: bytes):
        super().__init__()

        self.reserved_byte = reserved_byte

    def read(self, io: ByteIo) -> List[float] or None:
        read: int = from_byte(io.peek())

        if read == from_byte(NoneCodec.NONE_VALUE):
            return None

        size: bytes or None = io.read_size(self.reserved_byte)

        out: List[float] = []
        for i in range(0, size):
            out.append(self.double_codec.read(io))
        return out

    def write(self, io: ByteIo, array: List[float]) -> None:
        if array is None:
            io.write(NoneCodec.NONE_VALUE)
            return

        io.write_size(len(array), self.reserved_byte)
        for item in array:
            self.double_codec.write(io, item)

    def reserved_bytes(self) -> [bytes]:
        reserved_int: int = from_byte(self.reserved_byte)

        return [to_byte(reserved_int),
                to_byte(reserved_int + 1),
                to_byte(reserved_int + 2),
                to_byte(reserved_int + 3)]

    def writes(self, typez: type) -> bool:
        return False
