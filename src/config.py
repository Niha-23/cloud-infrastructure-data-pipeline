import os

from dotenv import load_dotenv

load_dotenv()


AWS_REGION = os.getenv(
    "AWS_REGION",
    "ca-central-1",
)

S3_BUCKET_NAME = os.getenv(
    "S3_BUCKET_NAME",
)

MYSQL_HOST = os.getenv(
    "MYSQL_HOST",
    "localhost",
)

MYSQL_PORT = int(
    os.getenv(
        "MYSQL_PORT",
        "3306",
    )
)

MYSQL_DATABASE = os.getenv(
    "MYSQL_DATABASE",
    "analytics",
)

MYSQL_USER = os.getenv(
    "MYSQL_USER",
    "analytics_user",
)

MYSQL_PASSWORD = os.getenv(
    "MYSQL_PASSWORD",
)