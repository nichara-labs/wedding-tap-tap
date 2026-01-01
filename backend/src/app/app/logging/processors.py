import logging
from collections.abc import Callable

from asgi_correlation_id import correlation_id
from structlog.typing import EventDict


def drop_color_message_key(
    _: logging.Logger, __: str, event_dict: EventDict
) -> EventDict:
    """Uvicorn logs the message a second time in the extra `color_message`, but we don't need it. This processor drops the key from the event dict if it exists."""
    event_dict.pop("color_message", None)
    return event_dict


def add_correlation(_: logging.Logger, __: str, event_dict: EventDict) -> EventDict:
    """Add request id under the 'request_id' key for all log entries if it exists."""
    if request_id := correlation_id.get():
        event_dict["request_id"] = request_id
    return event_dict


def add_git_commit(
    commit_sha: str,
) -> Callable[[logging.Logger, str, EventDict], EventDict]:
    """Add git commit under the 'commit' key."""

    def process(_: logging.Logger, __: str, event_dict: EventDict) -> EventDict:
        event_dict["commit"] = commit_sha
        return event_dict

    return process
