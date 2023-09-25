from dataclasses import dataclass
import dotenv
import os


@dataclass
class Config:
    user_info_token_url: str
    server_authorization_url: str
    server_token_url: str
    client_id: str
    client_secret: str
    callback_url: str


dotenv.load_dotenv()

config = Config(
    server_authorization_url='https://account.habr.com/oauth/authorize/?',
    server_token_url='https://account.habr.com/oauth/token/',
    user_info_token_url='https://account.habr.com/api/v1/me/',
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    callback_url=os.getenv('CALLBACK_URL'),
)


