import sys
import unittest

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.primitive.doubleCodec import DoubleCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import to_byte
from src.test.serialization.codec.test_codec import TestCodec


class TestFloatCodec(TestCodec):
    def test_wide_range(self):
        self.float_seria(None)
        self.float_seria(float('inf'))
        self.float_seria(float('-inf'))
        self.float_seria(1.7415152243978685e+308)
        self.float_seria(sys.float_info.min)
        self.float_seria(-1.7415152243978685e+308)
        self.float_seria(0.5)
        self.float_seria(1.5)
        self.float_seria(-0.5)
        self.float_seria(-1.5)

    def float_seria(self, value: None or float):
        codec: Codec[float] = DoubleCodec(to_byte(12))
        writer: ByteIo = self.writer()
        codec.write(writer, value)
        writer.close()

        reader: ByteIo = self.reader()
        pim: float = codec.read(reader)
        self.assertEqual(pim, value)
        reader.close()


if __name__ == '__main__':
    unittest.main()
