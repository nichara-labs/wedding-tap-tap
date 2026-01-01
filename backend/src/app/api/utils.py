import inspect
from functools import reduce
from urllib.parse import urljoin

from app.settings import Settings


def make_uri(settings: Settings, path: str) -> str:
    """Construct a URI using the given path, e.g. given `/path` -> `http://localhost:8000/path`."""
    return reduce(
        urljoin,
        [
            str(settings.app.backend_url),
            # Trailing slash is necessary for urljoin to interpret as a directory
            f"{settings.app.api_prefix.strip('/')}/",
            # Leading slashes cause urljoin to reset to root
            path.strip("/"),
        ],
    )


def get_route_prefix(until: str = "api") -> str:
    """Derive a URL route prefix from the calling module's path relative to a specified ancestor directory.

    Constructs a URL path prefix by finding the specified ancestor directory in the module path and joining all subsequent path components with forward slashes. The specified ancestor directory is excluded from the resulting path.

    Args:
        until (str): The ancestor directory name to start building the path from (exclusive).

    Returns:
        str: The URL route prefix starting with "/", or an empty string if no path components exist after the specified ancestor. Underscores in path components are replaced with hyphens.

    Raises:
        RuntimeError: If unable to access frame information, or if the specified ancestor directory is not found in the module path.

    Examples:
        For a module at path `.../api/v1/users.py`:
        >>> get_route_prefix(until="api")
        "/v1/users"
        >>> get_route_prefix(until="v1")
        "/users"

    Notes:
        The function uses frame inspection to determine the calling module's path, so it should be called directly from the module where the route prefix is needed.
    """
    # Get the name of the calling module
    frame = inspect.currentframe()
    if frame is None:
        msg = "Could not get current frame."
        raise RuntimeError(msg)

    parent_frame = frame.f_back
    if parent_frame is None:
        msg = "Could not get parent frame."
        raise RuntimeError(msg)

    try:
        module = inspect.getmodule(parent_frame)
        if module is None:
            msg = "Could not get module from parent frame."
            raise RuntimeError(msg)

        # Split the module path and build the route prefix
        parts = module.__name__.split(".")
        try:
            api_index = parts.index(until)
            route_parts = parts[api_index + 1 :]
            url = "/" + "/".join(route_parts) if route_parts else ""
            return url.replace("_", "-")
        except ValueError as e:
            msg = f"Module path does not contain {until=} component."
            raise RuntimeError(msg) from e

    finally:
        # Properly clean up frame references to prevent memory leaks
        del frame
        del parent_frame
