import backoff
from httpx import HTTPError

from collabry.common.http_client import HTTPClient

from .models import CareerTrack, Skill, Specialization
from .settings import HabrCareerSettings


class HabrCareerClient(HTTPClient):
    BASE_URL = "https://career.habr.com"

    def __init__(self, api_key: str):
        headers = {"X-Access-Token": api_key}

        super().__init__(base_url=self.BASE_URL, headers=headers)

    @backoff.on_exception(backoff.expo, HTTPError, max_tries=3, raise_on_giveup=False)
    async def get_career_track(self, user_id: str) -> CareerTrack:
        path = "/api/v1/users/career_track"
        params = {"id": user_id}

        response = await self.get(url=path, params=params)
        response.raise_for_status()

        data = response.json()
        career_track = CareerTrack(
            login=data["login"],
            full_name=data["full_name"],
            avatar=data["avatar"],
            skills=[Skill(id=item["id"], title=item["title"]) for item in data["skills"]],
            specializations=[
                Specialization(id=item["id"], title=item["title"]["ru"])
                for item in data["specializations"]
            ],
        )

        return career_track


def get_habr_career_client(settings: HabrCareerSettings) -> HabrCareerClient:
    return HabrCareerClient(api_key=settings.api_key)
