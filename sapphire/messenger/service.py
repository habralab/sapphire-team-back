from facet import ServiceMixin

from .api.service import MessengerAPIService


class MessengerService(ServiceMixin):
    def __init__(self, api: MessengerAPIService):
        self._api = api

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._api,
        ]

    @property
    def api(self) -> MessengerAPIService:
        return self._api


def get_service(api: MessengerAPIService) -> MessengerService:
    return MessengerService(api=api)
