import unittest

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.primitive.intCodec import IntCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import to_byte
from src.test.serialization.codec.test_codec import TestCodec


class TestIntCodec(TestCodec):
    def test_wide_range(self):
        self.int_seria(None)
        self.int_seria(10)
        self.int_seria(-10)
        self.int_seria(-2147483648)
        self.int_seria(2147483647)

    def int_seria(self, value: None or int):
        codec: Codec[int] = IntCodec(to_byte(12))
        writer: ByteIo = self.writer()
        codec.write(writer, value)
        writer.close()

        reader: ByteIo = self.reader()
        pim: int = codec.read(reader)
        self.assertEqual(value, pim)
        reader.close()


if __name__ == '__main__':
    unittest.main()
