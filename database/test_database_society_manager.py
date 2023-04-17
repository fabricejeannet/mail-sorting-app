import pytest
from database_society_manager import SocietyManager
society_manager = SocietyManager()

def test_config():
    society_manager.database_manager.connect_to_database()
    society_manager.database_manager.empty_all_tables()

def test_dataframe_is_not_empty_after_setup():
    society_manager.setup_dataframe()
    assert society_manager.csv_manager.dataframe.empty == False

def test_insert_row_in_database_with_empty_dataframe_raises_error():
    society_manager.csv_manager.close_csv()
    society_manager.database_manager.connect_to_database()
    with pytest.raises(IndexError):
        society_manager.insert_row_in_database(0, 1)

def test_insert_row_in_database_with_valid_dataframe():
    society_manager.database_manager.connect_to_database()
    society_manager.setup_test_dataframe()
    society_manager.insert_row_in_database(0, 1)
    assert society_manager.database_manager.cursor.rowcount >= 1
    assert society_manager.check_if_society_exists("Société 1") == True
    
def test_check_if_society_exist_return_true():
    society_manager.database_manager.connect_to_database()
    assert society_manager.check_if_society_exists("Société 1") == True
     
def test_setup_test_dataframe():
    society_manager.setup_test_dataframe()
    assert society_manager.csv_manager.dataframe.empty == False    

def test_returning_good_query():
    society_manager.setup_test_dataframe()
    query = society_manager.get_insert_query_from_row_index(0, 1)
    assert query == 'INSERT INTO societes (raison_sociale, representant_legal, statut, nom_dirigeant, prenom_dirigeant, id_domiciliataire, id_externe) VALUES ("Société 1", "Mr. Grutier", "ABONNE", "Grutier", "Jean", "1", "1")'
