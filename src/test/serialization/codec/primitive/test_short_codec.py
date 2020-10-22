import unittest

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.primitive.shortCodec import ShortCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import to_byte
from src.test.serialization.codec.test_codec import TestCodec


class TestShortCodec(TestCodec):
    def test_wide_range(self):
        self.short_seria(None)
        self.short_seria(10)
        self.short_seria(-10)
        self.short_seria(-32768)
        self.short_seria(32767)

    def short_seria(self, value: None or int):
        codec: Codec[int] = ShortCodec(to_byte(12))
        writer: ByteIo = self.writer()
        codec.write(writer, value)
        writer.close()

        reader: ByteIo = self.reader()
        pim: int = codec.read(reader)
        self.assertEqual(value, pim)
        reader.close()


if __name__ == '__main__':
    unittest.main()
