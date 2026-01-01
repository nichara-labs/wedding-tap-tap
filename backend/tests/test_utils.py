from unittest.mock import Mock

from pydantic import BaseModel

from app.utils import cache, model_apply


class ContainsTarget(BaseModel):
    field1: str
    field2: Target


class ContainsTarget2(BaseModel):
    field1: str
    field2: Target
    field3: Other


class Target(BaseModel):
    target_field: str = "unset"


class Other(BaseModel):
    field3: str


class ModelForTesting(BaseModel):
    field1: str
    field2: ContainsTarget2
    field3: Target


def func_to_apply(target: Target) -> None:
    target.target_field = "set"


def test_model_apply() -> None:
    """Check that model_apply works recursively on nested models."""
    model = ModelForTesting(
        field1="test",
        field2=ContainsTarget2(
            field1="test",
            field2=Target(),
            field3=Other(field3="test"),
        ),
        field3=Target(),
    )
    model_apply(model, Target, func_to_apply)
    assert model.field2.field2.target_field == "set"
    assert model.field3.target_field == "set"


def test_cache() -> None:
    """Check that we are really caching."""
    mock = Mock()

    @cache
    def func_to_cache() -> None:
        mock()

    [func_to_cache() for _ in range(10)]

    mock.assert_called_once()
