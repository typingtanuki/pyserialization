from typing import BinaryIO
from typing import TypeVar

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.codecCache import CodecCache
from src.main.serialization.codec.utils.byteIo import ByteIo

T = TypeVar('T')


class Serializer:
    __codec_cache: CodecCache
    __writer: ByteIo

    def __init__(self, codec_cache: CodecCache, writer: BinaryIO):
        super().__init__()

        self.__codec_cache = codec_cache
        self.__writer = ByteIo(writer)

    def append(self, value: T, codec: None or Codec[T]) -> None:
        if codec is not None:
            codec.write(self.__writer, value)
            return

        codec: Codec[T] = self.__codec_cache.codec_for(value)

        if codec is None:
            raise ValueError(f"Missing codec for {type(value)}")

        codec.write(self.__writer, value)

    def close(self) -> None:
        self.__writer.close()
