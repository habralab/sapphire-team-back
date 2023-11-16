import uuid
from http import HTTPStatus
from typing import Type

import pytest
from faker import Faker

from autotests.clients.rest.exceptions import ResponseException
from autotests.clients.rest.messenger.client import MessengerRestClient
from autotests.utils import Empty


@pytest.mark.parametrize("client", (
    pytest.lazy_fixture("oleg_messenger_rest_client"),
    pytest.lazy_fixture("oleg_activated_messenger_rest_client"),
    pytest.lazy_fixture("matvey_messenger_rest_client"),
    pytest.lazy_fixture("matvey_activated_messenger_rest_client"),
))
@pytest.mark.parametrize("members", (
    {uuid.uuid4(), uuid.uuid4()},
    Empty,
))
@pytest.mark.asyncio
async def test_get_chats(client: MessengerRestClient, members: set[uuid.UUID] | Type[Empty]):
    await client.get_chats(members=members)


@pytest.mark.parametrize("members", (
    {uuid.uuid4(), uuid.uuid4()},
    Empty,
))
@pytest.mark.asyncio
async def test_get_chats_not_authenticated(
        messenger_rest_client: MessengerRestClient,
        members: set[uuid.UUID] | Type[Empty],
):
    with pytest.raises(ResponseException) as exception:
        await messenger_rest_client.get_chats(members=members)

    assert exception.value.status_code == HTTPStatus.UNAUTHORIZED
    assert exception.value.body == b'{"detail":"Not authenticated."}'


@pytest.mark.parametrize("client", (
    pytest.lazy_fixture("oleg_messenger_rest_client"),
    pytest.lazy_fixture("oleg_activated_messenger_rest_client"),
    pytest.lazy_fixture("matvey_messenger_rest_client"),
    pytest.lazy_fixture("matvey_activated_messenger_rest_client"),
))
@pytest.mark.asyncio
async def test_get_chat(
        chat_id: uuid.UUID,
        oleg_id: uuid.UUID,
        matvey_id: uuid.UUID,
        client: MessengerRestClient,
):
    chat = await client.get_chat(chat_id=chat_id)

    assert chat.id == chat_id
    assert chat.is_personal is True
    assert set(chat.members) == {oleg_id, matvey_id}


@pytest.mark.asyncio
async def test_get_chat_not_authenticated(
        chat_id: uuid.UUID,
        messenger_rest_client: MessengerRestClient,
):
    with pytest.raises(ResponseException) as exception:
        await messenger_rest_client.get_chat(chat_id=chat_id)

    assert exception.value.status_code == HTTPStatus.UNAUTHORIZED
    assert exception.value.body == b'{"detail":"Not authenticated."}'


@pytest.mark.parametrize("client", (
    pytest.lazy_fixture("oleg_messenger_rest_client"),
    pytest.lazy_fixture("oleg_activated_messenger_rest_client"),
    pytest.lazy_fixture("matvey_messenger_rest_client"),
    pytest.lazy_fixture("matvey_activated_messenger_rest_client"),
    pytest.lazy_fixture("random_messenger_rest_client"),
))
@pytest.mark.asyncio
async def test_get_chat_not_found(client: MessengerRestClient):
    with pytest.raises(ResponseException) as exception:
        await client.get_chat(chat_id=uuid.uuid4())

    assert exception.value.status_code == HTTPStatus.NOT_FOUND
    assert exception.value.body == b'{"detail":"Not found."}'


@pytest.mark.asyncio
async def test_get_chat_forbidden(
        chat_id: uuid.UUID,
        random_messenger_rest_client: MessengerRestClient,
):
    with pytest.raises(ResponseException) as exception:
        await random_messenger_rest_client.get_chat(chat_id=chat_id)

    assert exception.value.status_code == HTTPStatus.FORBIDDEN
    assert exception.value.body == b'{"detail":"Forbidden."}'


@pytest.mark.parametrize("client", (
    pytest.lazy_fixture("oleg_messenger_rest_client"),
    pytest.lazy_fixture("oleg_activated_messenger_rest_client"),
    pytest.lazy_fixture("matvey_messenger_rest_client"),
    pytest.lazy_fixture("matvey_activated_messenger_rest_client"),
))
@pytest.mark.asyncio
async def test_get_chat_messages(chat_id: uuid.UUID, client: MessengerRestClient):
    messages = await client.get_chat_messages(chat_id=chat_id)

    for message in messages.data:
        assert message.chat_id == chat_id


