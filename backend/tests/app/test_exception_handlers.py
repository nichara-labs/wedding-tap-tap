import pytest
from httpx import AsyncClient

from app.db.repositories import ErrorRepo

pytestmark = pytest.mark.anyio


class TestGlobalExceptionHandler:
    @pytest.fixture(autouse=True)
    def _fixtures(
        self,
        client: AsyncClient,
        error_endpoint: str,
        error_repo: ErrorRepo,
    ) -> None:
        self.client = client
        self.error_endpoint = error_endpoint
        self.error_repo = error_repo

    async def test_errors_logged_to_db(self) -> None:
        """Assert that the global exception handler logs backend errors to the database."""
        with pytest.raises(ValueError, match="Test error"):
            await self.client.post(self.error_endpoint)
        errors = await self.error_repo.get_by_field_multiple(lambda _: [])
        assert len(errors) == 1
        assert errors[0].message == "ValueError('Test error')"
