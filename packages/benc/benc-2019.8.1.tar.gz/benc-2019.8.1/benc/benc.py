"""
    benc.py: pure-python bencode (de|en)coder compatible with Python >=3.6
    Copyright: Peter Tripp (@notpeter) <notpeter@notpeter.net>
    License: MIT
"""

import io
import itertools
import struct
from typing import BinaryIO, ByteString, Dict, Iterable, Iterator, List, Union

Bencodable = Union[int, str, List['Bencodable'], Dict[str, 'Bencodable']]


def _decode(gen: Iterable[bytes], initial: bytes = None) -> Bencodable:
    def capture_until(gen: Iterable[bytes], until: bytes, initial: bytes = b'') -> bytes:
        """Captures until a stop character (e.g. b'e'[0] or b':'[0]) is reached."""
        chunk = bytearray(initial)
        while True:
            char = next(gen)
            if char == until:
                return bytes(chunk)  # NOTE: the chunk does not include the until character
            chunk.extend(char)

    def capture_bytes(gen: Iterable[bytes], length: int, initial=b'') -> bytes:
        """Captures a length of bytes from a byte iterable."""
        chunk = bytearray(initial)
        while len(chunk) < length:
            chunk.extend(next(gen))
        return bytes(chunk)  # convert from bytearray to bytes

    char = next(gen) if initial is None else initial

    if char == b'i':  # integers (i01234567899999e)
        return int(capture_until(gen, b'e'))

    elif char in b'0123456789':  # strings (7:abcdefg)
        length = int(capture_until(gen, b':', initial=char))
        return capture_bytes(gen, length)

    elif char == b'l':  # list (le)
        wip = []
        while True:
            char = next(gen)
            if char == b'e':  # 'e' (end) of the list
                return wip
            wip.append(_decode(gen, initial=char))

    elif char == b'd':  # dictionary (de)
        wip = {}
        while True:
            char = next(gen)
            if char == b'e':  # 'e' (end) of the dict
                return wip
            key = _decode(gen, initial=char)
            value = _decode(gen)
            wip[key] = value
    raise ValueError(f"Unexpected character: {char!r}.")


def encode(obj: Bencodable, coerce=False) -> bytes:
    """Encodes the passed data with bencode."""
    if isinstance(obj, int):
        return b'i%de' % obj
    elif isinstance(obj, bytes):
        return b'%d:%b' % (len(obj), obj)
    elif isinstance(obj, list):
        return b'l%be' % b"".join(map(encode, obj))
    elif isinstance(obj, dict) and all(isinstance(key, bytes) for key in obj.keys()):
        return b"d%be" % b"".join(map(encode, itertools.chain(*sorted(obj.items()))))
    raise NotImplementedError(f"Unsupported type: '{type(obj).__name__}' for value: '{obj}'")


def decode(obj: Union[BinaryIO, ByteString]):
    def bytes_from_bytes(obj: bytes) -> Iterator[bytes]:
        """Yields bytes when iterating over bytes instead of ints"""
        for integer in obj:
            yield struct.pack("B", integer)

    def bytes_from_file(f) -> Iterator[bytes]:
        """Yields one byte at a time from a file_object"""
        chunk = f.read(1)
        while chunk != b'':
            yield chunk
            chunk = f.read(1)

    if isinstance(obj, io.IOBase):
        gen = bytes_from_file(obj)
    elif isinstance(obj, ByteString):
        gen = bytes_from_bytes(obj)
    else:
        raise ValueError(f"Unable to decode. Unkonwn how to handle type {type(obj)!r} .")

    value = _decode(gen)
    try:
        next(gen)  # This generator should be empty
    except StopIteration:
        return value
    raise ValueError("Finished bdecoding before reaching end of buffer.")
