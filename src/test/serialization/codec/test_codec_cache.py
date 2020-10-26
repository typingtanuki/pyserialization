import unittest

from src.main.serialization.codec.array.booleanArrayCodec import BooleanArrayCodec
from src.main.serialization.codec.array.byteArrayCodec import ByteArrayCodec
from src.main.serialization.codec.codecCache import CodecCache
from src.main.serialization.codec.object.noneCodec import NoneCodec
from src.main.serialization.codec.object.stringCodec import StringCodec
from src.main.serialization.codec.primitive.booleanCodec import BooleanCodec
from src.main.serialization.codec.primitive.bytesCodec import BytesCodec
from src.main.serialization.codec.primitive.charCodec import CharCodec
from src.main.serialization.codec.primitive.doubleCodec import DoubleCodec
from src.main.serialization.codec.primitive.floatCodec import FloatCodec
from src.main.serialization.codec.primitive.intCodec import IntCodec
from src.main.serialization.codec.primitive.longCodec import LongCodec
from src.main.serialization.codec.primitive.shortCodec import ShortCodec
from src.main.serialization.codec.utils.bytes import to_byte
from src.test.serialization.codec.test_codec import TestCodec


class TestCodecCache(TestCodec):
    def test_find_ser(self) -> None:
        cache: CodecCache = CodecCache()

        cache.register(BooleanCodec(cache.next_free_marker()))
        cache.register(BytesCodec(cache.next_free_marker()))
        cache.register(CharCodec(cache.next_free_marker()))
        cache.register(StringCodec(cache.next_free_marker(), 0))
        cache.register(DoubleCodec(cache.next_free_marker()))
        cache.register(FloatCodec(cache.next_free_marker()))
        cache.register(IntCodec(cache.next_free_marker()))
        cache.register(LongCodec(cache.next_free_marker()))
        cache.register(ShortCodec(cache.next_free_marker()))
        cache.register(BooleanArrayCodec(cache.next_free_marker()))
        cache.register(ByteArrayCodec(cache.next_free_marker()))

        self.assertIsInstance(cache.codec_for(True), BooleanCodec)
        self.assertIsInstance(cache.codec_for(to_byte(12)), ByteArrayCodec)
        self.assertIsInstance(cache.codec_for(None), NoneCodec)
        self.assertIsInstance(cache.codec_for("a"), StringCodec)
        self.assertIsInstance(cache.codec_for(12), LongCodec)
        self.assertIsInstance(cache.codec_for(1.2), DoubleCodec)


if __name__ == '__main__':
    unittest.main()
