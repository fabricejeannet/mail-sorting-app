from database_manager import DatabaseManager
from database_society_manager import SocietyManager

class AliasManager:
    
    def __init__(self):
        self.database_manager = DatabaseManager()
        self.database_society_manager = SocietyManager()
    
    def add_alias_with_company_name(self, alias_text, company_name):
        if self.check_if_alias_already_exist(alias_text):
            raise ValueError("L'alias existe déjà")
        query = self.get_insert_query_from_alias_and_company_name(alias_text, company_name)
        self.database_manager.connect_to_database()
        self.database_manager.execute_void_query(query)
    
    def add_alias_with_company_id(self, alias_text, company_id):
        query = self.get_insert_query_from_alias_and_company_id(alias_text, company_id)
        self.database_manager.connect_to_database()
        self.database_manager.execute_void_query(query)
    
    def get_alias(self,alias_text):
        if alias_text == "":
            raise ValueError("Le nom de l'alias ne peut pas être vide")
        query = "SELECT * FROM alias WHERE alias = '{}'".format(alias_text)
        return self.database_manager.execute_fetchone_query(query)
    
    def get_insert_query_from_alias_and_company_name(self, alias_text, company_name):
        if alias_text == "":
            raise ValueError("Le nom de l'alias ne peut pas être vide")
        company_id = self.database_society_manager.get_society_id_from_name(company_name)
        if company_id == None:
            raise ValueError("La société n'existe pas")
        return "INSERT INTO alias (societe_id, alias) VALUES ('{}', '{}')".format(company_id, alias_text)
    
    def get_insert_query_from_alias_and_company_id(self, alias_text, company_id):
        if alias_text == "":
            raise ValueError("Le nom de l'alias ne peut pas être vide")
        return "INSERT INTO alias (societe_id, alias) VALUES ('{}', '{}')".format(company_id, alias_text)
    
    def remove_alias(self, alias_text):
        if self.get_alias(alias_text) == None:
            raise ValueError("L'alias n'existe pas")
        query = "DELETE FROM alias WHERE alias = '{}'".format(alias_text)
        self.database_manager.execute_void_query(query)
        
    def get_all_company_alias(self, company_name):
        query = "SELECT * FROM alias WHERE societe_id = '{}'".format(self.database_society_manager.get_society_id_from_name(company_name))
        return self.database_manager.execute_fetchall_query(query)
    
    def check_if_alias_already_exist(self, alias_text):
        query = "SELECT * FROM alias WHERE alias = '{}'".format(alias_text)
        return self.database_manager.execute_fetchone_query(query) != None