import unittest
from typing import BinaryIO

from src.main.serialization.codec.codecCache import CodecCache
from src.main.serialization.codec.primitive.booleanCodec import BooleanCodec
from src.main.serialization.codec.primitive.bytesCodec import BytesCodec
from src.main.serialization.codec.primitive.charCodec import CharCodec
from src.main.serialization.deserializer.Deserializer import Deserializer
from src.main.serialization.deserializer.DeserializerFactory import DeserializerFactory


class TestInterop(unittest.TestCase):
    def test_interop(self) -> None:
        cache: CodecCache = CodecCache()

        cache.register(BooleanCodec(cache.next_free_marker()))
        cache.register(BytesCodec(cache.next_free_marker()))
        cache.register(CharCodec(cache.next_free_marker()))
        # cache.register(DoubleCodec(cache.next_free_marker()))
        # cache.register(FloatCodec(cache.next_free_marker()))
        # cache.register(IntCodec(cache.next_free_marker()))
        # cache.register(LongCodec(cache.next_free_marker()))
        # cache.register(ShortCodec(cache.next_free_marker()))

        # cache.register(StringCodec(cache.next_free_marker(), 0))

        # cache.register(BooleanArrayCodec(cache.next_free_marker()))
        # cache.register(ByteArrayCodec(cache.next_free_marker()))
        # cache.register(CharArrayCodec(cache.next_free_marker()))
        # cache.register(DoubleArrayCodec(cache.next_free_marker()))
        # cache.register(FloatArrayCodec(cache.next_free_marker()))
        # cache.register(IntArrayCodec(cache.next_free_marker()))
        # cache.register(LongArrayCodec(cache.next_free_marker()))
        # cache.register(ShortArrayCodec(cache.next_free_marker()))

        # cache.register(MapCodec(cache.next_free_marker(), cache))
        # cache.register(QueueCodec(cache.next_free_marker(), cache))
        # cache.register(SetCodec(cache.next_free_marker(), cache))
        # cache.register(ListCodec(cache.next_free_marker(), cache))
        # cache.register(CollectionCodec(cache.next_free_marker(), cache))

        file: str = "./interop.test"
        reader: BinaryIO = open(file, "rb")

        deserializer: Deserializer = DeserializerFactory(cache).new_deserializer(reader)
        deserialized: any = deserializer.read()

        self.assertIsInstance(deserialized, list)


if __name__ == '__main__':
    unittest.main()
