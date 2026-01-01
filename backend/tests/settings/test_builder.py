import json
from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from app.settings._base import BaseModelNoExtra
from app.settings._builder import SettingsBuilder
from app.settings._ssm_parameter import SsmParameter

_SSM_PREFIX = "prefix"


class SettingsGroupA(BaseModelNoExtra):
    foo: str
    para: SsmParameter[str]


class SettingsGroupB(BaseModelNoExtra):
    bar: int
    para_with_override: SsmParameter[str]


class Settings(BaseModelNoExtra):
    foo: str
    bar: int
    para: SsmParameter[str]
    para_with_override: SsmParameter[str]
    group_a: SettingsGroupA
    group_b: SettingsGroupB


@pytest.fixture
def raw_yaml() -> str:
    return """
    foo: foo
    bar: 1
    para: {}
    para_with_override:
        override: override_value
    group_a:
        foo: foo
        para: {}
    group_b:
        bar: 1
        para_with_override:
            override: override_value2
    """


@pytest.fixture
def dict_which_returns_key_as_value() -> MagicMock:
    mock_dict = MagicMock()
    mock_dict.__getitem__ = lambda _self, item: item
    return mock_dict


def mock_get_para(_self: SettingsBuilder, path: str, _region: str) -> str:
    """Fake version which returns the path as the value of the parameter."""
    return path


@pytest.fixture
def settings(raw_yaml: str) -> Generator[Settings]:
    builder = SettingsBuilder(Settings)
    with patch("app.settings._builder.SettingsBuilder._get_parameter", mock_get_para):
        yield builder.build(raw_yaml, lambda _: "unused", lambda _: _SSM_PREFIX)


def test_settings_built_correctly(settings: Settings) -> None:
    assert settings.model_dump_json() == json.dumps(
        {
            "foo": "foo",
            "bar": 1,
            "para": f"/{_SSM_PREFIX}/para",
            "para_with_override": "override_value",
            "group_a": {"foo": "foo", "para": f"/{_SSM_PREFIX}/group_a/para"},
            "group_b": {"bar": 1, "para_with_override": "override_value2"},
        },
        separators=(",", ":"),
    )


def test_pydantic_generic_metadata() -> None:
    """Test that the undocumented function __pydantic_generic_metadata we are using to extract the generic type works."""

    class Model[T](BaseModelNoExtra):
        foo: T

    model = Model[int](foo=1)
    assert model.__pydantic_generic_metadata__["args"] == (int,)
