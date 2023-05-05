import pytest
from database_domiciliary_manager import DomiciliaryManager
domiciliary_manager = DomiciliaryManager()
domiciliary_manager.database_manager.connect_to_database()
domiciliary_manager.database_manager.empty_domiciliary_table()


def test_add_domiciliary():
    domiciliary_manager.add_domiciliary("Société 1", "123456")
    assert domiciliary_manager.database_manager.cursor.rowcount >= 1
    assert domiciliary_manager.get_domiciliary("Société 1") != None

def test_add_already_existing_domiciliary_raises_error():
    with pytest.raises(ValueError):
        domiciliary_manager.add_domiciliary("Société 1", "123456")
    
def test_get_good_insert_query_from_domiciliary():
    query = domiciliary_manager.get_insert_query_from_domiciliary("Société 1", "123456")
    assert query == "INSERT INTO domiciliataires (raison_sociale, cle_domiciliation) VALUES ('Société 1', '123456')"
    
def test_get_domiciliary():
    assert domiciliary_manager.get_domiciliary("Société 1") != None

def test_get_domiciliary_raises_error_with_empty_domiciliary_name():
    with pytest.raises(ValueError):
        domiciliary_manager.get_domiciliary("")

def test_get_domiciliary_return_none_with_non_existing_domiciliary_name():
    assert domiciliary_manager.get_domiciliary(
        domiciliary_name="existe pas") == None

def test_remove_domiciliary():
    domiciliary_manager.remove_domiciliary("Société 1")
    assert domiciliary_manager.get_domiciliary("Société 1") == None

def test_remove_domiciliary_raises_error_with_empty_domiciliary_name():
    with pytest.raises(ValueError):
        domiciliary_manager.remove_domiciliary("")
        
def test_remove_domiciliary_raises_error_with_non_existing_domiciliary_name():
    with pytest.raises(ValueError):
        domiciliary_manager.remove_domiciliary("existe pas")

def test_get_insert_query_raises_error_with_empty_domiciliary_name():
    with pytest.raises(ValueError):
        domiciliary_manager.get_insert_query_from_domiciliary("", "123456")