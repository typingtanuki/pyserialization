from io import BufferedWriter, BufferedReader

from codec import Codec, T


class NoneCodec(Codec[None]):
    def __init__(self):
        super().__init__()

    def read(self, wrapper: BufferedReader) -> None:
        if wrapper.read1() is not None:
            raise TypeError("Could not deserialize as null.")
        return None

    def write(self, wrapper: BufferedWriter, value: None) -> None:
        wrapper.write(bytes(-128))

    def reservedBytes(self) -> [bytes]:
        return [bytes(-128)]

    def writes(self, typez: type) -> bool:
        return False
