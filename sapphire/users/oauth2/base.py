import yarl

from sapphire.common.http_client import HTTPClient


class OAuth2BaseBackend(HTTPClient):
    authorization_url: str
    token_url: str
    grant_type: str

    def __init__(self, client_id: str, client_secret: str):
        self._client_id = client_id
        self._client_secret = client_secret

        super().__init__()

    def get_authorization_url(self, state: str, redirect_url: str | None = None) -> str:
        query_parameters = {
            "client_id": self._client_id,
            "redirect_uri": redirect_url,
            "response_type": "code",
            "state": state,
        }

        url = yarl.URL(self.authorization_url)
        url %= query_parameters

        return str(url)

    async def get_token(self, code: str) -> str | None:
        payload = {
            "grant_type": self.grant_type,
            "code": code,
            "client_id": self._client_id,
            "client_secret": self._client_secret,
        }
        response = await self.post(url=self.token_url, data=payload)
        data = response.json()

        return data["access_token"]
