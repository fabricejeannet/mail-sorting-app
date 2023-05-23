from csv_processor.csv_manager import CsvManager
from csv_processor.csv_constants import *
from exceptions.custom_exceptions import *
import pandas
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
    csv_manager.open_csv_file("tests/test.csv")
    assert csv_manager.dataframe.empty == False
    

def test_get_ids():
    csv_manager.dataframe = pandas.DataFrame({ID:[1,2,3]})
    assert csv_manager.get_ids().equals(pandas.Series([1,2,3]))
    csv_manager.open_csv_file("tests/test.csv")
    assert csv_manager.get_ids().equals(pandas.Series([1,2,3,4,5,6,7]))


def test_get_ids_on_missing_column_raise_error():
    csv_manager.dataframe = pandas.DataFrame()
    with pytest.raises(MissingColumnException) as exception_info:
        csv_manager.get_ids()
    assert exception_info.value.message == ID + COLUMN_IS_MISSING
    
    
def test_get_company_names():
    csv_manager.dataframe = pandas.DataFrame({COMPANY_NAME:["a","b","c"]})
    assert csv_manager.get_company_names().equals(pandas.Series(["a","b","c"]))
    

def test_get_company_names_on_missing_column_raise_error():
    csv_manager.dataframe = pandas.DataFrame()
    with pytest.raises(MissingColumnException) as exception_info:
        csv_manager.get_company_names()
    assert exception_info.value.message == COMPANY_NAME + COLUMN_IS_MISSING
    
    
def test_get_legal_representatives():
    csv_manager.dataframe = pandas.DataFrame({LEGAL_REPRESENTATIVE:["Jean Jacques","b","c"]})
    assert csv_manager.get_legal_representatives().equals(pandas.Series(["Jean Jacques","b","c"]))
    

def test_get_legal_representatives_on_missing_column_raise_error():
    csv_manager.dataframe = pandas.DataFrame()
    with pytest.raises(MissingColumnException) as exception_info:
        csv_manager.get_legal_representatives()
    assert exception_info.value.message == LEGAL_REPRESENTATIVE + COLUMN_IS_MISSING
    
    
def test_get_subscription_status():
    csv_manager.dataframe = pandas.DataFrame({STATUS:["ABONNE","DESABONNE","RADIE"]})
    assert csv_manager.get_subscription_status().equals(pandas.Series(["ABONNE","DESABONNE","RADIE"]))
    
    
def test_get_subscription_status_on_missing_column_raise_error():
    csv_manager.dataframe = pandas.DataFrame()
    with pytest.raises(MissingColumnException) as exception_info:
        csv_manager.get_subscription_status()
    assert exception_info.value.message == STATUS + COLUMN_IS_MISSING
    
    
def test_get_director_names():
    csv_manager.dataframe = pandas.DataFrame({DIRECTOR_NAME:["Jean Jacques","b","c"]})
    assert csv_manager.get_director_names().equals(pandas.Series(["Jean Jacques","b","c"]))
    

def test_get_director_names_on_missing_column_raise_error():
    csv_manager.dataframe = pandas.DataFrame()
    with pytest.raises(MissingColumnException) as exception_info:
        csv_manager.get_director_names()
    assert exception_info.value.message == DIRECTOR_NAME + COLUMN_IS_MISSING
    
    
def test_get_trademark_names():
    csv_manager.dataframe = pandas.DataFrame({TRADEMARK_NAME:["My company","b","c"]})
    assert csv_manager.get_trademark_names().equals(pandas.Series(["My company","b","c"]))
    
    
def test_get_trademark_names_on_missing_column_raise_error():
    csv_manager.dataframe = pandas.DataFrame()
    with pytest.raises(MissingColumnException) as exception_info:
        csv_manager.get_trademark_names()
    assert exception_info.value.message == TRADEMARK_NAME + COLUMN_IS_MISSING
    
    
def test_get_clients_data_dictionnary():
    mock_data = {DIRECTOR_NAME:["Jean Jacques","b","c"], TRADEMARK_NAME:["My company","b","c"], ID:[1,2,3], COMPANY_NAME:["a","b","c"], LEGAL_REPRESENTATIVE:["Jean Jacques","b","c"], STATUS:["ABONNE","DESABONNE","RADIE"]}
    csv_manager.dataframe = pandas.DataFrame({DIRECTOR_NAME:["Jean Jacques","b","c"], TRADEMARK_NAME:["My company","b","c"], ID:[1,2,3], COMPANY_NAME:["a","b","c"], LEGAL_REPRESENTATIVE:["Jean Jacques","b","c"], STATUS:["ABONNE","DESABONNE","RADIE"]}) 
    for index in range(len(csv_manager.dataframe)):
        assert csv_manager.get_clients_data_dictionnary()[DIRECTOR_NAME][index] == mock_data[DIRECTOR_NAME][index]
        assert csv_manager.get_clients_data_dictionnary()[TRADEMARK_NAME][index] == mock_data[TRADEMARK_NAME][index]
        assert csv_manager.get_clients_data_dictionnary()[ID][index] == mock_data[ID][index]
        assert csv_manager.get_clients_data_dictionnary()[COMPANY_NAME][index] == mock_data[COMPANY_NAME][index]
        assert csv_manager.get_clients_data_dictionnary()[LEGAL_REPRESENTATIVE][index] == mock_data[LEGAL_REPRESENTATIVE][index]
        assert csv_manager.get_clients_data_dictionnary()[STATUS][index] == mock_data[STATUS][index]
