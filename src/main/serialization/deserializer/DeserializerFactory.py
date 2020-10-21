from typing import BinaryIO

from src.main.serialization.codec.codecCache import CodecCache
from src.main.serialization.deserializer.Deserializer import Deserializer


class DeserializerFactory:
    __codec_cache: CodecCache

    def __init__(self, codec_cache: CodecCache):
        super().__init__()

        self.__codec_cache = codec_cache

    def new_deserializer(self, reader: BinaryIO) -> Deserializer:
        return Deserializer(self.__codec_cache, reader)
