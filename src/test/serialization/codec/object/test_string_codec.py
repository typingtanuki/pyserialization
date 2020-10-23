import unittest

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.object.stringCodec import StringCodec
from src.main.serialization.codec.primitive.shortCodec import ShortCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import to_byte
from src.test.serialization.codec.test_codec import TestCodec


class TestStringCodec(TestCodec):
    def test_wide_range(self):
        self.string_seria(None)
        self.string_seria("abc")
        self.string_seria("123")
        self.string_seria("ほげほげ")
        self.string_seria("漢字漢字")
        self.string_seria("""  % Total\t\t\t\t    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0   162    0     0    0     0      0   \t\t\t   0 --:--:-- --:--:-- --:--:--     0
100     6    0     6    0  \r\n\0\t\t\t   0      0      0 --:--:--  0:00:09 --:--:--     1      漢字漢字漢字漢字漢字漢字漢字漢字
  漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字
  漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字
  漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字漢字""")

    def string_seria(self, value: None or str):
        codec: Codec[str] = StringCodec(to_byte(12), 0)
        writer: ByteIo = self.writer()
        codec.write(writer, value)
        writer.close()

        reader: ByteIo = self.reader()
        pim: int = codec.read(reader)
        self.assertEqual(value, pim)
        reader.close()


if __name__ == '__main__':
    unittest.main()
