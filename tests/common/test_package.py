from unittest.mock import mock_open, patch

import pytest

from sapphire.common.package import get_version

PYPROJECT_CONTENT_TEMPLATE = """
[tool.poetry]
version = "{version}"
"""
PYPROJECT_CONTENT_WITHOUT_VERSION = """
[tool.poetry]
name = "any-name"
"""


@pytest.mark.parametrize("version", (
    "0.0.0",
    "1.2.3",
))
def test_get_version(version: str):
    content = PYPROJECT_CONTENT_TEMPLATE.format(version=version).encode()
    with patch("sapphire.common.package.open", new_callable=mock_open, read_data=content):
        actual_version = get_version()

    assert actual_version == version


def test_get_version_without_version():
    content = PYPROJECT_CONTENT_WITHOUT_VERSION.encode()
    with patch("sapphire.common.package.open", new_callable=mock_open, read_data=content):
        actual_version = get_version()

    assert actual_version is None
