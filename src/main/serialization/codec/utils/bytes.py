def to_byte(value: int) -> bytes:
    """Byte operation, int to 1 byte"""
    return (value - 128).to_bytes(1, byteorder="big", signed=True)


def from_byte(value: bytes) -> int:
    """Byte operation, 1 byte to int"""
    return int.from_bytes(value, byteorder="big", signed=True) + 128
