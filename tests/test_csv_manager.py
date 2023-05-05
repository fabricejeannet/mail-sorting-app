from csv_utils.csv_manager import CsvManager
from exceptions.custom_exceptions import *
import pytest
csv_manager = CsvManager()

def test_check_if_file_is_a_csv():
    assert csv_manager.is_a_csv_file("test.csv") == True
    assert csv_manager.is_a_csv_file("test.txt") == False
    assert csv_manager.is_a_csv_file("test.csv.txt") == False
    assert csv_manager.is_a_csv_file("test.CSV") == True
    assert csv_manager.is_a_csv_file("test.CSV.txt") == False

def test_trying_to_open_invalid_csv_file_raise_error():
    with pytest.raises(TryToOpenNonCsvFile):
        csv_manager.open_csv_file("test.txt")
    with pytest.raises(TryToOpenNonCsvFile):
        csv_manager.open_csv_file("test.csv.txt")
    with pytest.raises(TryToOpenNonCsvFile):
        csv_manager.open_csv_file("test.CSV.txt")
        
def test_trying_to_open_valid_csv_file_does_not_raise_error():
    csv_manager.open_csv_file("test.csv")
    assert csv_manager.dataframe.empty == False