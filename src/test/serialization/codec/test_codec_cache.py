import unittest
from io import BufferedWriter, BufferedReader

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.codecCache import CodecCache
from src.main.serialization.codec.object.noneCodec import NoneCodec
from src.main.serialization.codec.primitive.booleanCodec import BooleanCodec
from src.main.serialization.codec.primitive.bytesCodec import BytesCodec
from src.main.serialization.codec.primitive.charCodec import CharCodec
from src.test.serialization.codec.test_codec import TestCodec


class TestCodecCache(TestCodec):
    def test_find_ser(self) -> None:
        cache: CodecCache = CodecCache()
        boolean_codec: BooleanCodec = BooleanCodec(cache.next_free_marker())
        cache.register(boolean_codec)
        bytes_codec: BytesCodec = BytesCodec(cache.next_free_marker())
        cache.register(bytes_codec)
        char_codec: CharCodec = CharCodec(cache.next_free_marker())
        cache.register(char_codec)

        self.assertIsInstance(cache.codec_for(True), BooleanCodec)
        self.assertIsInstance(cache.codec_for(Codec.to_byte(12)), BytesCodec)
        self.assertIsInstance(cache.codec_for(None), NoneCodec)
        self.assertIsInstance(cache.codec_for("a"), CharCodec)
