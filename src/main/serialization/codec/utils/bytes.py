def to_byte(value: int) -> bytes:
    """Byte operation, int to 1 byte"""
    return int_to_byte(value - 128)


def from_byte(value: bytes) -> int:
    """Byte operation, 1 byte to int"""
    return int_from_byte(value) + 128


def int_to_byte(value: int) -> bytes:
    """Byte operation, int to 1 byte"""
    return value.to_bytes(1, byteorder="big", signed=True)


def int_from_byte(value: bytes) -> int:
    """Byte operation, 1 byte to int"""
    return int.from_bytes(value, byteorder="big", signed=True)


def join_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(list(a) + list(b))


def byte_length(a: bytes, length: int) -> bytes:
    if len(a) == length:
        return a

    out: bytearray = bytearray(length)
    shift: int = length - len(a)
    for i in range(0, len(a)):
        out[shift + i] = a[i]
    return bytes(out)
