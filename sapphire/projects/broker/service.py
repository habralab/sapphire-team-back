import asyncio

from sapphire.common.broker.service import BaseBrokerProducerService
from sapphire.projects.settings import ProjectsSettings


class ProjectsBrokerService(BaseBrokerProducerService):
    pass


def get_service(
        loop: asyncio.AbstractEventLoop,
        settings: ProjectsSettings,
) -> ProjectsBrokerService:
    return ProjectsBrokerService(
        loop=loop,
        servers=settings.producer_servers,
    )
