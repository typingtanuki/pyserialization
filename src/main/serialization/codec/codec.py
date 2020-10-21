from typing import TypeVar, Generic

from src.main.serialization.codec.utils.byteIo import ByteIo

T = TypeVar('T')


class Codec(Generic[T]):
    """Codec to (de)serialize type 'T' """

    def __init__(self):
        super().__init__()

    def read(self, io: ByteIo) -> T or None:
        raise NotImplemented()

    def write(self, io: ByteIo, value: T) -> None:
        raise NotImplemented()

    def reserved_bytes(self) -> [bytes]:
        raise NotImplemented()

    def writes(self, typez: type) -> bool:
        raise NotImplemented()
