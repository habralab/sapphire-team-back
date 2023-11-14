import pydantic

from sapphire.users.settings import UsersSettings

from .base import OAuth2BaseBackend


class HabrUser(pydantic.BaseModel):
    id: str
    login: str
    email: pydantic.EmailStr
    is_active: bool
    is_email_confirmed: bool


class OAuth2HabrBackend(OAuth2BaseBackend):
    authorization_url = "https://account.habr.com/oauth/authorize/"
    token_url = "https://account.habr.com/oauth/token/"
    grant_type = "authorization_code"
    me_url = "https://account.habr.com/api/v1/me/"

    async def get_user_info(self, token: str) -> HabrUser:
        headers = {"Authorization": f"Token {token}"}
        response = await self.get(url=self.me_url, headers=headers)
        data = response.json()
        user_data = data["user"]

        return HabrUser(
            id=user_data["id"],
            login=user_data["login"],
            email=user_data["email"],
            is_active=(user_data["is_active"] == "1"),
            is_email_confirmed=(user_data["is_email_confirmed"] == "1"),
        )


def get_oauth2_backend(settings: UsersSettings) -> OAuth2HabrBackend:
    return OAuth2HabrBackend(
        client_id=settings.habr_oauth2_client_id,
        client_secret=settings.habr_oauth2_client_secret,
    )
