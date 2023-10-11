from facet import ServiceMixin

from .api.service import ProjectsAPIService
from .broker.service import ProjectsBrokerService


class ProjectsService(ServiceMixin):
    def __init__(self, api: ProjectsAPIService, broker: ProjectsBrokerService):
        self._api = api
        self._broker = broker

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._api,
            self._broker,
        ]

    @property
    def api(self) -> ProjectsAPIService:
        return self._api

    @property
    def broker(self) -> ProjectsBrokerService:
        return self._broker


def get_service(api: ProjectsAPIService, broker: ProjectsBrokerService) -> ProjectsService:
    return ProjectsService(api=api, broker=broker)
