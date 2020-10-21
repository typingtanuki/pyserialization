import unittest

from src.main.serialization.codec.utils.byteIo import ByteIo


class TestCodec(unittest.TestCase):
    def writer(self) -> ByteIo:
        file: str = "/d/tmp/seria.test"
        return ByteIo(open(file, "wb"))

    def reader(self) -> ByteIo:
        file: str = "/d/tmp/seria.test"
        return ByteIo(open(file, "rb"))


if __name__ == '__main__':
    unittest.main()
