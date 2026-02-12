import os
import json
import base64
from datetime import datetime
from typing import List, Dict, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2


class PasswordVault:
    """Зашифрованное хранилище паролей"""

    def __init__(self, vault_file='data/vault.dat'):
        self.vault_file = vault_file
        self.key = None
        self.cipher = None
        self.unlocked = False
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """Создание директории для данных"""
        os.makedirs(os.path.dirname(self.vault_file), exist_ok=True)

    def _derive_key(self, master_password: str, salt: bytes = None) -> tuple:
        """
        Получение ключа шифрования из мастер-пароля
        """
        if salt is None:
            salt = os.urandom(16)

        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        return key, salt

    def create_vault(self, master_password: str) -> bool:
        """
        Создание нового хранилища
        """
        try:
            key, salt = self._derive_key(master_password)
            cipher = Fernet(key)

            vault_data = {
                'salt': base64.b64encode(salt).decode(),
                'passwords': []
            }

            encrypted = cipher.encrypt(json.dumps(vault_data['passwords']).encode())
            vault_data['passwords'] = base64.b64encode(encrypted).decode()

            with open(self.vault_file, 'w') as f:
                json.dump(vault_data, f)

            self.key = key
            self.cipher = cipher
            self.unlocked = True
            return True
        except Exception as e:
            print(f"Ошибка создания хранилища: {e}")
            return False

    def unlock_vault(self, master_password: str) -> bool:
        """
        Разблокировка хранилища
        """
        try:
            if not os.path.exists(self.vault_file):
                return False

            with open(self.vault_file, 'r') as f:
                vault_data = json.load(f)

            salt = base64.b64decode(vault_data['salt'])
            key, _ = self._derive_key(master_password, salt)
            cipher = Fernet(key)

            encrypted = base64.b64decode(vault_data['passwords'])
            cipher.decrypt(encrypted)

            self.key = key
            self.cipher = cipher
            self.unlocked = True
            return True
        except Exception:
            return False

    def lock_vault(self):
        """Блокировка хранилища"""
        self.key = None
        self.cipher = None
        self.unlocked = False

    def get_passwords(self) -> List[Dict]:
        """
        Получение всех сохраненных паролей
        """
        if not self.unlocked:
            return []

        try:
            with open(self.vault_file, 'r') as f:
                vault_data = json.load(f)

            encrypted = base64.b64decode(vault_data['passwords'])
            decrypted = self.cipher.decrypt(encrypted)
            return json.loads(decrypted.decode())
        except Exception:
            return []

    def save_passwords(self, passwords: List[Dict]) -> bool:
        """
        Сохранение паролей в хранилище
        """
        if not self.unlocked:
            return False

        try:
            with open(self.vault_file, 'r') as f:
                vault_data = json.load(f)

            encrypted = self.cipher.encrypt(json.dumps(passwords).encode())
            vault_data['passwords'] = base64.b64encode(encrypted).decode()

            with open(self.vault_file, 'w') as f:
                json.dump(vault_data, f)

            return True
        except Exception:
            return False

    def add_password(self, service: str, username: str, password: str, notes: str = "") -> bool:
        """
        Добавление нового пароля
        """
        passwords = self.get_passwords()

        new_entry = {
            'id': len(passwords) + 1,
            'service': service,
            'username': username,
            'password': password,
            'notes': notes,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'updated_at': datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        passwords.append(new_entry)
        return self.save_passwords(passwords)

    def delete_password(self, password_id: int) -> bool:
        """
        Удаление пароля
        """
        passwords = self.get_passwords()
        passwords = [p for p in passwords if p['id'] != password_id]
        return self.save_passwords(passwords)

    def update_password(self, password_id: int, **kwargs) -> bool:
        """
        Обновление пароля
        """
        passwords = self.get_passwords()
        for password in passwords:
            if password['id'] == password_id:
                password.update(kwargs)
                password['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                break
        return self.save_passwords(passwords)


vault = PasswordVault()