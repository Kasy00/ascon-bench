from typing import List
# permutacja i niskopoziomowe funkcje
# Minimalna, czytelna implementacja permutacji ASCON (320-bit state)
# Implementacja oparta na specyfikacji ASCON (permutation p_12 / p_6 parametry).
# Referencja: Ascon spec. See: ascon-spec-round2.pdf

# constants
ROUND_CONSTANTS = [
    0x000000000000000f,0x000000000000000e,0x000000000000000d,0x000000000000000c,
    0x000000000000000b,0x000000000000000a,0x0000000000000009,0x0000000000000008,
    0x0000000000000007,0x0000000000000006,0x0000000000000005,0x0000000000000004
]

def rol(x: int, r: int, w: int=64) -> int:
    r %= w
    return ((x << r) & ((1<<w)-1)) | (x >> (w-r))

def ascon_permutation(state: List[int], rounds: int = 12) -> None:
    """
    In-place permutation on 5 64-bit words (state length 5).
    state: list of 5 ints (64-bit)
    rounds: number of rounds (e.g., 12 for initialization/finalization)
    """
    assert len(state) == 5
    for r in range(12-rounds, 12):
        # add round constant
        rc = ROUND_CONSTANTS[r]
        state[2] ^= rc

        # substitution layer (S-box) - 5-word S-box (from spec)
        x0,x1,x2,x3,x4 = state
        x0 ^= x4; x4 ^= x3; x2 ^= x1
        t0 = (~x0) & x1
        t1 = (~x1) & x2
        t2 = (~x2) & x3
        t3 = (~x3) & x4
        t4 = (~x4) & x0
        x0 ^= t1; x1 ^= t2; x2 ^= t3; x3 ^= t4; x4 ^= t0
        x1 ^= x0; x0 ^= x4; x3 ^= x2; x2 = ~x2 & ((1<<64)-1)

        # linear diffusion layer (rotations)
        state[0] = x0 ^ rol(x0, 19) ^ rol(x0, 28)
        state[1] = x1 ^ rol(x1, 61) ^ rol(x1, 39)
        state[2] = x2 ^ rol(x2, 1)  ^ rol(x2, 6)
        state[3] = x3 ^ rol(x3, 10) ^ rol(x3, 17)
        state[4] = x4 ^ rol(x4, 7)  ^ rol(x4, 41)
