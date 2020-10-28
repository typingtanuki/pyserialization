from src.main.serialization.codec.array.abstractArrayCodec import AbstractArrayCodec
from src.main.serialization.codec.primitive.intCodec import IntCodec
from src.main.serialization.codec.utils.bytes import int_to_byte


class IntArrayCodec(AbstractArrayCodec[int]):
    """Codec for int list type"""

    def __init__(self, reserved_byte: bytes):
        super().__init__(reserved_byte, IntCodec(int_to_byte(0)))

    def writes(self, typez: type) -> bool:
        return False
