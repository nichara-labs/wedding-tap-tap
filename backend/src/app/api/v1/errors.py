from fastapi import APIRouter
from structlog.stdlib import get_logger

from app.api.utils import get_route_prefix
from app.app.dependencies import DbSessionDep
from app.db.repositories import ErrorRepo
from app.models import CreateErrorRequest, ErrorModel

_log = get_logger(__name__)

router = APIRouter(prefix=get_route_prefix(), tags=["errors"])


@router.post("")
async def errors(params: CreateErrorRequest, db: DbSessionDep) -> ErrorModel:
    """Client side errors should be POSTed here."""

    error = await ErrorRepo(db).from_request(params)
    return ErrorModel.from_error(error)
