import unittest

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.primitive.booleanCodec import BooleanCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import to_byte
from src.test.serialization.codec.test_codec import TestCodec


class TestBooleanCodec(TestCodec):
    def test_type_check(self):
        codec: Codec[bool] = BooleanCodec(to_byte(12))
        self.assertTrue(codec.writes(bool))
        self.assertFalse(codec.writes(str))

    def test_true(self):
        codec: Codec[bool] = BooleanCodec(to_byte(12))

        writer: ByteIo = self.writer()
        codec.write(writer, True)
        writer.close()

        reader: ByteIo = self.reader()
        self.assertTrue(codec.read(reader))
        reader.close()

    def test_false(self):
        codec: Codec[bool] = BooleanCodec(to_byte(12))

        writer: ByteIo = self.writer()
        codec.write(writer, False)
        writer.close()

        reader: ByteIo = self.reader()
        self.assertFalse(codec.read(reader))
        reader.close()

    def test_mix(self):
        codec: Codec[bool] = BooleanCodec(to_byte(12))

        writer: ByteIo = self.writer()
        codec.write(writer, False)
        codec.write(writer, True)
        codec.write(writer, True)
        codec.write(writer, None)
        codec.write(writer, False)
        codec.write(writer, True)
        writer.close()

        reader: ByteIo = self.reader()
        self.assertFalse(codec.read(reader))
        self.assertTrue(codec.read(reader))
        self.assertTrue(codec.read(reader))
        self.assertEqual(codec.read(reader), None)
        self.assertFalse(codec.read(reader))
        self.assertTrue(codec.read(reader))
        reader.close()

    def test_wide_range(self):
        self.boolean_seria(None)
        self.boolean_seria(True)
        self.boolean_seria(False)

    def boolean_seria(self, value: None or bool):
        codec: Codec[bool] = BooleanCodec(to_byte(12))
        writer: ByteIo = self.writer()
        codec.write(writer, value)
        writer.close()

        reader: ByteIo = self.reader()
        self.assertEqual(codec.read(reader), value)
        reader.close()


if __name__ == '__main__':
    unittest.main()
