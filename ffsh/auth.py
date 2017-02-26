from random import randint, getrandbits

from schnorr.main import cp1251_to_int


class FiatShamirProver:
    """
    Поведение подтверждающего свою личность
    """
    def __init__(self, keys):
        self.public_key, self.__private_key = keys
        self.r = None

    def first_message(self, init_value=None):
        """
        Создание начального сообщения
        :return: начальное значение, начальное сообщение
        """
        v, n = self.public_key
        self.r = randint(1, n-1) if init_value is None else cp1251_to_int(init_value)
        return self.r, pow(self.r, 2, n)

    def answer(self, bit):
        """
        Шифрование закрытым ключом
        :param bit: ответ проверяющего
        :return: зашфрованное сообщение
        """
        v, n = self.public_key
        return (self.r * self.__private_key) % n if bit else self.r


class FiatShamirVerifier:
    """
    Поведение проводящего аутентификацию
    """
    def __init__(self, public_key):
        self.prover_key = public_key
        self.bit = None
        self.message = None

    def answer_with_bit(self, message):
        """
        первоначальный обмен сообщениями с проверяемым
        :param message: сообщение, зашифрованное открытым ключом проверяемого
        :return: случайный бит
        """
        self.message = message
        self.bit = getrandbits(1)
        return self.bit

    def verify(self, encrypted):
        """
        Подтверждение личности проверяемого
        :param encrypted: сообщение, зашифрованное закрытым ключом проверяемого
        :return: расшифрованное сообщение, результат проверки
        """
        v, n = self.prover_key
        decrypted = (pow(encrypted, 2, n) * v) % n if self.bit else pow(encrypted, 2, n)
        return decrypted, decrypted == self.message
