import collections
from typing import Deque, TypeVar

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.codecCache import CodecCache
from src.main.serialization.codec.object.noneCodec import NoneCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import *

T = TypeVar('T')


class QueueCodec(Codec[Deque[T]]):
    """
    Codec for queues
    """

    start: bytes
    end: bytes

    codec_cache: CodecCache
    value_codec: Codec[T] or None

    def __init__(self,
                 reserved_byte: bytes,
                 codec_cache: CodecCache,
                 value_type: type or None = None):
        super().__init__()

        self.start = reserved_byte
        self.end = int_to_byte(int_from_byte(reserved_byte) + 1)
        self.codec_cache = codec_cache
        if value_type is None:
            self.value_codec = None
        else:
            self.value_codec = codec_cache.codec_for_type(value_type)

    def read(self, io: ByteIo) -> Deque[T] or None:
        marker: bytes = io.read()

        if marker == NoneCodec.NONE_VALUE:
            return None

        if marker != self.start:
            raise TypeError("Start of queue not found")

        out: Deque[T] = collections.deque()

        while True:
            marker = io.peek()

            if marker == self.end:
                io.read()
                return out

            codec: Codec = self.value_codec
            if codec is None:
                codec = self.codec_cache.get(marker)
            out.append(codec.read(io))

    def write(self, io: ByteIo, collection: Deque[T]) -> None:
        if collection is None:
            io.write(NoneCodec.NONE_VALUE)
            return

        io.write(self.start)
        for value in collection:
            codec: Codec = self.value_codec
            if codec is None:
                codec = self.codec_cache.codec_for(value)
            codec.write(io, value)
        io.write(self.end)

    def reserved_bytes(self) -> [bytes]:
        return [self.start, self.end]

    def writes(self, typez: type) -> bool:
        if typez is collections.deque:
            return True
        return False
