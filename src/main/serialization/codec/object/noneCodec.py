from io import BufferedWriter, BufferedReader

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.utils.bytes import to_byte


class NoneCodec(Codec[None]):
    """Codec for the None type"""

    NONE_VALUE: bytes = to_byte(0)
    """Special value used to encode 'None'"""

    def __init__(self):
        super().__init__()

    def read(self, wrapper: BufferedReader) -> None:
        if wrapper.read(1) != NoneCodec.NONE_VALUE:
            raise TypeError("Could not deserialize as null.")
        return None

    def write(self, wrapper: BufferedWriter, value: None) -> None:
        wrapper.write(NoneCodec.NONE_VALUE)

    def reserved_bytes(self) -> [bytes]:
        return [NoneCodec.NONE_VALUE]

    def writes(self, typez: type) -> bool:
        if typez is type(None):
            return True
        return False
