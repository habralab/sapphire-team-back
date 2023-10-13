import requests
import yarl


class BaseRestClient:
    def __init__(self, session: requests.Session, base_url: yarl.URL | str):
        self._session = session
        self._base_url = yarl.URL(base_url)

    def request(self, path: str, **kwargs) -> requests.Response:
        url = self._base_url / path.lstrip("/")

        return self._session.request(url=str(url), verify=False, **kwargs)

    def get(self, path: str, **kwargs) -> requests.Response:
        return self.request(path=path, method="GET", **kwargs)
