import unittest
from typing import List

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.codecCache import CodecCache
from src.main.serialization.codec.object.collectionCodec import CollectionCodec
from src.main.serialization.codec.object.stringCodec import StringCodec
from src.main.serialization.codec.primitive.intCodec import IntCodec
from src.main.serialization.codec.primitive.longCodec import LongCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.test.serialization.codec.test_codec import TestCodec


class TestCollectionCodec(TestCodec):
    def test_read_write(self):
        list: List[any] = []
        for i in range(0, 500):
            list.append(i)
            self.list_seria(list)

    def test_read_write_mixed(self):
        list: List[any] = []
        for i in range(0, 500):
            list.append(i)
            if i % 3 == 0:
                list.append(f"test_{i}")
            self.list_seria(list)

    def list_seria(self, value: None or List[any]):
        codec_cache: CodecCache = CodecCache()
        codec_cache.register(IntCodec(codec_cache.next_free_marker()))
        codec_cache.register(LongCodec(codec_cache.next_free_marker()))
        codec_cache.register(StringCodec(codec_cache.next_free_marker(), 0))
        codec: Codec[List[any]] = CollectionCodec(codec_cache.next_free_marker(), codec_cache)
        codec_cache.register(codec)

        writer: ByteIo = self.writer()
        codec.write(writer, value)
        writer.close()

        reader: ByteIo = self.reader()
        pim: int = codec.read(reader)
        self.assertEqual(value, pim)
        reader.close()


if __name__ == '__main__':
    unittest.main()
