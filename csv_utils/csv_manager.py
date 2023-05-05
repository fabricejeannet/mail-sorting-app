import pandas
from exceptions.custom_exceptions import *

class CsvManager:
    
    def __init__(self):
        self.dataframe = pandas.DataFrame()
        
        
    def is_a_csv_file(self,file_name):
        return file_name.lower().endswith(".csv")
    
    
    def open_csv_file(self,file_name):
        if not self.is_a_csv_file(file_name):
            raise TryToOpenNonCsvFile()
        self.dataframe = pandas.read_csv(file_name)
    