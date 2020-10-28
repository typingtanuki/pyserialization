import unittest
from typing import List, Set

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.codecCache import CodecCache
from src.main.serialization.codec.object.setCodec import SetCodec
from src.main.serialization.codec.object.stringCodec import StringCodec
from src.main.serialization.codec.primitive.intCodec import IntCodec
from src.main.serialization.codec.primitive.longCodec import LongCodec
from src.main.serialization.codec.utils.byteIo import ByteIo
from src.test.serialization.codec.test_codec import TestCodec


class TestSetCodec(TestCodec):
    def test_read_write(self):
        q: Set[any] = set()
        for i in range(0, 500):
            q.add(i)
            self.list_seria(q)

    def test_read_write_mixed(self):
        q: Set[any] = set()
        for i in range(0, 500):
            q.add(i)
            if i % 3 == 0:
                q.add(f"test_{i}")
            self.list_seria(q)

    def list_seria(self, value: None or List[any]):
        codec_cache: CodecCache = CodecCache()
        codec_cache.register(IntCodec(codec_cache.next_free_marker()))
        codec_cache.register(LongCodec(codec_cache.next_free_marker()))
        codec_cache.register(StringCodec(codec_cache.next_free_marker(), 0))
        codec: Codec[List[any]] = SetCodec(codec_cache.next_free_marker(), codec_cache)
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
