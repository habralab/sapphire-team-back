import uuid

import pytest


@pytest.fixture
def user_1_id() -> uuid.UUID:
    return uuid.UUID()


@pytest.fixture
def user_2_id() -> uuid.UUID:
    return uuid.UUID()
