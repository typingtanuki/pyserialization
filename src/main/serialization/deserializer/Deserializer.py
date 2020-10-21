from typing import TypeVar, BinaryIO

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.codecCache import CodecCache
from src.main.serialization.codec.utils.byteIo import ByteIo

T = TypeVar('T')


class Deserializer:
    __codec_cache: CodecCache
    __reader: ByteIo

    def __init__(self, codec_cache: CodecCache, reader: BinaryIO):
        super().__init__()

        self.__codec_cache = codec_cache
        self.__reader = ByteIo(reader)

    def read(self, codec: None or Codec[T] = None) -> T:
        if codec is not None:
            return codec.read(self.__reader)

        found: Codec = self.__codec_cache.get(self.__reader.peek())
        return found.read(self.__reader)

    def close(self) -> None:
        self.__reader.close()
