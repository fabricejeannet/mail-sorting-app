import pytest
from database_alias_manager import AliasManager
from database_society_manager import SocietyManager
from database_domiciliary_manager import DomiciliaryManager
society_manager = SocietyManager()
alias_manager = AliasManager()
domiciliary_manager = DomiciliaryManager()

def test_config():
    alias_manager.database_manager.connect_to_database()
    alias_manager.database_manager.empty_all_tables()
    society_manager.database_manager.connect_to_database()
    society_manager.setup_test_dataframe()
    domiciliary_manager.database_manager.connect_to_database()
    domiciliary_manager.add_domiciliary("Dom 1", None)
    domiciliary_manager.database_manager.disconnect_from_database()
    society_manager.insert_row_in_database(0, 1)
    society_manager.database_manager.disconnect_from_database()

def test_adding_alias_on_non_existing_company_raises_error():
    with pytest.raises(ValueError):
        alias_manager.add_alias_with_company_name("Alias 1", "existe pas")

def test_adding_alias_with_empty_name_raises_error():
    with pytest.raises(ValueError):
        alias_manager.add_alias_with_company_name("", "Société 1")

def test_adding_alias_with_existing_name_raises_error():
    alias_manager.add_alias_with_company_name("Alias 1", "Société 1")
    with pytest.raises(ValueError):
        alias_manager.add_alias_with_company_name("Alias 1", "Société 1")
        
def test_remove_alias_with_empty_name_raises_error():
    with pytest.raises(ValueError):
        alias_manager.remove_alias("")
        
def test_remove_alias_with_non_existing_name_raises_error():
    with pytest.raises(ValueError):
        alias_manager.remove_alias("existe pas")

def test_remove_alias_with_existing_name():
    alias_manager.remove_alias("Alias 1")
    assert alias_manager.get_alias("Alias 1") == None