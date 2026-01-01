import io
import uuid
from collections.abc import AsyncGenerator, Generator
from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest
from moto import mock_aws

from app.services.aws.client import get_client
from app.services.aws.s3 import S3, S3DoesNotExistError
from app.settings import Settings

DATA = b"test data"
TEST_KEY = "test-key"

pytestmark = pytest.mark.anyio


@pytest.fixture(autouse=True)
def create_bucket(settings: Settings) -> Generator[None]:
    """Creates the bucket for the tests."""
    with mock_aws():
        client = get_client("s3")
        client.create_bucket(Bucket=settings.aws.s3.app_bucket)
        yield


@pytest.fixture
async def s3(settings: Settings) -> AsyncGenerator[S3]:
    """Prepares an S3 object for testing"""
    with mock_aws():
        _io = io.BytesIO(DATA)
        s3 = await S3.from_file_or_bytes(
            _io, bucket=settings.aws.s3.app_bucket, key=TEST_KEY
        )
        yield s3
        await s3.delete()


class TestS3:
    def test_from_s3_uri(self) -> None:
        """Tests for slashes in the key"""
        uri = "s3://some-bucket/path/to/key"
        s3 = S3.from_s3_uri(uri)
        assert s3.bucket == "some-bucket"
        assert s3.key == "path/to/key"

    def test_from_virtual_hosted_uri(self) -> None:
        """Tests for slashes in the key"""
        uri = "https://bucket-name.s3.region-code.amazonaws.com/path/to/key"
        s3 = S3.from_virtual_hosted_uri(uri)
        assert s3.bucket == "bucket-name"
        assert s3.key == "path/to/key"
        assert s3.region == "region-code"

    async def test_upload_from_bytes(self, s3: S3) -> None:
        _io = await s3.download()
        _io.seek(0)
        assert _io.read() == DATA

    async def test_upload_from_file_and_download_to_bytes(
        self, settings: Settings
    ) -> None:
        with mock_aws():
            key = "test_upload_from_file"
            with NamedTemporaryFile() as f:
                f.write(DATA)
                f.flush()
                # Read from the filename so we are using a different file descriptor
                # So we don't need to seek(0), to simulate opening the file
                s3 = await S3.from_file_or_bytes(
                    Path(f.name), bucket=settings.aws.s3.app_bucket, key=key
                )
            assert await s3.exists()
            _io = await s3.download()
            _io.seek(0)
            assert _io.read() == DATA
            await s3.delete()

    async def test_deleted_and_exists(self, s3: S3) -> None:
        await s3.delete()
        assert not await s3.exists()

    async def test_download_to_file(self, s3: S3) -> None:
        temp_name = f"/tmp/{uuid.uuid4().hex}"  # noqa: S108
        await s3.download_to_file(Path(temp_name))
        assert Path(temp_name).read_bytes() == DATA

    async def test_download_is_bytes_io(self, s3: S3) -> None:
        """So we can use .getvalue() in downstream functions without seeking."""
        _io = await s3.download()
        assert _io.getvalue() == DATA

    async def test_wait_until_exists_already_exists(self, s3: S3) -> None:
        assert await s3.wait_until_exists()

    async def test_wait_until_exists_doesnt_exist(self, settings: Settings) -> None:
        s3 = S3(settings.aws.s3.app_bucket, key="does-not-exist")
        with pytest.raises(S3DoesNotExistError):
            await s3.wait_until_exists(1)
