import pytest
from fastapi.testclient import TestClient

from sapphire.users.api.service import UsersAPIService
from sapphire.users.database.service import get_service
from sapphire.users.jwt import JWTMethods, get_jwt_methods
from sapphire.users.oauth2.habr import get_oauth2_backend
from sapphire.users.settings import UsersSettings


@pytest.fixture()
def test_client(settings: UsersSettings) -> UsersAPIService:
    database = get_service(settings=settings)
    jwt_methods = get_jwt_methods(settings=settings)
    habr_oauth2 = get_oauth2_backend(settings=settings)
    service = UsersAPIService(
        database=database, jwt_methods=jwt_methods, habr_oauth2=habr_oauth2
    )
    return TestClient(service.get_app())


@pytest.fixture()
def jwt_methods(settings: UsersSettings) -> JWTMethods:
    return get_jwt_methods(settings=settings)
