from typing import Type, Any

import pytest
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
