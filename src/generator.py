import random
import string
from typing import Optional


class PasswordGenerator:
    """Генератор безопасных паролей"""

    LOWERCASE = string.ascii_lowercase
    UPPERCASE = string.ascii_uppercase
    DIGITS = string.digits
    SYMBOLS = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    LEVELS = {
        "Низкий": {
            "lowercase": True,
            "uppercase": False,
            "digits": True,
            "symbols": False,
            "min_length": 6,
            "max_length": 12
        },
        "Средний": {
            "lowercase": True,
            "uppercase": True,
            "digits": True,
            "symbols": False,
            "min_length": 8,
            "max_length": 16
        },
        "Высокий": {
            "lowercase": True,
            "uppercase": True,
            "digits": True,
            "symbols": True,
            "min_length": 12,
            "max_length": 24
        },
        "Очень высокий": {
            "lowercase": True,
            "uppercase": True,
            "digits": True,
            "symbols": True,
            "min_length": 16,
            "max_length": 32
        }
    }

    def __init__(self):
        self.current_password = None

    def generate_password(self, length: int, use_lowercase: bool = True,
                          use_uppercase: bool = True, use_digits: bool = True,
                          use_symbols: bool = True, exclude_ambiguous: bool = False) -> str:
        """
        Генерация пароля с заданными параметрами
        """
        if length < 4:
            length = 4

        chars = ""
        if use_lowercase:
            chars += self.LOWERCASE
        if use_uppercase:
            chars += self.UPPERCASE
        if use_digits:
            chars += self.DIGITS
        if use_symbols:
            chars += self.SYMBOLS

        if not chars:
            chars = self.LOWERCASE + self.DIGITS

        if exclude_ambiguous:
            ambiguous = "Il1O0"
            chars = ''.join(c for c in chars if c not in ambiguous)

        password = []

        if use_lowercase:
            password.append(random.choice(self.LOWERCASE))
        if use_uppercase:
            password.append(random.choice(self.UPPERCASE))
        if use_digits:
            password.append(random.choice(self.DIGITS))
        if use_symbols:
            password.append(random.choice(self.SYMBOLS))

        for _ in range(length - len(password)):
            password.append(random.choice(chars))

        random.shuffle(password)

        self.current_password = ''.join(password)
        return self.current_password

    def generate_by_level(self, level: str, length: Optional[int] = None) -> str:
        """
        Генерация пароля по уровню сложности
        """
        if level not in self.LEVELS:
            level = "Средний"

        config = self.LEVELS[level]

        if length is None:
            length = random.randint(config["min_length"], config["max_length"])

        return self.generate_password(
            length=length,
            use_lowercase=config["lowercase"],
            use_uppercase=config["uppercase"],
            use_digits=config["digits"],
            use_symbols=config["symbols"]
        )

    def check_strength(self, password: str) -> tuple:
        """
        Проверка сложности пароля
        """
        score = 0
        feedback = []

        if len(password) >= 16:
            score += 3
            feedback.append("✓ Отличная длина")
        elif len(password) >= 12:
            score += 2
            feedback.append("✓ Хорошая длина")
        elif len(password) >= 8:
            score += 1
            feedback.append("✓ Достаточная длина")
        else:
            feedback.append("✗ Слишком короткий")

        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append("✗ Нет строчных букв")

        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("✗ Нет заглавных букв")

        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("✗ Нет цифр")

        if any(c in self.SYMBOLS for c in password):
            score += 2
            feedback.append("✓ Есть спецсимволы")
        else:
            feedback.append("✗ Нет спецсимволов")

        unique_chars = len(set(password))
        if unique_chars > len(password) * 0.7:
            score += 1
            feedback.append("✓ Хорошее разнообразие")

        if score >= 7:
            rating = "Очень надежный"
            color = "#4CAF50"
        elif score >= 5:
            rating = "Надежный"
            color = "#2196F3"
        elif score >= 3:
            rating = "Средний"
            color = "#FF9800"
        else:
            rating = "Слабый"
            color = "#f44336"

        return rating, feedback, color, score


generator = PasswordGenerator()