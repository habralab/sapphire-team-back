from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15

from sapphire.common.utils.rsa256 import generate_rsa_keys


def test_generate_rsa_keys():
    keys = generate_rsa_keys()

    message = b"Hello, world!"
    public_key = serialization.load_ssh_public_key(data=keys.public_key.encode())
    private_key = serialization.load_pem_private_key(data=keys.private_key.encode(), password=None)
    padding = PKCS1v15()

    encrypted_message = public_key.encrypt(message, padding)
    decrypted_message = private_key.decrypt(encrypted_message, padding)
    assert decrypted_message == message
