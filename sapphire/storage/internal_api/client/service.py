from sapphire.storage.internal_api.service import StorageGRPCService

from .settings import StorageInternalAPIClientSettings


class StorageInternalAPIClient(StorageGRPCService.Client):
    pass


def get_client(settings: StorageInternalAPIClientSettings) -> StorageInternalAPIClient:
    return StorageInternalAPIClient(
        host=settings.storage_grpc_host,
        port=settings.storage_grpc_port,
    )
