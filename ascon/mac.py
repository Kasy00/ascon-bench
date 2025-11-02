# ascon/mac.py
from ascon.aead import Ascon128

class AsconMAC:
    def __init__(self, key: bytes):
        self._ae = Ascon128(key)

    def mac(self, message: bytes) -> bytes:
        nonce = b'\x00'*16
        _, tag = self._ae.encrypt(nonce, b'', message)
        return tag

    def verify(self, message: bytes, tag: bytes) -> bool:
        nonce = b'\x00'*16
        _, ctag = self._ae.encrypt(nonce, b'', message)
        return ctag == tag
