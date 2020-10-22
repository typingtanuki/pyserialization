import unittest

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.primitive.longCodec import LongCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import to_byte
from src.test.serialization.codec.test_codec import TestCodec


class TestLongCodec(TestCodec):
    def test_wide_range(self):
        self.long_seria(None)
        self.long_seria(10)
        self.long_seria(-10)
        self.long_seria(-36029896530591744)
        self.long_seria(36028797018963968)

    def long_seria(self, value: None or int):
        codec: Codec[int] = LongCodec(to_byte(12))
        writer: ByteIo = self.writer()
        codec.write(writer, value)
        writer.close()

        reader: ByteIo = self.reader()
        pim: int = codec.read(reader)
        self.assertEqual(value, pim)
        reader.close()


if __name__ == '__main__':
    unittest.main()
