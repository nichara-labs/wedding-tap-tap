import pytest
from fastapi import FastAPI, Request
from httpx import AsyncClient

from app.app.dependencies import (
    RequiresLoginDep,
    SessionDataDep,
    SettingsDep,
)

pytestmark = pytest.mark.anyio


class TestRequiresLoginDep:
    async def test_requires_login_dep(self, app: FastAPI, client: AsyncClient) -> None:
        """Test that RequiresLoginDep really does require login."""
        app.add_api_route("/test", lambda: "test", dependencies=[RequiresLoginDep])
        resp = await client.get("/test")
        assert resp.status_code == 401


class TestSessionDataDep:
    async def test_user_not_logged_in(self, app: FastAPI, client: AsyncClient) -> None:
        """Test that SessionDataDep raises 403 when the user is not logged in"""

        async def _test(_: SessionDataDep) -> None: ...

        app.get("/test")(_test)
        resp = await client.get("/test")
        assert resp.status_code == 401

    async def test_invalid_session_data_403_message(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        """Test that SessinDataDep raises 401 with the correct message when the session data is invalid"""

        async def _set_invalid_session_data(r: Request, settings: SettingsDep) -> None:
            r.session[settings.session.user_data_key] = {"invalid": 123}

        async def _test(_: SessionDataDep) -> None: ...

        app.get("/set_invalid_session_data")(_set_invalid_session_data)
        app.get("/test")(_test)

        await client.get("/set_invalid_session_data")

        resp = await client.get("/test")
        assert resp.status_code == 401
        assert resp.json() == {"detail": "Session data is invalid", "status_code": 401}
