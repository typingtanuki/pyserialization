from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.object.noneCodec import NoneCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import *


class StringCodec(Codec[str]):
    """
    Codec for strings
    """

    optimized_from: int
    size_1: int

    def __init__(self, reserved_byte: bytes, optimized_count: int):
        super().__init__()

        self.optimized_from = from_byte(reserved_byte)
        self.size_1 = from_byte(reserved_byte) + optimized_count

    def read(self, io: ByteIo) -> str or None:
        size: int or None
        read: int = from_byte(io.peek())

        if read == from_byte(NoneCodec.NONE_VALUE):
            return None

        if self.optimized_from <= read < self.size_1:
            size = read - self.optimized_from
        else:
            size = io.read_size(to_byte(self.size_1))
        if size is None:
            return None

        if size == 0:
            return ""

        raw_bytes: bytes = io.read(size)
        return str(raw_bytes, "UTF-8")

    def write(self, io: ByteIo, value: str) -> None:
        if value is None:
            io.write(NoneCodec.NONE_VALUE)
            return

        data: bytes = value.encode("UTF-8")
        length: int = len(data)
        if length < self.size_1 - self.optimized_from:
            io.write(to_byte((self.optimized_from + length) & 0xFF))
        else:
            io.write_size(length, to_byte(self.size_1))
        if length != 0:
            io.write(data)

    def reserved_bytes(self) -> [bytes]:
        size: int = self.size_1 - self.optimized_from + 4
        reserved: [bytes] = []
        for i in range(0, size):
            reserved.append(to_byte((self.optimized_from + i) & 0xFF))
        return reserved

    def writes(self, typez: type) -> bool:
        if typez is str:
            return True
        return False
