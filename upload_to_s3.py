from pathlib import Path

from src.config import (
    AWS_REGION,
    S3_BUCKET_NAME,
    S3_RAW_PREFIX,
)
from src.storage.s3 import S3Storage


def main():
    local_file = Path("sample_data/customers.csv")

    if not local_file.exists():
        raise FileNotFoundError(
            f"Input file not found: {local_file}"
        )

    storage = S3Storage(
        bucket_name=S3_BUCKET_NAME,
        region_name=AWS_REGION,
    )

    s3_key = f"{S3_RAW_PREFIX}customers.csv"

    print(f"Uploading {local_file}...")
    print(f"Destination: s3://{S3_BUCKET_NAME}/{s3_key}")

    storage.upload_file(
        local_path=str(local_file),
        s3_key=s3_key,
    )

    print("SUCCESS: File uploaded to S3.")


if __name__ == "__main__":
    main()