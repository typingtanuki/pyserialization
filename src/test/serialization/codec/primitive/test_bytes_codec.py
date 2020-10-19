import unittest
from io import BufferedWriter, BufferedReader

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.primitive.bytesCodec import BytesCodec
from src.test.serialization.codec.test_codec import TestCodec
from src.main.serialization.codec.utils.bytes import to_byte


class TestBytesCodec(TestCodec):
    def test_type_check(self):
        codec: Codec[bytes] = BytesCodec(to_byte(12))
        self.assertFalse(codec.writes(bool))
        self.assertFalse(codec.writes(str))
        self.assertTrue(codec.writes(bytes))

    def test_0b(self):
        codec: Codec[bytes] = BytesCodec(to_byte(12))

        writer: BufferedWriter = self.writer()
        codec.write(writer, bytes(1))
        writer.close()

        reader: BufferedReader = self.reader()
        self.assertEqual(codec.read(reader), bytes(1))
        reader.close()

    def test_1b(self):
        codec: Codec[bytes] = BytesCodec(to_byte(12))

        writer: BufferedWriter = self.writer()
        codec.write(writer, to_byte(1))
        writer.close()

        reader: BufferedReader = self.reader()
        self.assertEqual(codec.read(reader), to_byte(1))
        reader.close()

    def test_123b(self):
        codec: Codec[bytes] = BytesCodec(to_byte(12))

        writer: BufferedWriter = self.writer()
        codec.write(writer, to_byte(123))
        writer.close()

        reader: BufferedReader = self.reader()
        self.assertEqual(codec.read(reader), to_byte(123))
        reader.close()

    def test_mix(self):
        codec: Codec[bytes] = BytesCodec(to_byte(12))

        writer: BufferedWriter = self.writer()
        codec.write(writer, to_byte(123))
        codec.write(writer, to_byte(255))
        codec.write(writer, to_byte(255))
        codec.write(writer, None)
        codec.write(writer, to_byte(123))
        codec.write(writer, to_byte(255))
        writer.close()

        reader: BufferedReader = self.reader()
        self.assertEqual(codec.read(reader), to_byte(123))
        self.assertEqual(codec.read(reader), to_byte(255))
        self.assertEqual(codec.read(reader), to_byte(255))
        self.assertEqual(codec.read(reader), None)
        self.assertEqual(codec.read(reader), to_byte(123))
        self.assertEqual(codec.read(reader), to_byte(255))
        reader.close()


if __name__ == '__main__':
    unittest.main()