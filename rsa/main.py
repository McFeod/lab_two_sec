import pprint

from rsa.auth import RSAClient

if __name__ == '__main__':
    alice = RSAClient()
    bob = RSAClient()

    alice.handshake(bob)

    message = b"hello, world"

    pp = pprint.PrettyPrinter(indent=4)

    def _():
        alice_signed_message = alice.sign_message(message)
        alice_encrypted_message = alice.encrypt_message(alice_signed_message)

        bob_decrypted_message = bob.decrypt_message(alice_encrypted_message)
        bob_check_sign = bob.check_sign(bob_decrypted_message)
        pp.pprint(locals())

    _()
