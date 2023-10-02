import pytest
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from sapphire.users.settings import UsersSettings


@pytest.fixture()
def access_token_common_key() -> rsa.RSAPrivateKey:
    return rsa.generate_private_key(
        backend=crypto_default_backend(), public_exponent=65537, key_size=2048
    )


@pytest.fixture()
def refresh_token_common_key() -> rsa.RSAPrivateKey:
    return rsa.generate_private_key(
        backend=crypto_default_backend(), public_exponent=65537, key_size=2048
    )


@pytest.fixture()
def access_token_private_key(access_token_common_key: rsa.RSAPrivateKey) -> bytes:
    return access_token_common_key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption(),
    )


@pytest.fixture()
def access_token_public_key(access_token_common_key: rsa.RSAPrivateKey) -> bytes:
    return access_token_common_key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH, crypto_serialization.PublicFormat.OpenSSH
    )


@pytest.fixture()
def refresh_token_private_key(refresh_token_common_key: rsa.RSAPrivateKey) -> bytes:
    return refresh_token_common_key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption(),
    )


@pytest.fixture()
def refresh_token_public_key(refresh_token_common_key: rsa.RSAPrivateKey) -> bytes:
    return refresh_token_common_key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH, crypto_serialization.PublicFormat.OpenSSH
    )


@pytest.fixture()
def settings(
    access_token_private_key: bytes,
    access_token_public_key: bytes,
    refresh_token_private_key: bytes,
    refresh_token_public_key: bytes,
) -> UsersSettings:
    return UsersSettings(
        habr_oauth2_client_id="habr_oauth2_client_id",
        habr_oauth2_client_secret="habr_oauth2_client_secret",
        jwt_access_token_private_key=access_token_private_key,
        jwt_access_token_public_key=access_token_public_key,
        jwt_refresh_token_private_key=refresh_token_private_key,
        jwt_refresh_token_public_key=refresh_token_public_key,
    )
