from database_manager import DatabaseManager

class DomiciliaryManager:
    
    def __init__(self):
        self.database_manager = DatabaseManager()
    
    def add_domiciliary(self, domiciliary_name, domiciliary_key):
        if self.check_if_domiciliary_already_exist_from_name(domiciliary_name):
            raise ValueError("Le domiciliataire existe déjà")
        query = self.get_insert_query_from_domiciliary(domiciliary_name, domiciliary_key)
        self.database_manager.execute_void_query(query)
        
    def get_insert_query_from_domiciliary(self, domiciliary_name, domiciliary_key):
        if domiciliary_name == "":
            raise ValueError("Le nom du domiciliataire ne peut pas être vide")
        return "INSERT INTO domiciliataires (raison_sociale, cle_domiciliation) VALUES ('{}', '{}')".format(domiciliary_name, domiciliary_key)
    
    def remove_domiciliary(self, domiciliary_name):
        if not self.check_if_domiciliary_already_exist_from_name(domiciliary_name):
            raise ValueError("Le domiciliataire n'existe pas")
        query = "DELETE FROM domiciliataires WHERE raison_sociale = '{}'".format(domiciliary_name)
        self.database_manager.cursor.execute(query)
        self.database_manager.connection.commit()
        
    def check_if_domiciliary_already_exist_from_name(self, domiciliary_name):
        if domiciliary_name == "":
            raise ValueError("Le nom du domiciliataire ne peut pas être vide")
        if self.get_domiciliary(domiciliary_name) == None:
            return False
        return True
    
    def check_if_domiciliary_already_exist_from_id(self, domiciliary_id):
        if domiciliary_id == "":
            raise ValueError("L'id du domiciliataire ne peut pas être vide")
        if self.get_domiciliary_from_id(domiciliary_id) == None:
            return False
        return True
    
    def get_all_domiciliaries(self):
        query = "SELECT * FROM domiciliataires"
        return self.database_manager.execute_fetchall_query(query)
    
    def get_domiciliary(self, domiciliary_name):
        if domiciliary_name == "":
            raise ValueError("Le nom du domiciliataire ne peut pas être vide")
        query = "SELECT * FROM domiciliataires WHERE raison_sociale = '{}'".format(domiciliary_name)
        return self.database_manager.execute_fetchone_query(query)    
    
    def get_domiciliary_id_from_name(self, domiciliary_name):
        query = "SELECT id FROM domiciliataires WHERE raison_sociale = '{}'".format(domiciliary_name)
        return self.database_manager.execute_fetchone_query(query)[0]
       
    def get_domiciliary_name_from_id(self, domiciliary_name):
        query = "SELECT * FROM domiciliataires WHERE raison_sociale = '{}'".format(domiciliary_name)
        return self.database_manager.execute_fetchall_query(query)[0]