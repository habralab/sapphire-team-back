from .client import StorageRestClient


def test_health(storage_rest_client: StorageRestClient):
    storage_rest_client.get_health()
