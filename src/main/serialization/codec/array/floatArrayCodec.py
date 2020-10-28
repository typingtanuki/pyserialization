from src.main.serialization.codec.array.abstractArrayCodec import AbstractArrayCodec
from src.main.serialization.codec.primitive.floatCodec import FloatCodec
from src.main.serialization.codec.utils.bytes import int_to_byte


class FloatArrayCodec(AbstractArrayCodec[float]):
    """Codec for float list type"""

    def __init__(self, reserved_byte: bytes):
        super().__init__(reserved_byte, FloatCodec(int_to_byte(0)))

    def writes(self, typez: type) -> bool:
        return False
