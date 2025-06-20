from cryptography.fernet import Fernet
import base64
import hashlib

def generate_key_from_password(password: str) -> bytes:
    digest = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(digest)

def encrypt_data(data: bytes, password: str) -> bytes:
    key = generate_key_from_password(password)
    f = Fernet(key)
    return f.encrypt(data)

def decrypt_data(data: bytes, password: str) -> bytes:
    key = generate_key_from_password(password)
    f = Fernet(key)
    return f.decrypt(data)
