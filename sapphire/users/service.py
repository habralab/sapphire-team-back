from facet import ServiceMixin

from .api.service import UsersAPIService
from .internal_api.service import UsersInternalAPIService


class UsersService(ServiceMixin):
    def __init__(self, api: UsersAPIService, internal_api: UsersInternalAPIService):
        self._api = api
        self._internal_api = internal_api

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._api,
            self._internal_api,
        ]

    @property
    def api(self) -> UsersAPIService:
        return self._api

    @property
    def internal_api(self) -> UsersInternalAPIService:
        return self._internal_api


def get_service(api: UsersAPIService, internal_api: UsersInternalAPIService) -> UsersService:
    return UsersService(api=api, internal_api=internal_api)
