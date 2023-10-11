from facet import ServiceMixin

from .api.service import UsersAPIService


class UsersService(ServiceMixin):
    def __init__(self, api: UsersAPIService):
        self._api = api

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._api,
        ]

    @property
    def api(self) -> UsersAPIService:
        return self._api


def get_service(api: UsersAPIService) -> UsersService:
    return UsersService(api=api)
