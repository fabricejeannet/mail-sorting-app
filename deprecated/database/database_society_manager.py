import mysql.connector
from csv_importer import CsvManager
from database_manager import DatabaseManager

class SocietyManager:
    
    def __init__(self):
        self.database_manager = DatabaseManager()
        self.csv_manager = CsvManager()
        
    def setup_dataframe(self):
        self.csv_manager.open_csv("clients.csv")
        
    def setup_test_dataframe(self):
        self.csv_manager.open_csv("test.csv")
            
    def insert_row_in_database(self, index, domiciliary_id):
        query = self.get_insert_query_from_row_index(index, domiciliary_id)
        self.database_manager.execute_void_query(query)     
        
    def add_society(self, index, domiciliary_id):
        external_id = self.csv_manager.get_external_id_from_index(index)
        if not self.check_if_society_exists_from_external_id(external_id=external_id):
            self.insert_row_in_database(index, domiciliary_id)
        else:
            raise ValueError("La société existe déjà")
            
    def update_society(self, index, domiciliary_id):
        pass
        
                
    def get_society_id_from_name(self, company_name):
        query = "SELECT id FROM societes WHERE raison_sociale = '{}'".format(company_name)
        self.database_manager.connect_to_database()
        query_result = self.database_manager.execute_fetchone_query(query)
        if query_result == None:
            raise ValueError("La société n'existe pas")
        return self.database_manager.execute_fetchone_query(query)[0]
    
    def get_societe_name_from_id(self, company_id):
        query = "SELECT raison_sociale FROM societes WHERE id = '{}'".format(company_id)
        self.database_manager.connect_to_database()
        return self.database_manager.execute_fetchone_query(query)[0]
    
        """_summary_ : Checks if a society exists in the database
        __param__ : company_name : the name of the company to check
        __return__ : True if the company exists, False otherwise
        """
    def check_if_society_exists(self, company_name):
        query = "SELECT * FROM societes WHERE raison_sociale = '{}'".format(company_name)
        self.database_manager.connect_to_database()
        return self.database_manager.execute_fetchone_query(query) != None
    
    def check_if_society_exists_from_external_id(self, external_id):
        query = "SELECT * FROM societes WHERE id_externe = '{}'".format(external_id)
        self.database_manager.connect_to_database()
        return self.database_manager.execute_fetchone_query(query) != None
    
    def remove_society(self, company_name):
        if not self.check_if_society_exists(company_name):
            raise ValueError("La société n'existe pas")
        else:
            query = "DELETE FROM societes WHERE raison_sociale = '{}'".format(company_name)
            self.database_manager.execute_void_query(query)
    
    def remove_all_societies(self):
        self.database_manager.empty_society_table()
    
    def get_insert_query_from_row_index(self, index, domiciliary_id):  
        status = self.csv_manager.get_subscription_status_from_index(index)
        company_name = self.csv_manager.get_company_name_from_index(index)
        director_first_name = self.csv_manager.get_only_director_first_name_from_index(index)
        director_last_name = self.csv_manager.get_only_director_last_name_from_index(index)
        legal_representative = self.csv_manager.get_legal_representative_from_index(index)
        external_id = self.csv_manager.get_external_id_from_index(index)
        prepared_query = 'INSERT INTO societes (raison_sociale, representant_legal, statut, nom_dirigeant, prenom_dirigeant, id_domiciliataire, id_externe) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}")'
        prepared_query =  prepared_query.format(company_name,
                                    legal_representative, 
                                    status, 
                                    director_last_name, 
                                    director_first_name, 
                                    domiciliary_id, 
                                    external_id)
        return prepared_query
