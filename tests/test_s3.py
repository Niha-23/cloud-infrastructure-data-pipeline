from pathlib import Path

from src.storage.s3 import S3Storage


BUCKET_NAME = "cloud-infrastructure-data-pipeline-niharika"


def test_s3_connection():
    s3 = S3Storage(BUCKET_NAME)

    response = s3.s3_client.list_objects_v2(
        Bucket=BUCKET_NAME,
        MaxKeys=1
    )

    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200


def test_raw_customers_file_exists():
    s3 = S3Storage(BUCKET_NAME)

    assert s3.file_exists("raw/customers.csv")


def test_download_raw_customers(tmp_path):
    s3 = S3Storage(BUCKET_NAME)

    local_file = Path(tmp_path) / "customers.csv"

    s3.download_file(
        "raw/customers.csv",
        str(local_file)
    )

    assert local_file.exists()
    assert local_file.stat().st_size > 0