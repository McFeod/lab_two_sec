import pprint

from rsa.auth import RSAClient


def rsa_auth_demo():
    alice = RSAClient()
    bob = RSAClient()
    alice.handshake(bob)
    context = {'gen': alice.keygen.steps}

    def auth():
        message = 'Фед'.encode('cp1251')
        encrypted_bytes, encrypted_numbers = bob.encrypt_message(message)
        decrypted_message = alice.decrypt_message(encrypted_bytes)
        passed = (message == decrypted_message)
        return locals()
    context['auth'] = auth()
    return context


if __name__ == '__main__':
    alice = RSAClient()
    bob = RSAClient()

    alice.handshake(bob)

    message = b"hello, world"

    pp = pprint.PrettyPrinter(indent=4)

    def _():
        alice_signed_message = alice.sign_message(message)
        alice_encrypted_message = alice.encrypt_message(alice_signed_message)[0]

        bob_decrypted_message = bob.decrypt_message(alice_encrypted_message)
        bob_check_sign = bob.check_sign(bob_decrypted_message)
        pp.pprint(locals())

    _()
