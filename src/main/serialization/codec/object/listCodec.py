from typing import TypeVar

from src.main.serialization.codec.codecCache import CodecCache
from src.main.serialization.codec.object.collectionCodec import CollectionCodec

T = TypeVar('T')


class ListCodec(CollectionCodec[T]):
    """
    Codec for lists
    """

    def __init__(self,
                 reserved_byte: bytes,
                 codec_cache: CodecCache,
                 value_type: type or None = None):
        super().__init__(reserved_byte, codec_cache, value_type)
