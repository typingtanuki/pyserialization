from src.main.serialization.codec.codecCache import CodecCache
from src.main.serialization.serializer.Serializer import Serializer


class SerializerFactory:
    __codec_cache: CodecCache

    def __init__(self, codec_cache: CodecCache):
        super().__init__()
        self.__codec_cache = codec_cache

    def new_serializer(self) -> Serializer:
        return Serializer(self.__codec_cache)
