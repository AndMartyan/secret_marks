import os

from cryptography.fernet import Fernet
from config import KEY_PATH

def read_encryption_key():
    """Функция для считывания ключа из файла"""
    key_file = KEY_PATH
    if os.path.exists(key_file):
        with open(key_file, "rb") as file:
            key = file.read()
            return key
    else:
        # Если файл с ключом отсутствует, генерируем новый ключ
        key = Fernet.generate_key()
        with open(key_file, "wb") as file:
            file.write(key)
        return key


SECRET_KEY = read_encryption_key()
fernet = Fernet(SECRET_KEY)
