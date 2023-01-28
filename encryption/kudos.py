from cryptography.hazmat.backends import default_backend

backend = default_backend()
iterations = 2 ** 12

from cryptography.fernet import Fernet


def encrypt(kudo_text: str, password: str) -> bytes:
    return Fernet(password.encode()).encrypt(kudo_text.encode())


def decrypt(token: bytes, password: str) -> str:
    return Fernet(password).decrypt(token).decode("utf-8")
