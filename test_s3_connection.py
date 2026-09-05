from src.storage.s3 import S3Storage
from src.config import (
    AWS_REGION,
    S3_BUCKET_NAME,
)


def main():
    storage = S3Storage(
        bucket_name=S3_BUCKET_NAME,
        region_name=AWS_REGION,
    )

    print("Testing connection to S3...")
    print(f"Bucket: {S3_BUCKET_NAME}")
    print(f"Region: {AWS_REGION}")

    test_key = "raw/customers.csv"

    exists = storage.file_exists(test_key)

    if exists:
        print(f"SUCCESS: {test_key} already exists in S3.")
    else:
        print(f"SUCCESS: Connected to S3, but {test_key} does not exist yet.")


if __name__ == "__main__":
    main()