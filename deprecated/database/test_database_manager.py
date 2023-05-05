from database_manager import DatabaseManager

database_manager = DatabaseManager()

def test_connexion_is_valid():
    database_manager.connect_to_database()
    assert database_manager.connection.is_connected() == True
    
def test_connexion_is_closed():
    database_manager.connect_to_database()
    database_manager.disconnect_from_database()
    assert database_manager.connection.is_connected() == False