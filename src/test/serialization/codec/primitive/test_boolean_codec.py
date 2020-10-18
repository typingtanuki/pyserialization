import unittest
from io import BufferedWriter, BufferedReader

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.primitive.booleanCodec import BooleanCodec
from src.test.serialization.codec.test_codec import TestCodec


class TestBooleanCodec(TestCodec):
    def test_type_check(self):
        codec: Codec[bool] = BooleanCodec(Codec.to_byte(12))
        self.assertTrue(codec.writes(bool))
        self.assertFalse(codec.writes(str))

    def test_true(self):
        codec: Codec[bool] = BooleanCodec(Codec.to_byte(12))

        writer: BufferedWriter = self.writer()
        codec.write(writer, True)
        writer.close()

        reader: BufferedReader = self.reader()
        self.assertTrue(codec.read(reader))
        reader.close()

    def test_false(self):
        codec: Codec[bool] = BooleanCodec(Codec.to_byte(12))

        writer: BufferedWriter = self.writer()
        codec.write(writer, False)
        writer.close()

        reader: BufferedReader = self.reader()
        self.assertFalse(codec.read(reader))
        reader.close()

    def test_mix(self):
        codec: Codec[bool] = BooleanCodec(Codec.to_byte(12))

        writer: BufferedWriter = self.writer()
        codec.write(writer, False)
        codec.write(writer, True)
        codec.write(writer, True)
        codec.write(writer, None)
        codec.write(writer, False)
        codec.write(writer, True)
        writer.close()

        reader: BufferedReader = self.reader()
        self.assertFalse(codec.read(reader))
        self.assertTrue(codec.read(reader))
        self.assertTrue(codec.read(reader))
        self.assertEqual(codec.read(reader), None)
        self.assertFalse(codec.read(reader))
        self.assertTrue(codec.read(reader))
        reader.close()


if __name__ == '__main__':
    unittest.main()
