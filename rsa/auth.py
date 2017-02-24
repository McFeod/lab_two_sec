import hashlib
from functools import partial

from rsa.keygen import RSAKeygen, SYMBOL_SIZE
from utils.bigint_utils import numbers_to_bytes, bytes_to_numbers
numbers_to_bytes = partial(numbers_to_bytes, size=SYMBOL_SIZE)
bytes_to_numbers = partial(bytes_to_numbers, size=SYMBOL_SIZE)


class RSAClient:
    def __init__(self):
        self.keygen = RSAKeygen()
        self.public_key, self.__private_key = self.keygen.generate_key()
        self.recipient = None

    def handshake(self, other):
        """
        Обмен публичными ключами
        """
        self.recipient = other
        other.recipient = self

    def encrypt_message(self, message):
        """
        Шифрование при помощи публичного ключа адресата.
        Полученные числа упаковываются в байты
        :param message: исходное сообщение
        :return: зашифрованное сообщение в байтах, зашифрованное сообщение (числа)
        """
        numbers = apply_to_bytes(message, self.recipient.public_key)
        return numbers_to_bytes(numbers), numbers

    def decrypt_message(self, message):
        """
        Расшифровка при помощи собственного приватного ключа.
        :param message: упакованные в байты числа, составляющие зашифрованное сообщение
        :return: сообщение в открытом виде
        """
        return apply_to_numbers(bytes_to_numbers(message), self.__private_key)

    def sign_message(self, message):
        """
        Добавление электронной подписи (зашифрованной собственным приватным ключом хеш-суммы от
                        исходного сообщения)
        :param message: исходное сообщение
        :return: исходное сообщение с дописанными в конец байтами электронной подписи
        """
        return message + numbers_to_bytes(
            apply_to_bytes(hashlib.md5(message).digest(), self.__private_key))

    def check_sign(self, signed_message):
        """
        Проверка чужой подписи.
        Зная использованную для подписи хеш-функцию, можно четко определить, какое количество
        байт в конце сообщения необходимо преобразовывать в числа и расшифровывать при помощи
        публичного ключа подписавшего
        :param signed_message: подписанное сообщение
        :return: True, если в расшифрованной части содежится хеш остального сообщения
        """
        message = signed_message[:-0x80]
        sign = bytes_to_numbers(signed_message[-0x80:])
        return hashlib.md5(message).digest() == apply_to_numbers(sign, self.recipient.public_key)


def apply_to_symbol(symbol, key):
    """
    Применение шифрования / дешифрования
    :param symbol: исходное число / байт
    :param key: публичный или секретный ключ
    :return: зашифрованный символ (число)
    """
    return pow(symbol, *key)


def apply_to_numbers(numbers, key):
    """
    Применение шифрования / дешифрования к группе чисел
    """
    return bytes(apply_to_symbol(x, key) for x in numbers)


def apply_to_bytes(message, key):
    """
    Применение шифрования / дешифрования побайтово к строке
    """
    return [apply_to_symbol(int(x), key) for x in message]
