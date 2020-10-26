import unittest
from typing import List

from src.main.serialization.codec.array.floatArrayCodec import FloatArrayCodec
from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import to_byte
from src.test.serialization.codec.test_codec import TestCodec


class TestFloatArrayCodec(TestCodec):
    def test_wide_range(self):
        self.float_seria(None)
        self.float_seria([])
        self.float_seria([1.2, -1.3, 10.0, -100.2])

    def float_seria(self, value: None or List[float]):
        codec: Codec[float] = FloatArrayCodec(to_byte(12))
        writer: ByteIo = self.writer()
        codec.write(writer, value)
        writer.close()

        reader: ByteIo = self.reader()
        read: None or List[float] = codec.read(reader)

        if value is None:
            self.assertIsNone(read)
        else:
            self.assertEqual(len(value), len(read))
            for i in range(0, len(value)):
                self.assertGreaterEqual(value[i], read[i] - 0.1)
                self.assertLessEqual(value[i], read[i] + 0.1)
        reader.close()


if __name__ == '__main__':
    unittest.main()
