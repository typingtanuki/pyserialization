import unittest
from typing import List

from src.main.serialization.codec.array.charArrayCodec import CharArrayCodec
from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import to_byte
from src.test.serialization.codec.test_codec import TestCodec


class TestCharArrayCodec(TestCodec):
    def test_wide_range(self):
        self.chars_seria(None)
        self.chars_seria([])
        self.chars_seria(["a", "b", "c", "d"])
        self.chars_seria(["漢", "字"])

    def chars_seria(self, value: None or List[str]):
        codec: Codec[str] = CharArrayCodec(to_byte(12))
        writer: ByteIo = self.writer()
        codec.write(writer, value)
        writer.close()

        reader: ByteIo = self.reader()
        self.assertEqual(codec.read(reader), value)
        reader.close()


if __name__ == '__main__':
    unittest.main()
