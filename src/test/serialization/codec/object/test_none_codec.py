import unittest

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.object.noneCodec import NoneCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.test.serialization.codec.test_codec import TestCodec


class TestNoneCodec(TestCodec):
    def test_type_check(self):
        codec: Codec[None] = NoneCodec()
        self.assertFalse(codec.writes(bool))
        self.assertFalse(codec.writes(str))
        self.assertFalse(codec.writes(bytes))
        self.assertTrue(codec.writes(type(None)))

    def test_none(self):
        codec: Codec[None] = NoneCodec()

        writer: ByteIo = self.writer()
        codec.write(writer, None)
        writer.close()

        reader: ByteIo = self.reader()
        self.assertEqual(codec.read(reader), None)
        reader.close()

    def test_mix(self):
        codec: Codec[None] = NoneCodec()

        writer: ByteIo = self.writer()
        codec.write(writer, None)
        codec.write(writer, None)
        codec.write(writer, None)
        writer.close()

        reader: ByteIo = self.reader()
        self.assertEqual(codec.read(reader), None)
        self.assertEqual(codec.read(reader), None)
        self.assertEqual(codec.read(reader), None)
        reader.close()


if __name__ == '__main__':
    unittest.main()
