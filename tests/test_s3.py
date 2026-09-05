from pathlib import Path
from unittest.mock import MagicMock

from src.storage.s3 import S3Storage


BUCKET_NAME = "test-bucket"


def test_s3_connection():
    s3 = S3Storage(BUCKET_NAME)

    s3.s3_client.list_objects_v2 = MagicMock(
        return_value={
            "Contents": []
        }
    )

    response = s3.s3_client.list_objects_v2(
        Bucket=BUCKET_NAME,
        MaxKeys=1
    )

    assert response["Contents"] == []

    s3.s3_client.list_objects_v2.assert_called_once_with(
        Bucket=BUCKET_NAME,
        MaxKeys=1
    )


def test_raw_customers_file_exists():
    s3 = S3Storage(BUCKET_NAME)

    s3.s3_client.head_object = MagicMock(
        return_value={}
    )

    assert s3.file_exists("raw/customers.csv")

    s3.s3_client.head_object.assert_called_once_with(
        Bucket=BUCKET_NAME,
        Key="raw/customers.csv"
    )


def test_download_raw_customers(tmp_path):
    s3 = S3Storage(BUCKET_NAME)

    local_file = Path(tmp_path) / "customers.csv"

    def fake_download(
        bucket,
        key,
        filename
    ):
        Path(filename).write_text(
            "customer_id,name,email\n"
            "1,Test,test@example.com\n"
        )

    s3.s3_client.download_file = MagicMock(
        side_effect=fake_download
    )

    s3.download_file(
        "raw/customers.csv",
        str(local_file)
    )

    assert local_file.exists()

    assert "test@example.com" in local_file.read_text()

    s3.s3_client.download_file.assert_called_once_with(
        BUCKET_NAME,
        "raw/customers.csv",
        str(local_file)
    )