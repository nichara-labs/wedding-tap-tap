import json

import pytest
from httpx import AsyncClient

from app.db.repositories import ErrorRepo

pytestmark = pytest.mark.anyio


@pytest.fixture
def error_url() -> str:
    return "/v1/errors"


async def test_client_errors_saved_to_db(
    client: AsyncClient, error_url: str, error_repo: ErrorRepo
) -> None:
    test_error = "This is an error message"
    meta = json.dumps({"key": "value"})
    response = await client.post(error_url, json={"message": test_error, "meta": meta})
    assert response.status_code == 200
    errors = await error_repo.get_by_field_multiple(lambda _: [])
    assert len(errors) == 1
    assert errors[0].message == test_error
    assert errors[0].meta == meta
    assert errors[0].source == "frontend"
