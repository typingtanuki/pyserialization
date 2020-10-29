from typing import Set, TypeVar

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.codecCache import CodecCache
from src.main.serialization.codec.object.noneCodec import NoneCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import *

T = TypeVar('T')


class SetCodec(Codec[Set[any]]):
    """
    Codec for sets
    """

    reserved_byte: bytes
    codec_cache: CodecCache
    value_codec: Codec[T] or None

    def __init__(self,
                 reserved_byte: bytes,
                 codec_cache: CodecCache,
                 value_type: type or None = None):
        super().__init__()

        self.reserved_byte = reserved_byte
        self.codec_cache = codec_cache
        if value_type is None:
            self.value_codec = None
        else:
            self.value_codec = codec_cache.codec_for_type(value_type)

    def read(self, io: ByteIo) -> Set[T] or None:
        read: int = from_byte(io.peek())

        if read == from_byte(NoneCodec.NONE_VALUE):
            return None

        size: int = io.read_size(self.reserved_byte)

        out: Set[any] = set()
        for i in range(0, size):
            codec: Codec = self.value_codec
            if codec is None:
                codec = self.codec_cache.get(io.peek())
            out.add(codec.read(io))
        return out

    def write(self, io: ByteIo, collection: Set[T]) -> None:
        if collection is None:
            io.write(NoneCodec.NONE_VALUE)
            return

        io.write_size(len(collection), self.reserved_byte)

        for value in collection:
            codec: Codec = self.value_codec
            if codec is None:
                codec = self.codec_cache.codec_for(value)
            codec.write(io, value)

    def reserved_bytes(self) -> [bytes]:
        reserved_int: int = from_byte(self.reserved_byte)

        return [to_byte(reserved_int),
                to_byte(reserved_int + 1),
                to_byte(reserved_int + 2),
                to_byte(reserved_int + 3)]

    def writes(self, typez: type) -> bool:
        if typez is set:
            return True
        return False
