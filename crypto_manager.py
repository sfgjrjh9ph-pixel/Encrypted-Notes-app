"""Encryption helpers.

The user's master password is never stored anywhere. Instead:
  1. A random salt is generated once and saved alongside the notes file.
  2. Every time the app starts, PBKDF2-HMAC-SHA256 (480,000 rounds) turns the
     password + salt into a symmetric key.
  3. That key encrypts/decrypts the whole notes payload with Fernet, which
     provides authenticated encryption (AES-128-CBC + HMAC), so a wrong
     password is always detected instead of producing garbled data.
"""
import base64
import os

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

KDF_ITERATIONS = 480_000
SALT_SIZE = 16


class WrongPasswordError(Exception):
    """Raised when a password fails to decrypt the notes payload."""


def generate_salt() -> bytes:
    return os.urandom(SALT_SIZE)


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERATIONS,
    )
    key_bytes = kdf.derive(password.encode("utf-8"))
    return base64.urlsafe_b64encode(key_bytes)


def encrypt(data: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(data)


def decrypt(token: bytes, key: bytes) -> bytes:
    try:
        return Fernet(key).decrypt(token)
    except InvalidToken as exc:
        raise WrongPasswordError("Incorrect master password.") from exc
