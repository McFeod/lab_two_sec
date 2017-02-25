from schnorr.auth import SchnorrAuthServer, SchnorrAuthClient


def schnorr_auth_demo():
    alice = SchnorrAuthClient()
    bob = SchnorrAuthServer(alice.public_key)

    context = {'gen': alice.keygen.steps}

    def auth():
        k_char = 'Ф'
        k, message = alice.generate_message(cp1251_to_int(k_char))
        answer_char = 'е'
        first_answer = bob.exchange_open_messages(message, cp1251_to_int(answer_char))
        encrypted_message = alice.encrypt_message(first_answer)
        decrypted_message, passed = bob.check_encrypted_message(encrypted_message)
        return locals()
    context['auth'] = auth()
    return context


def cp1251_to_int(symbol):
    return bytes(symbol, 'cp1251')[0]
