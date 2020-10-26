import unittest

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.primitive.bytesCodec import BytesCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import to_byte
from src.test.serialization.codec.test_codec import TestCodec


class TestBytesCodec(TestCodec):
    def test_0b(self):
        codec: Codec[bytes] = BytesCodec(to_byte(12))

        writer: ByteIo = self.writer()
        codec.write(writer, bytes(1))
        writer.close()

        reader: ByteIo = self.reader()
        self.assertEqual(codec.read(reader), bytes(1))
        reader.close()

    def test_1b(self):
        codec: Codec[bytes] = BytesCodec(to_byte(12))

        writer: ByteIo = self.writer()
        codec.write(writer, to_byte(1))
        writer.close()

        reader: ByteIo = self.reader()
        self.assertEqual(codec.read(reader), to_byte(1))
        reader.close()

    def test_123b(self):
        codec: Codec[bytes] = BytesCodec(to_byte(12))

        writer: ByteIo = self.writer()
        codec.write(writer, to_byte(123))
        writer.close()

        reader: ByteIo = self.reader()
        self.assertEqual(codec.read(reader), to_byte(123))
        reader.close()

    def test_mix(self):
        codec: Codec[bytes] = BytesCodec(to_byte(12))

        writer: ByteIo = self.writer()
        codec.write(writer, to_byte(123))
        codec.write(writer, to_byte(255))
        codec.write(writer, to_byte(255))
        codec.write(writer, None)
        codec.write(writer, to_byte(123))
        codec.write(writer, to_byte(255))
        writer.close()

        reader: ByteIo = self.reader()
        self.assertEqual(codec.read(reader), to_byte(123))
        self.assertEqual(codec.read(reader), to_byte(255))
        self.assertEqual(codec.read(reader), to_byte(255))
        self.assertEqual(codec.read(reader), None)
        self.assertEqual(codec.read(reader), to_byte(123))
        self.assertEqual(codec.read(reader), to_byte(255))
        reader.close()

    def test_wide_range(self):
        self.byte_seria(None)
        for i in range(0, 255):
            self.byte_seria(to_byte(i))

    def byte_seria(self, value: None or bytes):
        codec: Codec[bytes] = BytesCodec(to_byte(12))
        writer: ByteIo = self.writer()
        codec.write(writer, value)
        writer.close()

        reader: ByteIo = self.reader()
        self.assertEqual(codec.read(reader), value)
        reader.close()


if __name__ == '__main__':
    unittest.main()
