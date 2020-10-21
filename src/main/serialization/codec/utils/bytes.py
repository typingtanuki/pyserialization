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
