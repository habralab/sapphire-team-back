from .client import MessengerRestClient


def test_health(messenger_rest_client: MessengerRestClient):
    messenger_rest_client.get_health()
