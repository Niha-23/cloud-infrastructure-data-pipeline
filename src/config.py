import os

from dotenv import load_dotenv

load_dotenv()


AWS_REGION = os.getenv(
    "AWS_REGION",
    "us-east-2"
)

S3_BUCKET_NAME = os.getenv(
    "S3_BUCKET_NAME",
    "cloud-infrastructure-data-pipeline-niharika"
)

S3_RAW_PREFIX = os.getenv(
    "S3_RAW_PREFIX",
    "raw/"
)

S3_PROCESSED_PREFIX = os.getenv(
    "S3_PROCESSED_PREFIX",
    "processed/"
)