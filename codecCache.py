from typing import Type

from codec import Codec
from noneCodec import NoneCodec


class CodecCache:
    NULL_CODEC: Codec[None] = NoneCodec()

    codecArray: [Codec] = []
    codecList: [Codec] = []
    codecMapping: {Type: Codec} = {}

    def __init__(self):
        super.__init__()
        for i in range(0, 256):
            self.codecArray[i] = None

    def nextFreeMarker(self) -> bytes:
        for i in range(0, 256):
            codec: Codec = self.codecArray[i]
            if codec is None:
                return bytes(i - 128)

        raise ValueError("The codec cache is full.")

    def register(self, codec: Codec) -> None:
        for val in codec.reservedBytes():
            if self.codecArray[val + 128] is not None:
                raise ValueError("Byte " + val + " already registered.")

        self.codecList.append(codec)
        for val in codec.reservedBytes():
            self.codecArray[int(val + 128)] = codec

    def get(self, key: bytes) -> Codec:
        return self.codecArray[int(key + 128)]

    def codecFor(self, value: any) -> Codec:
        if object is None:
            return self.NULL_CODEC
        return self.codecForType(type(value))

    def codecForType(self, typez: type) -> Codec:
        codec: Codec = self.codecMapping.get(typez)
        if codec is not None:
            return codec

        return self.searchCodecForClass(typez)

    def searchCodecForClass(self, typez: type) -> Codec:
        for registered in self.codecList:
            if registered.writes(typez):
                self.codecMapping[typez] = registered
                return registered

        raise Exception("Missing type " + type)
