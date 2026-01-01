import json

import pytest

from app.settings._ssm_parameter import (
    SsmParameter,
    _ParameterNotFetchedError,
)

_val = "test_value"


def test_override_bypasses_parameter_retrieval() -> None:
    para = SsmParameter[str](override=_val)
    assert para.value == _val


def test_raises_error_for_missing_parameter() -> None:
    para = SsmParameter[str]()
    with pytest.raises(_ParameterNotFetchedError):
        _ = para.value


def test_serialize() -> None:
    para = SsmParameter[str]()
    para._internal_value = _val
    assert para.model_dump_json() == json.dumps(para.value)


def test_serialize_with_override() -> None:
    para = SsmParameter[str](override=_val)
    assert para.model_dump_json() == json.dumps(para.value)
