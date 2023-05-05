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
    csv_manager.dataframe = pandas.DataFrame({IDENTIFIANT:[1,2,3]})
    assert csv_manager.get_ids().equals(pandas.Series([1,2,3]))


def test_get_ids_on_missing_column_raise_error():
    csv_manager.dataframe = pandas.DataFrame()
    with pytest.raises(MissingColumnException) as exception_info:
        csv_manager.get_ids()
    assert exception_info.value.message == IDENTIFIANT + COLUMN_IS_MISSING
    
    
def test_get_company_names():
    csv_manager.dataframe = pandas.DataFrame({RAISON_SOCIALE:["a","b","c"]})
    assert csv_manager.get_company_names().equals(pandas.Series(["a","b","c"]))
    

def test_get_company_names_on_missing_column_raise_error():
    csv_manager.dataframe = pandas.DataFrame()
    with pytest.raises(MissingColumnException) as exception_info:
        csv_manager.get_company_names()
    assert exception_info.value.message == RAISON_SOCIALE + COLUMN_IS_MISSING
    
    
def test_get_legal_representatives():
    csv_manager.dataframe = pandas.DataFrame({REPRESENTANT_LEGAL:["Jean Jacques","b","c"]})
    assert csv_manager.get_legal_representatives().equals(pandas.Series(["Jean Jacques","b","c"]))
    

def test_get_legal_representatives_on_missing_column_raise_error():
    csv_manager.dataframe = pandas.DataFrame()
    with pytest.raises(MissingColumnException) as exception_info:
        csv_manager.get_legal_representatives()
    assert exception_info.value.message == REPRESENTANT_LEGAL + COLUMN_IS_MISSING
    
    
def test_get_subscription_status():
    csv_manager.dataframe = pandas.DataFrame({STATUT:["ABONNE","DESABONNE","RADIE"]})
    assert csv_manager.get_subscription_status().equals(pandas.Series(["ABONNE","DESABONNE","RADIE"]))
    
    
def test_get_subscription_status_on_missing_column_raise_error():
    csv_manager.dataframe = pandas.DataFrame()
    with pytest.raises(MissingColumnException) as exception_info:
        csv_manager.get_subscription_status()
    assert exception_info.value.message == STATUT + COLUMN_IS_MISSING
    
    
def test_get_director_names():
    csv_manager.dataframe = pandas.DataFrame({NOM_PRENOM_DIRIGEANT:["Jean Jacques","b","c"]})
    assert csv_manager.get_director_names().equals(pandas.Series(["Jean Jacques","b","c"]))
    

def test_get_director_names_on_missing_column_raise_error():
    csv_manager.dataframe = pandas.DataFrame()
    with pytest.raises(MissingColumnException) as exception_info:
        csv_manager.get_director_names()
    assert exception_info.value.message == NOM_PRENOM_DIRIGEANT + COLUMN_IS_MISSING
    
    
def test_get_trademark_names():
    csv_manager.dataframe = pandas.DataFrame({MARQUE_COMMERCIALE:["My company","b","c"]})
    assert csv_manager.get_trademark_names().equals(pandas.Series(["My company","b","c"]))
    
    
def test_get_trademark_names_on_missing_column_raise_error():
    csv_manager.dataframe = pandas.DataFrame()
    with pytest.raises(MissingColumnException) as exception_info:
        csv_manager.get_trademark_names()
    assert exception_info.value.message == MARQUE_COMMERCIALE + COLUMN_IS_MISSING
    
    
def test_get_clients_data_dictionnary():
    mock_data_for_dataframe = { MARQUE_COMMERCIALE:["My company"], NOM_PRENOM_DIRIGEANT:["Jean Jacques"], STATUT:["ABONNE"], REPRESENTANT_LEGAL:["Jean Jacques"], RAISON_SOCIALE:["My company"], IDENTIFIANT:[1]}
    csv_manager.dataframe = pandas.DataFrame(mock_data_for_dataframe)
    assert csv_manager.get_clients_data_dictionnary() == mock_data_for_dataframe