from src.main.serialization.codec.array.abstractArrayCodec import AbstractArrayCodec
from src.main.serialization.codec.primitive.longCodec import LongCodec
from src.main.serialization.codec.utils.bytes import int_to_byte


class LongArrayCodec(AbstractArrayCodec[int]):
    """Codec for long list type"""

    def __init__(self, reserved_byte: bytes):
        super().__init__(reserved_byte, LongCodec(int_to_byte(0)))

    def writes(self, typez: type) -> bool:
        return False
