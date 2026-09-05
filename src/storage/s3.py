import boto3
from botocore.exceptions import ClientError

from src.logger import get_logger


logger = get_logger(__name__)


class S3Storage:
    """Handles file operations with Amazon S3."""

    def __init__(
        self,
        bucket_name: str,
        region_name: str = "us-east-2"
    ):
        self.bucket_name = bucket_name

        self.s3_client = boto3.client(
            "s3",
            region_name=region_name
        )

    def download_file(
        self,
        s3_key: str,
        local_path: str
    ) -> None:
        """Download a file from S3."""

        try:
            self.s3_client.download_file(
                self.bucket_name,
                s3_key,
                local_path
            )

            logger.info(
                "Downloaded s3://%s/%s to %s",
                self.bucket_name,
                s3_key,
                local_path
            )

        except ClientError:
            logger.exception(
                "Failed to download s3://%s/%s",
                self.bucket_name,
                s3_key
            )
            raise

    def upload_file(
        self,
        local_path: str,
        s3_key: str
    ) -> None:
        """Upload a file to S3."""

        try:
            self.s3_client.upload_file(
                local_path,
                self.bucket_name,
                s3_key
            )

            logger.info(
                "Uploaded %s to s3://%s/%s",
                local_path,
                self.bucket_name,
                s3_key
            )

        except ClientError:
            logger.exception(
                "Failed to upload %s to s3://%s/%s",
                local_path,
                self.bucket_name,
                s3_key
            )
            raise

    def file_exists(self, s3_key: str) -> bool:
        """Check whether a file exists in S3."""

        try:
            self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )

            return True

        except ClientError as error:
            error_code = error.response.get("Error", {}).get("Code")

            if error_code == "404":
                return False

            raise