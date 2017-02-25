from random import randint

from schnorr.keygen import SchnorrKeygen

MAX_ANSWER = 0xffffffff


class SchnorrAuthServer:
    """
    Поведение проводящего аутентификацию
    """
    def __init__(self, public_key):
        self.recipient_key = public_key
        self.recipient_message = None
        self.answer = None

    def exchange_open_messages(self, recipient_message, answer=None):
        """
        Обмен сообщениями с клиентом
        :param recipient_message: начальное сообщение от проверяемого
        :param answer: [необязательный параметр] ответ на сообщение
        :return: ответ на сообщение
        """
        self.recipient_message = recipient_message
        self.answer = randint(1, MAX_ANSWER) if answer is None else answer
        return self.answer

    def check_encrypted_message(self, encrypted):
        """
        Проверка подлинности
        :param encrypted: сообщение, зашифрованное закрытым ключом испытуемого
        :return: расшифрованное сообщение, результат проверки (bool)
        """
        y, p, _, g = self.recipient_key
        # decrypted = (pow(encrypted, g) * pow(y, self.answer)) % p  # медленно
        decrypted = (pow(encrypted, g, p) * pow(y, self.answer, p)) % p
        return decrypted, decrypted == self.recipient_message


class SchnorrAuthClient:
    """
    Поведение подтверждающего свою личность
    """
    def __init__(self):
        self.keygen = SchnorrKeygen()
        self.public_key, self.__private_key = self.keygen.generate_key()
        self.start_symbol = None

    def generate_message(self, start_symbol=None):
        """
        Создание начального сообщения
        :param start_symbol: [необязательный параметр] начальное значение, используемое при генерации
        :return: начальное значение, начальное сообщение
        """
        _, p, q, g = self.public_key
        self.start_symbol = randint(1, q) if start_symbol is None else start_symbol
        return self.start_symbol, pow(g, start_symbol, p)

    def encrypt_message(self, message):
        """
        Шифрование сообщения закрытым ключом
        :param message: сообщение от проверяющего
        :return: зашифрованное сообщение
        """
        _, _, q, _ = self.public_key
        return (self.start_symbol + self.__private_key * message) % q
