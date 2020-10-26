from src.main.serialization.codec.array.abstractArrayCodec import AbstractArrayCodec
from src.main.serialization.codec.primitive.intCodec import IntCodec
from src.main.serialization.codec.utils.bytes import to_byte


class IntArrayCodec(AbstractArrayCodec[int]):
    """Codec for int list type"""

    def __init__(self, reserved_byte: bytes):
        super().__init__(reserved_byte, IntCodec(to_byte(1)))

    def writes(self, typez: type) -> bool:
        return False
