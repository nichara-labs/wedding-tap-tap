from pydantic import BaseModel


class S3File(BaseModel):
    """An uploaded S3 file."""

    url: str
    """The S3 HTTP URL of the file."""
    key: str
    """S3 key of the file."""
    bucket: str
