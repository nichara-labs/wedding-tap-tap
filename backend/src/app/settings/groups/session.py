from textwrap import dedent
from typing import Annotated, Literal

from pydantic import Field, SecretStr

from app.settings._base import BaseModelNoExtra
from app.settings._ssm_parameter import SsmParameter


class SessionSettings(BaseModelNoExtra):
    signing_key: Annotated[
        SsmParameter[SecretStr], Field(description="Signing key for session cookies")
    ]
    max_age: Annotated[
        int, Field(description="Max age of the session cookie, in seconds")
    ] = 60 * 60 * 24 * 7  # 1 week
    user_data_key: Annotated[
        str, Field(description="Key in session data where user data in stored")
    ] = "user-data"

    cookie_name: Annotated[
        str,
        Field(
            description=dedent(
                """
                Name of the session cookie.

                Note: When developing locally on Chrome, do not add __Host- or __Secure- as a prefix, as Chrome does not treat localhost as a secure origin.

                __Host- prefixed cookies are strictly host-scoped, require HTTPS, secure flag, and path=/. They cannot have a domain specified. This provides more security over the Domain attribute.

                For details: https://datatracker.ietf.org/doc/html/draft-ietf-httpbis-rfc6265bis#section-4.1.3.2
                """
            )
        ),
    ] = "__Host-session"

    same_site: Annotated[
        Literal["lax", "none"],
        Field(
            description="SameSite attribute of the session cookie. Must be 'lax' or 'none' for the client to send the session cookie (containing 'state') during the OAuth redirect."
        ),
    ] = "lax"

    secure: Annotated[
        bool, Field(description="Secure attribute of the session cookie")
    ] = True
