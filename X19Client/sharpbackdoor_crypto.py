from __future__ import annotations

import base64
import os
import random
import string
from typing import List

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


KEYS_HEX: List[str] = [
    "60F1E0D1FD635362430747215CF1C2FF",
    "EA5B62D27D0338374852C4B9469D7AC6",
    "17238D55501C5F020B155FB3303591E6",
    "8C5CEAE0F443E006A050266F73ADD5B0",
    "1C02CE22FB22F0E72060217418F351F3",
    "9A01773FEBB0CFE0EBDBF37F4D23C27F",
    "43F32300BF252CC320E2572ACE766367",
    "07F161011B3101F1ED0301735631E734",
    "0454E7707A5F37565601E100406060AF",
    "647554BAD3100C43C16660F002CC10F3",
    "E157213170F842382032564265B0B043",
    "914FC59311B04151393EF6896A847636",
    "0710C0205D224237025323265C145FA1",
    "054E6F01165267025C3111F562A921E9",
    "722D1789E792E2CA0D5322211FD0F5AE",
    "91F7C751FCF671F34943430772341799",
]


def to_hex(data: bytes, upper: bool = False) -> str:
    return data.hex().upper() if upper else data.hex()


def to_binary(data: bytes) -> str:
    # Match C# ToBinary: 8 bits per byte, left-padded with '0'
    return "".join(f"{b:08b}" for b in data)


def random_string(length: int) -> str:
    # Match C# RandomHelper.RandomString using [a-zA-Z0-9]
    alphabet = string.ascii_letters + string.digits
    rng = random.SystemRandom()
    return "".join(rng.choice(alphabet) for _ in range(length))


def md5_bytes(data: bytes) -> bytes:
    # Use hashlib for MD5
    import hashlib

    md5 = hashlib.md5()
    md5.update(data)
    return md5.digest()


def md5_hex(data: bytes, upper: bool = False) -> str:
    return md5_bytes(data).hex().upper() if upper else md5_bytes(data).hex()


def _aes_cbc_encrypt_no_padding(key: bytes, data: bytes, iv: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    return encryptor.update(data) + encryptor.finalize()


def _aes_cbc_decrypt_zero_padding(key: bytes, data: bytes, iv: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    return decryptor.update(data) + decryptor.finalize()


def _pick_key(nibble_flag: int) -> bytes:
    index = (nibble_flag >> 4) & 0x0F
    return bytes.fromhex(KEYS_HEX[index])


def http_encrypt(body: bytes) -> bytes:
    # Align to 16-bytes blocks and append 16 random ASCII bytes immediately after body
    block = 16
    target_len = ((len(body) + block) + (block - 1)) // block * block
    buffer_ = bytearray(target_len)
    buffer_[0:len(body)] = body

    tail_random = random_string(16).encode("ascii")
    buffer_[len(body):len(body) + 16] = tail_random
    # Remaining bytes (if any) are zeros by default

    # Compose flag with low-nibble fixed to 0xC and high-nibble random in [0..0xE]
    high_nibble = random.SystemRandom().randrange(0, 15)
    flag = (high_nibble << 4) | 0x0C

    iv = random_string(16).encode("ascii")
    key = _pick_key(flag)
    cipher_text = _aes_cbc_encrypt_no_padding(key, bytes(buffer_), iv)

    result = bytearray(16 + len(cipher_text) + 1)
    result[0:16] = iv
    result[16:16 + len(cipher_text)] = cipher_text
    # In C#: array3[array3.Length ^ 1] = b; Length is odd, so it's the last index
    result[-1] = flag
    return bytes(result)


def http_decrypt(payload: bytes) -> bytes:
    # Extract info
    flag = payload[-1]
    iv = payload[0:16]
    cipher_text = payload[16:-1]

    key = _pick_key(flag)
    plain_padded = _aes_cbc_decrypt_zero_padding(key, cipher_text, iv)

    # Trim trailing zeros (PaddingMode.Zeros behavior)
    last_non_zero = len(plain_padded) - 1
    while last_non_zero >= 0 and plain_padded[last_non_zero] == 0:
        last_non_zero -= 1
    if last_non_zero < 0:
        return b""
    return plain_padded[: last_non_zero + 1]


def compute_dynamic_token(path: str, body: bytes, token: str) -> str:
    # 1) md5_hex(token) + body(utf8 string) + salt + path.TrimEnd('?')
    salt = "0eGsBkhl"
    payload_builder = md5_hex(token.encode("utf-8")) + body.decode("utf-8") + salt + path.rstrip("?")

    # 2) md5_hex of the builder, then treat its hex ASCII as bytes
    md5_hex_ascii_bytes = md5_hex(payload_builder.encode("utf-8")).encode("utf-8")

    # 3) Build binary string (128 bits) and rotate left by 6 bits
    binary_string = to_binary(md5_hex_ascii_bytes)
    binary_string = binary_string[6:] + binary_string[:6]

    # 4) For each byte position, reverse bits inside the byte, then XOR with original
    transformed = bytearray(md5_hex_ascii_bytes)
    for i in range(len(transformed)):
        section = binary_string[i * 8 : i * 8 + 8]
        reversed_byte = 0
        for j in range(8):
            if section[7 - j] == "1":
                reversed_byte |= (1 << (j & 0x1F))
        transformed[i] = reversed_byte ^ transformed[i]

    # 5) base64, take first 16, '+'->'m', '/'->'o', then append '1'
    b64 = base64.b64encode(bytes(transformed)).decode("ascii")
    token_short = b64[:16].replace("+", "m").replace("/", "o") + "1"
    return token_short


def encrypt_request_body_hex(obj_json_bytes: bytes) -> str:
    """Helper to produce hex string same as C# HttpEncrypt(...).ToHex()"""
    return to_hex(http_encrypt(obj_json_bytes))


__all__ = [
    "to_hex",
    "to_binary",
    "random_string",
    "md5_bytes",
    "md5_hex",
    "http_encrypt",
    "http_decrypt",
    "compute_dynamic_token",
    "encrypt_request_body_hex",
]

