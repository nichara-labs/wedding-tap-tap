from typing import Annotated

from pydantic import StringConstraints

PathPrefix = Annotated[str, StringConstraints(pattern=r"^(/.*[^/])?$")]
"""Validation type for a URL path prefix that can be a blank string or must start with a forward slash (/) and not end with one, e.g. '/api', '/v1/users'"""

NoLeadingTrailingSlashes = Annotated[str, StringConstraints(pattern=r"^[^/].*[^/]$")]
