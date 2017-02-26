from schnorr.auth import SchnorrVerifier, SchnorrProver


def schnorr_auth_demo():
    peggy = SchnorrProver()
    victor = SchnorrVerifier(peggy.public_key)

    context = {'gen': peggy.keygen.steps}

    def auth():
        k_char = 'Ф'
        k, message = peggy.generate_message(cp1251_to_int(k_char))
        answer_char = 'е'
        first_answer = victor.exchange_open_messages(message, cp1251_to_int(answer_char))
        encrypted_message = peggy.encrypt_message(first_answer)
        decrypted_message, passed = victor.check_encrypted_message(encrypted_message)
        return locals()
    context['auth'] = auth()
    return context


def cp1251_to_int(symbol):
    return bytes(symbol, 'cp1251')[0]
