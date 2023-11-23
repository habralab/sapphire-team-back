from http import HTTPStatus
import uuid
from typing import Type

import pytest
from autotests.clients.rest.exceptions import ResponseException

from autotests.clients.rest.notifications.client import NotificationsRestClient
from autotests.utils import Empty


@pytest.mark.parametrize("client", (
        pytest.lazy_fixture("oleg_notifications_rest_client"),
        pytest.lazy_fixture("oleg_activated_notifications_rest_client"),
        pytest.lazy_fixture("matvey_notifications_rest_client"),
        pytest.lazy_fixture("matvey_activated_notifications_rest_client"),
        pytest.lazy_fixture("random_notifications_rest_client"),
))
@pytest.mark.parametrize(
    ("is_read", "page", "per_page"),
    (
        (Empty, 1, 10),
        (True, 1, 10),
    ),
)
@pytest.mark.asyncio
async def test_get_notifications(
        client: NotificationsRestClient,
        is_read: bool | Type[Empty],
        page: int | Type[Empty],
        per_page: int | Type[Empty],
):

    notifications = await client.get_notifications(
        page=page,
        per_page=per_page,
        is_read=is_read,
    )

    for notification in notifications.data:
        if is_read is not Empty:
            assert notification.is_read == is_read


@pytest.mark.asyncio
async def test_get_notifications_not_authenticated(
        notifications_rest_client: NotificationsRestClient,
):
    with pytest.raises(ResponseException) as exception:
        await notifications_rest_client.get_notifications()

    assert exception.value.status_code == HTTPStatus.UNAUTHORIZED
    assert exception.value.body == b'{"detail":"Not authenticated."}'


@pytest.mark.parametrize(("client", "recipient_id", "notification_id"), (
    (
        pytest.lazy_fixture("oleg_notifications_rest_client"),
        pytest.lazy_fixture("oleg_id"),
        pytest.lazy_fixture("oleg_notification_id"),
    ),
    (
        pytest.lazy_fixture("oleg_activated_notifications_rest_client"),
        pytest.lazy_fixture("oleg_id"),
        pytest.lazy_fixture("oleg_notification_id"),
    ),
    (
        pytest.lazy_fixture("matvey_notifications_rest_client"),
        pytest.lazy_fixture("matvey_id"),
        pytest.lazy_fixture("matvey_notification_id"),
    ),
    (
        pytest.lazy_fixture("matvey_activated_notifications_rest_client"),
        pytest.lazy_fixture("matvey_id"),
        pytest.lazy_fixture("matvey_notification_id"),
    ),
))
@pytest.mark.asyncio
async def test_get_notification(
        client: NotificationsRestClient,
        recipient_id: uuid.UUID,
        notification_id: uuid.UUID,
):
    notification = await client.get_notification(notification_id=notification_id)

    assert notification.id == notification_id
    assert notification.recipient_id == recipient_id


@pytest.mark.parametrize("notification_id", (
    pytest.lazy_fixture("oleg_notification_id"),
    pytest.lazy_fixture("matvey_notification_id"),
    uuid.uuid4(),
))
@pytest.mark.asyncio
async def test_get_notification_not_authenticated(
        notifications_rest_client: NotificationsRestClient,
        notification_id: uuid.UUID,
):
    with pytest.raises(ResponseException) as exception:
        await notifications_rest_client.get_notification(notification_id=notification_id)

    assert exception.value.status_code == HTTPStatus.UNAUTHORIZED
    assert exception.value.body == b'{"detail":"Not authenticated."}'


@pytest.mark.parametrize("client", (
    pytest.lazy_fixture("oleg_notifications_rest_client"),
    pytest.lazy_fixture("oleg_activated_notifications_rest_client"),
    pytest.lazy_fixture("matvey_notifications_rest_client"),
    pytest.lazy_fixture("matvey_activated_notifications_rest_client"),
))
@pytest.mark.asyncio
async def test_get_notification_not_found(client: NotificationsRestClient):
    with pytest.raises(ResponseException) as exception:
        await client.get_notification(notification_id=uuid.uuid4())

    assert exception.value.status_code == HTTPStatus.NOT_FOUND
    assert exception.value.body == b'{"detail":"Not found."}'


@pytest.mark.parametrize(("client", "notification_id"), (
    (
        pytest.lazy_fixture("oleg_notifications_rest_client"),
        pytest.lazy_fixture("matvey_notification_id"),
    ),
    (
        pytest.lazy_fixture("oleg_activated_notifications_rest_client"),
        pytest.lazy_fixture("matvey_notification_id"),
    ),
    (
        pytest.lazy_fixture("matvey_notifications_rest_client"),
        pytest.lazy_fixture("oleg_notification_id"),
    ),
    (
        pytest.lazy_fixture("matvey_activated_notifications_rest_client"),
        pytest.lazy_fixture("oleg_notification_id"),
    ),
))
@pytest.mark.asyncio
async def test_get_notification_forbidden(
        client: NotificationsRestClient,
        notification_id: uuid.UUID,
):
    with pytest.raises(ResponseException) as exception:
        await client.get_notification(notification_id=notification_id)

    assert exception.value.status_code == HTTPStatus.FORBIDDEN
    assert exception.value.body == b'{"detail":"Forbidden."}'
