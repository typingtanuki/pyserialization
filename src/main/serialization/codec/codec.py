from io import BufferedReader, BufferedWriter
from typing import TypeVar, Generic

T = TypeVar('T')


class Codec(Generic[T]):
    """Codec to (de)serialize type 'T' """

    def __init__(self):
        super().__init__()

    def read(self, wrapper: BufferedReader) -> T or None:
        raise NotImplemented()

    def write(self, wrapper: BufferedWriter, value: T) -> None:
        raise NotImplemented()

    def reserved_bytes(self) -> [bytes]:
        raise NotImplemented()

    def writes(self, typez: type) -> bool:
        raise NotImplemented()
