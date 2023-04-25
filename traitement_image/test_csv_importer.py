import pytest
from custom_exceptions import *
from csv_importer import CsvManager, csv_constants, pandas
csv_importer = CsvManager()

def test_accepts_a_csv_file() :
    file_name = 'test.csv'
    assert csv_importer.check_file_type(file_name) == True

def test_accepts_a_csv_file_ignoring_case() :
    file_name = 'test.cSv'
    assert csv_importer.check_file_type(file_name) == True

def test_refuses_non_csv_file() :
    file_name = 'test.png'
    assert csv_importer.check_file_type(file_name) == False

def test_refuses_non_csv_file_with_csv_in_name() :
    file_name = 'test.csv.png'
    assert csv_importer.check_file_type(file_name) == False

def test_can_load_dataframe_from_csv_file():
    csv_importer.load_dataframe_from_csv_file('clients.csv')
    assert isinstance(csv_importer.dataframe, pandas.DataFrame)
    
def test_correctly_reset_dataframe():
    csv_importer.reset_dataframe()
    assert csv_importer.dataframe.empty == True


def test_can_retrieve_company_names():
    test_company = "CoolWorking"
    mock_data = {csv_constants.RAISON_SOCIALE : [test_company]}
    csv_importer.dataframe = pandas.DataFrame(data = mock_data)
    assert  csv_importer.get_company_names()[0] == test_company
    
def test_raises_error_on_missing_column_raison_sociale():
    csv_importer.dataframe = pandas.DataFrame(columns=[csv_constants.REPRESENTANT_LEGAL, csv_constants.STATUT, csv_constants.NOM_PRENOM_DIRIGEANT])
    with pytest.raises(MissingColumnException) as exception_msg:
        csv_importer.get_company_names()
    assert str(exception_msg.value) == 'company' + COLUMN_IS_MISSING
    
           
def test_can_retrieve_legal_representative():
    test_representative = "John Doe"
    mock_data = {csv_constants.REPRESENTANT_LEGAL : [test_representative]}
    csv_importer.dataframe = pandas.DataFrame(data = mock_data)
    assert  csv_importer.get_legal_representatives()[0] == test_representative
 
def test_raises_error_on_missing_column_legal_representative():
    csv_importer.dataframe = pandas.DataFrame(columns=[csv_constants.RAISON_SOCIALE, csv_constants.STATUT, csv_constants.NOM_PRENOM_DIRIGEANT])
    with pytest.raises(KeyError):
        csv_importer.get_legal_representatives()

def test_can_retrieve_subscription_status():
    test_status = "ABONNE"
    mock_data = {csv_constants.STATUT : [test_status]}
    csv_importer.dataframe = pandas.DataFrame(data = mock_data)
    assert  csv_importer.get_subscription_status()[0] == test_status

def test_raises_error_on_missing_column_subscription_status():
    csv_importer.dataframe = pandas.DataFrame(columns=[csv_constants.RAISON_SOCIALE, csv_constants.REPRESENTANT_LEGAL, csv_constants.NOM_PRENOM_DIRIGEANT])
    with pytest.raises(KeyError):
        csv_importer.get_subscription_status()

def test_can_retrieve_name_of_director():
    test_name = "John Doe"
    mock_data = {csv_constants.NOM_PRENOM_DIRIGEANT : [test_name]}
    csv_importer.dataframe = pandas.DataFrame(data = mock_data)
    assert  csv_importer.get_director_names()[0] == test_name

def test_raises_error_on_missing_column_director_name():
    csv_importer.dataframe = pandas.DataFrame(columns=[csv_constants.RAISON_SOCIALE, csv_constants.REPRESENTANT_LEGAL, csv_constants.STATUT])
    with pytest.raises(KeyError):
        csv_importer.get_director_names()