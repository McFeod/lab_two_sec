def numbers_to_bytes(numbers, size):
    """
    Перевод чисел в байты
    :param numbers: список целых чисел
    :param size: максимальный размер числа в байтах
    :return: объект bytes
    """
    return b"".join(x.to_bytes(size, 'little') for x in numbers)


def bytes_to_numbers(message, size):
    """
    Преобразование набора байт в список чисел
    :param message: исходные данные
    :param size: размер одного числа в байтах
    :return: список целых чисел
    """
    return [int.from_bytes(message[x: x + size], 'little') for x in range(0, len(message), size)]
