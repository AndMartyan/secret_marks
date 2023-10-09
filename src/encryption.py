import hashlib


def hash_text(text: str, salt: str) -> str:
    return hashlib.sha256(salt.encode() + text.encode()).hexdigest()


def match_hashed_text(hashed_text: str, secret: str, user_salt: str) -> bool:
    return hashed_text == hashlib.sha256(user_salt.encode() + secret.encode()).hexdigest()


def secret_encode(secret: str, key: str):
    encoded = bytearray(len(secret))
    for i in range(len(secret)):
        encoded[i] = ord(secret[i]) ^ ord(key[i % len(key)])
    return bytes(encoded)


def secret_decode(encoded, key: str) -> str:
    decoded = bytearray(len(encoded))
    for i in range(len(encoded)):
        decoded[i] = encoded[i] ^ ord(key[i % len(key)])
    return decoded.decode()
