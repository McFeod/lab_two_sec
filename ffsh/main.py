from ffsh.auth import FiatShamirProver, FiatShamirVerifier
from ffsh.keygen import FiatShamirKeygen

T = 64  # число аккредитаций
PREDEFINED_MESSAGES = 'Федосеев'  # для сообщений Пегги используем коды букв фамилии, пока возможно


def fiat_shamir_auth_demo():
    trent = FiatShamirKeygen()
    peggy = FiatShamirProver(trent.generate_key())
    victor = FiatShamirVerifier(peggy.public_key)

    context = {'gen': trent.steps}
    auth_context = []

    def get_init_value(idx):
        if idx < len(PREDEFINED_MESSAGES):
            return PREDEFINED_MESSAGES[idx]

    def fiat_shamir_tour(init_value):
        r, message = peggy.first_message(init_value)
        bit = victor.answer_with_bit(message)
        encrypted_message = peggy.answer(bit)
        decrypted_message, passed = victor.verify(encrypted_message)
        return locals()

    for i in range(T):
        auth_context.append(fiat_shamir_tour(get_init_value(i)))

    context['auth'] = auth_context
    return context

