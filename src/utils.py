import random
import string
import secrets


def generate_pronounceable(length=12):
    """
    Генерация произносимого пароля
    """
    vowels = 'aeiou'
    consonants = ''.join(c for c in string.ascii_lowercase if c not in vowels)

    password = []
    for i in range(length):
        if i % 2 == 0:
            password.append(random.choice(consonants))
        else:
            password.append(random.choice(vowels))

    if length > 4:
        password[0] = password[0].upper()
        password[-1] = random.choice(string.digits)

    return ''.join(password)


def generate_pin(length=6):
    """
    Генерация PIN-кода
    """
    return ''.join(secrets.choice(string.digits) for _ in range(length))


def calculate_entropy(password):
    """
    Расчет энтропии пароля
    """
    charset_size = 0

    if any(c.islower() for c in password):
        charset_size += 26
    if any(c.isupper() for c in password):
        charset_size += 26
    if any(c.isdigit() for c in password):
        charset_size += 10
    if any(c in string.punctuation for c in password):
        charset_size += len(string.punctuation)

    if charset_size == 0:
        return 0

    entropy = len(password) * (charset_size.bit_length())
    return entropy