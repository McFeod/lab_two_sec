from functools import partial
from random import randint

from sympy import randprime, sqrt_mod_iter
from sympy.ntheory.modular import crt

MIN_RANDOM = 0x10000000  # границы для p и q
MAX_RANDOM = 0xffffffff
get_random_prime = partial(randprime, MIN_RANDOM, MAX_RANDOM)


def get_residue(n):
    """
    Вычисляет случайный квадратичный вычет и его обратное значения
    :param n: модуль вычета, простое число
    :return:
    """
    max_x = (n >> 1) + 1
    result = None

    def try_random_residue():
        res = pow(randint(1, max_x), 2, n)
        try:
            rev_res = int(crt((res, n), (0, 1))[0]) // res
            return res, rev_res
        except (ZeroDivisionError, TypeError):
            return None

    while result is None:
        result = try_random_residue()
    return result


def find_private_key(a, p):
    """
    Находит наименьшее решение уравнения x**2 = a mod p
    """
    return min(sqrt_mod_iter(a, p))


class FiatShamirKeygen:
    steps = None  # хранение промежуточных вычислений для отчёта

    def generate_key(self):
        """

        Генерация ключей
        :return: кортеж из открытой и закрытой частей
        """
        p = get_random_prime()          # инициализация
        q = get_random_prime()
        n = p * q                       # модуль
        v, v_1 = get_residue(n)         # квадратичный вычет и обратное значение
        s = find_private_key(v_1, n)    # наименьшее значение sqrt_mod
        public_key = (v, n)
        private_key = s
        self.steps = locals()
        return public_key, private_key


if __name__ == '__main__':
    keygen = FiatShamirKeygen()
    print(keygen.generate_key())
    print(keygen.steps)
