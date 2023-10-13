from facet import ServiceMixin

from .api.service import NotificationsAPIService
from .broker.service import NotificationsBrokerService


class NotificationsService(ServiceMixin):
    def __init__(self, api: NotificationsAPIService, broker: NotificationsBrokerService):
        self._api = api
        self._broker = broker

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._api,
            self._broker,
        ]

    @property
    def api(self) -> NotificationsAPIService:
        return self._api

    @property
    def broker(self) -> NotificationsBrokerService:
        return self._broker


def get_service(
        api: NotificationsAPIService,
        broker: NotificationsBrokerService,
) -> NotificationsService:
    return NotificationsService(api=api, broker=broker)
