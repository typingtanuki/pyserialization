import unittest

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.primitive.charCodec import CharCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import to_byte
from src.test.serialization.codec.test_codec import TestCodec


class TestCharCodec(TestCodec):
    def test_type_check(self):
        codec: Codec[str] = CharCodec(to_byte(12))
        self.assertFalse(codec.writes(bool))
        # Interop
        self.assertFalse(codec.writes(str))
        self.assertFalse(codec.writes(bytes))

    def test_a(self):
        codec: Codec[str] = CharCodec(to_byte(12))

        writer: ByteIo = self.writer()
        codec.write(writer, "a")
        writer.close()

        reader: ByteIo = self.reader()
        self.assertEqual(codec.read(reader), "a")
        reader.close()

    def test_prct(self):
        codec: Codec[str] = CharCodec(to_byte(12))

        writer: ByteIo = self.writer()
        codec.write(writer, "%")
        writer.close()

        reader: ByteIo = self.reader()
        self.assertEqual(codec.read(reader), "%")
        reader.close()

    def test_kanji(self):
        codec: Codec[str] = CharCodec(to_byte(12))

        writer: ByteIo = self.writer()
        codec.write(writer, "字")
        writer.close()

        reader: ByteIo = self.reader()
        self.assertEqual(codec.read(reader), "字")
        reader.close()

    def test_mix(self):
        codec: Codec[str] = CharCodec(to_byte(12))

        writer: ByteIo = self.writer()
        codec.write(writer, "a")
        codec.write(writer, "文")
        codec.write(writer, "字")
        codec.write(writer, None)
        codec.write(writer, "漢")
        codec.write(writer, "字")
        writer.close()

        reader: ByteIo = self.reader()
        self.assertEqual(codec.read(reader), "a")
        self.assertEqual(codec.read(reader), "文")
        self.assertEqual(codec.read(reader), "字")
        self.assertEqual(codec.read(reader), None)
        self.assertEqual(codec.read(reader), "漢")
        self.assertEqual(codec.read(reader), "字")
        reader.close()

    def test_wide_range(self):
        self.char_seria(None)
        for i in range(0, 0x10ffff, 50):
            self.char_seria(chr(i))

    def char_seria(self, value: None or str):
        codec: Codec[str] = CharCodec(to_byte(12))
        writer: ByteIo = self.writer()
        codec.write(writer, value)
        writer.close()

        reader: ByteIo = self.reader()
        self.assertEqual(codec.read(reader), value)
        reader.close()


if __name__ == '__main__':
    unittest.main()
