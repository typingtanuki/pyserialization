from src.main.serialization.codec.array.abstractArrayCodec import AbstractArrayCodec
from src.main.serialization.codec.primitive.longCodec import LongCodec
from src.main.serialization.codec.utils.bytes import to_byte


class LongArrayCodec(AbstractArrayCodec[int]):
    """Codec for long list type"""

    def __init__(self, reserved_byte: bytes):
        super().__init__(reserved_byte, LongCodec(to_byte(1)))

    def writes(self, typez: type) -> bool:
        return False
