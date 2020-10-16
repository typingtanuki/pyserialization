from io import BufferedReader, BufferedWriter
from typing import TypeVar, Generic

T = TypeVar('T')


class Codec(Generic[T]):
    NULL: bytes = bytes(-128)

    def __init__(self):
        super().__init__()

    def read(self, wrapper: BufferedReader) -> T:
        raise NotImplemented()

    def write(self, wrapper: BufferedWriter, value: T) -> None:
        raise NotImplemented()

    def reservedBytes(self) -> [bytes]:
        raise NotImplemented()

    def writes(self, typez: type) -> bool:
        raise NotImplemented()
