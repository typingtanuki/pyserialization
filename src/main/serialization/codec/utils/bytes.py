def to_byte(value: int) -> bytes:
    """Byte operation, int to 1 byte"""
    return value.to_bytes(1, byteorder="big")


def from_byte(value: bytes) -> int:
    """Byte operation, 1 byte to int"""
    return int.from_bytes(value, byteorder="big")
