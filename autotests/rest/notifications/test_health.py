from .client import NotificationsRestClient


def test_health(notifications_rest_client: NotificationsRestClient):
    notifications_rest_client.get_health()
