from fastapi import APIRouter
from pydantic import EmailStr
from structlog.stdlib import get_logger

from app.api.utils import get_route_prefix
from app.app.dependencies import DbSessionDep
from app.db.repositories import EmailRepo
from app.db.schema import Email

_log = get_logger(__name__)

router = APIRouter(prefix=get_route_prefix(), tags=["email"])


@router.post("/subscribe")
async def subscribe(email: EmailStr, db: DbSessionDep) -> None:
    """Subscribe user to mailing list."""

    emails = EmailRepo(db)
    await emails.create_or_update(Email(email=email))
