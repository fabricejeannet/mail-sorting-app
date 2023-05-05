import pandas
from exceptions.custom_exceptions import *
from csv_processor.csv_constants import *

class CsvManager:
    
    def __init__(self):
        self.dataframe = pandas.DataFrame()
        
        
    def is_a_csv_file(self,file_name):
        return file_name.lower().endswith(".csv")
    
    
    def open_csv_file(self,file_name):
        if not self.is_a_csv_file(file_name):
            raise TryToOpenNonCsvFile()
        self.dataframe = pandas.read_csv(file_name)
    
    
    def get_ids(self):
        try :
            dataframe_ids = self.dataframe[IDENTIFIANT]
        except :
            raise MissingColumnException(IDENTIFIANT)
        return dataframe_ids
    
    
    def get_company_names(self):
        try :
            dataframe_company_names = self.dataframe[RAISON_SOCIALE]
        except :
            raise MissingColumnException(RAISON_SOCIALE)
        return dataframe_company_names
    
    
    def get_legal_representatives(self):
        try :
            dataframe_legal_representatives = self.dataframe[REPRESENTANT_LEGAL]
        except :
            raise MissingColumnException(REPRESENTANT_LEGAL)
        return dataframe_legal_representatives
    
    
    def get_subscription_status(self):
        try :
            dataframe_subscription_status = self.dataframe[STATUT]
        except :
            raise MissingColumnException(STATUT)
        return dataframe_subscription_status
    
    
    def get_director_names(self):
        try :
            dataframe_director_names = self.dataframe[NOM_PRENOM_DIRIGEANT]
        except :
            raise MissingColumnException(NOM_PRENOM_DIRIGEANT)
        return dataframe_director_names
    
    
    def get_trademark_names(self):
        try :
            dataframe_trademark_names = self.dataframe[MARQUE_COMMERCIALE]
        except :
            raise MissingColumnException(MARQUE_COMMERCIALE)
        return dataframe_trademark_names
    
    
    def get_clients_data_dictionnary(self):
        ids = self.get_ids()
        company_names = self.get_company_names()
        legal_representatives = self.get_legal_representatives()
        subscription_status = self.get_subscription_status()
        director_names = self.get_director_names()
        trademark_names = self.get_trademark_names()
        clients_data_dictionnary = {}
        for i in range(len(ids)):
            clients_data_dictionnary[ids[i]] = [company_names[i],legal_representatives[i],subscription_status[i],director_names[i],trademark_names[i]]
        return clients_data_dictionnary