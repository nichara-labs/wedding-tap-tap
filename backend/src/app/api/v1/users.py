from fastapi import APIRouter

from app.api.utils import get_route_prefix

router = APIRouter(prefix=get_route_prefix(), tags=["users"])
