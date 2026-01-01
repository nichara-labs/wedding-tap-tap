from typing import Annotated

from pydantic import Field

from app.settings._base import BaseModelNoExtra


class AwsS3Settings(BaseModelNoExtra):
    """S3 buckets used by the application."""

    app_bucket: Annotated[
        str,
        Field(description="Primary application bucket used for uploads and downloads"),
    ]


class AwsSettings(BaseModelNoExtra):
    """Settings related to AWS services e.g. S3, SageMaker, Bedrock."""

    region: Annotated[str, Field(description="AWS region used for all AWS services")]
    s3: AwsS3Settings
