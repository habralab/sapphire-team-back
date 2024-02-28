import datetime

from pydantic import BaseModel

from sapphire.common.utils.rsa256 import generate_rsa_keys

access_token = generate_rsa_keys()
refresh_token = generate_rsa_keys()


class JWTSettings(BaseModel):
    access_token_private_key: str = access_token.private_key
    access_token_public_key: str = access_token.public_key
    refresh_token_private_key: str = refresh_token.private_key
    refresh_token_public_key: str = refresh_token.public_key
    access_token_expires: datetime.timedelta = datetime.timedelta(minutes=5)
    refresh_token_expires: datetime.timedelta = datetime.timedelta(days=30)
