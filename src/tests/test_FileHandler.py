import pytest
import pandas as pd
from unittest import mock
from utils.FileHandler import FileHandler, DataFormatError


def test_load_data_success():
    # Mock the pandas read_csv method to return a DataFrame
    mock_data = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    with mock.patch("pandas.read_csv", return_value=mock_data):
        file_handler = FileHandler("dummy_path.csv")
        pd.testing.assert_frame_equal(file_handler.data, mock_data)


def test_load_data_file_not_found():
    # Mock the pandas read_csv method to raise a FileNotFoundError
    with mock.patch("pandas.read_csv", side_effect=FileNotFoundError):
        with pytest.raises(
            DataFormatError, match="Error loading data from dummy_path.csv: "
        ):
            FileHandler("dummy_path.csv")


def test_load_data_format_error():
    # Mock the pandas read_csv method to raise a ValueError
    with mock.patch("pandas.read_csv", side_effect=ValueError):
        with pytest.raises(
            DataFormatError, match="Error loading data from dummy_path.csv: "
        ):
            FileHandler("dummy_path.csv")
