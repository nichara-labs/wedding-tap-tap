import asyncio
import io
import re
import time
from pathlib import Path
from typing import Any, BinaryIO
from uuid import uuid4

from botocore.exceptions import ClientError
from starlette.concurrency import run_in_threadpool
from structlog.stdlib import get_logger

from app.services.aws.client import get_client
from app.services.utils import log_time

_logger = get_logger(__name__)


class S3DoesNotExistError(Exception): ...


class S3:
    """
    Abstraction around S3 objects with an async interface.

    Usage:

    ```python
    s3 = S3("ap-southeast-1")
    bucket = s3.bucket("my-bucket")
    await bucket.upload(Path("path/to/local/file.txt"), "remote/file.txt")
    ```

    Blocking calls from the boto3 library are run in a threadpool.
    """

    s3_uri_regex = r"s3://(?P<bucket>[^/]+)/(?P<key>.*)"
    s3_virtual_hosted_regex = (
        r"https://(?P<bucket>.*?).s3.(?P<region>.*?).amazonaws.com/(?P<key>.*)"
    )

    def __init__(self, bucket: str, key: str, region: str | None = None) -> None:
        self.region = region
        self.client = get_client("s3", region=region)
        self.bucket = bucket
        self.key = key

    @property
    def virtual_hosted_uri(self) -> str:
        return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{self.key}"

    @property
    def s3_uri(self) -> str:
        return f"s3://{self.bucket}/{self.key}"

    @classmethod
    def from_s3_uri(cls, uri: str, region: str | None = None) -> S3:
        """Create from an S3 URI (`s3://bucket/path/to/key`)."""

        match = re.match(cls.s3_uri_regex, uri)
        if not match:
            msg = f"Invalid S3 URI: {uri}"
            raise ValueError(msg)
        return S3(bucket=match.group("bucket"), key=match.group("key"), region=region)

    @classmethod
    def from_virtual_hosted_uri(cls, uri: str) -> S3:
        """
        Create from a [virtual-hosted-style URI](https://docs.aws.amazon.com/AmazonS3/latest/userguide/VirtualHosting.html#deprecated-global-endpoint) URI.

        The format is as follows: https://{bucket-name}.s3.{region-code}.amazonaws.com/{key-name}.
        """
        match = re.match(
            cls.s3_virtual_hosted_regex,
            uri,
        )
        if not match:
            msg = f"Invalid S3 URI: {uri}"
            raise ValueError(msg)
        return S3(
            bucket=match.group("bucket"),
            key=match.group("key"),
            region=match.group("region"),
        )

    @classmethod
    async def from_file_or_bytes(
        cls,
        path_or_bytes: Path | BinaryIO,
        bucket: str,
        key: str | None = None,
        region: str | None = None,
    ) -> S3:
        """
        Upload file or bytes to S3 and return the S3 object.

        Args:
            path_or_bytes: Path to file or bytes to upload.
            bucket: Name of S3 bucket to upload to.
            key: S3 key to upload to. If not provided a random uuid will be generated. Invalid characters are replaced.
            region: AWS region the bucket is in.
        """
        client = get_client("s3", region)
        s3_key = cls._replace_invalid_characters(key) if key else uuid4().hex

        _log: dict[str, Any] = {
            "s3_file": path_or_bytes.as_posix()
            if isinstance(path_or_bytes, Path)
            else "<bytes>",
            "s3_bucket": bucket,
            "s3_key": s3_key,
        }

        try:
            with log_time(_logger.info, "Uploading file/bytes to S3"):
                if isinstance(path_or_bytes, Path):
                    await run_in_threadpool(
                        client.upload_file, path_or_bytes.as_posix(), bucket, s3_key
                    )
                else:
                    await run_in_threadpool(
                        client.upload_fileobj,
                        Fileobj=path_or_bytes,
                        Bucket=bucket,
                        Key=s3_key,
                    )
        except Exception:
            _logger.exception("Failed to upload file to S3", **_log)
            raise

        _logger.info("Uploaded file successfully", **_log)

        return cls(key=s3_key, bucket=bucket, region=region)

    @classmethod
    def is_valid_s3_uri(cls, uri: str) -> bool:
        return bool(re.fullmatch(cls.s3_uri_regex, uri))

    @classmethod
    def is_valid_virtual_hosted_uri(cls, uri: str) -> bool:
        return bool(re.fullmatch(cls.s3_virtual_hosted_regex, uri))

    async def download_to_file(self, path: Path) -> None:
        """Download the S3 object to a file."""
        await run_in_threadpool(
            self.client.download_file,
            Bucket=self.bucket,
            Key=self.key,
            Filename=path.as_posix(),
        )
        _logger.info(
            "Downloaded S3 file successfully",
            key=self.key,
            bucket=self.bucket,
            dl_path=path,
        )

    async def download(self) -> io.BytesIO:
        """Download this S3 object to bytes."""
        _io = io.BytesIO()
        await run_in_threadpool(
            self.client.download_fileobj, Bucket=self.bucket, Key=self.key, Fileobj=_io
        )
        _io.seek(0)
        return _io

    async def exists(self) -> bool:
        """Check if this S3 object exists."""
        try:
            await run_in_threadpool(
                self.client.head_object,
                Bucket=self.bucket,
                Key=self.key,
            )
        except ClientError:
            return False
        else:
            return True

    async def wait_until_exists(self, timeout_s: int = 60, interval_s: int = 1) -> bool:
        """Wait until the S3 object this points to exists, or raises. Returns True if the object exists within the timeout."""
        now = time.time()
        while not (exists := await self.exists()):
            if time.time() - now >= timeout_s:
                msg = f"Failed to fetch {self.bucket=}, {self.key=}"
                raise S3DoesNotExistError(msg)
            await asyncio.sleep(interval_s)
        return exists

    async def delete(self) -> None:
        """Delete the S3 object."""
        await run_in_threadpool(
            self.client.delete_object, Bucket=self.bucket, Key=self.key
        )
        _logger.debug(
            "Deleted S3 object key=%s bucket=%s", key=self.key, bucket=self.bucket
        )

    @classmethod
    def _replace_invalid_characters(cls, key: str) -> str:
        """Replace characters that would be invalid for an S3 key."""
        return key.replace("/", "_")
