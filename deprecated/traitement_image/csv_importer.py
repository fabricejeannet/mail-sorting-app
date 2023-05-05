import pandas
from custom_exceptions import *
import pytest

from csv_constants import *

class CsvManager :
    

    def __init__(self):
        self.dataframe = pandas.DataFrame()


    def check_file_type(self,file_name) :
        
        return file_name.lower().endswith(".csv")


    def load_dataframe_from_csv_file(self,file_name) :
        
        self.dataframe = pandas.read_csv(file_name)
        

    def reset_dataframe(self) :

        self.dataframe = pandas.DataFrame()


    def get_ids(self):
        try :
            res = self.dataframe[IDENTIFIANT]
        except :
            raise MissingColumnException("id")
        return res

    def get_company_names(self) :
        try :
            res = self.dataframe[RAISON_SOCIALE]
        except :
            raise MissingColumnException("company")
        return self.dataframe[RAISON_SOCIALE]
    

    def get_legal_representatives(self) :
        return self.dataframe[REPRESENTANT_LEGAL]


    def get_subscription_status(self) :
        return self.dataframe[STATUT]
    

    def get_director_names(self) :
        return self.dataframe[NOM_PRENOM_DIRIGEANT]    


    def get_trademark_names(self) :
        return self.dataframe[MARQUE_COMMERCIALE]
    
    
    def get_clients_data_dictionnary(self):

        self.clients_data_list = {}
        self.clients_data_list[RAISON_SOCIALE] = csv_manager.get_company_names()
        self.clients_data_list[REPRESENTANT_LEGAL] = csv_manager.get_director_names()
        self.clients_data_list[MARQUE_COMMERCIALE] = csv_manager.get_trademark_names()
        self.clients_data_list[STATUT] = csv_manager.get_subscription_status()
        return self.clients_data_list