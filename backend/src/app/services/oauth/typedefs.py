from pydantic import BaseModel


class UserInfo(BaseModel):
    """User information from the provider."""

    sub: str
    email: str
    email_verified: bool
    name: str
    picture: str | None = None
