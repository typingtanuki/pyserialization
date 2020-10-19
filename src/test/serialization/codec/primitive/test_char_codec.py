import unittest
from io import BufferedWriter, BufferedReader

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.primitive.charCodec import CharCodec
from src.test.serialization.codec.test_codec import TestCodec
from src.main.serialization.codec.utils.bytes import to_byte


class TestCharCodec(TestCodec):
    def test_type_check(self):
        codec: Codec[str] = CharCodec(to_byte(12))
        self.assertFalse(codec.writes(bool))
        self.assertTrue(codec.writes(str))
        self.assertFalse(codec.writes(bytes))

    def test_a(self):
        codec: Codec[str] = CharCodec(to_byte(12))

        writer: BufferedWriter = self.writer()
        codec.write(writer, "a")
        writer.close()

        reader: BufferedReader = self.reader()
        self.assertEqual(codec.read(reader), "a")
        reader.close()

    def test_prct(self):
        codec: Codec[str] = CharCodec(to_byte(12))

        writer: BufferedWriter = self.writer()
        codec.write(writer, "%")
        writer.close()

        reader: BufferedReader = self.reader()
        self.assertEqual(codec.read(reader), "%")
        reader.close()

    def test_kanji(self):
        codec: Codec[str] = CharCodec(to_byte(12))

        writer: BufferedWriter = self.writer()
        codec.write(writer, "字")
        writer.close()

        reader: BufferedReader = self.reader()
        self.assertEqual(codec.read(reader), "字")
        reader.close()

    def test_mix(self):
        codec: Codec[str] = CharCodec(to_byte(12))

        writer: BufferedWriter = self.writer()
        codec.write(writer, "a")
        codec.write(writer, "文")
        codec.write(writer, "字")
        codec.write(writer, None)
        codec.write(writer, "漢")
        codec.write(writer, "字")
        writer.close()

        reader: BufferedReader = self.reader()
        self.assertEqual(codec.read(reader), "a")
        self.assertEqual(codec.read(reader), "文")
        self.assertEqual(codec.read(reader), "字")
        self.assertEqual(codec.read(reader), None)
        self.assertEqual(codec.read(reader), "漢")
        self.assertEqual(codec.read(reader), "字")
        reader.close()


if __name__ == '__main__':
    unittest.main()
