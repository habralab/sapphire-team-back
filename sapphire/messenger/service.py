from facet import ServiceMixin


class MessengerService(ServiceMixin):
    def __init__(self):
        pass

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return []


def get_service() -> MessengerService:
    return MessengerService()
