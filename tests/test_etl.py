import pandas as pd

from src.transformation.etl import transform


def test_transform_removes_duplicate_customers():

    data = pd.DataFrame(
        {
            "customer_id": [1, 1, 2],
            "name": [
                "Alice",
                "Alice",
                "Bob",
            ],
            "email": [
                "ALICE@example.com",
                "ALICE@example.com",
                "BOB@example.com",
            ],
            "country": [
                "Canada",
                "Canada",
                "USA",
            ],
            "signup_date": [
                "2025-01-01",
                "2025-01-01",
                "2025-02-01",
            ],
            "spend": [
                100,
                100,
                500,
            ],
        }
    )

    result = transform(data)

    assert len(result) == 2


def test_transform_normalizes_email():

    data = pd.DataFrame(
        {
            "customer_id": [1],
            "name": ["Alice"],
            "email": [
                " ALICE@EXAMPLE.COM "
            ],
            "country": ["Canada"],
            "signup_date": [
                "2025-01-01"
            ],
            "spend": [100],
        }
    )

    result = transform(data)

    assert (
        result.iloc[0]["email"]
        == "alice@example.com"
    )