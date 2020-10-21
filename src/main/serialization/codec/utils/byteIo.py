from typing import BinaryIO


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

    def read(self) -> bytes:
        if self.__peek is not None:
            value: bytes = self.__peek
            self.__peek = None
            return value

        return self.__io.read(1)

    def read2(self) -> bytes:
        if self.__peek is not None:
            raise ValueError("Being peaked")

        return self.__io.read(2)

    def read3(self) -> bytes:
        if self.__peek is not None:
            raise ValueError("Being peaked")

        return self.__io.read(3)

    def write(self, byte: bytes) -> None:
        if self.__peek is not None:
            raise ValueError("Being peaked")

        self.__io.write(byte)

    def close(self) -> None:
        self.__io.close()
