from facet import ServiceMixin


class StorageService(ServiceMixin):
    def __init__(self):
        pass

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return []


def get_service() -> StorageService:
    return StorageService()
