from Utils import read_json_file
import pytest
from unittest.mock import patch, mock_open


@patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
def test_read_json_file_file_exists(mock_file):
    file_path = "test_file.json"
    result = read_json_file(file_path)

    # Assert that the file is opened with the correct path
    mock_file.assert_called_once_with(file_path, "r")

    # Assert that the returned data is as expected
    assert result == {"key": "value"}


@patch("builtins.open", side_effect=FileNotFoundError)
def test_read_json_file_file_not_found(mock_file):
    file_path = "non_existent_file.json"
    result = read_json_file(file_path)

    # Assert that the file is opened with the correct path
    mock_file.assert_called_once_with(file_path, "r")

    # Assert that an empty dictionary is returned when the file is not found
    assert result == {}


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data='[{"id": 1, "name": "Recipe 1"}, {"id": 2, "name": "Recipe 2"}]',
)
def test_read_json_file_list(mock_file):
    file_path = "recipe_list.json"
    result = read_json_file(file_path)

    # Assert that the file is opened with the correct path
    mock_file.assert_called_once_with(file_path, "r")

    # Assert that the returned data is a list of dictionaries
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["name"] == "Recipe 1"
    assert result[1]["id"] == 2


# Add more tests as needed for other functions in your app
