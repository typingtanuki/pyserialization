from src.main.serialization.codec.array.abstractArrayCodec import AbstractArrayCodec
from src.main.serialization.codec.primitive.doubleCodec import DoubleCodec
from src.main.serialization.codec.utils.bytes import int_to_byte


class DoubleArrayCodec(AbstractArrayCodec[float]):
    """Codec for double list type"""

    def __init__(self, reserved_byte: bytes):
        super().__init__(reserved_byte, DoubleCodec(int_to_byte(0)))

    def writes(self, typez: type) -> bool:
        return False
