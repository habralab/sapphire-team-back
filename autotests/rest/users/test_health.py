from .client import UsersRestClient


def test_health(users_rest_client: UsersRestClient):
    users_rest_client.get_health()
