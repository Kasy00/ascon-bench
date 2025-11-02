from ascon.core import ascon_permutation, rol
from typing import Iterable
# ASCON-Hash
def ascon_hash(data: bytes) -> bytes:
    # Simple sponge-like hashing using the state permutation.
    # Not optimized; for correctness/benchmarking.
    rate = 8
    state = [0]*5
    # absorb
    padded = data + b'\x80'
    while len(padded) % rate != 0:
        padded += b'\x00'
    import struct
    for i in range(0, len(padded), rate):
        block = padded[i:i+rate]
        w = int.from_bytes(block.ljust(8,b'\x00'), 'big')
        state[0] ^= w
        ascon_permutation(state, rounds=12)
    # squeeze 32 bytes (256-bit hash)
    out = b''
    while len(out) < 32:
        out += state[0].to_bytes(8,'big')
        ascon_permutation(state, rounds=12)
    return out[:32]
