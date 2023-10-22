import datetime
import uuid

import jwt
import pytest

from autotests.settings import AutotestsSettings


@pytest.fixture
def user_1_id() -> uuid.UUID:
    return uuid.UUID()


@pytest.fixture
def user_2_id() -> uuid.UUID:
    return uuid.UUID()


@pytest.fixture
def user_1_access_token(settings: AutotestsSettings, user_1_id: uuid.UUID) -> str:
    payload = {
        "user_id": str(user_1_id),
        "exp": int(datetime.datetime.now().timestamp()) + 24 * 3600,
    }
    return jwt.encode(payload, settings.jwt_access_token_private_key, algorithm="RS256")


@pytest.fixture
def user_2_access_token(settings: AutotestsSettings, user_2_id: uuid.UUID) -> str:
    payload = {
        "user_id": str(user_2_id),
        "exp": int(datetime.datetime.now().timestamp()) + 24 * 3600,
    }
    return jwt.encode(payload, settings.jwt_access_token_private_key, algorithm="RS256")

