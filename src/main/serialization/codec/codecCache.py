from typing import Type

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.object.noneCodec import NoneCodec


class CodecCache:
    NULL_CODEC: Codec[None] = NoneCodec()

    codecArray: [Codec] = []
    codecList: [Codec] = []
    codecMapping: {Type: Codec} = {}

    def __init__(self):
        super().__init__()

        for i in range(0, 256):
            self.codecArray.append(None)

        self.register(self.NULL_CODEC)

    def next_free_marker(self) -> bytes:
        for i in range(0, 256):
            codec: Codec = self.codecArray[i]
            if codec is None:
                return Codec.to_byte(i)

        raise ValueError("The codec cache is full.")

    def register(self, codec: Codec) -> None:
        for val in codec.reserved_bytes():
            if self.codecArray[Codec.from_byte(val)] is not None:
                raise ValueError("Byte " + val + " already registered.")

        self.codecList.append(codec)
        for val in codec.reserved_bytes():
            self.codecArray[Codec.from_byte(val)] = codec

    def get(self, key: bytes) -> Codec:
        return self.codecArray[Codec.from_byte(key)]

    def codec_for(self, value: any) -> Codec:
        if object is None:
            return self.NULL_CODEC
        return self.codec_for_type(type(value))

    def codec_for_type(self, typez: type) -> Codec:
        codec: Codec = self.codecMapping.get(typez)
        if codec is not None:
            return codec

        return self.search_codec_for_class(typez)

    def search_codec_for_class(self, typez: type) -> Codec:
        for registered in self.codecList:
            if registered.writes(typez):
                self.codecMapping[typez] = registered
                return registered

        raise Exception("Missing type " + str(typez))
