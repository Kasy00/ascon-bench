try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives import hashes, hmac
    HAS_CRYPTO = True
except Exception:
    HAS_CRYPTO = False

class AESGCMAdapter:
    def __init__(self, key: bytes):
        assert len(key) in (16, 24, 32)
        if not HAS_CRYPTO:
            raise RuntimeError('cryptography not installed')
        self._a = AESGCM(key)

    def encrypt(self, nonce: bytes, plaintext: bytes, ad: bytes = b'') -> tuple[bytes, bytes]:
        data = self._a.encrypt(nonce, plaintext, ad)
        ct, tag = data[:-16], data[-16:]
        return ct, tag

    def decrypt(self, nonce: bytes, ciphertext: bytes, tag: bytes, ad: bytes = b'') -> tuple[bytes, bool]:
        data = ciphertext + tag
        pt = self._a.decrypt(nonce, data, ad)
        return pt, True

class SHA256Adapter:
    def hash(self, data: bytes) -> bytes:
        if not HAS_CRYPTO:
            raise RuntimeError('cryptography not installed')
        digest = hashes.Hash(hashes.SHA256())
        digest.update(data)
        return digest.finalize()

class HMACSHA256Adapter:
    def __init__(self, key: bytes):
        if not HAS_CRYPTO:
            raise RuntimeError('cryptography not installed')
        self._k = key
    def mac(self, message: bytes) -> bytes:
        h = hmac.HMAC(self._k, hashes.SHA256())
        h.update(message)
        return h.finalize()

def aes_gcm_encrypt(key: bytes, nonce: bytes, plaintext: bytes, ad: bytes = b'') -> bytes:
    a = AESGCMAdapter(key)
    ct, tag = a.encrypt(nonce, plaintext, ad)
    return ct + tag

def aes_gcm_decrypt(key: bytes, nonce: bytes, ciphertext_and_tag: bytes, ad: bytes = b'') -> bytes:
    a = AESGCMAdapter(key)
    ct, tag = ciphertext_and_tag[:-16], ciphertext_and_tag[-16:]
    pt, ok = a.decrypt(nonce, ct, tag, ad)
    return pt

def sha256_hash(data: bytes) -> bytes:
    return SHA256Adapter().hash(data)

def hmac_sha256_mac(key: bytes, data: bytes) -> bytes:
    return HMACSHA256Adapter(key).mac(data)

__all__ = [
    "AESGCMAdapter",
    "SHA256Adapter",
    "HMACSHA256Adapter",
    "aes_gcm_encrypt",
    "aes_gcm_decrypt",
    "sha256_hash",
    "hmac_sha256_mac",
]