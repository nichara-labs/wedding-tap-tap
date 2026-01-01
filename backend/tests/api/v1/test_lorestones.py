from datetime import datetime

import pytest

from app.models import LorestoneDailyClaimResponse
from tests.fixtures.common import ClientWithLogin

pytestmark = pytest.mark.anyio


@pytest.fixture
def lorestones_base_url() -> str:
    return "/v1/lorestones"


async def test_balance_defaults_to_zero(
    client_with_login: ClientWithLogin,
    lorestones_base_url: str,
) -> None:
    client = client_with_login["client"]

    response = await client.get(lorestones_base_url)
    assert response.status_code == 200
    assert response.json() == {"balance": 0}


async def test_daily_claim_awards_once_per_day(
    client_with_login: ClientWithLogin,
    lorestones_base_url: str,
) -> None:
    client = client_with_login["client"]

    claim_response = await client.post(lorestones_base_url + "/daily")
    assert claim_response.status_code == 200

    payload = LorestoneDailyClaimResponse.model_validate(claim_response.json())
    assert payload.claimed_amount == 100
    assert payload.balance == 100
    assert payload.claimed_at <= payload.next_claim_at
    assert isinstance(payload.claimed_at, datetime)

    second_attempt = await client.post(lorestones_base_url + "/daily")
    assert second_attempt.status_code == 429

    balance_after = await client.get(lorestones_base_url)
    assert balance_after.status_code == 200
    assert balance_after.json() == {"balance": 100}
