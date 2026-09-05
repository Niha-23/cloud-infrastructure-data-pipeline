import pandas as pd
import pytest

from src.ingestion.csv_ingestion import load_csv


def test_load_csv_success(tmp_path):
    csv_file = tmp_path / "customers.csv"

    csv_file.write_text(
        "customer_id,name,email\n"
        "1,John,john@example.com\n"
        "2,Jane,jane@example.com\n"
    )

    dataframe = load_csv(str(csv_file))

    assert isinstance(dataframe, pd.DataFrame)
    assert len(dataframe) == 2
    assert list(dataframe.columns) == [
        "customer_id",
        "name",
        "email",
    ]


def test_load_csv_file_not_found(tmp_path):
    missing_file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError, match="Input file not found"):
        load_csv(str(missing_file))