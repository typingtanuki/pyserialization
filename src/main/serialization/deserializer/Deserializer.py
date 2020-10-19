from io import BufferedReader
from typing import TypeVar

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.codecCache import CodecCache

T = TypeVar('T')


class Deserializer:
    __codec_cache: CodecCache
    __reader: BufferedReader

    def __init__(self, codec_cache: CodecCache, reader: BufferedReader):
        super().__init__()

        self.__codec_cache = codec_cache
        self.__reader = reader

    def read(self, codec: None or Codec[T] = None) -> T:
        if codec is not None:
            return codec.read(self.__reader)

        found: Codec = self.__codec_cache.get(self.__reader.peek())
        return found.read(self.__reader)
