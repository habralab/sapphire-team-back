from contextvars import ContextVar
from typing import Sequence, Type

import pytest

from sapphire.common.utils.functools import get_nested


@pytest.mark.parametrize(("structure", "key", "expected_result"), (
    (
        {"a": {"b": {"c": 1}}},
        ["a", "b", "c"],
        1,
    ),
    (
        {"a": 1, "b": 2, "c": 3},
        ["a", "b", "c"],
        None,
    ),
    (
        {1: {2: {3: "a"}}},
        ["1", "2", "3"],
        None,
    ),
))
def test_get_nested(structure: dict, key: Sequence, expected_result):
    result = get_nested(structure, *key)

    assert result == expected_result
