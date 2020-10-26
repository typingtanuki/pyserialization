import unittest
from typing import List

from src.main.serialization.codec.array.byteArrayCodec import ByteArrayCodec
from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import to_byte
from src.test.serialization.codec.test_codec import TestCodec


class TestByteArrayCodec(TestCodec):
    def test_wide_range(self):
        self.bytes_seria(None)
        self.bytes_seria(bytes())
        self.bytes_seria(bytes(10))
        self.bytes_seria("abcd".encode("UTF-8"))

    def bytes_seria(self, value: None or List[bool]):
        codec: Codec[bytes] = ByteArrayCodec(to_byte(12))
        writer: ByteIo = self.writer()
        codec.write(writer, value)
        writer.close()

        reader: ByteIo = self.reader()
        self.assertEqual(codec.read(reader), value)
        reader.close()


if __name__ == '__main__':
    unittest.main()
