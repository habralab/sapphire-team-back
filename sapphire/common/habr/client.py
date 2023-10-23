from sapphire.common.http_client import HTTPClient

from .models import GenderEnum, UserCard
from .settings import HabrSettings


class HabrClient(HTTPClient):
    BASE_URL = "https://habr.com/api/v2"
    GENDER_MAPPING = {
        "0": None,
        "1": GenderEnum.MALE,
        "2": GenderEnum.FEMALE,
    }

    def __init__(self, api_key: str):
        headers = {"ApiKey": api_key}

        super().__init__(base_url=self.BASE_URL, headers=headers)

    async def get_user_card(self, username: str) -> UserCard:
        response = await self.get(url=f"/users/{username}/card")

        data = response.json()
        user_card = UserCard(
            username=data["alias"],
            full_name=data["full_name"],
            avatar=data["avatarUrl"],
            speciality=data["speciality"],
            gender=self.GENDER_MAPPING[data["gender"]],
        )

        return user_card


def get_habr_client(settings: HabrSettings) -> HabrClient:
    return HabrClient(api_key=settings.habr_api_key)
