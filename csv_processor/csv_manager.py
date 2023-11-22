import pandas
import glob
import pathlib
import re
import logging
from exceptions.custom_exceptions import *
from text_processor.text_cleaner import TextCleaner
from csv_processor.csv_constants import *
from config_processor.config_importer import ConfigImporter

class CsvManager:
    
    def __init__(self):
        self.dataframe = pandas.DataFrame()
        config_importer = ConfigImporter()
        self.text_cleaner = TextCleaner()
        self.csv_file_path = config_importer.get_csv_file_path()
        logging.info("csv_file_path: " + self.csv_file_path)
        self.csv_file_regex = config_importer.get_csv_file_regex()
        self.ID = config_importer.get_csv_id_column()
        self.COMPANY_NAME = config_importer.get_csv_company_name_column()
        self.LEGAL_REPRESENTATIVE = config_importer.get_csv_owner_column()
        self.STATUS = config_importer.get_csv_status_column()
        self.DOMICILIATION_AGENT = config_importer.get_csv_domiciliation_agent_column()
        self.TRADEMARK = config_importer.get_csv_trademark_column()
        
    def is_a_csv_file(self,file_name):
        return file_name.lower().endswith(".csv")
    
    
    def get_latest_csv_file(self):
        
        list_of_files = glob.glob(self.csv_file_path + "*.csv")
        found_csv_file = False
        logging.info("List of found csv files : " + str(list_of_files))
        
        while not found_csv_file and list_of_files:
            #Get latest file depending on last modification date of the file
            latest_file = max(list_of_files, key=lambda file: pathlib.Path(file).stat().st_mtime)
            
            logging.info("Latest csv file found: " + latest_file)
            if re.search(self.csv_file_regex, latest_file):
                found_csv_file = True
            else:
                list_of_files.remove(latest_file)
                
        if not found_csv_file:
            raise NoCsvFileFound()
        
        return latest_file
        
        
    def open_csv_file(self,file_path):
        if not self.is_a_csv_file(file_path):
            raise TryToOpenNonCsvFile()
        
        self.dataframe = pandas.read_csv(file_path)
            
        if self.dataframe.empty:
            raise TryToOpenEmptyCsvFile()
        
        #Replace NaN values by empty string
        self.dataframe = self.dataframe.fillna("")
    
    
    def get_ids(self):
        try :
            dataframe_ids = self.dataframe[self.ID]
        except KeyError:
            raise MissingColumnException(self.ID)
        return dataframe_ids
    
    
    def get_company_names(self):
        try :
            dataframe_company_names = self.dataframe[self.COMPANY_NAME]
            for index in range(len(dataframe_company_names)):
                cleaned_name = self.text_cleaner.clean_text_without_checking_validity(dataframe_company_names[index])
                dataframe_company_names[index] = cleaned_name
        except KeyError:
            raise MissingColumnException(self.COMPANY_NAME)
        return dataframe_company_names
    
    
    def get_legal_representatives(self):
        try :
            dataframe_legal_representatives = self.dataframe[self.LEGAL_REPRESENTATIVE]
            for index in range(len(dataframe_legal_representatives)):
                cleaned_name = self.text_cleaner.clean_text_without_checking_validity(dataframe_legal_representatives[index])
                dataframe_legal_representatives[index] = cleaned_name
        except KeyError:
            raise MissingColumnException(self.LEGAL_REPRESENTATIVE)
        return dataframe_legal_representatives
    
    
    def get_subscription_status(self):
        try :
            dataframe_subscription_status = self.dataframe[self.STATUS]
        except KeyError:
            raise MissingColumnException(self.STATUS)
        return dataframe_subscription_status
    
    
    def get_domiciliation_agents(self):
        try:
            dataframe_domiciliation_agents = self.dataframe[self.DOMICILIATION_AGENT]
        except KeyError:
            raise MissingColumnException(self.DOMICILIATION_AGENT)
        return dataframe_domiciliation_agents
        
        
    def get_trademarks(self):
        try:
            dataframe_trademarks = self.dataframe[self.TRADEMARK]
            for index in range(len(dataframe_trademarks)):
                cleaned_name = self.text_cleaner.clean_text_without_checking_validity(dataframe_trademarks[index])
                dataframe_trademarks[index] = cleaned_name
        except KeyError:
            raise MissingColumnException(self.TRADEMARK)
        return dataframe_trademarks

    
    def get_clients_data_dictionnary(self):
        clients_data_dictionnary = {}
        clients_data_dictionnary[self.ID] = self.get_ids()
        clients_data_dictionnary[self.COMPANY_NAME] = self.get_company_names()
        clients_data_dictionnary[self.STATUS] = self.get_subscription_status()
        clients_data_dictionnary[self.LEGAL_REPRESENTATIVE] = self.get_legal_representatives()
        clients_data_dictionnary[self.DOMICILIATION_AGENT] = self.get_domiciliation_agents()
        clients_data_dictionnary[self.TRADEMARK] = self.get_trademarks()
        return clients_data_dictionnary