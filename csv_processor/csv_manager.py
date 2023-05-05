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
        if self.dataframe.empty:
            raise TryToOpenEmptyCsvFile()
    
    
    def get_ids(self):
        try :
            dataframe_ids = self.dataframe[ID]
        except :
            raise MissingColumnException(ID)
        return dataframe_ids
    
    
    def get_company_names(self):
        try :
            dataframe_company_names = self.dataframe[COMPANY_NAME]
        except :
            raise MissingColumnException(COMPANY_NAME)
        return dataframe_company_names
    
    
    def get_legal_representatives(self):
        try :
            dataframe_legal_representatives = self.dataframe[LEGAL_REPRESENTATIVE]
        except :
            raise MissingColumnException(LEGAL_REPRESENTATIVE)
        return dataframe_legal_representatives
    
    
    def get_subscription_status(self):
        try :
            dataframe_subscription_status = self.dataframe[STATUS]
        except :
            raise MissingColumnException(STATUS)
        return dataframe_subscription_status
    
    
    def get_director_names(self):
        try :
            dataframe_director_names = self.dataframe[DIRECTOR_NAME]
        except :
            raise MissingColumnException(DIRECTOR_NAME)
        return dataframe_director_names
    
    
    def get_trademark_names(self):
        try :
            dataframe_trademark_names = self.dataframe[TRADEMARK_NAME]
        except :
            raise MissingColumnException(TRADEMARK_NAME)
        return dataframe_trademark_names
    
    
    def get_clients_data_dictionnary(self):
        clients_data_dictionnary = {}
        clients_data_dictionnary[ID] = self.get_ids()
        clients_data_dictionnary[COMPANY_NAME] = self.get_company_names()
        clients_data_dictionnary[STATUS] = self.get_subscription_status()
        clients_data_dictionnary[DIRECTOR_NAME] = self.get_director_names()
        clients_data_dictionnary[TRADEMARK_NAME] = self.get_trademark_names()
        clients_data_dictionnary[LEGAL_REPRESENTATIVE] = self.get_legal_representatives()
        return clients_data_dictionnary