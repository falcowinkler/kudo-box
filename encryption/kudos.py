import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

backend = default_backend()
iterations = 2 ** 12

from cryptography.fernet import Fernet


# from https://stackoverflow.com/a/55147077/3885491
def _derive_key(password: bytes, salt: bytes, iterations=iterations) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=backend)
    return b64e(kdf.derive(password))


def make_password(team_name: str, channel_name: str, key: str) -> str:
    """creates a "password" from a server side secret, the somewhat-secret team
     and the channel name."""
    return f"{team_name}/{channel_name}/{key}"


def encrypt(kudo_text: str, password: str) -> bytes:
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(kudo_text.encode('utf-8'))),
        )
    )


def decrypt(token: bytes, password: str) -> str:
    decoded = b64d(token)
    salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iter, 'big')
    key = _derive_key(password.encode(), salt, iterations)
    return Fernet(key).decrypt(token).decode('utf-8')
