from typing import TYPE_CHECKING, Literal, overload

import boto3

from app.utils import cache

if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_ssm import SSMClient
    from mypy_boto3_sts import STSClient

_Services = Literal["s3", "sts", "ssm"]


@overload
def get_client(service: Literal["s3"], region: str | None = None) -> S3Client: ...


@overload
def get_client(service: Literal["ssm"], region: str | None = None) -> SSMClient: ...


@overload
def get_client(service: Literal["sts"], region: str | None = None) -> STSClient: ...


def get_client(
    service: _Services,
    region: str | None = None,
):
    """
    Create a Boto3 Client for a specified AWS service, or fetch from cache.

    Notes:
    - If region is not specified, uses the region from the assumed AWS role.
    - Unlike Resources and Sessions, clients are generally [thread safe](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/clients.html#multithreading-or-multiprocessing-with-clients)
    """
    return _get_client(service, region)


@cache
def _get_client(
    service: _Services, region: str | None = None
) -> S3Client | STSClient | SSMClient:
    """Separated so that type checking works when using cache."""
    session = boto3.Session()
    return session.client(service, region_name=region)
