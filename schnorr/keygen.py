from functools import partial
from random import randint

from sympy import randprime, primitive_root, nthroot_mod

from sympy.ntheory.factor_ import smoothness
from sympy.ntheory.modular import crt

MIN_RANDOM = 0x10000000  # границы для p и q
MAX_RANDOM = 0xffffffff
MAX_POWER = 0xffff       # верхняя граница для показателей степени (для скорости)
MAX_ATTEMPTS = MAX_RANDOM
get_random_prime = partial(randprime, MIN_RANDOM, MAX_RANDOM)


def find_open_key(p, gx):
    """
    Используя китайскую теорему об остатках, найдём у из открытого ключа
    :param p: p из открытого ключа
    :param gx: g**x, x - секретный ключ
    :return: y
    """
    return int(crt((gx, p), (0, 1))[0]) // gx


def find_root(p, q):
    """
    Поиск g из открытого ключа.
    Быстрый аналог _nthroot_mod1 из sympy для случая s=1, all_roots=False
    """
    return (pow(primitive_root(p), (p - 1) // q, p)) % p


class SchnorrKeygen:
    steps = None

    def generate_key(self):
        """
        Генерация ключа для схемы Шнорра
        :return: открытый и закрытый ключ
        """
        p = get_random_prime()
        q = smoothness(p - 1)[0]            # максимальный простой делитель
        x = randint(1, min(MAX_POWER, q))
        g = find_root(p, q)
        y = find_open_key(p, pow(g, x))
        public_key = (y, p, q, g)
        private_key = x
        self.steps = locals()
        return public_key, private_key
