import aiohttp
import yarl


class OAuth2BaseBackend:
    authorization_url: str
    token_url: str
    grant_type: str

    def __init__(self, client_id: str, client_secret: str):
        self._client_id = client_id
        self._client_secret = client_secret

    def get_authorization_url(self, redirect_url: str | None = None) -> str:
        state = "test"
        query_parameters = {
            "client_id": self._client_id,
            "redirect_uri": redirect_url,
            "response_type": "code",
            "state": state,
        }

        url = yarl.URL(self.authorization_url)
        url %= query_parameters

        return str(url)

    async def check_state(self, state: str) -> bool:
        return state == "test"

    async def get_token(self, state: str, code: str) -> str | None:
        if not await self.check_state(state=state):
            return None

        payload = {
            "grant_type": self.grant_type,
            "code": code,
            "client_id": self._client_id,
            "client_secret": self._client_secret,
        }
        async with aiohttp.request(method="POST", url=self.token_url, data=payload) as response:
            data = await response.json()

        return data["access_token"]
