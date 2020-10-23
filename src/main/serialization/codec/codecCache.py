from typing import Type

from src.main.serialization.codec.codec import Codec
from src.main.serialization.codec.object.noneCodec import NoneCodec
from src.main.serialization.codec.utils.bytes import *


class CodecCache:
    """Codec cache, in charge of registering and managing codecs"""

    __NONE_CODEC: Codec[None] = NoneCodec()
    """Special codec for the 'None' type"""

    codecList: [Codec] = []
    """List of all registered codecs"""
    codecArray: [Codec] = []
    """
    Array of codecs, indexed by reserved bytes. 
    Used for de-serialization lookup
    """
    codecMapping: {Type: Codec} = {}
    """
    Mapping of type → Codec.
    Populated as types are being serialized.
    Used for serialization lookup"""

    def __init__(self):
        super().__init__()

        self.codecArray.clear()

        # Initialize blank codec array
        for i in range(0, 256):
            self.codecArray.append(None)

        # Register the "None" codec
        self.register(self.__NONE_CODEC)

    def next_free_marker(self) -> bytes:
        """
        Detect next available byte marker
        :return: The first free byte marker
        """
        for i in range(0, 256):
            codec: Codec = self.codecArray[i]
            if codec is None:
                return to_byte(i)

        raise ValueError("The codec cache is full.")

    def register(self, codec: Codec) -> None:
        """
        Register a new codec in cache
        :param codec: The codec to register
        """
        for val in codec.reserved_bytes():
            if self.codecArray[from_byte(val)] is not None:
                raise ValueError(f"Byte {from_byte(val)} already registered.")

        self.codecList.append(codec)
        for val in codec.reserved_bytes():
            self.codecArray[from_byte(val)] = codec

    def get(self, key: bytes) -> Codec:
        """
        Retrieve a codec by key
        :param key: The byte marker corresponding to the codec
        :return: The corresponding codec
        """
        int_key: int = from_byte(key)
        codec: Codec or None = self.codecArray[int_key]
        if codec is None:
            raise ValueError(f"Byte {int_key} is not registered.")
        return codec

    def codec_for(self, value: any) -> Codec:
        """
        Retrieve a codec by value type

        :param value: The value we want to serialize
        :return: The codec corresponding to this type
        """
        if object is None:
            return self.__NONE_CODEC
        return self.codec_for_type(type(value))

    def codec_for_type(self, typez: type) -> Codec:
        """
        Retrieve a codec by type

        :param typez: The type we want to serialize
        :return: The codec corresponding to this type
        """
        codec: Codec = self.codecMapping.get(typez)
        if codec is not None:
            return codec

        return self.__search_codec_for_class(typez)

    def __search_codec_for_class(self, typez: type) -> Codec:
        """
        Scan available codecs to find matching type.

        Caches the mapping for future efficient use.

        :param typez: The type we are looking for
        :return: The codec corresponding to this type
        """
        for registered in self.codecList:
            if registered.writes(typez):
                self.codecMapping[typez] = registered
                return registered

        raise Exception(f"Missing codec for type {typez}")
