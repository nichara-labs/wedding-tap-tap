from abc import ABC
from typing import Annotated

from pydantic import Field

from app.settings._base import BaseModelNoExtra


class BaseProviderSettings(ABC, BaseModelNoExtra):
    """
    Base configuration for an OAuth 2.0 provider, based on standard parameters for the authorization request (https://datatracker.ietf.org/doc/html/rfc6749#section-4.1.1).

    Note: due to significant differences between providers' implementations of the protocol (e.g. different certificate assertion parameters, with Apple using `client_secret` while Entra uses `client_assertion`), it's not possible to have a base class that covers all parameters.
    """

    name: str
    client_id: str
    configuration_endpoint: Annotated[
        str,
        Field(
            description=" OpenID Provider Configuration endpoint used to obtain the authorization and token endpoints. E.g. `https://accounts.google.com/.well-known/openid-configuration`."
        ),
    ]
