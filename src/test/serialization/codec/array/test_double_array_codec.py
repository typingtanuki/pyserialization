import unittest
from typing import List

from src.main.serialization.codec.array.doubleArrayCodec import DoubleArrayCodec
from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import to_byte
from src.test.serialization.codec.test_codec import TestCodec


class TestDoubleArrayCodec(TestCodec):
    def test_wide_range(self):
        self.double_seria(None)
        self.double_seria([])
        self.double_seria([1.2, -1.3])

    def double_seria(self, value: None or List[float]):
        codec: Codec[float] = DoubleArrayCodec(to_byte(12))
        writer: ByteIo = self.writer()
        codec.write(writer, value)
        writer.close()

        reader: ByteIo = self.reader()
        self.assertEqual(codec.read(reader), value)
        reader.close()


if __name__ == '__main__':
    unittest.main()
