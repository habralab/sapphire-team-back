from facet import ServiceMixin

from .api.service import MessengerAPIService
from .broker.service import MessengerBrokerService


class MessengerService(ServiceMixin):
    def __init__(self, api: MessengerAPIService, broker: MessengerBrokerService):
        self._api = api
        self._broker = broker

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._api,
            self._broker,
        ]

    @property
    def api(self) -> MessengerAPIService:
        return self._api

    @property
    def broker(self) -> MessengerBrokerService:
        return self._broker


def get_service(api: MessengerAPIService, broker: MessengerBrokerService) -> MessengerService:
    return MessengerService(api=api, broker=broker)