@pytest.mark.asyncio
async def test_get_chat_messages_not_authenticated(
        chat_id: uuid.UUID,
        messenger_rest_client: MessengerRestClient,
):
    with pytest.raises(ResponseException) as exception:
        await messenger_rest_client.get_chat_messages(chat_id=chat_id)

    assert exception.value.status_code == HTTPStatus.UNAUTHORIZED
    assert exception.value.body == b'{"detail":"Not authenticated."}'


@pytest.mark.parametrize("client", (
    pytest.lazy_fixture("oleg_messenger_rest_client"),
    pytest.lazy_fixture("oleg_activated_messenger_rest_client"),
    pytest.lazy_fixture("matvey_messenger_rest_client"),
    pytest.lazy_fixture("matvey_activated_messenger_rest_client"),
    pytest.lazy_fixture("random_messenger_rest_client"),
))
@pytest.mark.asyncio
async def test_get_chat_messages_not_found(client: MessengerRestClient):
    with pytest.raises(ResponseException) as exception:
        await client.get_chat_messages(chat_id=uuid.uuid4())

    assert exception.value.status_code == HTTPStatus.NOT_FOUND
    assert exception.value.body == b'{"detail":"Not found."}'


@pytest.mark.asyncio
async def test_get_chat_messages_forbidden(
        chat_id: uuid.UUID,
        random_messenger_rest_client: MessengerRestClient,
):
    with pytest.raises(ResponseException) as exception:
        await random_messenger_rest_client.get_chat_messages(chat_id=chat_id)

    assert exception.value.status_code == HTTPStatus.FORBIDDEN
    assert exception.value.body == b'{"detail":"Forbidden."}'


@pytest.mark.parametrize(("user_id", "client"), (
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("oleg_messenger_rest_client")),
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("oleg_activated_messenger_rest_client")),
    (pytest.lazy_fixture("matvey_id"), pytest.lazy_fixture("matvey_messenger_rest_client")),
    (
        pytest.lazy_fixture("matvey_id"),
        pytest.lazy_fixture("matvey_activated_messenger_rest_client"),
    ),
))
@pytest.mark.asyncio
async def test_create_chat_message(
        faker: Faker,
        chat_id: uuid.UUID,
        user_id: uuid.UUID,
        client: MessengerRestClient,
):
    text = faker.text()

    message = await client.create_chat_message(chat_id=chat_id, text=text)

    assert message.chat_id == chat_id
    assert message.user_id == user_id
    assert message.text == text


@pytest.mark.asyncio
async def test_create_chat_message_not_authenticated(
        faker: Faker,
        chat_id: uuid.UUID,
        messenger_rest_client: MessengerRestClient,
):
    with pytest.raises(ResponseException) as exception:
        await messenger_rest_client.create_chat_message(chat_id=chat_id, text=faker.text())

    assert exception.value.status_code == HTTPStatus.UNAUTHORIZED
    assert exception.value.body == b'{"detail":"Not authenticated."}'


@pytest.mark.parametrize("client", (
    pytest.lazy_fixture("oleg_messenger_rest_client"),
    pytest.lazy_fixture("oleg_activated_messenger_rest_client"),
    pytest.lazy_fixture("matvey_messenger_rest_client"),
    pytest.lazy_fixture("matvey_activated_messenger_rest_client"),
    pytest.lazy_fixture("random_messenger_rest_client"),
))
@pytest.mark.asyncio
async def test_create_chat_message_not_found(faker: Faker, client: MessengerRestClient):
    with pytest.raises(ResponseException) as exception:
        await client.create_chat_message(chat_id=uuid.uuid4(), text=faker.text())

    assert exception.value.status_code == HTTPStatus.NOT_FOUND
    assert exception.value.body == b'{"detail":"Not found."}'


@pytest.mark.asyncio
async def test_create_chat_message_forbidden(
        faker: Faker,
        chat_id: uuid.UUID,
        random_messenger_rest_client: MessengerRestClient,
):
    with pytest.raises(ResponseException) as exception:
        await random_messenger_rest_client.create_chat_message(chat_id=chat_id, text=faker.text())

    assert exception.value.status_code == HTTPStatus.FORBIDDEN
    assert exception.value.body == b'{"detail":"Forbidden."}'
