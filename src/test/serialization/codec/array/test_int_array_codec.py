import unittest
from typing import List

from src.main.serialization.codec.array.intArrayCodec import IntArrayCodec
from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import to_byte
from src.test.serialization.codec.test_codec import TestCodec


class TestIntArrayCodec(TestCodec):
    def test_wide_range(self):
        self.ints_seria(None)
        self.ints_seria([])
        self.ints_seria([1, 2, -3])

    def ints_seria(self, value: None or List[int]):
        codec: Codec[float] = IntArrayCodec(to_byte(12))
        writer: ByteIo = self.writer()
        codec.write(writer, value)
        writer.close()

        reader: ByteIo = self.reader()
        self.assertEqual(codec.read(reader), value)
        reader.close()


if __name__ == '__main__':
    unittest.main()
