import collections
from typing import Set, List

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.codecCache import CodecCache
from src.main.serialization.codec.object.noneCodec import NoneCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import *


class CollectionCodec(Codec[List[any]]):
    """
    Codec for collections
    """

    reserved_byte: bytes
    codec_cache: CodecCache

    def __init__(self, reserved_byte: bytes, codec_cache: CodecCache):
        super().__init__()

        self.reserved_byte = reserved_byte
        self.codec_cache = codec_cache

    def read(self, io: ByteIo) -> List[any] or None:
        read: int = from_byte(io.peek())

        if read == from_byte(NoneCodec.NONE_VALUE):
            return None

        size: int = io.read_size(self.reserved_byte)

        out: List[any] = []
        for i in range(0, size):
            out.append(self.codec_cache.get(io.peek()).read(io))
        return out

    def write(self, io: ByteIo, value: List[any]) -> None:
        if value is None:
            io.write(NoneCodec.NONE_VALUE)
            return

        io.write_size(len(value), self.reserved_byte)

        for value in value:
            self.codec_cache.codec_for(value).write(io, value)

    def reserved_bytes(self) -> [bytes]:
        reserved_int: int = from_byte(self.reserved_byte)

        return [to_byte(reserved_int),
                to_byte(reserved_int + 1),
                to_byte(reserved_int + 2),
                to_byte(reserved_int + 3)]

    def writes(self, typez: type) -> bool:
        return False
