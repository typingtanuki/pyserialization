from typing import Dict, TypeVar

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.codecCache import CodecCache
from src.main.serialization.codec.object.noneCodec import NoneCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import *

T = TypeVar('T')
U = TypeVar('U')


class MapCodec(Codec[Dict[T, U]]):
    """
    Codec for dictionaries
    """

    reserved_byte: bytes
    codec_cache: CodecCache

    key_codec: Codec[T] or None
    value_codec: Codec[U] or None

    def __init__(self,
                 reserved_byte: bytes,
                 codec_cache: CodecCache,
                 key_type: type or None = None,
                 value_type: type or None = None):
        super().__init__()

        self.reserved_byte = reserved_byte
        self.codec_cache = codec_cache

        if key_type is None:
            self.key_codec = None
        else:
            self.key_codec = codec_cache.codec_for_type(key_type)

        if value_type is None:
            self.value_codec = None
        else:
            self.value_codec = codec_cache.codec_for_type(value_type)

    def read(self, io: ByteIo) -> Dict[T, U] or None:
        read: int = from_byte(io.peek())

        if read == from_byte(NoneCodec.NONE_VALUE):
            return None

        size: int = io.read_size(self.reserved_byte)

        out: Dict[T, U] = {}
        for i in range(0, size):
            k_codec: Codec[T] = self.key_codec
            if k_codec is None:
                k_codec = self.codec_cache.get(io.peek())
            key: T = k_codec.read(io)

            v_codec: Codec[U] = self.value_codec
            if v_codec is None:
                v_codec = self.codec_cache.get(io.peek())
            value: T = v_codec.read(io)

            out[key] = value
        return out

    def write(self, io: ByteIo, dictionary: Dict[T, U]) -> None:
        if dictionary is None:
            io.write(NoneCodec.NONE_VALUE)
            return

        io.write_size(len(dictionary), self.reserved_byte)

        for key, value in dictionary.items():
            k_codec: Codec[T] = self.key_codec
            if k_codec is None:
                k_codec = self.codec_cache.codec_for(key)

            v_codec: Codec[U] = self.value_codec
            if v_codec is None:
                v_codec = self.codec_cache.codec_for(value)

            k_codec.write(io, key)
            v_codec.write(io, value)

    def reserved_bytes(self) -> [bytes]:
        reserved_int: int = from_byte(self.reserved_byte)

        return [to_byte(reserved_int),
                to_byte(reserved_int + 1),
                to_byte(reserved_int + 2),
                to_byte(reserved_int + 3)]

    def writes(self, typez: type) -> bool:
        if typez is Dict:
            return True
        return False
