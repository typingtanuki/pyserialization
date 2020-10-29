import collections
import unittest
from typing import BinaryIO, Deque, List

from src.main.serialization.codec.array.booleanArrayCodec import BooleanArrayCodec
from src.main.serialization.codec.array.byteArrayCodec import ByteArrayCodec
from src.main.serialization.codec.array.charArrayCodec import CharArrayCodec
from src.main.serialization.codec.array.doubleArrayCodec import DoubleArrayCodec
from src.main.serialization.codec.array.floatArrayCodec import FloatArrayCodec
from src.main.serialization.codec.array.intArrayCodec import IntArrayCodec
from src.main.serialization.codec.array.longArrayCodec import LongArrayCodec
from src.main.serialization.codec.array.shortArrayCodec import ShortArrayCodec
from src.main.serialization.codec.codecCache import CodecCache
from src.main.serialization.codec.object.collectionCodec import CollectionCodec
from src.main.serialization.codec.object.listCodec import ListCodec
from src.main.serialization.codec.object.mapCodec import MapCodec
from src.main.serialization.codec.object.queueCodec import QueueCodec
from src.main.serialization.codec.object.setCodec import SetCodec
from src.main.serialization.codec.object.stringCodec import StringCodec
from src.main.serialization.codec.primitive.booleanCodec import BooleanCodec
from src.main.serialization.codec.primitive.bytesCodec import BytesCodec
from src.main.serialization.codec.primitive.charCodec import CharCodec
from src.main.serialization.codec.primitive.doubleCodec import DoubleCodec
from src.main.serialization.codec.primitive.floatCodec import FloatCodec
from src.main.serialization.codec.primitive.intCodec import IntCodec
from src.main.serialization.codec.primitive.longCodec import LongCodec
from src.main.serialization.codec.primitive.shortCodec import ShortCodec
from src.main.serialization.codec.utils.bytes import int_to_byte
from src.main.serialization.deserializer.Deserializer import Deserializer
from src.main.serialization.deserializer.DeserializerFactory import DeserializerFactory


def make_codec() -> CodecCache:
    cache: CodecCache = CodecCache()

    cache.register(BooleanCodec(cache.next_free_marker()))
    cache.register(BytesCodec(cache.next_free_marker()))
    cache.register(CharCodec(cache.next_free_marker()))
    cache.register(DoubleCodec(cache.next_free_marker()))
    cache.register(FloatCodec(cache.next_free_marker()))
    cache.register(IntCodec(cache.next_free_marker()))
    cache.register(LongCodec(cache.next_free_marker()))
    cache.register(ShortCodec(cache.next_free_marker()))

    cache.register(StringCodec(cache.next_free_marker(), 0))

    cache.register(BooleanArrayCodec(cache.next_free_marker()))
    cache.register(ByteArrayCodec(cache.next_free_marker()))
    cache.register(CharArrayCodec(cache.next_free_marker()))
    cache.register(DoubleArrayCodec(cache.next_free_marker()))
    cache.register(FloatArrayCodec(cache.next_free_marker()))
    cache.register(IntArrayCodec(cache.next_free_marker()))
    cache.register(LongArrayCodec(cache.next_free_marker()))
    cache.register(ShortArrayCodec(cache.next_free_marker()))

    cache.register(MapCodec(cache.next_free_marker(), cache))
    cache.register(QueueCodec(cache.next_free_marker(), cache))
    cache.register(SetCodec(cache.next_free_marker(), cache))
    cache.register(ListCodec(cache.next_free_marker(), cache))
    cache.register(CollectionCodec(cache.next_free_marker(), cache))
    return cache


