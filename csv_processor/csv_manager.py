import pandas
import glob
import pathlib
import re
import logging
from exceptions.custom_exceptions import *
from csv_processor.csv_constants import *
from config_processor.config_importer import ConfigImporter

class CsvManager:
    
    def __init__(self):
        self.dataframe = pandas.DataFrame()
        self.config_importer = ConfigImporter()
        self.csv_file_path = self.config_importer.get_csv_file_path()
        logging.info("csv_file_path: " + self.csv_file_path)
        self.csv_file_regex = self.config_importer.get_csv_file_regex()
        
        
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
            dataframe_ids = self.dataframe[ID]
        except KeyError:
            raise MissingColumnException(ID)
        return dataframe_ids
    
    
    def get_company_names(self):
        try :
            dataframe_company_names = self.dataframe[COMPANY_NAME]
        except KeyError:
            raise MissingColumnException(COMPANY_NAME)
        return dataframe_company_names
    
    
    def get_legal_representatives(self):
        try :
            dataframe_legal_representatives = self.dataframe[LEGAL_REPRESENTATIVE]
        except KeyError:
            raise MissingColumnException(LEGAL_REPRESENTATIVE)
        return dataframe_legal_representatives
    
    
    def get_subscription_status(self):
        try :
            dataframe_subscription_status = self.dataframe[STATUS]
        except KeyError:
            raise MissingColumnException(STATUS)
        return dataframe_subscription_status
    
    
    def get_director_names(self):
        try :
            dataframe_director_names = self.dataframe[DIRECTOR_NAME]
        except KeyError:
            raise MissingColumnException(DIRECTOR_NAME)
        return dataframe_director_names
    
    
    def get_trademark_names(self):
        try :
            dataframe_trademark_names = self.dataframe[TRADEMARK_NAME]
        except KeyError:
            raise MissingColumnException(TRADEMARK_NAME)
        return dataframe_trademark_names
    
    
    def get_id_from_index(self,index):
        return self.dataframe.loc[index,ID]
    
    def get_company_name_from_index(self,index):
        return self.dataframe.loc[index,COMPANY_NAME]
    
    
    def get_legal_representative_from_index(self,index):
        return self.dataframe.loc[index,LEGAL_REPRESENTATIVE]
    
    
    def get_subscription_status_from_index(self,index):
        return self.dataframe.loc[index,STATUS]
    
    
    def get_director_name_from_index(self,index):
        return self.dataframe.loc[index,DIRECTOR_NAME]
    
    
    def get_trademark_name_from_index(self,index):
        return self.dataframe.loc[index,TRADEMARK_NAME]
    
    
    def get_clients_data_dictionnary(self):
        clients_data_dictionnary = {}
        clients_data_dictionnary[ID] = self.get_ids()
        clients_data_dictionnary[COMPANY_NAME] = self.get_company_names()
        clients_data_dictionnary[STATUS] = self.get_subscription_status()
        clients_data_dictionnary[DIRECTOR_NAME] = self.get_director_names()
        clients_data_dictionnary[TRADEMARK_NAME] = self.get_trademark_names()
        clients_data_dictionnary[LEGAL_REPRESENTATIVE] = self.get_legal_representatives()
        return clients_data_dictionnary