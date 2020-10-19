from io import BufferedWriter
from typing import TypeVar

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.codecCache import CodecCache

T = TypeVar('T')


class Serializer:
    __codec_cache: CodecCache
    __writer: BufferedWriter

    def __init__(self, codec_cache: CodecCache, writer: BufferedWriter):
        super().__init__()

        self.__codec_cache = codec_cache
        self.__writer = writer

    def append(self, value: T) -> None:
        codec: Codec[T] = self.__codec_cache.codec_for(value)

        if codec is None:
            raise ValueError(f"Missing codec for {type(value)}")

        codec.write(self.__writer, value)

    def append(self, value: T, codec: Codec[T]) -> None:
        codec.write(self.__writer, value)

    def close(self) -> None:
        self.__writer.close()
