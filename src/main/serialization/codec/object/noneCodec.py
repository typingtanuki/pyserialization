from io import BufferedWriter, BufferedReader

from src.main.serialization.codec.codec import Codec


class NoneCodec(Codec[None]):
    NULL_VALUE: bytes = Codec.to_byte(0)

    def __init__(self):
        super().__init__()

    def read(self, wrapper: BufferedReader) -> None:
        if wrapper.read(1) != NoneCodec.NULL_VALUE:
            raise TypeError("Could not deserialize as null.")
        return None

    def write(self, wrapper: BufferedWriter, value: None) -> None:
        wrapper.write(NoneCodec.NULL_VALUE)

    def reserved_bytes(self) -> [bytes]:
        return [NoneCodec.NULL_VALUE]

    def writes(self, typez: type) -> bool:
        if typez is type(None):
            return True
        return False
