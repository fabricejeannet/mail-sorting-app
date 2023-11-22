from csv_processor.csv_manager import CsvManager
from csv_processor.csv_constants import *
from config_processor.config_importer import ConfigImporter
from exceptions.custom_exceptions import *
import pandas
import pytest
csv_manager = CsvManager()
config_importer = ConfigImporter()

ID = config_importer.get_csv_id_column()
COMPANY_NAME = config_importer.get_csv_company_name_column()
LEGAL_REPRESENTATIVE = config_importer.get_csv_owner_column()
STATUS = config_importer.get_csv_status_column()
DOMICILIATION_AGENT = config_importer.get_csv_domiciliation_agent_column()

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
    assert csv_manager.get_ids().equals(pandas.Series([1,2,3,4,5,6,7,8,9]))


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
    
    
    
def test_get_clients_data_dictionnary():
    mock_data = {ID:[1,2,3], COMPANY_NAME:["a","b","c"], LEGAL_REPRESENTATIVE:["Jean Jacques","b","c"], STATUS:["ABONNE","DESABONNE","RADIE"], DOMICILIATION_AGENT:["a","b","c"]}
    csv_manager.dataframe = pandas.DataFrame(mock_data) 
    for index in range(len(csv_manager.dataframe)):
        assert csv_manager.get_clients_data_dictionnary()[ID][index] == mock_data[ID][index]
        assert csv_manager.get_clients_data_dictionnary()[COMPANY_NAME][index] == mock_data[COMPANY_NAME][index]
        assert csv_manager.get_clients_data_dictionnary()[LEGAL_REPRESENTATIVE][index] == mock_data[LEGAL_REPRESENTATIVE][index]
        assert csv_manager.get_clients_data_dictionnary()[STATUS][index] == mock_data[STATUS][index]
