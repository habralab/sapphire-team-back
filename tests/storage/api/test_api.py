import pytest

from fastapi.testclient import TestClient
from unittest import mock

from sapphire.storage.api.service import StorageAPIService
from sapphire.storage.database.service import get_service
from sapphire.storage.settings import StorageSettings


@pytest.mark.asyncio
def test_specializations():
    ...