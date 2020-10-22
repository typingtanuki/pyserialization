from typing import BinaryIO

from src.main.serialization.codec.utils.bytes import int_from_byte, join_bytes, byte_length


class ByteIo:
    __io: BinaryIO
    __peek: None or bytes = None

    def __init__(self, io: BinaryIO):
        self.__io = io

    def peek(self) -> bytes:
        if self.__peek is not None:
            raise ValueError("Already peaked")

        self.__peek = self.__io.read(1)
        return self.__peek

    def read(self,
             length: int = 1,
             buffer_size: int or None = None) -> bytes:
        out: bytes
        if self.__peek is not None:
            value: bytes = self.__peek
            self.__peek = None

            if length == 1:
                out = value
            else:
                out = join_bytes(value, self.read(length - 1))
        else:
            out = self.__io.read(length)

        if buffer_size is None:
            return out

        return byte_length(out, buffer_size)

    def read_int(self, length: int = 1) -> int:
        return int_from_byte(self.read(length))

    def write(self, byte: bytes) -> None:
        if self.__peek is not None:
            raise ValueError("Being peaked")

        self.__io.write(byte)

    def close(self) -> None:
        self.__io.close()

    def write1(self, value: int) -> None:
        self.__io.write((value & 0xFF).to_bytes(1, byteorder="big"))

    def write2(self, value: int) -> None:
        self.__io.write(((value >> 8) & 0xFF).to_bytes(1, byteorder="big"))
        self.write1(value)

    def write3(self, value: int) -> None:
        self.__io.write(((value >> 16) & 0xFF).to_bytes(1, byteorder="big"))
        self.write2(value)

    def write4(self, value: int) -> None:
        self.__io.write(((value >> 24) & 0xFF).to_bytes(1, byteorder="big"))
        self.write3(value)

    def write5(self, value: int) -> None:
        self.__io.write(((value >> 32) & 0xFF).to_bytes(1, byteorder="big"))
        self.write4(value)

    def write6(self, value: int) -> None:
        self.__io.write(((value >> 40) & 0xFF).to_bytes(1, byteorder="big"))
        self.write5(value)

    def write7(self, value: int) -> None:
        self.__io.write(((value >> 48) & 0xFF).to_bytes(1, byteorder="big"))
        self.write6(value)

    def write8(self, value: int) -> None:
        self.__io.write(((value >> 56) & 0xFF).to_bytes(1, byteorder="big"))
        self.write7(value)