class TestInterop(unittest.TestCase):
    def test_interop(self) -> None:
        cache: CodecCache = make_codec()

        file: str = "./interop.test"
        # self.read_file(file)
        reader: BinaryIO = open(file, "rb")

        deserializer: Deserializer = DeserializerFactory(cache).new_deserializer(reader)
        deserialized: any = deserializer.read()
        reader.close()

        self.assertIsInstance(deserialized, collections.deque)

        queue: Deque[any] = deserialized
        self.assertEqual(20, len(queue))

        types: List[type] = [int, int, int, int, int, float, float, float, float, bool, bool, type(None),
                             collections.deque, dict, collections.deque, dict, str, str, str, str]

        values: List[any] = [1, 2147483647, -2147483648, 9223372036854775807, -9223372036854775808,
                             1.7976931348623157e+308, 5e-324, -5e-324, 3.6455610097781983e-304, False, True, None,
                             collections.deque([]), {}, collections.deque([False, True, None]),
                             {'abc': None, 'def': 'd', 'g': 'ef', 12: False, True: True}, "test", "c", "漢字漢字", "漢"]

        for i in range(0, 20):
            entry: any = queue[i]
            print(f"{i} - {entry} - {type(entry)} (value)")
            print(f"{i} - {values[i]} - {types[i]} (expected)")
            self.assertIsInstance(entry, types[i])
            self.assertEqual(entry, values[i])

    def test_primitive_interop(self) -> None:
        cache: CodecCache = make_codec()

        file: str = "./primitives.test"
        # self.read_file(file)
        reader: BinaryIO = open(file, "rb")

        deserializer: Deserializer = DeserializerFactory(cache).new_deserializer(reader)

        self.check_primitive(deserializer)
        reader.close()

    def test_arrays_interop(self) -> None:
        cache: CodecCache = make_codec()

        file: str = "./arrays.test"
        # self.read_file(file)
        reader: BinaryIO = open(file, "rb")

        deserializer: Deserializer = DeserializerFactory(cache).new_deserializer(reader)

        # None
        self.assertEqual(deserializer.read(), None)
        self.check_arrays(deserializer)
        reader.close()

    def test_simple_interop(self) -> None:
        cache: CodecCache = make_codec()

        file: str = "./simple.test"
        # self.read_file(file)
        reader: BinaryIO = open(file, "rb")

        deserializer: Deserializer = DeserializerFactory(cache).new_deserializer(reader)

        self.check_primitive(deserializer)
        self.assertEqual(deserializer.read(), "abc漢字def")
        self.check_arrays(deserializer)
        reader.close()

    def check_primitive(self, deserializer):
        # None
        self.assertEqual(deserializer.read(), None)

        # Booleans
        self.assertEqual(deserializer.read(), True)
        self.assertEqual(deserializer.read(), False)
        self.assertEqual(deserializer.read(), None)

        # Bytes
        self.assertEqual(deserializer.read(), int_to_byte(123))

        # Chars
        self.assertEqual(deserializer.read(), "a")
        self.assertEqual(deserializer.read(), "漢")

        # Double
        self.assertEqual(deserializer.read(), 123.123)

        # Float
        value: float = deserializer.read()
        self.assertGreaterEqual(value, -123.124)
        self.assertLessEqual(value, -123.122)

        # Int
        self.assertEqual(deserializer.read(), 123)

        # Long
        self.assertEqual(deserializer.read(), 133)

        # Short
        self.assertEqual(deserializer.read(), 456)

    def check_arrays(self, deserializer):
        # Booleans
        self.assertEqual(deserializer.read(), [True, False, True])

        # Bytes
        self.assertEqual(deserializer.read(), [int_to_byte(12),
                                               int_to_byte(0),
                                               (255).to_bytes(1, byteorder="big", signed=False)])

        # Chars
        self.assertEqual(deserializer.read(), ["a", "b", "漢", "字"])

        # Double
        self.assertEqual(deserializer.read(), [1.2, -23.45])

        # Float
        value: [float] = deserializer.read()
        self.assertGreaterEqual(value[0], 1.1)
        self.assertLessEqual(value[0], 1.3)
        self.assertGreaterEqual(value[1], -23.46)
        self.assertLessEqual(value[1], -23.44)

        # Int
        self.assertEqual(deserializer.read(), [1, 254])

        # Long
        self.assertEqual(deserializer.read(), [1, 254])

        # Short
        self.assertEqual(deserializer.read(), [1, -2])

    def read_file(self, file: str) -> None:
        reader: BinaryIO = open(file, "rb")
        read: bytes or None = reader.read(1)
        print(file)
        while len(read) > 0:
            print(f"{read} / {read[0]} / {read[0] - 128}")
            read = reader.read(1)
        reader.close()


if __name__ == '__main__':
    unittest.main()
