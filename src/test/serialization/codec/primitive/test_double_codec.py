import sys
import unittest

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.primitive.doubleCodec import DoubleCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.main.serialization.codec.utils.bytes import to_byte
from src.test.serialization.codec.test_codec import TestCodec


class TestDoubleCodec(TestCodec):
    def test_wide_range(self):
        self.double_seria(None)
        self.double_seria(float('inf'))
        self.double_seria(float('-inf'))
        self.double_seria(1.7415152243978685e+308)
        self.double_seria(sys.float_info.min)
        self.double_seria(-1.7415152243978685e+308)
        self.double_seria(0.5)
        self.double_seria(1.5)
        self.double_seria(-0.5)
        self.double_seria(-1.5)

    def double_seria(self, value: None or float):
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
