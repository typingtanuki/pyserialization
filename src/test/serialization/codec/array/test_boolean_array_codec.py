import unittest
from typing import List

from src.main.serialization.codec.array.booleanArrayCodec import BooleanArrayCodec
from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import to_byte
from src.test.serialization.codec.test_codec import TestCodec


class TestBooleanArrayCodec(TestCodec):
    def test_wide_range(self):
        self.boolean_seria(None)
        self.boolean_seria([True])
        self.boolean_seria([False])
        self.boolean_seria([False, True, True, False, True])

    def boolean_seria(self, value: None or List[bool]):
        codec: Codec[List[bool]] = BooleanArrayCodec(to_byte(12))
        writer: ByteIo = self.writer()
        codec.write(writer, value)
        writer.close()

        reader: ByteIo = self.reader()
        self.assertEqual(codec.read(reader), value)
        reader.close()


if __name__ == '__main__':
    unittest.main()
