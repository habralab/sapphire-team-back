import datetime
import uuid

import jwt
import pytest

from autotests.settings import AutotestsSettings


@pytest.fixture
def oleg_id() -> uuid.UUID:
    return uuid.UUID("e23dfa16-6d0f-4de2-a1b1-a42f8a5bfd94")


@pytest.fixture
def matvey_id() -> uuid.UUID:
    return uuid.UUID("07dcf2a2-0a9e-4674-a5d5-8103eddcf68e")


@pytest.fixture
def oleg_access_token(settings: AutotestsSettings, oleg_id: uuid.UUID) -> str:
    payload = {
        "user_id": str(oleg_id),
        "exp": int(datetime.datetime.now().timestamp()) + 24 * 3600,
    }
    return jwt.encode(payload, settings.jwt_access_token_private_key, algorithm="RS256")


@pytest.fixture
def matvey_access_token(settings: AutotestsSettings, matvey_id: uuid.UUID) -> str:
    payload = {
        "user_id": str(matvey_id),
        "exp": int(datetime.datetime.now().timestamp()) + 24 * 3600,
    }
    return jwt.encode(payload, settings.jwt_access_token_private_key, algorithm="RS256")
